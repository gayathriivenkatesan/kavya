Param([string]$filepath,[string]$destinationfile,[string]$username,[string]$password,[string]$sfcase,[string]$res)

function Run-MySQLQuery{
Param(
        [Parameter(
            Mandatory = $true,
            ParameterSetName = '',
            ValueFromPipeline = $true)]
            [string]$query         
        )
        Begin {
        Write-Verbose "Starting Begin Section"		
        }
        Process {
        Write-Verbose "Starting Process Section"
        try {
        # load MySQL driver and create connection
        Write-Verbose "Create Database Connection"
        $sqlConn = New-Object System.Data.SqlClient.SqlConnection
        
        $sqlConn.ConnectionString = "Server=tcp:DLNOTIFYPRDDB1V.JDADELIVERS.COM,1433;Initial Catalog=notify_db;Persist Security Info=False;User ID=hu_notify_db;;Password=Bv6cM7PHrsvdAnyu;;MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=True;Connection Timeout=30;"
        $sqlConn.Open()
        $sqlcmd = $sqlConn.CreateCommand()            
        $sqlcmd = New-Object System.Data.SqlClient.SqlCommand			
        #Write-Verbose "Open Database Connection"
        $sqlcmd.Connection = $sqlConn 					
        # Run MySQL Querys
        Write-Verbose "Run MySQL Querys"
        $sqlcmd.CommandText = $query 
        $adp = New-Object System.Data.SqlClient.SqlDataAdapter $sqlcmd
        $data = New-Object System.Data.DataSet
        $adp.Fill($data) | Out-Null
        return $data.Tables[0]	
        }	
	
        catch {
        Write-Host "Could not run MySQL Query" $Error[0]	
        }	
        Finally {
        Write-Verbose "Close Connection"
        $sqlConn.Close()
        }
        }
        End {
        Write-Verbose "Starting End Section"
        }

}

$sql= Run-MySQLQuery -query 'select * from server_inventory'

$servers1 = $sql.customer_server

$filepath = import-csv -path "C:\xampp\htdocs\server_decomm\bigfix_server_decomm\server_cleanup_common_input.csv"
$decomm_servers=$filepath.bigfixserver | ?{$_ -ne ""}

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

$limit=$decomm_servers.count
$count=0

$file = import-csv -path "C:\Abhishek\bigfixservers.csv"
$servers = Invoke-RestMethod -Method Get -Credential $cred -Headers $headers -Uri "https://dlbigfixapp1v.jdadelivers.com:52311/api/computers"
    $out_result = @()
    $cname = '' 
        
        foreach ($item in $file)
        {
              
              $cname=$item.split(".")[0].ToLower()
              $cname
              
              if($decomm_servers | ?{$_ -eq $cname}){
                  write-verbose -Verbose "$($cname) - Found" 
                  $count=$count+1
                  $c_id = $servers.BESAPI.Computer.id
                  $com1=Invoke-restmethod -Method Get -Credential $cred -Headers $headers -Uri "https://dlbigfixapp1v.jdadelivers.com:52311/api/computer/$c_id"
                  $com1 
                  if($count -eq $limit){
                  break
                  }
                 
              }
          #$out_result += $cname
 }

$out_result | Out-File "C:\Abhishek\log\server.csv"
           

<#

function Email($path)
{
    $SMTPMessage = New-Object System.Net.Mail.MailMessage
    $SMTPServer = "mailout.jdadelivers.com"
    $SMTPMessage.from="madugula.shivani@blueyonder.com"  #
    $to = "madugula.shivani@blueyonder.com"   #CS-India-Bladelogic@blueyonder.com
    $cc = @("madugula.shivani@blueyonder.com","nikhileswarreddy.jonnavaram@blueyonder.com")
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
    $SMTPMessage.Attachments.Add($path)
    $SMTPClient.Send($SMTPMessage)

}

Email -path "C:\Abhishek\log\server.csv"

#>
