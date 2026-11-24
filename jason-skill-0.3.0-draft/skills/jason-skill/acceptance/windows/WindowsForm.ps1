param([Parameter(Mandatory=$true)][string]$ResultFile)

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$target = [System.IO.Path]::GetFullPath($ResultFile)
if (Test-Path -LiteralPath $target) { throw 'Choose a fresh result file for this test.' }
$form = New-Object System.Windows.Forms.Form
$form.Text = 'Jason Skill Parity Test'
$form.ClientSize = New-Object System.Drawing.Size(470, 235)

$label = New-Object System.Windows.Forms.Label
$label.Text = 'Test text'
$label.Location = New-Object System.Drawing.Point(20, 20)
$inputBox = New-Object System.Windows.Forms.TextBox
$inputBox.AccessibleName = 'Test text'
$inputBox.Location = New-Object System.Drawing.Point(20, 42)
$inputBox.Width = 380
$check = New-Object System.Windows.Forms.CheckBox
$check.Text = 'Enable test'
$check.Location = New-Object System.Drawing.Point(20, 78)
$increment = New-Object System.Windows.Forms.Button
$increment.Text = 'Add one'
$increment.Location = New-Object System.Drawing.Point(20, 113)
$countLabel = New-Object System.Windows.Forms.Label
$countLabel.Text = 'Count: 0'
$countLabel.Location = New-Object System.Drawing.Point(120, 117)
$save = New-Object System.Windows.Forms.Button
$save.Text = 'Save test'
$save.Location = New-Object System.Drawing.Point(20, 153)
$status = New-Object System.Windows.Forms.Label
$status.Text = 'Not saved'
$status.Location = New-Object System.Drawing.Point(20, 192)
$status.AutoSize = $true
$state = @{ Count = 0 }
$increment.add_Click({
    $state.Count++
    $countLabel.Text = "Count: $($state.Count)"
})
$save.add_Click({
    $result = @{ name = $inputBox.Text; enabled = $check.Checked; count = $state.Count }
    $json = ConvertTo-Json -Compress -InputObject $result
    try {
        $stream = [System.IO.File]::Open($target, [System.IO.FileMode]::CreateNew)
        try {
            $bytes = [System.Text.Encoding]::UTF8.GetBytes($json)
            $stream.Write($bytes, 0, $bytes.Length)
        } finally { $stream.Dispose() }
        $status.Text = "Saved: $($inputBox.Text) / $($check.Checked)"
        $save.Enabled = $false
    } catch {
        $status.Text = 'Save failed. Choose a new writable result destination.'
    }
})
$form.Controls.AddRange(@($label,$inputBox,$check,$increment,$countLabel,$save,$status))
[void]$form.ShowDialog()
