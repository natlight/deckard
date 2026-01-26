$ExtensionPath = Resolve-Path "..\extension"

# Common Chrome Install Locations
$ChromePaths = @(
    "C:\Program Files\Google\Chrome\Application\chrome.exe",
    "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe"
)

$ChromeExe = $null
foreach ($path in $ChromePaths) {
    if (Test-Path $path) {
        $ChromeExe = $path
        break
    }
}

if ($ChromeExe) {
    Write-Host "Launching Chrome with Deckard Extension..."
    Start-Process -FilePath $ChromeExe -ArgumentList "--load-extension=""$ExtensionPath"""
} else {
    Write-Error "Chrome executable not found."
    exit 1
}
