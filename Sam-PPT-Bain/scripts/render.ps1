param(
    [Parameter(Mandatory = $true)][string]$Deck,
    [Parameter(Mandatory = $true)][string]$OutDir,
    [int]$Width = 1920,
    [int]$Height = 1080
)
# Render every slide with the real PowerPoint (the only renderer that proves the file opens and shows fonts right).
$ErrorActionPreference = "Stop"
New-Item -ItemType Directory -Force $OutDir | Out-Null
$pp = New-Object -ComObject PowerPoint.Application
$p = $pp.Presentations.Open((Resolve-Path $Deck).Path, $true, $false, $false)
try {
    $i = 1
    foreach ($s in $p.Slides) {
        $s.Export((Join-Path (Resolve-Path $OutDir).Path ("slide-{0:D2}.png" -f $i)), "PNG", $Width, $Height)
        $i++
    }
    "rendered $($i - 1)"
}
finally {
    $p.Close()
}
