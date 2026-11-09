# Quick Deployment Helper Script
# Run this anytime to check deployment status

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "            BUSINESS PLAN GENERATOR - DEPLOYMENT HELPER             " -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Check build status
Write-Host "🔍 Checking build status..." -ForegroundColor Yellow
if (Test-Path "dist\BusinessPlanGenerator.exe") {
    $file = Get-Item "dist\BusinessPlanGenerator.exe"
    $sizeMB = [math]::Round($file.Length/1MB, 2)
    
    Write-Host ""
    Write-Host "✅ BUILD COMPLETE!" -ForegroundColor Green
    Write-Host "   📦 File: BusinessPlanGenerator.exe" -ForegroundColor White
    Write-Host "   💾 Size: $sizeMB MB" -ForegroundColor White
    Write-Host "   📅 Built: $($file.LastWriteTime)" -ForegroundColor White
    Write-Host ""
    
    # Next steps
    Write-Host "⏭️  NEXT STEPS:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "1️⃣  TEST LOCALLY" -ForegroundColor Cyan
    Write-Host "   cd dist" -ForegroundColor Gray
    Write-Host "   .\BusinessPlanGenerator.exe" -ForegroundColor Gray
    Write-Host ""
    Write-Host "2️⃣  CREATE GITHUB RELEASE" -ForegroundColor Cyan
    Write-Host "   • Go to: https://github.com/venkatashivabramha/Gen-AI/releases" -ForegroundColor Gray
    Write-Host "   • Click 'Draft a new release'" -ForegroundColor Gray
    Write-Host "   • Tag: v1.1.0" -ForegroundColor Gray
    Write-Host "   • Title: v1.1.0 - Critical Bug Fixes" -ForegroundColor Gray
    Write-Host "   • Upload: dist\BusinessPlanGenerator.exe" -ForegroundColor Gray
    Write-Host "   • Copy description from: DEPLOYMENT_v1.1.0.md" -ForegroundColor Gray
    Write-Host ""
    Write-Host "3️⃣  PUBLISH & SHARE" -ForegroundColor Cyan
    Write-Host "   Download link will be:" -ForegroundColor Gray
    Write-Host "   https://github.com/venkatashivabramha/Gen-AI/releases/download/v1.1.0/BusinessPlanGenerator.exe" -ForegroundColor Blue
    Write-Host ""
    
} else {
    Write-Host ""
    Write-Host "⏳ BUILD IN PROGRESS..." -ForegroundColor Yellow
    Write-Host "   Check the separate PowerShell window" -ForegroundColor Gray
    Write-Host "   ⏰ Estimated time: 5-10 minutes" -ForegroundColor Gray
    Write-Host ""
    Write-Host "   To check status, run this script again:" -ForegroundColor White
    Write-Host "   .\check_deployment.ps1" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "   Or check manually:" -ForegroundColor White
    Write-Host "   Test-Path dist\BusinessPlanGenerator.exe" -ForegroundColor Cyan
    Write-Host ""
}

# Show git status
Write-Host "📊 GIT STATUS:" -ForegroundColor Magenta
Write-Host "   Latest commits:" -ForegroundColor Gray
git log --oneline -3 | ForEach-Object { Write-Host "   $_" -ForegroundColor White }
Write-Host ""

# Documentation
Write-Host "📚 DOCUMENTATION:" -ForegroundColor Blue
Write-Host "   • DEPLOYMENT_v1.1.0.md - Full guide" -ForegroundColor White
Write-Host "   • QUICK_REFERENCE.txt - Quick steps" -ForegroundColor White
Write-Host "   • DEPLOYMENT_SUMMARY.txt - Summary" -ForegroundColor White
Write-Host ""

Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
