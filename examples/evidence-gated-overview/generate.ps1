param(
  [Parameter(Mandatory=$true)][string]$ReviewVersion,
  [string]$PythonExe = 'python'
)
$ErrorActionPreference = 'Stop'
$sampleDir = $PSScriptRoot
$repoDir = [IO.Path]::GetFullPath((Join-Path $sampleDir '..\..'))
$reviewRoot = Join-Path $sampleDir 'review'
$reviewDir = Join-Path $reviewRoot $ReviewVersion
$sourcePath = Join-Path $reviewDir 'source.pptx'
$fullPng = Join-Path $reviewDir 'full.png'
$spec = Get-Content -Raw -LiteralPath (Join-Path $sampleDir 'design-spec.json') | ConvertFrom-Json
if (Test-Path -LiteralPath $reviewDir) { throw 'Use a fresh ReviewVersion; existing source and review evidence are not overwritten.' }
if (-not (Get-Command $PythonExe -CommandType Application -ErrorAction SilentlyContinue)) { throw 'Set -PythonExe to the bundled Python executable returned by load_workspace_dependencies.' }
[void][IO.Directory]::CreateDirectory($reviewDir)

function Pt([double]$mm) { return [single]($mm * 72 / 25.4) }
function Rgb([string]$hex) { return [int]([Convert]::ToInt32($hex.Substring(0,2),16) + 256*[Convert]::ToInt32($hex.Substring(2,2),16) + 65536*[Convert]::ToInt32($hex.Substring(4,2),16)) }

# Every run creates a new file in its own directory. Do not close, activate,
# or mutate any existing presentation, including the frozen publication source.
$processesBefore = @(Get-Process -Name POWERPNT -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id)
$ppt = New-Object -ComObject PowerPoint.Application
$presentation = $ppt.Presentations.Add(0)
$presentation.PageSetup.SlideWidth = Pt 170
$presentation.PageSetup.SlideHeight = Pt 80
$slide = $presentation.Slides.Add(1,12)
$slide.FollowMasterBackground = 0
$slide.Background.Fill.Solid()
$slide.Background.Fill.ForeColor.RGB = Rgb 'FFFFFF'
$native = @{}
$lineReport = @()

