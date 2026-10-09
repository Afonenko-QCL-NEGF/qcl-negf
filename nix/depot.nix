# The manifest hashes archive bytes. fetchurl verifies those bytes before extraction.
{ pkgs, metadata }:
let archive = pkgs.fetchurl {
  # Match the verified local prefetch performed by ops/solver.ts.
  name = "qcl-negf-julia-depot.tar.gz";
  inherit (metadata) url hash;
};
in pkgs.runCommand "qcl-negf-julia-depot" {
  nativeBuildInputs = [ pkgs.gnutar pkgs.gzip ];
} ''
  mkdir -p "$out"
  tar --extract --gzip --file=${archive} --directory="$out" --no-same-owner
''
