[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$search_query = "all:matroid+AND+all:secretary"
$max_results = 20
$url = "http://export.arxiv.org/api/query?search_query=$search_query&start=0&max_results=$max_results&sortBy=relevance&sortOrder=descending"

Write-Host "Querying arXiv API..."
$xmlString = (Invoke-WebRequest -Uri $url).Content
$xml = [xml]$xmlString

$ns = @{ default = "http://www.w3.org/2005/Atom" }

$papersDir = "papers"
if (!(Test-Path -Path $papersDir)) {
    New-Item -ItemType Directory -Path $papersDir | Out-Null
}

$metadata = @()
$i = 1

$entries = Select-Xml -Xml $xml -XPath "//default:entry" -Namespace $ns
foreach ($entryNode in $entries) {
    $entry = $entryNode.Node
    
    $title = ""
    if ($entry.title) {
        $title = $entry.title.Replace("`n", " ").Replace("`r", "").Trim()
    }
    
    $summary = ""
    if ($entry.summary) {
        $summary = $entry.summary.Replace("`n", " ").Replace("`r", "").Trim()
    }
    
    $authors = @()
    if ($entry.author) {
        foreach ($a in $entry.author) {
            $authors += $a.name
        }
    }
    $authorsStr = $authors -join ", "
    
    $pdfUrl = ""
    if ($entry.link) {
        foreach ($link in $entry.link) {
            if ($link.title -eq "pdf") {
                $pdfUrl = $link.href
                break
            }
        }
    }
    
    if (-not [string]::IsNullOrEmpty($pdfUrl) -and -not $pdfUrl.EndsWith(".pdf")) {
        $pdfUrl += ".pdf"
    }
    
    $paperId = ""
    if ($entry.id) {
        $idParts = $entry.id -split "/"
        $paperId = $idParts[$idParts.Length - 1]
    }
    
    $filename = "$paperId.pdf"
    $filepath = Join-Path -Path $papersDir -ChildPath $filename
    
    Write-Host "[$i/$max_results] Downloading $title ..."
    if (!(Test-Path -Path $filepath)) {
        try {
            Invoke-WebRequest -Uri $pdfUrl -OutFile $filepath
            Start-Sleep -Seconds 1
        } catch {
            Write-Host "Error downloading $pdfUrl"
        }
    } else {
        Write-Host "File $filename already exists, skipping."
    }
    
    $paperData = @{
        title = $title
        authors = $authorsStr
        summary = $summary
        published = $entry.published
        pdf_url = $pdfUrl
        local_pdf = "papers/$filename"
    }
    
    $metadata += $paperData
    $i++
}

$metadata | ConvertTo-Json -Depth 3 | Out-File "papers_metadata.json" -Encoding utf8
Write-Host "Successfully downloaded $($entries.Count) papers and saved metadata."
