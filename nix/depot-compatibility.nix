# Validation metadata stays outside the archive derivation and its environment.
let
  exact = value: names: builtins.isAttrs value && builtins.attrNames value == builtins.sort builtins.lessThan names;
  sha = value: builtins.isString value && builtins.match "[0-9a-f]{64}" value != null;
  hash = value: builtins.hashString "sha256" (builtins.toJSON value);
  store = value: builtins.isString value && builtins.match "/nix/store/[0-9abcdfghijklmnpqrsvwxyz]{32}-[A-Za-z0-9+._-]+" value != null;
  bases = [ "JuliaProject.toml" "Project.toml" "JuliaManifest-v1.13.toml" "Manifest-v1.13.toml"
    "JuliaManifest.toml" "Manifest.toml" "AppManifest.toml" "JuliaArtifacts.toml" "Artifacts.toml"
    "JuliaLocalPreferences.toml" "LocalPreferences.toml" ];
  roots = [ "julia" "components/QCLNEGF.jl" "components/QCLNEGFRunner.jl" ];
  rootNames = builtins.concatLists (map (root: map (base: "${root}/${base}") bases) roots);
  recipeNames = [ "components/QCLNEGFRunner.jl/tools/prepare_depot.jl"
    "components/QCLNEGFRunner.jl/tools/depot_native_facts.jl"
    "ops/depot_producer.ts" "nix/depot-compatibility.nix" "nix/depot-project.nix" ];
  graph = v: exact v [ "format" "revision" "components" ] && v.format == "qcl-negf.git-graph.v1"
    && builtins.isString v.revision && builtins.match "[0-9a-f]{40}" v.revision != null
    && builtins.isList v.components && builtins.length v.components > 0 && builtins.length v.components <= 64
    && builtins.all (r: exact r [ "path" "revision" "url" ]
      && builtins.isString r.path && builtins.match "components/[A-Za-z0-9][A-Za-z0-9.-]*" r.path != null
      && builtins.isString r.revision && builtins.match "[0-9a-f]{40}" r.revision != null
      && builtins.isString r.url && builtins.match "https://github.com/[A-Za-z0-9-]+/[A-Za-z0-9_.-]+" r.url != null) v.components
    && builtins.length (builtins.attrNames (builtins.listToAttrs (map (r: {name=r.path;value=true;}) v.components))) == builtins.length v.components;
