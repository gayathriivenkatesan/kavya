############################################################
#
# REMOVE DNS Server FROM DNS
# 
############################################################

Param([string]$filepath,[string]$destinationfile,[string]$username,[string]$sfcase,[string]$password)

#$filepath="\\vincromi0019\C$\Decommissioning\decomm_portal\server_cleanup_common_input.csv"
#$destinationfile="test.html"
#$sfcase="1234"
#$Username = "jdadelivers\1028742"
#$Password = "SMPrs!@140495"
$date = (Get-Date).ToString("MM/d/yyyy")
#$filepath
$time = (Get-Date).AddMinutes(1).ToString("HH:mm")
$datetime = (Get-Date).ToString("MMd_HHmm")
#$user_sch="jdadelivers\1028742"
#$pswd_sch="SMPrs!@140495"
$res = schtasks.exe /create  /sc once /SD $date /ST $time /TN "Test schedule $datetime" /F /tr "powershell.exe -command & {'C:\xampp\htdocs\server_decomm\DNS\base.ps1' '$filepath,$destinationfile,$sfcase,$username,$password'}" /RU $username /RP $password #/RL HIGHEST

return $res


#powershell.exe -command & {"C:\xampp\htdocs\server_decomm\DNS\base1.ps1" "\\vincromi0019\C$\Decommissioning\decomm_portal\server_cleanup_common_input.csv,test.html,1234,jdadelivers\1028742,SMPrs!@140495"}