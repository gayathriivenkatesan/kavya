#$filepath="\\vincromi0019\C$\Decommissioning\decomm_portal\server_cleanup_common_input.csv"
#$destinationfile="test.html"
#$sfcase="123"
#$Username = "jdadelivers\1028742"
#$Password = "SMPrs!@140495"
Param([string]$filepath,[string]$destinationfile,[string]$username,[string]$sfcase,[string]$password)

#$filepath=$args[0]
#$destinationfile=$args[1]
#$sfcase=$args[2]
#$username=$args[3]
#$password=$args[4]
Write-Host "1 - $filepath"
Write-Host $destinationfile
Write-Output $username
$path="\\vincromi0019\C$\xampp\htdocs\server_decomm\decomm_logs\$sfcase"
$date=Get-Date -Format "dd_MM_yyy_HH_mm_ss"