foreach ($obj in $spec.objects) {
  if ($obj.kind -eq 'line') {
    for ($s=0; $s -lt $obj.points.Count-1; $s++) {
      $p1=$obj.points[$s]; $p2=$obj.points[$s+1]
      $isLast=($s -eq $obj.points.Count-2)
      $segmentName = if ($obj.points.Count -eq 2) {$obj.name} else {"$($obj.name)__$($s+1)"}
      $item = $slide.Shapes.AddConnector(1,(Pt $p1[0]),(Pt $p1[1]),(Pt $p2[0]),(Pt $p2[1]))
      $item.Name=$segmentName
      $item.Line.ForeColor.RGB=Rgb $obj.color
      $item.Line.Weight=[single]$obj.width
      $item.Line.BeginArrowheadStyle=1
      $item.Line.EndArrowheadStyle= if ($obj.arrow -and $isLast) {3} else {1}
      $item.Line.EndArrowheadLength=1
      $item.Line.EndArrowheadWidth=1
      if ($s -eq 0 -and $obj.attachStart) { $item.ConnectorFormat.BeginConnect($native[$obj.attachStart.name],[int]$obj.attachStart.site) }
      if ($isLast -and $obj.attachEnd) { $item.ConnectorFormat.EndConnect($native[$obj.attachEnd.name],[int]$obj.attachEnd.site) }
      $native[$segmentName]=$item
      $lineReport += [ordered]@{name=$segmentName;begin_connected=([int]$item.ConnectorFormat.BeginConnected -eq -1);end_connected=([int]$item.ConnectorFormat.EndConnected -eq -1);begin_x_pt=[double]$item.Left;begin_y_pt=[double]$item.Top;width_pt=[double]$item.Width;height_pt=[double]$item.Height}
    }
    continue
  }
  $b=$obj.bounds
  if ($obj.kind -eq 'shape') {
    $item=$slide.Shapes.AddShape([int]$obj.type,(Pt $b[0]),(Pt $b[1]),(Pt $b[2]),(Pt $b[3]))
    $item.Fill.Solid(); $item.Fill.ForeColor.RGB=Rgb $obj.fill
    $item.Line.ForeColor.RGB=Rgb $obj.line
    $item.Line.Weight=[single]$obj.width
    if ($obj.width -eq 0) { $item.Line.Visible=0 }
  } else {
    $item=$slide.Shapes.AddTextbox(1,(Pt $b[0]),(Pt $b[1]),(Pt $b[2]),(Pt $b[3]))
    $item.Fill.Visible=0; $item.Line.Visible=0
    $tf=$item.TextFrame2
    $tf.AutoSize=0; $tf.WordWrap=-1
    $tf.MarginLeft=0; $tf.MarginRight=0; $tf.MarginTop=0; $tf.MarginBottom=0
    $tf.VerticalAnchor=3
    $tf.TextRange.Text=$obj.text
    $tf.TextRange.Font.Name='Arial'
    $tf.TextRange.Font.Size=[single]$obj.size
    $tf.TextRange.Font.Bold=if($obj.bold){-1}else{0}
    $tf.TextRange.Font.Italic=if($obj.italic){-1}else{0}
    $tf.TextRange.Font.Fill.ForeColor.RGB=Rgb $obj.color
    $tf.TextRange.ParagraphFormat.Alignment=if($obj.align -eq 'center'){2}elseif($obj.align -eq 'right'){3}else{1}
    $tf.TextRange.ParagraphFormat.SpaceBefore=0
    $tf.TextRange.ParagraphFormat.SpaceAfter=0
  }
  $item.Name=$obj.name
  $item.AlternativeText="Evidence-gated overview; $($obj.level); $($obj.name)"
  $native[$obj.name]=$item
}

# Source notes are scientific explanation, not a review verdict.
$slide.NotesPage.Shapes.Placeholders.Item(2).TextFrame.TextRange.Text = "Scientific source: $($spec.source_attribution). Detail a: chunk and embed to prepare the index; online lookup and reranking yield passages. Detail b: assemble the question and evidence prompt, generate, parse cited claims, then compare every cited claim against its source span. One attempt is one draft/check cycle; at most three total attempts. All weights frozen. Retrieved content is evidence, never an instruction or a weight update. Logging is omitted as an implementation detail. Companion: examples/evidence-gated-overview/detail.md. No experimental data or numerical performance claims."
$presentation.SaveAs($sourcePath,24)
$slide.Export($fullPng,'PNG',2040,960)

# Measure actual PowerPoint text bounds: this catches clipping at the fixed
# publication-size geometry; a finding calls for local recomposition.
$textMetrics=@()
foreach ($obj in $spec.objects | Where-Object kind -eq 'text') {
  $s=$native[$obj.name]; $tr=$s.TextFrame2.TextRange
  $textMetrics += [ordered]@{name=$obj.name;text=$tr.Text;font_pt=[double]$tr.Font.Size;box_width_pt=[double]$s.Width;box_height_pt=[double]$s.Height;rendered_width_pt=[double]$tr.BoundWidth;rendered_height_pt=[double]$tr.BoundHeight;exceeds_box=([double]$tr.BoundWidth -gt [double]$s.Width+0.5 -or [double]$tr.BoundHeight -gt [double]$s.Height+0.5)}
}

