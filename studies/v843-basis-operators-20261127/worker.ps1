param(
    [Parameter(Mandatory=$true)][string]$Task,
    [Parameter(Mandatory=$true)][int]$Cpus,
    [Parameter(Mandatory=$true)][string]$Budget,
    [string]$Part
)
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
$scratch = (Get-Location).Path
@"
task = "$Task"
status = "technical_error"
error_type = "worker_setup"
"@ | Set-Content -LiteralPath 'summary.toml' -Encoding Ascii
try {
    Expand-Archive -LiteralPath 'source.zip' -DestinationPath (Join-Path $scratch 'source')
    $workProfile = Join-Path $scratch 'profile'
    New-Item -ItemType Directory -Path $workProfile | Out-Null
    $env:USERPROFILE = $workProfile
    $env:HOME = $workProfile
    $env:HOMEDRIVE = Split-Path -Qualifier $workProfile
    $env:HOMEPATH = $workProfile.Substring($env:HOMEDRIVE.Length)
    $env:JULIA_DEPOT_PATH = Join-Path $scratch 'depot'
    $env:JULIA_PKG_PRECOMPILE_AUTO = '0'
    $env:OPENBLAS_NUM_THREADS = '1'
    $env:OMP_NUM_THREADS = '1'
    $env:MKL_NUM_THREADS = '1'
    $env:QCL_PARENT_RESULTS = $scratch
    $env:QCL_RESULT = Join-Path $scratch 'summary.toml'
    $env:QCL_SLOT_CPUS = $Cpus
    $mask = (Get-Process -Id $PID).ProcessorAffinity.ToInt64()
    $env:QCL_AFFINITY_CPUS = ([Convert]::ToString($mask, 2) -replace '0','').Length
    $env:QCL_BUDGET_GIB = $Budget
    $threads = $Cpus
    if ($Task -in 'B7','B9','B11') { $threads = 1 }
    $arguments = @('--startup-file=no','--compiled-modules=existing',"--threads=$threads,0",'--gcthreads=1,0',
                  '--project=source/runner','source/studies/v843-basis-operators-20261127/worker.jl',$Task)
    if ($Part) { $arguments += $Part }
    $process = Start-Process -FilePath 'C:\QCL-Julia\bin\julia.exe' -NoNewWindow -Wait -PassThru `
        -WorkingDirectory $scratch -ArgumentList $arguments `
        -RedirectStandardOutput (Join-Path $scratch 'julia.stdout') `
        -RedirectStandardError (Join-Path $scratch 'julia.stderr')
    Get-Content -LiteralPath 'julia.stdout'
    foreach ($line in (Get-Content -LiteralPath 'julia.stderr')) { [Console]::Error.WriteLine($line) }
    exit $process.ExitCode
} catch {
    [Console]::Error.WriteLine($_.ToString())
    exit 1
}
