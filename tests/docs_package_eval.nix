# Pure source constructor probes. No build/import of Julia or dependency download.
{ nixpkgs ? /nix/store/q6zfrswar6d0fkihnxc198vmkdxrmvq5-source }:
let
  lib = import (nixpkgs + "/lib");
  root = ../.;
  fake = name: { outPath = "/nix/store/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa-${name}";
    drvPath = "/nix/store/bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb-${name}.drv";
    version = "fixture"; __toString = v: v.outPath; };
  pkgs = rec {
    inherit lib;
    python314 = (fake "python") // { version = "3.14.7"; withPackages = f:
      (fake "python-env") // { interpreter = "/nix/store/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa-python-env/bin/python3.14"; }; };
    nodejs_24 = (fake "node-npm-wrapper") // { version = "24.0.0"; };
    nodejs-slim_24 = (fake "node-runtime") // { version = "24.0.2"; };
    git = fake "git";
    runCommand = name: environment: script: builtins.derivation (environment // {
      inherit name; system = "x86_64-linux"; builder = "/bin/sh"; args = [ "-c" script ];
    });
    linkFarm = name: entries: runCommand name { links = builtins.toJSON entries; } "exit 99";
    writeText = name: text: runCommand name { inherit text; } "exit 99";
  };
  projectFor = packages: (import ../flake.nix).outputs { self = self; platform = {
    inputs.nixpkgs = { inherit lib; legacyPackages.x86_64-linux = packages; };
  }; };
  project = projectFor pkgs;
  self = { outPath = builtins.appendContext (toString root) { "${toString nixpkgs}" = { path = true; }; }; rev = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
    lib = project.lib // {
      mkPinnedJulia = args: (fake "julia") // { version = "1.13.0"; };
      mkPreparedDepot = args: fake "depot";
    };
  };
  sources = { format = "qcl-negf.git-graph.v1"; revision = self.rev; components = []; };
  metadata = { format = "qcl-negf.julia-depot.v1"; sources = sources; julia = "1.13.0";
    juliaManifest = builtins.hashFile "sha256" ../julia/Manifest.toml;
    provenance = "Явный source-only v1 fixture";
    url = "file:///synthetic/no-native-archive"; hash = "sha256-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA="; };
  empty = builtins.toFile "p17-source-only-empty-map.json" "{}";
  file = { path = empty; sha256 = builtins.hashFile "sha256" empty; };
  createWith = constructor: graph: raw: asset: review: constructor { system = "x86_64-linux";
    inherit metadata; capturedMetadata = raw; assetInputs = asset; reviewInputs = review;
    sources = graph; juliaTestProfile = "production-build"; juliaTestWorkerLimit = 2; };
  create = graph: raw: createWith project.lib.mkDocumentation graph raw file file;
  differentInput = builtins.toFile "p17-source-only-other-map.json" "{\"sourceOnlyFixture\":1}";
  otherFile = { path = differentInput; sha256 = builtins.hashFile "sha256" differentInput; };
  changedAssets = createWith project.lib.mkDocumentation sources (builtins.toJSON metadata) otherFile file;
  changedReviews = createWith project.lib.mkDocumentation sources (builtins.toJSON metadata) file otherFile;
  otherTools = projectFor (pkgs // { nodejs-slim_24 = (fake "node-other-output") // { version = "24.0.1"; }; });
  otherWrapper = projectFor (pkgs // { nodejs_24 = (fake "node-other-wrapper") // { version = "24.9.9"; }; });
  changedWrapper = createWith otherWrapper.lib.mkDocumentation sources (builtins.toJSON metadata) file file;
  changedTool = createWith otherTools.lib.mkDocumentation sources (builtins.toJSON metadata) file file;
  one = create sources (builtins.toJSON metadata);
  two = create (sources // { components = [ { path = "components/fixture";
    revision = "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb";
    url = "https://github.com/fixture/fixture"; } ]; }) (builtins.toJSON metadata);
  mismatch = builtins.tryEval ((create sources "{}").drvPath);
  originalRaw = " \n" + builtins.toJSON metadata + "\n";
  withRaw = create sources originalRaw;
  rawRecord = withRaw.passthru.inputs.prepared_depot.metadata;
  tool = withRaw.passthru.inputs.tools.python;
  node = one.passthru.inputs.tools.node;
  nodeLink = lib.findFirst (entry: entry.name == "node") null
    (builtins.fromJSON (builtins.unsafeDiscardStringContext one.passthru.inputClosure.links));
  expectedPath = "${pkgs.python314.withPackages (p: [])}/bin:${pkgs.nodejs-slim_24}/bin:${fake "julia"}/bin:${pkgs.git}/bin";
  rawRetained = builtins.readFile rawRecord.path;
  wrong = builtins.tryEval ((create sources (builtins.toJSON (metadata // { julia = "wrong"; }))).drvPath);
  selected = import ../nix/docs-sources.nix { inherit lib root; };
  selectedPaths = lib.filesystem.listFilesRecursive selected.presentation;
  forbidden = builtins.filter (p: builtins.match ".*(/\\.git/|/\\.build/|/tests/).*" (toString p) != null) selectedPaths;
in assert builtins.typeOf self.outPath == "string";
assert builtins.hasContext self.outPath;
assert project.lib ? mkDocumentation;
assert node.output == toString pkgs.nodejs-slim_24;
assert node.executable == "${pkgs.nodejs-slim_24}/bin/node";
assert node.expected_version == pkgs.nodejs-slim_24.version;
assert node.drv == pkgs.nodejs-slim_24.drvPath;
assert node.output != toString pkgs.nodejs_24;
assert nodeLink.path == toString pkgs.nodejs-slim_24;
assert one.PATH == expectedPath;
assert one.drvPath == changedWrapper.drvPath;
assert one.drvPath != two.drvPath;
assert one.drvPath == (create sources (builtins.toJSON metadata)).drvPath;
assert !mismatch.success && !wrong.success;
assert rawRetained == originalRaw;
assert rawRecord.sha256 == builtins.hashString "sha256" originalRaw;
assert one.drvPath != withRaw.drvPath;
assert tool.executable == (pkgs.python314.withPackages (p: [])).interpreter;
assert !(builtins.hasContext tool.drv);
assert forbidden == [];
assert one.drvPath != changedAssets.drvPath;
assert one.drvPath != changedReviews.drvPath;
assert one.drvPath != changedTool.drvPath;
assert toString one.passthru.inputs.prepared_depot.store_path == toString two.passthru.inputs.prepared_depot.store_path;
{ sameInputsSameDerivation = true; changedGraphDocsMiss = true; rawMismatchReject = true; originalUnicodeWhitespaceRetained = true; rawBytesAffectDocsKey = true; derivationMetadataHasNoDependencyContext = true; sourceProjectionExcludesBuildGitTests = true; assetsReviewToolInputsAffectDocsKey = true; graphDoesNotRetagDepot = true;
  nodeRuntimeMetadataClosurePathAgree = true; npmWrapperDoesNotAffectDocsKey = true;
  native = "NOT_RUN; mock tools/depot, symbolic derivations only"; }
