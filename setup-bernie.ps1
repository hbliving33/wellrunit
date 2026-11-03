<#
.SYNOPSIS
  One-time setup for Bernie on wellrunit.com.  Run it once from your PowerShell machine.

.WHAT IT DOES
  1. In your hbliving.com Microsoft 365 tenant, creates an app called "Well Run IT - Bernie mail" that can send mail
     ONLY as support@wellrunit.com.  It uses Exchange RBAC for Applications, so the app gets no tenant-wide Mail.Send
     permission in Entra; Exchange limits it to the one mailbox.
  2. Creates a random session key, and a random private ntfy channel for emergency alerts to your and Vicki's phones.
  3. Asks you to paste four values from Cloudflare (API token, account ID, Turnstile site key and secret key).
  4. Saves all nine values as GitHub secrets on hbliving33/wellrunit using the GitHub CLI, then starts the deploy.

  Personal tenant (hbliving.com), not iMDx.  No log file is written, and secret values are never written to disk.

.RUN
  cd to the folder you saved it in, then:  .\setup-bernie.ps1
  It's safe to run again; it reuses the app, scope and assignment if they already exist, and makes a new client secret.
#>
#Requires -Version 7
param(
    [string]$Admin   = 'eric@hbliving.com',
    [string]$Mailbox = 'support@wellrunit.com',
    [string]$Repo    = 'hbliving33/wellrunit'
)
$ErrorActionPreference = 'Stop'
$AppName   = 'Well Run IT - Bernie mail'
$ScopeName = 'Bernie - support mailbox only'
function Say($msg, $color = 'Gray') { Write-Host $msg -ForegroundColor $color }

# ---------- modules and tools ----------
foreach ($m in 'Microsoft.Graph.Authentication', 'Microsoft.Graph.Applications', 'ExchangeOnlineManagement') {
    if (-not (Get-Module -ListAvailable -Name $m)) { Say "Installing $m..."; Install-Module $m -Scope CurrentUser -Force -AllowClobber }
    Import-Module $m
}
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    Say 'Installing the GitHub CLI...'
    winget install --id GitHub.cli -e --accept-source-agreements --accept-package-agreements | Out-Null
    $env:Path = [Environment]::GetEnvironmentVariable('Path', 'Machine') + ';' + [Environment]::GetEnvironmentVariable('Path', 'User')
}
gh auth status 2>$null | Out-Null
if ($LASTEXITCODE -ne 0) { Say 'Sign in to GitHub in the browser window that opens...' 'Cyan'; gh auth login --hostname github.com --git-protocol https --web }

# ---------- 1. Entra app (no API permissions granted here) ----------
Say "Signing in to Microsoft Graph (use $Admin)..." 'Cyan'
Connect-MgGraph -Scopes 'Application.ReadWrite.All' -NoWelcome
$tenant = (Get-MgContext).TenantId

$app = Get-MgApplication -Filter "displayName eq '$AppName'" | Select-Object -First 1
if (-not $app) { $app = New-MgApplication -DisplayName $AppName -SignInAudience 'AzureADMyOrg'; Say "Created app registration: $($app.AppId)" }
else { Say "Using existing app registration: $($app.AppId)" }

$sp = Get-MgServicePrincipal -Filter "appId eq '$($app.AppId)'" | Select-Object -First 1
if (-not $sp) { $sp = New-MgServicePrincipal -AppId $app.AppId; Say "Created service principal: $($sp.Id)" }

$expires = (Get-Date).AddMonths(24)
$pw = Add-MgApplicationPassword -ApplicationId $app.Id -PasswordCredential @{ displayName = "Bernie Worker {0:yyyy-MM-dd}" -f (Get-Date); endDateTime = $expires }
foreach ($old in (Get-MgApplication -ApplicationId $app.Id).PasswordCredentials | Where-Object { $_.KeyId -ne $pw.KeyId }) {
    Remove-MgApplicationPassword -ApplicationId $app.Id -KeyId $old.KeyId
    Say 'Removed an older client secret from a previous run.'
}
Say ("New client secret created.  It expires {0:MMMM d, yyyy}; run this script again before then." -f $expires) 'Yellow'

