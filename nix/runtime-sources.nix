# Native runtime resources only. Gitlinks still select the complete source graph.
{ lib, root }:
let
  source = base: required: optional: lib.fileset.toSource {
    root = base;
    fileset = lib.fileset.unions (
      (map (name: base + "/${name}") required)
      ++ (map (name: lib.fileset.maybeMissing (base + "/${name}")) optional)
    );
  };
in {
  core = source (root + "/components/QCLNEGF.jl")
    [ "Project.toml" "src" "LICENSE" ]
    [ "Manifest.toml" "Artifacts.toml" "ext" "deps" ];
  runner = source (root + "/components/QCLNEGFRunner.jl")
    [ "Project.toml" "src" "LICENSE" "schema" "tools/verify_schema_provenance.jl"
      "scripts/scientific_workflow.jl" "examples/config" ]
    [ "Manifest.toml" "Artifacts.toml" "ext" "deps" ];
  environment = source (root + "/julia") [ "Project.toml" "Manifest.toml" ] [];
}
