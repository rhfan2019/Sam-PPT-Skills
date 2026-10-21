# Export every slide of a deck to PNG with real PowerPoint (the rendering the user sees).
# Usage: powershell -ExecutionPolicy Bypass -File render.ps1 <deck.pptx> <out_dir> [width]
param(
    [Parameter(Mandatory = $true)][string]$Deck,
    [Parameter(Mandatory = $true)][string]$OutDir,
    [int]$Width = 1600
)
$ErrorActionPreference = "Stop"
$deckPath = (Resolve-Path $Deck).Path
New-Item -ItemType Directory -Force $OutDir | Out-Null
$outPath = (Resolve-Path $OutDir).Path

$app = New-Object -ComObject PowerPoint.Application
try {
    # ReadOnly, Untitled, WithWindow=false
    $pres = $app.Presentations.Open($deckPath, $true, $true, $false)
    $height = [int]($Width * $pres.PageSetup.SlideHeight / $pres.PageSetup.SlideWidth)
    foreach ($slide in $pres.Slides) {
        $name = "slide-{0:D2}.png" -f $slide.SlideIndex
        $slide.Export((Join-Path $outPath $name), "PNG", $Width, $height)
    }
    Write-Output ("rendered {0} slide(s) -> {1}" -f $pres.Slides.Count, $outPath)
    $pres.Close()
}
finally {
    if ($app.Presentations.Count -eq 0) { $app.Quit() }
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($app) | Out-Null
}
