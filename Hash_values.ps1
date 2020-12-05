param(
    [Parameter(Mandatory)] [string] $path
)
$HashFile = 'Hash('+(Get-Date -Format "yyyy-MM-dd")+' '+(Get-Date -Format "HH-mm-ss")+').txt'
if (Test-Path -Path $path){
    if ((Get-Item $path) -is [System.IO.DirectoryInfo]){
        Get-ChildItem $path | Get-FileHash | Select-Object -Property Hash, Path | Format-Table -HideTableHeaders | Out-File $HashFile -Encoding ascii -ErrorAction SilentlyContinue
        Write-Host "Hash file was created successfully"
    }else{
        Get-FileHash -Algorithm SHA256 -Path $path | Out-File $HashFile -Encoding ascii
        Write-Host "Hash file was created successfully"
    }
}else{
    Write-Host "The path not exist"
}
