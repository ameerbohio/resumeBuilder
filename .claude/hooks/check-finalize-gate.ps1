# PreToolUse hook (Bash|Write|Edit). Hard-blocks any write to 4-final-drafts/<slug>.md
# unless a fresh, matching pass-criteria PASS is recorded in .claude/pipeline-state/<slug>.json.
# "Matching" means the hash recorded there equals the hash of the CURRENT draft body in
# 3-compact-drafts/<slug>.md (everything after the "<!-- draft-below -->" sentinel) -- so any
# edit to the compact draft after the last pass-criteria run invalidates the recorded PASS.
#
# Hook input is JSON on stdin: { tool_name, tool_input: { command } | { file_path, ... }, ... }
# Silence + exit 0 = allow. JSON with hookSpecificOutput.permissionDecision="deny" = block.

$ErrorActionPreference = "Stop"

function Allow {
    exit 0
}

function Deny([string]$Reason) {
    $out = [ordered]@{
        hookSpecificOutput = [ordered]@{
            hookEventName            = "PreToolUse"
            permissionDecision       = "deny"
            permissionDecisionReason = $Reason
        }
    }
    $out | ConvertTo-Json -Depth 5 -Compress
    exit 0
}

try {
    $raw = [Console]::In.ReadToEnd()
    $data = $raw | ConvertFrom-Json
}
catch {
    Allow  # can't parse hook input -- fail open, don't brick unrelated tool calls
}

$toolName = $data.tool_name
$slug = $null

if ($toolName -eq "Write" -or $toolName -eq "Edit") {
    # Write/Edit's file_path is unambiguously the thing being written -- no read case to exclude.
    $targetText = $data.tool_input.file_path
    if (-not [string]::IsNullOrEmpty($targetText)) {
        $m = [regex]::Match($targetText, '4-final-drafts[/\\]([A-Za-z0-9._-]+)\.md')
        if ($m.Success) { $slug = $m.Groups[1].Value }
    }
}
elseif ($toolName -eq "Bash") {
    $cmd = $data.tool_input.command
    if (-not [string]::IsNullOrEmpty($cmd)) {
        # A Bash command merely *reading* a 4-final-drafts file (cat/head/grep/ls/diff-as-source)
        # must NOT be blocked -- only redirection/copy/move patterns that actually write into it.
        $m = [regex]::Match($cmd, '(?:>{1,2}\s*"?''?|\b(?:cp|mv|tee)\b(?:(?!\||;).)*?)4-final-drafts[/\\]([A-Za-z0-9._-]+)\.md')
        if ($m.Success) { $slug = $m.Groups[1].Value }
    }
}
else {
    Allow
}

if ([string]::IsNullOrEmpty($slug)) { Allow }  # not a write into 4-final-drafts/*.md at all

$compactPath = "3-compact-drafts/$slug.md"
$statePath = ".claude/pipeline-state/$slug.json"
$marker = "<!-- draft-below -->"

if (-not (Test-Path $compactPath)) {
    Deny "No 3-compact-drafts/$slug.md found. Finalize requires a compact draft with a recorded pass-criteria PASS -- run the Stage 3 loop first."
}

$content = Get-Content -Raw $compactPath
$idx = $content.IndexOf($marker)
if ($idx -lt 0) {
    Deny "3-compact-drafts/$slug.md is missing the '$marker' sentinel that marks where the draft body starts, so this gate can't isolate the draft content to verify it. Add the sentinel immediately before the draft body (see the compactor/finalize skill docs) before finalizing."
}

$draftBody = $content.Substring($idx + $marker.Length)
$draftBody = $draftBody.TrimStart("`r", "`n").TrimEnd()

$bytes = [System.Text.Encoding]::UTF8.GetBytes($draftBody)
$sha = [System.Security.Cryptography.SHA256]::Create()
$hashBytes = $sha.ComputeHash($bytes)
$currentHash = -join ($hashBytes | ForEach-Object { $_.ToString("x2") })

if (-not (Test-Path $statePath)) {
    Deny "No pass-criteria verdict recorded for '$slug' ($statePath missing). Run the pass-criteria skill (all nine gates -- raw-score, ats-score, and hr-simulation must each independently pass) before finalizing."
}

try {
    $state = Get-Content -Raw $statePath | ConvertFrom-Json
}
catch {
    Deny "$statePath exists but is not valid JSON. Re-run pass-criteria to regenerate it."
}

if ($state.verdict -ne "PASS") {
    Deny "Last recorded pass-criteria verdict for '$slug' is $($state.verdict) (recorded $($state.timestamp)). All nine gates must PASS before finalizing -- re-run pass-criteria and address the open gate(s)."
}

if ($state.draftHash -ne $currentHash) {
    Deny "3-compact-drafts/$slug.md has changed since the last pass-criteria PASS (recorded $($state.timestamp), hash $($state.draftHash)). The current draft hashes to $currentHash instead -- the recorded verdict no longer matches this content. Re-run pass-criteria before finalizing."
}

Allow
