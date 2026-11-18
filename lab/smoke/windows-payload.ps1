$ErrorActionPreference = 'Stop'
$inputHash = (Get-FileHash -LiteralPath 'challenge.txt' -Algorithm SHA256).Hash.ToLowerInvariant()
$identity = [Security.Principal.WindowsIdentity]::GetCurrent()
$principal = [Security.Principal.WindowsPrincipal]::new($identity)
$userSid = $identity.User.Value
$whoami = Join-Path ([Environment]::SystemDirectory) 'whoami.exe'
$groups = & $whoami /groups /fo csv /nh
if ($LASTEXITCODE -ne 0 -or -not $groups) {
    throw "Unable to inspect Windows token groups (whoami exit $LASTEXITCODE)"
}
$hasAdministratorsSid = [bool]($groups -match '^"(?:[^"]|"")*","(?:[^"]|"")*","S-1-5-32-544",')
$isAdministrator = $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if ($userSid -notmatch '^S-1-5-21-(\d+-){3}\d+$' -or
    $isAdministrator -or $hasAdministratorsSid) {
    throw "Expected an unprivileged Windows slot account, got $($identity.Name) ($userSid)"
}

[PSCustomObject]@{
    Hostname = $env:COMPUTERNAME
    User = $identity.Name
    UserSid = $userSid
    IsAdministrator = $isAdministrator
    HasAdministratorsSid = $hasAdministratorsSid
    InputSHA256 = $inputHash
} | ConvertTo-Json -Compress | Set-Content -LiteralPath 'result.json' -Encoding Ascii

$resultHash = (Get-FileHash -LiteralPath 'result.json' -Algorithm SHA256).Hash.ToLowerInvariant()
Write-Output "QCL_WINDOWS_RESULT_SHA256=$resultHash"
Write-Output 'QCL_WINDOWS_SMOKE_STDOUT'
[Console]::Error.WriteLine('QCL_WINDOWS_SMOKE_STDERR')
