$ErrorActionPreference = 'Stop'
$inputHash = (Get-FileHash -LiteralPath 'challenge.txt' -Algorithm SHA256).Hash.ToLowerInvariant()
$identity = [Security.Principal.WindowsIdentity]::GetCurrent()
$principal = [Security.Principal.WindowsPrincipal]::new($identity)
$userSid = $identity.User.Value
$claims = @($identity.UserClaims)
$primarySid = @($claims | Where-Object Type -eq ([Security.Claims.ClaimTypes]::PrimarySid))
if ($primarySid.Count -ne 1 -or $primarySid[0].Value -ne $userSid) {
    throw 'Unable to confirm Windows token account SID'
}
$groupSidTypes = @([Security.Claims.ClaimTypes]::GroupSid, [Security.Claims.ClaimTypes]::DenyOnlySid)
$hasAdministratorsSid = [bool]($claims | Where-Object {
    $_.Type -in $groupSidTypes -and $_.Value -eq 'S-1-5-32-544'
})
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
