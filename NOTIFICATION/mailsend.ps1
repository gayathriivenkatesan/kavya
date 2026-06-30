Param([string]$sfcase)

$b=@()

######MSSQL TEAM 
try{
$HtmlTable1 = "<table border='1' align='Left' cellpadding='2' cellspacing='0' style='color:black;font-family:arial,helvetica,sans-serif;text-align:left;'>
<tr style ='font-size:13px;font-weight: normal;background-color:#FFFF00;'>
<th align=left><b>Requestor</b></th>
<th align=left><b>SF</b></th>
<th align=left><b>CRQ</b></th>
<th align=left><b>Customer</b></th>
<th align=left><b>PM</b></th>
<th align=left><b>POD Lead</b></th>
<th align=left><b>ENV</b></th>
<th align=left><b>Servers</b></th>
</tr>"

$a=import-csv -Path C:\xampp\htdocs\server_decomm\NOTIFICATION\mail.csv|where{($_.Track -eq "MSSQL")}
if($a){
	foreach($row in $a){
		$HtmlTable1 += "<tr style='font-size:13px;background-color:#FFFFFF'>
		<td>" + $row.Requestor + "</td>
		<td>" + $row.SF + "</td>
		<td>" + $row.CRQ + "</td>
		<td>" + $row.Customer + "</td>
		<td>" + $row.PM+ "</td>
		<td>" + $row.POD + "</td>
		<td>" + $row.ENV + "</td>
		<td>" + $row.Servers + "</td>
		</tr>"
	}
	$HtmlTable1 +="<tr><p>Regards<br />Server-decomm-portal Team</p></tr>"
	$HtmlTable1 += "</table>"
	#$HtmlTable="<tr><p><br />Regards<br />Server-decomm-portal Team</p></tr>"
	#$HtmlTable1 +="<br /><br /><br /><tr><p><br />Regards<br />Server-decomm-portal Team</p></tr>"
	# Send the email
	#$smtpserver = "dlprsmtp.jdadelivers.com" 
	$smtpserver ="mailout.jdadelivers.com"
	$from = "BuildScripts@jdadelivers.com"
	$to = "CSBuildteam@blueyonder.com"
	#$to="gayathri.venkatesan@blueyonder.com"
	$subject = "Decom - MSSQL"
	$body = "Hi Team,<br/>Please proceed with the MSSQL DB Decomm process for the below list of servers.<br /><br />"+ $htmlTable1 
	Send-MailMessage -smtpserver $smtpserver -from $from -to $to -subject $subject -body $body -bodyashtml -Priority High
		$b +="Success mail send to SQL TEAM"
	}
	}
	catch{
		$b +="Failed to send mail to SQL TEAM"
	}
###ORACLE TEAM
try{
$HtmlTable2 = "<table border='1' align='Left' cellpadding='2' cellspacing='0' style='color:black;font-family:arial,helvetica,sans-serif;text-align:left;'>
<tr style ='font-size:13px;font-weight: normal;background-color:#FFFF00;'>
<th align=left><b>Requestor</b></th>
<th align=left><b>SF</b></th>
<th align=left><b>CRQ</b></th>
<th align=left><b>Customer</b></th>
<th align=left><b>PM</b></th>
<th align=left><b>POD Lead</b></th>
<th align=left><b>ENV</b></th>
<th align=left><b>Servers</b></th>
</tr>"

$a1=import-csv -Path C:\xampp\htdocs\server_decomm\NOTIFICATION\mail.csv|where{($_.Track -like "oracle")}
if($a1){
foreach($row in $a1){
    $HtmlTable2 += "<tr style='font-size:13px;background-color:#FFFFFF'>
    <td>" + $row.Requestor + "</td>
    <td>" + $row.SF + "</td>
    <td>" + $row.CRQ + "</td>
    <td>" + $row.Customer + "</td>
    <td>" + $row.PM+ "</td>
    <td>" + $row.POD + "</td>
    <td>" + $row.ENV + "</td>
    <td>" + $row.Servers + "</td>
    </tr>"
}
$HtmlTable2 +="<tr><p>Regards<br />Server-decomm-portal Team</p></tr>"
$HtmlTable2 += "</table>"
#$HtmlTable="<tr><p><br />Regards<br />Server-decomm-portal Team</p></tr>"
#$HtmlTable1 +="<br /><br /><br /><tr><p><br />Regards<br />Server-decomm-portal Team</p></tr>"
# Send the email
#$smtpserver = "dlprsmtp.jdadelivers.com" 
$smtpserver ="mailout.jdadelivers.com"
$from = "BuildScripts@jdadelivers.com"
$to = "CSBuildteam@blueyonder.com"
#$to="gayathri.venkatesan@blueyonder.com"
$subject = "Decom - Oracle"
$body = "Hi Team,<br/>Please proceed with the ORACLE DB Decomm process for the below list of servers.<br /><br/>"+ $htmlTable2 
Send-MailMessage -smtpserver $smtpserver -from $from -to $to -subject $subject -body $body -bodyashtml -Priority High
	$b +="Success mail send to Oracle  TEAM"
}
}
catch{
	$b +="Failed to send mail to Oracle TEAM"
}