in rec {
  inputs = { root, julia, system, juliaTestProfile ? "production-build", juliaTestWorkerLimit ? null }:
    let
      directory = path: let
        parts = builtins.filter builtins.isString (builtins.split "/" path);
        walk = current: rest: if rest == [] then current else
          let name = builtins.head rest; entries = builtins.readDir current;
          in assert (entries.${name} or null) == "directory";
             walk (current + "/${name}") (builtins.tail rest);
      in walk root parts;
      row = path: let
        parent = builtins.dirOf path; base = builtins.baseNameOf path;
        entries = builtins.readDir (directory parent);
        kind = entries.${base} or null;
      in assert kind == null || kind == "regular";
        { inherit path; sha256 = if kind == null then null else builtins.hashFile "sha256" (root + "/${path}"); };
      names = builtins.sort builtins.lessThan (rootNames ++ recipeNames ++ [
        "components/QCLNEGF.jl/.pkg/select_artifacts.jl" "components/QCLNEGFRunner.jl/.pkg/select_artifacts.jl" ]);
      manifest = assert (row "julia/Manifest.toml").sha256 != null; builtins.fromTOML (builtins.readFile (root + "/julia/Manifest.toml"));
      paths = builtins.concatLists (map (rows: map (r: r.path) (builtins.filter (r: r ? path) rows)) (builtins.attrValues manifest.deps));
      lockedPaths = builtins.sort builtins.lessThan paths == [ "../components/QCLNEGF.jl" "../components/QCLNEGFRunner.jl" ];
      canonicalEnv = builtins.all (name: !(builtins.pathExists (root + "/julia/${name}")))
        [ "JuliaProject.toml" "JuliaManifest-v1.13.toml" "Manifest-v1.13.toml" "JuliaManifest.toml" "AppManifest.toml" ];
      # Optional custom local selectors/preferences require a newly qualified profile.
      supported = builtins.all (r:
        !(builtins.hasAttr ".pkg" (builtins.readDir (directory r)))
        && !(builtins.pathExists (root + "/${r}/JuliaLocalPreferences.toml"))
        && !(builtins.pathExists (root + "/${r}/LocalPreferences.toml"))
        && builtins.all (name:
          let path = root + "/${r}/${name}"; entry = row "${r}/${name}";
          in entry.sha256 == null || !(builtins.hasAttr "preferences" (builtins.fromTOML (builtins.readFile path))))
          [ "Project.toml" "JuliaProject.toml" ]) roots;
    in assert system == "x86_64-linux";
       assert builtins.elem juliaTestProfile [ "production-build" "local-debug" ];
       assert juliaTestWorkerLimit == null || (builtins.isInt juliaTestWorkerLimit && juliaTestWorkerLimit > 0 && juliaTestWorkerLimit <= 9007199254740991);
       assert juliaTestProfile != "local-debug" || juliaTestWorkerLimit == null || juliaTestWorkerLimit == 2;
       assert supported && lockedPaths && canonicalEnv;
       assert builtins.all (p: (row p).sha256 != null) (recipeNames ++ map (r: "${r}/Project.toml") roots ++ [ "julia/Manifest.toml" ]);
       { schema="qcl-negf.julia-depot-inputs.v1"; inherit system;
         julia={version="1.13.0";drv=julia.drvPath;output=julia.outPath;profile=juliaTestProfile;
           test_workers=if juliaTestProfile == "local-debug" then 2 else juliaTestWorkerLimit;};
         files=map (p: if builtins.match ".*/\\.pkg/.*" p != null then {path=p;sha256=null;} else row p) names;
         selector_policy="locked-external-native-default-v1"; };
  valid = { metadata, expected, manifest }:
    let m=metadata;c=m.compatibility;n=c.native;
      test = exact m [ "format" "sources" "julia" "juliaManifest" "url" "hash" "compatibility" ]
        && m.format == "qcl-negf.julia-depot.v2" && m.julia == "1.13.0" && m.juliaManifest == manifest
        && graph m.sources && builtins.isString m.url && builtins.match "(file|https|http)://[^[:space:][:cntrl:]]+" m.url != null
        && builtins.match "(file|https|http)://[^/]*@.*" m.url == null
        && builtins.isString m.hash && builtins.match "sha256-[A-Za-z0-9+/]{43}=" m.hash != null
        && exact c [ "schema" "inputs" "inputs_sha256" "native" ]
        && c.schema == "qcl-negf.julia-depot-compatibility.v1" && c.inputs == expected && c.inputs_sha256 == hash expected
        && exact n [ "schema" "inputs_sha256" "julia_drv" "julia_output" "observed_platform"
          "preferences_sha256" "selector_closure_sha256" "artifact_selection_sha256" "receipt_sha256" ]
        && n.schema == "qcl-negf.julia-depot-native.v1" && n.inputs_sha256 == c.inputs_sha256
        && n.julia_drv == expected.julia.drv && n.julia_output == expected.julia.output
        && store n.julia_drv && store n.julia_output && builtins.isString n.observed_platform
        && builtins.stringLength n.observed_platform > 0 && builtins.stringLength n.observed_platform <= 1024
        && builtins.match "[!-~]+" n.observed_platform != null
        && builtins.all sha [ n.preferences_sha256 n.selector_closure_sha256 n.artifact_selection_sha256 n.receipt_sha256 ];
      checked=builtins.tryEval (builtins.deepSeq test test);
    in checked.success && checked.value;
  inherit hash;
}
