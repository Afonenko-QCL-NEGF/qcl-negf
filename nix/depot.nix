# The manifest hashes archive bytes. fetchurl verifies those bytes before extraction.
{ pkgs, metadata }:
let archive = pkgs.fetchurl { inherit (metadata) url hash; };
in pkgs.runCommand "qcl-negf-julia-depot" {
  nativeBuildInputs = [ pkgs.gnutar pkgs.gzip ];
} ''
  mkdir -p "$out"
  tar --extract --gzip --file=${archive} --directory="$out" --no-same-owner
''