####CITRIX TEAM
try{
$HtmlTable3 = "<table border='1' align='Left' cellpadding='2' cellspacing='0' style='color:black;font-family:arial,helvetica,sans-serif;text-align:left;'>
<tr style ='font-size:13px;font-weight: normal;background-color:#FFFF00;'>
<th align=left><b>Requestor</b></th>
<th align=left><b>SF</b></th>
<th align=left><b>CRQ</b></th>
<th align=left><b>Customer</b></th>
<th align=left><b>PM</b></th>
<th align=left><b>POD Lead</b></th>
<th align=left><b>ENV</b></th>
<th align=left><b>Servers</b></th>
</tr>"
$a2=import-csv -Path C:\xampp\htdocs\server_decomm\NOTIFICATION\mail.csv|where{($_.Track -like "citrix")}
if($a2){
foreach($row in $a2){
    $HtmlTable3 += "<tr style='font-size:13px;background-color:#FFFFFF'>
    <td>" + $row.Requestor + "</td>
    <td>" + $row.SF + "</td>
    <td>" + $row.CRQ + "</td>
    <td>" + $row.Customer + "</td>
    <td>" + $row.PM+ "</td>
    <td>" + $row.POD + "</td>
    <td>" + $row.ENV + "</td>
    <td>" + $row.Servers + "</td>
    </tr>"
}
$HtmlTable3 +="<tr><p>Regards<br />Server-decomm-portal Team</p></tr>"
$HtmlTable3 += "</table>"
#$HtmlTable="<tr><p><br />Regards<br />Server-decomm-portal Team</p></tr>"
#$HtmlTable1 +="<br /><br /><br /><tr><p><br />Regards<br />Server-decomm-portal Team</p></tr>"
# Send the email
#$smtpserver = "dlprsmtp.jdadelivers.com" 
$smtpserver ="mailout.jdadelivers.com"
$from = "BuildScripts@jdadelivers.com"
$to = "CSBuildteam@blueyonder.com"
#$to="gayathri.venkatesan@blueyonder.com"
$subject = "Decom - CITRIX"
$body = "Hi Team,<br/>Please proceed with the Citrix Decomm process for the below list of servers.<br /><br />"+ $htmlTable3 
Send-MailMessage -smtpserver $smtpserver -from $from -to $to -subject $subject -body $body -bodyashtml -Priority High
	$b +="Success mail send to CITRIX TEAM"
}
}
catch{
	$b +="Failed to send mail to CITRIX TEAM"
}

########SFT TEAM
try{
$HtmlTable4 = "<table border='1' align='Left' cellpadding='2' cellspacing='0' style='color:black;font-family:arial,helvetica,sans-serif;text-align:left;'>
<tr style ='font-size:13px;font-weight: normal;background-color:#FFFF00;'>
<th align=left><b>Requestor</b></th>
<th align=left><b>SF</b></th>
<th align=left><b>CRQ</b></th>
<th align=left><b>Customer</b></th>
<th align=left><b>PM</b></th>
<th align=left><b>POD Lead</b></th>
<th align=left><b>ENV</b></th>
<th align=left><b>Servers</b></th>
</tr>"

$a3=import-csv -Path C:\xampp\htdocs\server_decomm\NOTIFICATION\mail.csv|where{($_.Track -eq "mft")}
if($a3){
foreach($row in $a3){
    $HtmlTable1 += "<tr style='font-size:13px;background-color:#FFFFFF'>
    <td>" + $row.Requestor + "</td>
    <td>" + $row.SF + "</td>
    <td>" + $row.CRQ + "</td>
    <td>" + $row.Customer + "</td>
    <td>" + $row.PM+ "</td>
    <td>" + $row.POD + "</td>
    <td>" + $row.ENV + "</td>
    <td>" + $row.Servers + "</td>
    </tr>"
}
$HtmlTable4 +="<tr><p>Regards<br />Server-decomm-portal Team</p></tr>"
$HtmlTable4 += "</table>"
#$HtmlTable="<tr><p><br />Regards<br />Server-decomm-portal Team</p></tr>"
#$HtmlTable1 +="<br /><br /><br /><tr><p><br />Regards<br />Server-decomm-portal Team</p></tr>"
# Send the email
#$smtpserver = "dlprsmtp.jdadelivers.com" 
$smtpserver ="mailout.jdadelivers.com"
$from = "BuildScripts@jdadelivers.com"
$to = "CSBuildteam@blueyonder.com"
#$to="gayathri.venkatesan@blueyonder.com"
$subject = "Decom - MFT"
$body = "Hi Team,<br/>Please proceed with the  Decomm process for the below list of servers.<br /><br />"+ $htmlTable4 
Send-MailMessage -smtpserver $smtpserver -from $from -to $to -subject $subject -body $body -bodyashtml -Priority High
	$b +="Success mail send to MFT TEAM"
}
}
catch{
	$b +="Failed to send mail to MFT TEAM"
}
$b|out-file -filepath "C:\\xampp\htdocs\server_decomm\decomm_logs\$sfcase\notify.csv"