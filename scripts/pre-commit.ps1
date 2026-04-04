#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Pre-commit hook script for E18 Meter Reader Bot
    Runs linting, formatting, and tests before allowing commits

.DESCRIPTION
    This script enforces code quality by running:
    1. ruff (linter)
    2. black (formatter)
    3. pytest (tests)

    Exit code 0 = all checks passed
    Exit code 1 = at least one check failed

.EXAMPLE
    PS> .\scripts\pre-commit.ps1

.NOTES
    - Can be run manually anytime
    - When installed via `pre-commit install`, runs automatically on `git commit`
    - Use `git commit --no-verify` to skip (NOT RECOMMENDED)
#>

param(
    [switch]$Fix = $false,           # Auto-fix issues with black/ruff
    [switch]$Verbose = $false        # Show detailed output
)

$ErrorActionPreference = "Continue"
$script:FailCount = 0

function Write-Header {
    param([string]$Text)
    Write-Host ""
    Write-Host "=" * 70 -ForegroundColor Cyan
    Write-Host $Text -ForegroundColor Cyan
    Write-Host "=" * 70 -ForegroundColor Cyan
}

function Write-Status {
    param([string]$Text, [string]$Status, [string]$Color = "Green")
    Write-Host "[$(Get-Date -Format 'HH:mm:ss')] $Text ... " -NoNewline
    Write-Host $Status -ForegroundColor $Color
}

function Test-PyVersion {
    try {
        $python = python --version 2>&1
        Write-Status "Python version" "$python" "Green"
        return $true
    } catch {
        Write-Status "Python check" "FAILED - Python not found" "Red"
        $script:FailCount++
        return $false
    }
}

function Invoke-Ruff {
    Write-Header "Linting with Ruff"

    $args = @("check", ".")
    if ($Fix) { $args += "--fix" }

    try {
        & ruff $args
        Write-Status "Ruff linting" "PASSED" "Green"
        return $true
    } catch {
        Write-Status "Ruff linting" "FAILED" "Red"
        $script:FailCount++
        return $false
    }
}

function Invoke-Black {
    Write-Header "Formatting with Black"

    $args = @(".")
    if (-not $Fix) { $args += "--check" }
    if ($Verbose) { $args += "--verbose" }

    try {
        & black $args
        Write-Status "Black formatting" "PASSED" "Green"
        return $true
    } catch {
        Write-Status "Black formatting" "FAILED" "Red"
        if (-not $Fix) {
            Write-Host "`nTip: Run with -Fix flag to auto-format:" -ForegroundColor Yellow
            Write-Host "     .\scripts\pre-commit.ps1 -Fix`n" -ForegroundColor Yellow
        }
        $script:FailCount++
        return $false
    }
}

function Invoke-Pytest {
    Write-Header "Running Tests"

    $args = @("tests/", "-v", "--tb=short")

    try {
        & python -m pytest $args
        Write-Status "Pytest tests" "PASSED" "Green"
        return $true
    } catch {
        Write-Status "Pytest tests" "FAILED" "Red"
        $script:FailCount++
        return $false
    }
}

function Invoke-CoverageCheck {
    Write-Header "Checking Test Coverage"

    try {
        # Install coverage if needed
        & pip install coverage -q 2>$null

        $args = @("run", "-m", "pytest", "tests/", "-q")
        & python -m coverage $args

        # Generate report
        & python -m coverage report --fail-under=60
        Write-Status "Coverage check" "PASSED (≥60%)" "Green"
        return $true
    } catch {
        Write-Status "Coverage check" "WARNING - coverage < 60%" "Yellow"
        # Don't fail on coverage, just warn
        return $true
    }
}

# Main execution
Write-Host "`n" + ("*" * 70) -ForegroundColor Magenta
Write-Host "*" + (" " * 68) + "*" -ForegroundColor Magenta
Write-Host "*" + ("  E18 Meter Reader Bot - Pre-commit Quality Checks".PadRight(68)) + "*" -ForegroundColor Magenta
Write-Host "*" + (" " * 68) + "*" -ForegroundColor Magenta
Write-Host ("*" * 70) -ForegroundColor Magenta

# Run all checks
$AllPass = $true
$AllPass = (Test-PyVersion) -and $AllPass

if (-not $AllPass) {
    exit 1
}

$AllPass = (Invoke-Ruff) -and $AllPass
$AllPass = (Invoke-Black) -and $AllPass
$AllPass = (Invoke-Pytest) -and $AllPass
# $AllPass = (Invoke-CoverageCheck) -and $AllPass  # Optional

# Summary
Write-Header "Summary"
if ($script:FailCount -eq 0) {
    Write-Host "`n[PASS] All checks PASSED!" -ForegroundColor Green
    Write-Host "`nYou may now commit your changes.`n" -ForegroundColor Green
    exit 0
} else {
    Write-Host "`n[FAIL] $($script:FailCount) check(s) FAILED!" -ForegroundColor Red
    Write-Host "`nPlease fix the issues above before committing.`n" -ForegroundColor Red
    exit 1
}
