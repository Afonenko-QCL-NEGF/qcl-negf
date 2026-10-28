{ source, system ? "x86_64-linux" }:
let project = builtins.getFlake source;
    pkgs = project.inputs.platform.inputs.nixpkgs.legacyPackages.${system};
in { source = project.outPath; caBundle = "${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt"; }
