# One ordinary offline derivation. Every public input is already in the store.
{ inputsFile }:
let
  raw = builtins.fromJSON (builtins.readFile inputsFile);
  bind = value:
    if builtins.isString value && builtins.match "/nix/store/.*" value != null
    then builtins.storePath value
    else if builtins.isAttrs value then builtins.mapAttrs (_: bind) value
    else if builtins.isList value then map bind value
    else value;
  inputs = bind raw;
  # Asset manifest values are paths too; retain their contexts as dependencies.
  assets = bind (builtins.fromJSON (builtins.readFile inputs.asset_inputs.path));
  materialized = builtins.toFile "qcl-docs-producer-inputs.json" (builtins.toJSON inputs);
  assetDependencies = builtins.toJSON assets;
  reviewDependencies = builtins.toJSON (bind (builtins.fromJSON (builtins.readFile inputs.review_inputs.path)));
in builtins.derivation {
  name = "qcl-docs-pilot-v1";
  system = "x86_64-linux";
  builder = inputs.tools.python.executable;
  args = [ "-B" "${inputs.source_root}/ops/docs/produce.py" "--inputs" materialized ];
  inherit assetDependencies reviewDependencies;
  preferLocalBuild = true;
  allowSubstitutes = false;
  outputs = [ "out" ];
  PATH = "${inputs.tools.python.store_path}/bin:${inputs.tools.node.store_path}/bin:${inputs.tools.julia.store_path}/bin:${inputs.tools.git.store_path}/bin";
  PYTHONDONTWRITEBYTECODE = "1";
  PYTHONNOUSERSITE = "1";
  JULIA_PKG_OFFLINE = "true";
  JULIA_LOAD_PATH = "@:@stdlib";
  JULIA_NUM_THREADS = "1";
  OPENBLAS_NUM_THREADS = "1";
  OMP_NUM_THREADS = "1";
  MKL_NUM_THREADS = "1";
}
