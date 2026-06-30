Param([string]$filepath,[string]$destinationfile,[string]$sfcase)

$path = "C:\xampp\htdocs\server_decomm\bigfix_server_decomm"
$logdate = (get-date).ToString("dd-MMM-yyyy")
$date1= Get-Date -Format "dd-MM-yyyy hh:mm"

if(!(Test-Path -Path "C:\xampp\htdocs\server_decomm\decomm_logs\$sfcase")){
    New-Item "C:\xampp\htdocs\server_decomm\decomm_logs\$sfcase" -ItemType Directory
}

Start-Transcript -Path "$path\log\plan_log_$($logdate).txt"

$filepath1 = import-csv -path "C:\xampp\htdocs\server_decomm\bigfix_server_decomm\server_cleanup_common_input.csv"
$decomm_servers=$filepath1.bigfixserver | ?{$_ -ne ""}
$decomm_servers
$decomm_servers=$decomm_servers | foreach {$_.Split('.')[0].tolower()}
add-type @"
    using System.Net;
    using System.Security.Cryptography.X509Certificates;
    public class TrustAllCertsPolicy : ICertificatePolicy {
        public bool CheckValidationResult(
            ServicePoint srvPoint, X509Certificate certificate,
            WebRequest request, int certificateProblem) {
            return true;
        }
    }
"@
[System.Net.ServicePointManager]::CertificatePolicy = New-Object TrustAllCertsPolicy
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$username = "src_notpor"
$password = "User@098!" | ConvertTo-SecureString -AsPlainText -Force
$cred = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList $username,$password

$headers = @{
    Accept = "application/xml"

}

$file = import-csv -path "C:\Abhishek\bigfixservers.csv"
$out_result = @()
foreach($item in $decomm_servers){
     
      $data = $file | ?{$_.ComputerName -eq $item}
      if($data)
      {
          $url = "https://dlbigfixapp1v.jdadelivers.com:52311/api/computer/$($data.id)"
          $status = Invoke-RestMethod -Method Get -Credential $cred -Headers $headers -Uri $url
          if($status -eq "ok"){
          Write-Host "$item -Server Deleted" -BackgroundColor Green
          $custom_obj = [pscustomobject][ordered]@{
                  id = $data.id
                  ComputerName = $data.ComputerName
                  status = 'Decommissioned'
                  }
            $out_result += $custom_obj
          }
          else
          {
          Write-Host "$item -Server not found" -BackgroundColor Red
              $custom_obj1 = [pscustomobject][ordered]@{
              id = $data.id
              ComputerName = $data.ComputerName
              status = 'Server not found'
              }
            $out_result += $custom_obj1
          }
    }
      else
      {
      Write-Host "$item -Server unable to Delete" -BackgroundColor Red
      $custom_obj2 = [pscustomobject][ordered]@{
              id = 'NULL'
              ComputerName = $item
              status = 'server not found - Unable to Decommission'
              }
        $out_result += $custom_obj2
      }
}
$path1 = "C:\xampp\htdocs\server_decomm\bigfix_server_decomm\log\$($logdate).csv" 

$output = $out_result | Export-Csv -Path $path1 -NoTypeInformation


function Email($path1)
{
    $SMTPMessage = New-Object System.Net.Mail.MailMessage
    $SMTPServer = "mailout.jdadelivers.com"
    $SMTPMessage.from="madugula.shivani@blueyonder.com"  
    $to = "madugula.shivani@blueyonder.com"#,"CS-India-Bladelogic@blueyonder.com","abhishek.kona@blueyonder.com")
    $cc = @("madugula.shivani@blueyonder.com")#,"sukanyadevi.velaga@blueyonder.com","rama.bk@blueyonder.com"
      if($to)
        {
        $to=($to -replace ",",";") -split ";"
            foreach($t in $to)
            {
            if($t)
            {
                $SMTPMessage.To.Add($t)
            }
            }
        }
        
        if($cc)
        {
        $cc=($cc -replace ",",";") -split ";"
            foreach($c in $cc)
            {
            if($c)
            {
                $SMTPMessage.CC.Add($c)
            }
            }
        }
    $SMTPMessage.subject = "Decommissioned Servers - BigFix"
    $SMTPMessage.IsBodyHTML = $true
    $SMTPClient = New-Object Net.Mail.SmtpClient($SmtpServer, 25)
    $SMTPClient.UseDefaultCredentials = $False
    $messageBody = @"
    
<html>
<head>
<title>Page Title</title>
<style>
body {
  background-color: white;
  color: black;
  font-family: Arial, Helvetica, sans-serif;
}
h4 {
background-color: DodgerBlue;
text-align: center;
color: white;
}
p {
font-size : 14px
}
li {
font-size : 13px
}
div.regards{
font-size : 15px;
}
div.footer{
     line-height: 100%;
    font-size: 14px;
}
.space{
position: relative;
    left: 100px;
}
div.queue{
position: relative;
    bottom: 31px;
}
</style>
</head>
<body>
<img src="BlueYounder_mailheader.png" alt="logo_main">
<h4>BigFix Decommissioned Servers Report</h4>
<p>Hi Team,</p>
<p>Kindly find the attachment of BigFix Decommissioned Servers.</p>
<div class = "regards">
<b>Server Support Team</b><br>
<b>1-214-294-1126</b><br><br>
</div>
<img src="mailfooter.jpg" alt="logo" >
</body>
</html>


"@
    $SMTPMessage.Body = $messageBody #body
    $SMTPMessage.Attachments.Add($path1)
    $SMTPClient.Send($SMTPMessage)

}

Email -path $path1


$output1=@()
$count=$out_result.count
foreach($i1 in $out_result){
$d=New-Object -TypeName psobject 
 Add-Member -InputObject $d  -MemberType NoteProperty -Name 'sfcase' -Value $sfcase;  
 Add-Member -InputObject $d  -MemberType NoteProperty -Name 'Computer Name' -Value $i1.'ComputerName';
 Add-Member -InputObject $d  -MemberType NoteProperty -Name 'ID' -Value $i1.id;
 Add-Member -InputObject $d  -MemberType NoteProperty -Name 'Status' -Value $i1.'status';
 $d
  
 $output1+= $d
}
$g1="<html>
    <head>
    <style>
    table, th, td {
     border: 1px solid black;
    }
</style>
</head>
     <body>
     <center>
     <h1 ><b>BigFix Server Decommission</b></h1>
     <h4 ><b>Execution time: <span >$date1</span></b></h3>
     <h4 ><b>Executed by: <span >$username</span></b></h3>
     <table>
     <thead>
     <tr>
	 <th>SF Case</th>
     <th>Computer Name</th>
     <th>ID</th>
     <th>Status</th>
     </tr>
     </thead>
     <tbody>"
     $g1+= $output1|%{ 
     "<tr>
	 <td>$($_.sfcase)</td>
     <td>$($_.'Computer Name')</td>
     <td>$($_.id)</td>"
     if($_.Status -eq 'Server not found - Unable to Decommission'){
     "<td style='color:red;'>$($_.Status)</td>"
     }
     elseif($_.Status -eq 'Decommissioned'){
     "<td style='color:green;'>$($_.Status)</td>" 
     }
     elseif($_.Status -eq 'Server not found'){
     "<td style='color:red;'>$($_.Status)</td>" 
     }
     "</tr>"
     }
     $g1+="</tbody>
     </table>
     </center>
     </body>
     </html>"
$g1|out-file -FilePath "C:\xampp\htdocs\server_decomm\decomm_logs\$sfcase\$destinationfile"
Stop-Transcript