# ---------- 2. Exchange RBAC for Applications: Mail.Send on the support mailbox only ----------
Say "Signing in to Exchange Online as $Admin..." 'Cyan'
# -DisableWAM avoids the Windows sign-in broker crash ("Object reference not set...") in some terminals; it needs module 3.7.2 or later
if (-not (Get-Command Connect-ExchangeOnline).Parameters.ContainsKey('DisableWAM')) {
    Say 'Updating ExchangeOnlineManagement (3.7.2 or later is needed)...'
    Install-Module ExchangeOnlineManagement -Scope CurrentUser -Force -AllowClobber
    Remove-Module ExchangeOnlineManagement -ErrorAction SilentlyContinue
    Import-Module ExchangeOnlineManagement -Force
}
Connect-ExchangeOnline -UserPrincipalName $Admin -ShowBanner:$false -DisableWAM
$null = Get-Mailbox -Identity $Mailbox   # stops here if the mailbox doesn't exist

if (-not (Get-ServicePrincipal -Identity $app.AppId -ErrorAction SilentlyContinue)) {
    New-ServicePrincipal -AppId $app.AppId -ObjectId $sp.Id -DisplayName $AppName | Out-Null
    Say 'Registered the app with Exchange Online.'
}
if (-not (Get-ManagementScope -Identity $ScopeName -ErrorAction SilentlyContinue)) {
    New-ManagementScope -Name $ScopeName -RecipientRestrictionFilter "PrimarySmtpAddress -eq '$Mailbox'" | Out-Null
    Say "Created management scope: $ScopeName"
}
$have = Get-ManagementRoleAssignment -Role 'Application Mail.Send' -ErrorAction SilentlyContinue | Where-Object { $_.CustomResourceScope -eq $ScopeName }
if (-not $have) {
    New-ManagementRoleAssignment -App $app.AppId -Role 'Application Mail.Send' -CustomResourceScope $ScopeName | Out-Null
    Say 'Assigned Application Mail.Send, limited to the support mailbox.'
}
Say 'Permission check (InScope should be True):' 'Cyan'
Test-ServicePrincipalAuthorization -Identity $app.AppId -Resource $Mailbox | Format-Table RoleName, GrantedPermissions, AllowedResourceScope, InScope -AutoSize
Disconnect-ExchangeOnline -Confirm:$false
Disconnect-MgGraph | Out-Null

# ---------- 3. Random values ----------
$bytes = [byte[]]::new(48); [Security.Cryptography.RandomNumberGenerator]::Fill($bytes)
$sessionKey = [Convert]::ToBase64String($bytes)
$chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
$ntfy = 'wellrunit-alerts-' + (-join (1..24 | ForEach-Object { $chars[[Security.Cryptography.RandomNumberGenerator]::GetInt32($chars.Length)] }))

# ---------- 4. Cloudflare values (pasted, never shown) ----------
Write-Host ''
Write-Host 'Paste the four Cloudflare values.  Nothing you paste is shown or saved to disk.' -ForegroundColor Cyan
$cfToken   = Read-Host 'Cloudflare API token' -MaskInput
$cfAccount = Read-Host 'Cloudflare account ID'
$tsSite    = Read-Host 'Turnstile site key'
$tsSecret  = Read-Host 'Turnstile secret key' -MaskInput

# ---------- 5. GitHub secrets, then deploy ----------
$secrets = [ordered]@{
    CLOUDFLARE_API_TOKEN = $cfToken; CLOUDFLARE_ACCOUNT_ID = $cfAccount
    TURNSTILE_SITEKEY = $tsSite; TURNSTILE_SECRET = $tsSecret
    GRAPH_TENANT = $tenant; GRAPH_CLIENT_ID = $app.AppId; GRAPH_CLIENT_SECRET = $pw.SecretText
    SESSION_KEY = $sessionKey; NTFY_TOPIC = $ntfy
}
foreach ($k in $secrets.Keys) {
    if ([string]::IsNullOrWhiteSpace($secrets[$k])) { throw "$k is empty.  Nothing was saved to GitHub; run the script again." }
}
foreach ($k in $secrets.Keys) {
    $secrets[$k] | gh secret set $k --repo $Repo
    if ($LASTEXITCODE -ne 0) { throw "Couldn't save $k to GitHub." }
    Say "Saved GitHub secret $k"
}
gh workflow run worker.yml --repo $Repo
Say 'Deploy started: https://github.com/hbliving33/wellrunit/actions/workflows/worker.yml' 'Green'

Write-Host ''
Write-Host 'Last step, on your phone and Vicki''s:' -ForegroundColor Cyan
Write-Host '  Open the ntfy app, tap +, and subscribe to this channel name exactly:'
Write-Host "  $ntfy" -ForegroundColor Green
Write-Host '  Keep it private.  Anyone with the name could send alerts to your phones.'
Write-Host ''
Write-Host 'Note: Exchange can take 30 minutes to 2 hours to start honoring a new app permission.  If Bernie''s first test email doesn''t arrive, that''s why.' -ForegroundColor Yellow
