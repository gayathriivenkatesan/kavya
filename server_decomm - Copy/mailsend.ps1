Param([string]$username)

$b=@()

######MSSQL TEAM 
try{
$HtmlTable1 = "<table border='1' align='Left' cellpadding='2' cellspacing='0' style='color:black;font-family:arial,helvetica,sans-serif;text-align:left;'>
<tr style ='font-size:13px;font-weight: normal;background-color:#FFFF00;'>
<th align=left><b>Username</b></th>
</tr>"

$HtmlTable1 += "<tr style='font-size:13px;background-color:#FFFFFF'>
<td>" + $username + "</td>
</tr>"

#$HtmlTable1 +="<tr><p>Regards<br />Server-decomm-portal Team</p></tr>"
$HtmlTable1 += "</table>"
$final="<br><br><br><br><p>Regards<br>Server-decom-portal Team<br></p>"
$HtmlTable1 +=$final
#$HtmlTable="<tr><p><br />Regards<br />Server-decomm-portal Team</p></tr>"
#$HtmlTable1 +="<br /><br /><br /><tr><p><br />Regards<br />Server-decomm-portal Team</p></tr>"
# Send the email
#$smtpserver = "dlprsmtp.jdadelivers.com" 
$smtpserver ="mailout.jdadelivers.com"
$from = "BuildScripts@jdadelivers.com"
$to = "CSBuildteam@blueyonder.com"
#$to="gayathri.venkatesan@blueyonder.com"
$subject = "Service Account Credential Changed in DecommPortal"
$body = "Hi Team,<br/>Service Account Credential is changed by the below user in the Server Decommission Portal.<br /><br />"+ $htmlTable1 
Send-MailMessage -smtpserver $smtpserver -from $from -to $to -subject $subject -body $body -bodyashtml -Priority High
	$b ="Success mail send to TEAM"
}
catch{
	$b ="Failed to send mail to TEAM"
}
write-host $b