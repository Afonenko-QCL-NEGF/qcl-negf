# Realize exactly one selected immutable CURRENT documentation package/closure.
{ inputFile, inputSha256, target ? "docs" }:
let
  bytes = builtins.readFile inputFile;
  raw = builtins.fromJSON bytes;
  exact = value: names: builtins.isAttrs value && builtins.attrNames value == builtins.sort builtins.lessThan names;
  project = builtins.getFlake raw.source;
  file = name: text: let path = builtins.toFile name text;
    in { inherit path; sha256 = builtins.hashString "sha256" text; };
  artifact = project.lib.mkDocumentation {
    system = "x86_64-linux";
    metadata = builtins.fromJSON raw.depot_metadata_json;
    capturedMetadata = raw.depot_capture_json;
    sources = raw.sources;
    assetInputs = file "qcl-docs-asset-inputs.json" raw.asset_inputs_json;
    reviewInputs = file "qcl-docs-review-inputs.json" raw.review_inputs_json;
    juliaTestProfile = raw.factory.profile;
    juliaTestWorkerLimit = raw.factory.test_workers;
  };
in assert builtins.hashString "sha256" bytes == inputSha256;
assert exact raw [ "format" "source" "sources" "factory" "depot_metadata_json" "depot_capture_json"
  "depot_capture_sha256" "asset_inputs_json" "review_inputs_json" ];
assert raw.format == "qcl-negf.docs-package-inputs.v1";
assert builtins.hashString "sha256" raw.depot_capture_json == raw.depot_capture_sha256;
assert project.rev == raw.sources.revision;
assert exact raw.factory [ "profile" "test_workers" ];
assert builtins.elem target [ "docs" "inputs" ];
if target == "inputs" then artifact.passthru.inputClosure else artifact
