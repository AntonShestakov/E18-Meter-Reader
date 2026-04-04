param(
    [switch]$VerboseMode
)

$RootDir = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $RootDir
$EnvFile = Join-Path $RootDir '.env.local'

function Import-EnvFile {
    param([string]$Path)
    if (-not (Test-Path $Path)) {
        return
    }

    Get-Content $Path | ForEach-Object {
        if ($_ -match '^\s*#') { return }
        if ($_ -match '^\s*([^=]+)=(.*)$') {
            $key = $matches[1].Trim()
            $value = $matches[2].Trim()
            if ($value -ne '') {
                Set-Item -Path Env:$key -Value $value
            }
        }
    }
}

Import-EnvFile -Path $EnvFile

if (-not $env:DATABASE_URL) {
    Write-Error 'DATABASE_URL is not set. Please create .env.local with DATABASE_URL.'
    exit 1
}

if (-not $env:TELEGRAM_BOT_TOKEN) {
    Write-Warning 'TELEGRAM_BOT_TOKEN is not set. Set it in .env.local if you want to run the bot locally.'
}

$venvPath = Join-Path $RootDir 'venv'
if (-not (Test-Path $venvPath)) {
    python -m venv $venvPath
}

$PythonExe = Join-Path $venvPath 'Scripts\python.exe'
& $PythonExe -m pip install --upgrade pip
& $PythonExe -m pip install -e $RootDir

if (-not $env:FLYWAY_URL -or -not $env:FLYWAY_USER -or -not $env:FLYWAY_PASSWORD) {
    if ($env:DATABASE_URL -match '^postgresql://([^:]+):([^@]+)@([^:/]+)(:([0-9]+))?/([^?]+)') {
        $username = $matches[1]
        $password = $matches[2]
        $dbHost = $matches[3]
        $port = if ($matches[5]) { $matches[5] } else { '5432' }
        $database = $matches[6]
        $env:FLYWAY_URL = "jdbc:postgresql://${dbHost}:${port}/${database}"
        $env:FLYWAY_USER = $username
        $env:FLYWAY_PASSWORD = $password
        Write-Host 'Derived Flyway configuration from DATABASE_URL.'
    } else {
        Write-Error 'Could not parse DATABASE_URL for Flyway config.'
        exit 1
    }
}

$flywayExe = 'flyway'
try {
    Get-Command $flywayExe -ErrorAction Stop | Out-Null
} catch {
    Write-Error 'flyway CLI not found on PATH. Install Flyway or use Docker.'
    exit 1
}

& $flywayExe -locations=filesystem:migrations migrate
Write-Host 'Deployment complete. Bot dependencies installed and Flyway migrations applied.'
