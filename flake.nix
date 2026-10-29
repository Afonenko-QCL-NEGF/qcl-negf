{
  description = "QCL-NEGF integrated source graph and development environment";
  inputs.self.submodules = true;
  inputs.platform.url = "path:./components/qcl-negf-platform";
  outputs = { self, platform }: let
    systems = [ "x86_64-linux" "aarch64-linux" ];
    forAll = platform.inputs.nixpkgs.lib.genAttrs systems;
  in {
    inherit (platform) nixosModules;
    lib = {
      mkPinnedJulia = { system, juliaTestProfile ? "production-build", juliaTestWorkerLimit ? null }:
        import ./components/QCLNEGFRunner.jl/nix/julia.nix {
          pkgs = platform.inputs.nixpkgs.legacyPackages.${system};
          testProfile = juliaTestProfile; testWorkerLimit = juliaTestWorkerLimit;
        };
      depotCompatibilityInputs = { system, juliaTestProfile ? "production-build", juliaTestWorkerLimit ? null }:
        (import ./nix/depot-compatibility.nix).inputs {
          root = ./.; inherit system juliaTestProfile juliaTestWorkerLimit;
          julia = self.lib.mkPinnedJulia { inherit system juliaTestProfile juliaTestWorkerLimit; };
        };
      mkPreparedDepot = { system, metadata, juliaTestProfile ? "production-build", juliaTestWorkerLimit ? null }: let
        pkgs = platform.inputs.nixpkgs.legacyPackages.${system};
        policy = import ./nix/depot-compatibility.nix;
        v2 = metadata.format == "qcl-negf.julia-depot.v2";
        expected = self.lib.depotCompatibilityInputs { inherit system juliaTestProfile juliaTestWorkerLimit; };
        manifest = builtins.hashFile "sha256" ./julia/Manifest.toml;
        depot = import ./nix/depot.nix { inherit pkgs; metadata = { inherit (metadata) url hash; }; };
      in assert metadata.julia == "1.13.0";
         assert metadata.juliaManifest == manifest;
         assert if v2 then policy.valid { inherit metadata expected manifest; }
           else metadata.format == "qcl-negf.julia-depot.v1" && metadata.sources.revision == self.rev;
         depot // { qclDepotFormat = metadata.format;
           qclDepotInputsSha256 = if v2 then policy.hash expected else null; };
      mkApplication = { system }: platform.lib.mkApplication {
        inherit system;
        workspaceRoot = self.outPath;
      };
      mkDocumentation = { system, metadata, capturedMetadata, assetInputs, reviewInputs, sources,
        juliaTestProfile ? "production-build", juliaTestWorkerLimit ? null }: let
        pkgs = platform.inputs.nixpkgs.legacyPackages.${system};
        lib = pkgs.lib;
        root = /. + builtins.unsafeDiscardStringContext self.outPath;
        selected = import ./nix/docs-sources.nix { inherit lib root; };
        julia = self.lib.mkPinnedJulia { inherit system juliaTestProfile juliaTestWorkerLimit; };
        depot = self.lib.mkPreparedDepot { inherit system metadata juliaTestProfile juliaTestWorkerLimit; };
        python = pkgs.python314.withPackages (p: [ p.pyyaml p.jsonschema ]);
        workspace = pkgs.runCommand "qcl-documentation-sources" {
          coreRuntime = selected.runtime.core; runnerRuntime = selected.runtime.runner;
          environment = selected.runtime.environment; coreDocs = selected.core;
          runnerDocs = selected.runner; contracts = selected.contracts;
          presentation = selected.presentation;
        } ''
          mkdir -p "$out/components/QCLNEGF.jl" "$out/components/QCLNEGFRunner.jl" "$out/julia"
          cp -a "$coreRuntime"/. "$out/components/QCLNEGF.jl/"
          cp -a "$runnerRuntime"/. "$out/components/QCLNEGFRunner.jl/"
          cp -a "$environment"/. "$out/julia/"
          chmod -R u+w "$out"
          cp -a "$coreDocs"/. "$out/components/QCLNEGF.jl/"
          cp -a "$runnerDocs"/. "$out/components/QCLNEGFRunner.jl/"
          mkdir -p "$out/components/qcl-negf-contracts"
          cp -a "$contracts"/. "$out/components/qcl-negf-contracts/"
          cp -a "$presentation"/. "$out/"
        '';
        file = relative: { path = "${workspace}/${relative}";
          sha256 = builtins.hashFile "sha256" (root + "/${relative}"); };
        record = path: { inherit path; sha256 = builtins.hashFile "sha256" path; };
        bind = value:
          if builtins.isString value && builtins.match "/nix/store/.*" value != null
          then builtins.storePath value
          else if builtins.isAttrs value then builtins.mapAttrs (_: bind) value
          else if builtins.isList value then map bind value else value;
        assetClosure = builtins.toFile "qcl-docs-assets-closure.json"
          (builtins.toJSON (bind (builtins.fromJSON (builtins.readFile assetInputs.path))));
        reviewClosure = builtins.toFile "qcl-docs-reviews-closure.json"
          (builtins.toJSON (bind (builtins.fromJSON (builtins.readFile reviewInputs.path))));
        tool = output: executable: version: { output = toString output;
          executable = "${output}/bin/${executable}";
          drv = if output ? drvPath then builtins.unsafeDiscardStringContext output.drvPath else null;
          expected_version = version; };
        inputs = {
          source_root = workspace;
          source_graph = record (builtins.toFile "qcl-docs-source-graph.json" (builtins.toJSON sources));
          plan = file "ops/docs/pilot-plan.json";
          project = file "julia/Project.toml"; manifest = file "julia/Manifest.toml";
          prepared_depot = { store_path = depot;
            metadata = record (builtins.toFile "qcl-docs-depot-original.json" capturedMetadata); };
          assets_lock = file "ops/docs/assets.lock.json";
          asset_inputs = assetInputs; review_inputs = reviewInputs;
          tools = { python = (tool python "python3" pkgs.python314.version) // { executable = python.interpreter; };
            node = tool pkgs.nodejs-slim_24 "node" pkgs.nodejs-slim_24.version;
            git = tool pkgs.git "git" pkgs.git.version;
            julia = tool julia "julia" "1.13.0"; };
        };
        inputFile = pkgs.writeText "qcl-docs-producer-inputs.json" (builtins.toJSON inputs);
        inputClosure = pkgs.linkFarm "qcl-docs-inputs" (map (name: { inherit name; path = {
          inherit workspace depot python julia assetClosure reviewClosure inputFile;
          node = pkgs.nodejs-slim_24; git = pkgs.git;
        }.${name}; }) [ "workspace" "depot" "python" "julia" "node" "git" "assetClosure" "reviewClosure" "inputFile" ]);
        artifact = builtins.derivation {
          name = "qcl-negf-documentation-v1"; inherit system;
          builder = python.interpreter;
          args = [ "-B" "${workspace}/ops/docs/produce.py" "--inputs" inputFile ];
          inherit assetClosure reviewClosure;
          PATH = "${python}/bin:${pkgs.nodejs-slim_24}/bin:${julia}/bin:${pkgs.git}/bin";
          PYTHONDONTWRITEBYTECODE = "1"; PYTHONNOUSERSITE = "1";
          JULIA_PKG_OFFLINE = "true"; JULIA_LOAD_PATH = "@:@stdlib";
          JULIA_NUM_THREADS = "1"; OPENBLAS_NUM_THREADS = "1"; OMP_NUM_THREADS = "1"; MKL_NUM_THREADS = "1";
        };
      in assert system == "x86_64-linux";
         assert sources.format == "qcl-negf.git-graph.v1" && sources.revision == self.rev;
         assert builtins.isString capturedMetadata && builtins.stringLength capturedMetadata <= 65536;
         assert builtins.fromJSON capturedMetadata == metadata;
         assert builtins.hashFile "sha256" assetInputs.path == assetInputs.sha256;
         assert builtins.hashFile "sha256" reviewInputs.path == reviewInputs.sha256;
         artifact // { passthru = { inherit inputClosure inputs; }; };
      mkSolver = { system, preparedDepot, juliaTestProfile ? "production-build",
        juliaTestWorkerLimit ? null }: let
        pkgs = platform.inputs.nixpkgs.legacyPackages.${system};
        runtimeSources = import ./nix/runtime-sources.nix {
          inherit (pkgs) lib;
          root = ./.;
        };
      in assert (preparedDepot.qclDepotFormat or null) != "qcl-negf.julia-depot.v2" ||
        preparedDepot.qclDepotInputsSha256 == (import ./nix/depot-compatibility.nix).hash
          (self.lib.depotCompatibilityInputs { inherit system juliaTestProfile juliaTestWorkerLimit; });
      import ./components/QCLNEGFRunner.jl/nix/package.nix {
        inherit pkgs preparedDepot;
        # Select only the Results capture CLI from the shared locked PythonSet.
        # Runner retains one ordinary spawn when this capability is unavailable.
        captureExecutable = "${(self.lib.mkApplication { inherit system; }).captureRuntime}/bin/qcl-negf-results";
        testProfile = juliaTestProfile;
        julia = self.lib.mkPinnedJulia { inherit system juliaTestProfile juliaTestWorkerLimit; };
        coreSrc = runtimeSources.core;
        runnerSrc = runtimeSources.runner;
        environmentSrc = runtimeSources.environment;
      };
    };
    packages = forAll (system: {
      application = self.lib.mkApplication { inherit system; };
      default = self.packages.${system}.application;
    });
    devShells = forAll (system: let
      pkgs = platform.inputs.nixpkgs.legacyPackages.${system};
    in {
      default = pkgs.mkShell {
        packages = with pkgs; [ deno git gh nix nixos-rebuild uv python314 nodejs_24 prefetch-npm-deps opentofu ansible ];
        shellHook = ''
          export NIX_CONFIG="experimental-features = nix-command flakes"
        '';
      };
    });
    checks = forAll (system: {
      inherit (platform.checks.${system}) operations infrastructure slurm-vm;
    });
  };
}