& $PythonExe (Join-Path $repoDir 'scripts\prepare-overview-review.py') $sourcePath (Join-Path $sampleDir 'review-plan.json') $reviewDir
if ($LASTEXITCODE -ne 0) { throw 'Review-copy helper failed; source and full export exist.' }
$variantExports=@()
foreach ($variant in @(@{copy='detail-hidden.pptx';image='view-01.png';kind='title-and-L3-hidden'},@{copy='title-hidden.pptx';image='view-02.png';kind='title-hidden'})) {
  $copyPath=Join-Path $reviewDir $variant.copy
  $imagePath=Join-Path $reviewDir $variant.image
  $copy=$ppt.Presentations.Open($copyPath,-1,0,0)
  $copy.Slides.Item(1).Export($imagePath,'PNG',2040,960)
  $variantExports += [ordered]@{source=$copyPath;image=$imagePath;kind=$variant.kind;renderer='Microsoft PowerPoint Slide.Export';slide=1;native_shape_count=$copy.Slides.Item(1).Shapes.Count;exported_utc=[DateTime]::UtcNow.ToString('o')}
  $copy.Close()
}
$nativeShapes=@()
for($i=1;$i -le $slide.Shapes.Count;$i++) {
  $s=$slide.Shapes.Item($i)
  $nativeShapes += [ordered]@{name=$s.Name;type=[int]$s.Type;is_connector=([int]$s.Connector -eq -1);left_pt=[double]$s.Left;top_pt=[double]$s.Top;width_pt=[double]$s.Width;height_pt=[double]$s.Height}
}
# The user requests the final editable source remain open. Create one document
# window, without invoking Activate, GotoSlide, or changing an existing view.
$ppt.Visible=-1
$sourceWindow=$presentation.NewWindow()
$evidence=[ordered]@{
  target_application='Microsoft PowerPoint';microsoft_powerpoint_used=$true;backend='late-bound Windows COM; native object generation';renderer='PowerPoint Slide.Export';application_version=$ppt.Version;application_build=$ppt.Build;source=$sourcePath;full_png=$fullPng;source_last_write_utc=(Get-Item -LiteralPath $sourcePath).LastWriteTimeUtc.ToString('o');exported_utc=[DateTime]::UtcNow.ToString('o');slide=1;slide_count=$presentation.Slides.Count;publication_width_mm=170;publication_height_mm=80;export_px=@(2040,960);process_ids_before=$processesBefore;process_ids_after=@(Get-Process -Name POWERPNT | Select-Object -ExpandProperty Id);unrelated_presentations_modified=$false;used_active_window_or_view_api=$false;capability_probe_limitation='MCP static metadata could not load Office interop assemblies. Actual COM construction and Slide.Export results are recorded here.';native_shape_count=$slide.Shapes.Count;picture_count=@($nativeShapes | Where-Object {$_.type -in @(11,13)}).Count;text_box_count=$textMetrics.Count;connector_count=$lineReport.Count;autoshape_count=@($nativeShapes | Where-Object {$_.type -eq 1 -and -not $_.is_connector}).Count;text_bounds_findings=@($textMetrics | Where-Object exceeds_box);variants=$variantExports;review_copy_manifest=(Join-Path $reviewDir 'review-manifest.json');independent_review='pending; separate fresh reviewer to be assigned by main agent';self_score=$null;source_left_open=$true
}
$evidence | ConvertTo-Json -Depth 15 | Set-Content -LiteralPath (Join-Path $reviewDir 'renderer-evidence.json') -Encoding UTF8
([ordered]@{text=$textMetrics;connectors=$lineReport;native_objects=$nativeShapes}) | ConvertTo-Json -Depth 15 | Set-Content -LiteralPath (Join-Path $reviewDir 'structure.json') -Encoding UTF8
([ordered]@{source=$presentation.FullName;source_open=$true;source_editable=([int]$presentation.ReadOnly -ne -1);document_windows=$presentation.Windows.Count;application_version=$ppt.Version;native_shape_count=$slide.Shapes.Count;observed_utc=[DateTime]::UtcNow.ToString('o');unrelated_decks_modified=$false}) | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $reviewDir 'session-handoff.json') -Encoding UTF8
$evidence | ConvertTo-Json -Depth 5
