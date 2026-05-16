param(
  [string]$InputPath = "./data.xlsx",
  [string]$OutDir = "./data"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Import-Module ImportExcel

function Get-StringValue {
  param([object]$Value)
  if ($null -eq $Value) { return "" }
  return ([string]$Value).Trim()
}

function Get-SafeHeader {
  param(
    [string]$Raw,
    [int]$Index,
    [hashtable]$Seen
  )

  $name = $Raw.Trim()
  if ([string]::IsNullOrWhiteSpace($name)) {
    $name = "col_$Index"
  }

  $name = $name -replace "\s+", "_"
  $name = $name -replace "[^\p{L}\p{Nd}_\-]", ""
  if ([string]::IsNullOrWhiteSpace($name)) {
    $name = "col_$Index"
  }

  if (-not $Seen.ContainsKey($name)) {
    $Seen[$name] = 1
    return $name
  }

  $Seen[$name] += 1
  return "{0}_{1}" -f $name, $Seen[$name]
}

function To-NumberOrKeep {
  param([object]$Value)

  if ($null -eq $Value) { return $null }
  if ($Value -is [double] -or $Value -is [float] -or $Value -is [int] -or $Value -is [long] -or $Value -is [decimal]) {
    return $Value
  }

  $text = Get-StringValue -Value $Value
  if ([string]::IsNullOrWhiteSpace($text)) { return $null }

  $num = 0.0
  if ([double]::TryParse($text, [ref]$num)) {
    return $num
  }

  return $Value
}

function Convert-Sheet {
  param(
    [string]$Workbook,
    [string]$SheetName
  )

  $raw = Import-Excel -Path $Workbook -WorksheetName $SheetName -NoHeader
  if ($null -eq $raw -or $raw.Count -eq 0) {
    return @()
  }

  $props = $raw[0].PSObject.Properties.Name
  $scanRows = [Math]::Min(20, $raw.Count)

  $bestHeaderRow = -1
  $bestScore = -1

  for ($i = 0; $i -lt $scanRows; $i++) {
    $row = $raw[$i]
    $nonEmpty = 0
    foreach ($p in $props) {
      $v = Get-StringValue -Value $row.$p
      if ($v -ne "") { $nonEmpty++ }
    }
    if ($nonEmpty -gt $bestScore) {
      $bestScore = $nonEmpty
      $bestHeaderRow = $i
    }
  }

  if ($bestHeaderRow -lt 0) {
    return @()
  }

  $headerRow = $raw[$bestHeaderRow]
  $seen = @{}
  $headers = @()

  for ($c = 0; $c -lt $props.Count; $c++) {
    $prop = $props[$c]
    $rawName = Get-StringValue -Value $headerRow.$prop
    $headers += (Get-SafeHeader -Raw $rawName -Index ($c + 1) -Seen $seen)
  }

  $records = @()
  for ($r = $bestHeaderRow + 1; $r -lt $raw.Count; $r++) {
    $row = $raw[$r]
    $obj = [ordered]@{}
    $nonEmpty = 0

    for ($c = 0; $c -lt $props.Count; $c++) {
      $prop = $props[$c]
      $key = $headers[$c]
      $value = To-NumberOrKeep -Value $row.$prop
      if ($null -ne $value -and (Get-StringValue -Value $value) -ne "") { $nonEmpty++ }
      $obj[$key] = $value
    }

    if ($nonEmpty -gt 0) {
      $records += [pscustomobject]$obj
    }
  }

  return $records
}

$repoRoot = Split-Path -Parent $PSScriptRoot
$resolvedInput = Resolve-Path (Join-Path $repoRoot $InputPath)
$resolvedOut = Join-Path $repoRoot $OutDir
$sheetOut = Join-Path $resolvedOut "sheets"

New-Item -ItemType Directory -Path $resolvedOut -Force | Out-Null
New-Item -ItemType Directory -Path $sheetOut -Force | Out-Null

$sheetInfos = Get-ExcelSheetInfo -Path $resolvedInput
$manifestSheets = @()
$combinedData = $null

foreach ($s in $sheetInfos) {
  $sheetName = $s.Name
  $records = Convert-Sheet -Workbook $resolvedInput -SheetName $sheetName

  $safeFile = ($sheetName -replace "[^\w\-]", "_") + ".json"
  $outFile = Join-Path $sheetOut $safeFile
  ($records | ConvertTo-Json -Depth 20) | Set-Content -Path $outFile -Encoding utf8

  $manifestSheets += [pscustomobject]@{
    sheet = $sheetName
    file = "sheets/$safeFile"
    rows = $records.Count
  }

  if ($sheetName -eq "08_Combined Data") {
    $combinedData = $records
    ($records | ConvertTo-Json -Depth 20) | Set-Content -Path (Join-Path $resolvedOut "combined_data.json") -Encoding utf8
  }
}

if ($null -ne $combinedData) {
  $features = @()
  foreach ($row in $combinedData) {
    $lat = $null
    $lon = $null

    if ($row.PSObject.Properties.Name -contains "latitude") { $lat = $row.latitude }
    if ($row.PSObject.Properties.Name -contains "longitude") { $lon = $row.longitude }

    if ($null -eq $lat -or $null -eq $lon) { continue }

    $latVal = 0.0
    $lonVal = 0.0
    if (-not [double]::TryParse((Get-StringValue -Value $lat), [ref]$latVal)) { continue }
    if (-not [double]::TryParse((Get-StringValue -Value $lon), [ref]$lonVal)) { continue }

    if ($latVal -eq 0 -and $lonVal -eq 0) { continue }

    $props = [ordered]@{}
    foreach ($p in $row.PSObject.Properties.Name) {
      if ($p -in @("latitude", "longitude")) { continue }
      $props[$p] = $row.$p
    }

    $features += [pscustomobject]@{
      type = "Feature"
      geometry = [pscustomobject]@{
        type = "Point"
        coordinates = @($lonVal, $latVal)
      }
      properties = [pscustomobject]$props
    }
  }

  $geo = [pscustomobject]@{
    type = "FeatureCollection"
    features = $features
  }

  ($geo | ConvertTo-Json -Depth 30) | Set-Content -Path (Join-Path $resolvedOut "all_points.geojson") -Encoding utf8
}

$manifest = [pscustomobject]@{
  source_xlsx = (Split-Path $resolvedInput -Leaf)
  generated_at_utc = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
  total_sheets = $sheetInfos.Count
  files = $manifestSheets
}

($manifest | ConvertTo-Json -Depth 10) | Set-Content -Path (Join-Path $resolvedOut "manifest.json") -Encoding utf8

Write-Output "Data conversion complete."
Write-Output ("Sheets exported: {0}" -f $sheetInfos.Count)
if ($null -ne $combinedData) {
  Write-Output ("Combined rows: {0}" -f $combinedData.Count)
}
