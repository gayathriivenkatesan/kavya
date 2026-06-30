#Param([string]$region,[string]$hostname)
#Param([string]$region,[string]$hostname)

function Email($path1)
{
    $SMTPMessage = New-Object System.Net.Mail.MailMessage
    $SMTPServer = "mailout.jdadelivers.com"
    $SMTPMessage.from="nikhileswarreddy.jonnavaram@blueyonder.com"  
    $to = "nitin.manoji@blueyonder.com"#,"CS-India-Bladelogic@blueyonder.com","abhishek.kona@blueyonder.com")
    $cc = @("nikhileswarreddy.jonnavaram@blueyonder.com")#,"sukanyadevi.velaga@blueyonder.com","rama.bk@blueyonder.com"
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
    $SMTPMessage.subject = "IP reservation servers file"
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
<h4>IP reservation report</h4>
<p>Hi Team,</p>
<p>Kindly find the attachment of reservation IPs.</p>
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




########################################################3
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$form = New-Object System.Windows.Forms.Form
$form.Text = 'Data Entry Form'
$form.Size = New-Object System.Drawing.Size(300,350)
$form.StartPosition = 'CenterScreen'

$OKButton = New-Object System.Windows.Forms.Button
$OKButton.Location = New-Object System.Drawing.Point(75,190)
$OKButton.Size = New-Object System.Drawing.Size(75,23)
$OKButton.Text = 'OK'
$OKButton.DialogResult = [System.Windows.Forms.DialogResult]::OK
$form.AcceptButton = $OKButton
$form.Controls.Add($OKButton)

$CancelButton = New-Object System.Windows.Forms.Button
$CancelButton.Location = New-Object System.Drawing.Point(150,190)
$CancelButton.Size = New-Object System.Drawing.Size(75,23)
$CancelButton.Text = 'Cancel'
$CancelButton.DialogResult = [System.Windows.Forms.DialogResult]::Cancel
$form.CancelButton = $CancelButton
$form.Controls.Add($CancelButton)

##############33
$label = New-Object System.Windows.Forms.Label
$label.Location = New-Object System.Drawing.Point(10,20)
$label.Size = New-Object System.Drawing.Size(280,30)
$label.Text = 'Enter hostname-(For multiple provide comma seperated values)'
$form.Controls.Add($label)

$textBox = New-Object System.Windows.Forms.TextBox
$textBox.Location = New-Object System.Drawing.Point(10,50)
$textBox.Size = New-Object System.Drawing.Size(260,20)
$form.Controls.Add($textBox)
#########################


$label1 = New-Object System.Windows.Forms.Label
$label1.Location = New-Object System.Drawing.Point(10,80)
$label1.Size = New-Object System.Drawing.Size(280,20)
$label1.Text = 'Please select one subnet regions:'
$form.Controls.Add($label1)

$listBox = New-Object System.Windows.Forms.Listbox
$listBox.Location = New-Object System.Drawing.Point(10,100)
$listBox.Size = New-Object System.Drawing.Size(260,20)

$listBox.SelectionMode = 'MultiExtended'

[void] $listBox.Items.Add('Dallas')
[void] $listBox.Items.Add('Frankfurt')
[void] $listBox.Items.Add('Slough')
[void] $listBox.Items.Add('Kansas')
[void] $listBox.Items.Add('Atlanta')

$listBox.Height = 70
$form.Controls.Add($listBox)
$form.Topmost = $true

$result = $form.ShowDialog()





if ($result -eq [System.Windows.Forms.DialogResult]::OK)
{
    $region = $listBox.SelectedItems
    $region
    $Hostnames = $textBox.Text
    $Hostnames
}




#############################################################
if ("TrustAllCertsPolicy" -as [type]) {} else{
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

[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Ssl3, [Net.SecurityProtocolType]::Tls, [Net.SecurityProtocolType]::Tls11, [Net.SecurityProtocolType]::Tls12
}


Import-Module SwisPowerShell
$ipamServer = 'dljdaprdswa1v.jdadelivers.com'


#$username1="jdadelivers\_mgmt_int_solar_aut"
$username1="_mgmt_int_solar_aut"
#$res="Wq1#Yw6@4nQzP$Sm8"
$res="zIc8@D^9q3@B"

#$username1="jdadelivers\Decom_Task"
#$res="FlAsH@3300939399"

$secureCreds = New-Object -typename System.Management.Automation.PSCredential -argumentlist @($username1,(ConvertTo-SecureString -String $res -AsPlainText -Force)) 
 #$GroupID = (Get-SwisData $SwisConnection "SELECT GroupId, Address FROM IPAM.IPHistorySubnetInfo WHERE (Address='$IPSubnet')").GroupID;

$swis =Connect-Swis -host $ipamServer -credential $secureCreds 
$swis

$dl="Dallas"
$fr="Frankfurt"
$sl="Slough"
$ka="Kansas"
$al="Atlanta"



if($region -eq $dl)
{
$ip_add="172.20.4.0"
$range="22"

}
elseif($region -eq $fr){
$ip_add="172.20.128.0"
$range="22"

}
elseif($region -eq $sl){
$ip_add="172.20.96.0"
$range="22"

}
elseif($region -eq $ka){
$ip_add="172.20.32.0"
$range="22"

}
elseif($region -eq $al){

$ip_add="172.20.64.0"
$range="22"
}

$finaloutput=@()

#$Hostnames="hi,bye,tata"

$hostnames=$Hostnames -split ","

$hostnames.GetType()

foreach($hostname in $hostnames){

"Trying to reserver IP for $hostname"
$subnets=Invoke-SwisVerb $swis IPAM.SubnetManagement GetFirstAvailableIp @("$ip_add","$range")
$ip=$subnets.'#text'
Write-output "The next available ip - $($ip)"

$ips1= ping $ip
if($ips1 -imatch "100% loss"){
Write-Host "Ping check failed - Reserving IP"


$idQuery = ("SELECT IpNodeId,DisplayName,DnsBackward FROM IPAM.IPNode where IPAddress = `'{0}`'" -f $ip)
$nodeId =  Get-SwisData -SwisConnection $swis -Query $idQuery
#----------------------
Write-output "Nodeid - $($nodeId.IPNodeId)"


$nodeUri = ('swis://{0}/Orion/IPAM.IPNode/IpNodeId={1}' -f $ipamserver, $nodeId.IPNodeId)
			$CustomURI = $nodeuri + "/Custom"
            #Get-SwisObject -SwisConnection $swis -Uri $nodeUri
			
			set-SwisObject -SwisConnection $swis -Uri $nodeUri -Properties @{'Status' = 4}
            #set-SwisObject -SwisConnection $swis -Uri $nodeUri -Properties @{'Type' = "Static"}
            set-SwisObject -SwisConnection $swis -Uri $nodeUri -Properties @{'DnsBackward' = $hostname}
            set-SwisObject -SwisConnection $swis -Uri $nodeUri -Properties @{'Comments' = $null}
            set-SwisObject -SwisConnection $swis -Uri $nodeUri -Properties @{'Alias' = $null}
            #set-SwisObject -SwisConnection $swis -Uri $nodeUri -Properties @{'DnsBackward' = $null}
			set-Swisobject -swisconnection $swis -uri $CustomURI -properties @{'AdditionalComments' = "  "}
            set-Swisobject -swisconnection $swis -uri $CustomURI -properties @{'Customer_Code' = "  "}
            set-Swisobject -swisconnection $swis -uri $CustomURI -properties @{'Customer_Name' = "  "}
            set-Swisobject -swisconnection $swis -uri $CustomURI -properties @{'NAT' = "  "}
            set-Swisobject -swisconnection $swis -uri $CustomURI -properties @{'Gateway' = "  "}
     
            $v=Get-SwisObject -SwisConnection $swis -Uri "$nodeUri"
            $v



}
else{
Write-Host "IP already in use"
}

$output=[pscustomobject][ordered]@{
        Servername = $hostname
        IPAddress= $ip
        Region= $($region)
        
        
    }

$finaloutput+=$output

}





if($finaloutput)
{


$logdate = (get-date).ToString("dd-MMM-yyyy_hhmmss")

$filepath="C:\xampp\htdocs\server_decomm\IPAM\IP_reservation_data\ipreservation_$($logdate).csv"
     
$finaloutput | Export-Csv -Path "$filepath" -NoTypeInformation




Email -path $filepath


}