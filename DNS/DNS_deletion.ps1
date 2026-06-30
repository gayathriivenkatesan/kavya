############################################################
#
# REMOVE DNS Server FROM DNS
# 
############################################################

Param([string]$filepath,[string]$destinationfile,[string]$username,[string]$sfcase,[string]$password)
#write-host $sfcase
$date = (Get-Date).ToString("MM/dd/yyyy")
$time = (Get-Date).AddMinutes(1).ToString("HH:mm")
$datetime = (Get-Date).ToString("MMd_HHmm")
#write-host $datetime
#$user_sch="jdadelivers\1028742"
$count=$sfcase.length
$count
#write-host "schtasks.exe /create  /sc once /SD $date /ST $time /TN 'Test schedule $datetime' /F /tr command & {'C:\xampp\htdocs\server_decomm\DNS\base.ps1' '$filepath,$destinationfile,$sfcase,$username'}"
$res = schtasks.exe /create  /sc once /SD $date /ST $time /TN "Test schedule $datetime" /F /tr "powershell.exe -command & {'C:\xampp\htdocs\server_decomm\DNS\base2.ps1' '$filepath,$destinationfile,$sfcase,$username,$count'}" /RU $username /RP $password #/RL HIGHEST
write-host $res
#return $res


###note
#Decom_task,$res