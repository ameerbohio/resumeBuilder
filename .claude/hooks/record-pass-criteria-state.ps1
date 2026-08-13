# Run by the pass-criteria skill at the end of every run, PASS or FAIL, so the
# check-finalize-gate.ps1 PreToolUse hook has something deterministic to check against.
# Hashing logic here MUST stay identical to check-finalize-gate.ps1's -- both hash the
# draft body (content after "<!-- draft-below -->" in 3-compact-drafts/<slug>.md) the
# same way, or a correct PASS will look stale to the hook.
#
# Usage (call directly with & -- invoking via a nested `powershell -File` from
# an already-running PowerShell session has been observed to mangle the
# -GatesJson argument's quoting; `&` avoids the extra layer of argv reparsing):
#   & .claude/hooks/record-pass-criteria-state.ps1 `
#     -Slug "<slug>" -Verdict "PASS" -GatesJson '{"1_score_floor":"PASS",...,"9_bold_density":"PASS"}'

param(
    [Parameter(Mandatory = $true)][string]$Slug,
    [Parameter(Mandatory = $true)][ValidateSet("PASS", "FAIL")][string]$Verdict,
    [Parameter(Mandatory = $true)][string]$GatesJson
)

$ErrorActionPreference = "Stop"

$compactPath = "3-compact-drafts/$Slug.md"
$marker = "<!-- draft-below -->"

if (-not (Test-Path $compactPath)) {
    Write-Error "No such file: $compactPath"
    exit 1
}

$content = Get-Content -Raw $compactPath
$idx = $content.IndexOf($marker)
if ($idx -lt 0) {
    Write-Error "Missing sentinel '$marker' in $compactPath -- add it immediately before the draft body before running pass-criteria."
    exit 1
}

$draftBody = $content.Substring($idx + $marker.Length)
$draftBody = $draftBody.TrimStart("`r", "`n").TrimEnd()

$bytes = [System.Text.Encoding]::UTF8.GetBytes($draftBody)
$sha = [System.Security.Cryptography.SHA256]::Create()
$hashBytes = $sha.ComputeHash($bytes)
$hash = -join ($hashBytes | ForEach-Object { $_.ToString("x2") })

$gates = $GatesJson | ConvertFrom-Json

$state = [ordered]@{
    slug      = $Slug
    draftHash = $hash
    verdict   = $Verdict
    timestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
    gates     = $gates
}

New-Item -ItemType Directory -Force -Path ".claude/pipeline-state" | Out-Null
$statePath = ".claude/pipeline-state/$Slug.json"
$state | ConvertTo-Json -Depth 5 | Set-Content -Path $statePath -Encoding utf8

Write-Output "Recorded $Verdict for '$Slug' (hash $hash) -> $statePath"
