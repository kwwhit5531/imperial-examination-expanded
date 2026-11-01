param(
    [switch]$Launch,
    [switch]$StartAsCandidate
)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$modRoot = Join-Path $projectRoot 'imperial_examination_expanded'
$testRoot = Join-Path $projectRoot '.runtime/ck3-user'
$testModDir = Join-Path $testRoot 'mod'
$gameRoot = 'C:\Program Files (x86)\Steam\steamapps\common\Crusader Kings III'
if (-not (Test-Path -LiteralPath (Join-Path $modRoot 'descriptor.mod'))) {
    throw 'Mod descriptor is missing.'
}
New-Item -ItemType Directory -Force -Path $testModDir | Out-Null
$forwardModPath = $modRoot.Replace('\', '/')
$descriptor = Get-Content -Raw -LiteralPath (Join-Path $modRoot 'descriptor.mod')
$descriptor += "`npath=`"$forwardModPath`"`n"
[IO.File]::WriteAllText((Join-Path $testModDir 'imperial_examination_expanded.mod'), $descriptor, [Text.UTF8Encoding]::new($false))
$load = @{ enabled_mods = @('mod/imperial_examination_expanded.mod'); disabled_dlcs = @() } | ConvertTo-Json
[IO.File]::WriteAllText((Join-Path $testRoot 'dlc_load.json'), $load, [Text.UTF8Encoding]::new($false))
Write-Output "Prepared isolated test profile: $testRoot"
Write-Output 'Normal CK3 playsets, settings, and saves were not changed.'
if ($Launch) {
    if (Get-Process -Name ck3 -ErrorAction SilentlyContinue) {
        throw 'CK3 is already running. Close it before starting the isolated test.'
    }
    $gameArgs = @('-debug_mode', '-suppress_error_log', '-skip_checksum', "-userdir=`"$testRoot`"")
    if ($StartAsCandidate) {
        # Installed bookmark: Qin Guan, an examination candidate in 1066 China.
        $gameArgs += @('-skip', '-bookmark=bm_1066_china', '-play=c_nf_qin_79E6_4')
    }
    # This is an interactive game test: its window must be available for UI QA.
    Start-Process -FilePath (Join-Path $gameRoot 'binaries/ck3.exe') -WorkingDirectory $gameRoot -ArgumentList $gameArgs -WindowStyle Normal
    Write-Output 'Started CK3 with the isolated profile and prototype enabled.'
}
