############################################################
#
# IP RECLAIM -SERVER DECOMMISSION 
# 
############################################################

Param([string]$filepath,[string]$destinationfile,[string]$username1,[string]$sfcase,[string]$res)

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

######## FORMAT DATE #############

$date = Get-Date -Format "dd_MM_yyyy_hh_mm_ss"
$date1= Get-Date -Format "dd-MM-yyyy hh:mm:ss"
$user =(whoami).split("\")[1]

############# CREATION OF LOG FOLDER #############

if(!(Test-Path -Path "c:\xampp\htdocs\server_decomm\decomm_logs\$sfcase\")){
    New-Item "c:\xampp\htdocs\server_decomm\decomm_logs\$sfcase\" -ItemType Directory
}

Import-Module SwisPowerShell
$ipamServer = 'dljdaprdsw1ha.jdadelivers.com'

#$creds = Get-credential 
#[string][ValidateNotNullOrEmpty()] $vcenter_pass = $password
$username2="jdadelivers\Decom_Task"
#$password = ConvertTo-SecureString -String $password -AsPlainText -Force
$secureCreds = New-Object -typename System.Management.Automation.PSCredential -argumentlist @($username2,(ConvertTo-SecureString -String $res -AsPlainText -Force))
#$secureCreds = New-Object System.Management.Automation.PsCredential -ArgumentList $vcenter_pass ,$username

############# READING A INPUT FILE  ###########
$a=Import-csv -Path $filepath
# To  loop  through  the  csv list 
#$c=0
$a1=@()
try{
	foreach($i in $a)
	{
		$ip=($i.serverip).Trim() 
		#$domain=($i.domainname).trim() 
		$swis =Connect-Swis -host $ipamServer -credential $secureCreds
		#$swis=Connect-Swis -host $ipamServer -trusted
		#$swis=Connect-Swis -host $ipamServer -username $username -password $password
		$idQuery = ("SELECT IpNodeId,DisplayName,DnsBackward,comments,alias,status FROM IPAM.IPNode where IPAddress = `'{0}`'" -f $ip) #DisplayName,DnsBackward,comments,alias,status 
		$nodeId =  Get-SwisData -SwisConnection $swis -Query $idQuery -TimeOut 60 
        if($nodeId){
	    $nodeUri = ('swis://{0}/Orion/IPAM.IPNode/IpNodeId={1}' -f $ipamserver, $nodeId.IPnodeId)
            $v=Get-SwisObject -SwisConnection $swis -Uri "$nodeUri"
            $a2=$v.DisplayName.Tostring()+","+$v.DnsBackward.Tostring()+","+$v.comments.Tostring()+","+$v.alias.Tostring()+","+$v.Status.Tostring()+","+"success"
            $a1+=$a2
        }
        else{
            $a1+=",,,,,Failed not found"
        }
        $swis.close()
    }

}
catch{
    $a1+=$_
}
$output1=@()
$count=$a1.count
for($i1=0;$i1 -lt $count;$i1++){
$d=New-Object -TypeName psobject
 Add-Member -InputObject $d  -MemberType NoteProperty -Name 'SFCase' -Value $sfcase;
 Add-Member -InputObject $d  -MemberType NoteProperty -Name 'servername' -Value $a[$i1].serverip;
 Add-Member -InputObject $d  -MemberType NoteProperty -Name 'DnsBackward' -Value $a1[$i1].split(",")[1];
 Add-Member -InputObject $d  -MemberType NoteProperty -Name 'Comments' -Value $a1[$i1].split(",")[2];
 Add-Member -InputObject $d  -MemberType NoteProperty -Name 'alias' -Value $a1[$i1].split(",")[3];
 Add-Member -InputObject $d  -MemberType NoteProperty -Name 'Status' -Value $a1[$i1].split(",")[4];
 Add-Member -InputObject $d  -MemberType NoteProperty -Name 'State' -Value $a1[$i1].split(",")[-1];
 $output1+= $d
}
$file=$destinationfile.split(".")[0]
$output1|export-csv -Path "c:\xampp\htdocs\server_decomm\decomm_logs\$sfcase\precheckoverall_$file.csv"
$output1
$output2=@()
$output2 +=$output1| Where-Object {$_.State -EQ "success"}
write-host $output2
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
     <h4 ><b>IPAM Precheck Report</b></h4>
     <h4 ><b>Execution time: <span >$date1</span></b></h3>
     <h4 ><b>Executed by: <span >$username1</span></b></h4>
     <table>
     <thead>
     <tr>
	 <th>SFCase</th>
     <th>Server Name</th>
     <th>DNSBackward</th>
	 <th>Comments</th>
	 <th>alias</th>
     <th>Status</th>
     <th>State</th>
     </tr>
     </thead>
     <tbody>"
     $g1+= $output1|%{ 
     "<tr>
	 <td>$($_.SFCase)</td>
     <td>$($_.servername)</td>
     <td>$($_.DNSBackward)</td>
	 <td>$($_.Comments)</td>
	 <td>$($_.alias)</td>
     <td>$($_.Status)</td>"

     if($_.State -like "*Failed*"){
     "<td style='color:red;'>$($_.State)</td>"
     }
     else{
     "<td style='color:green;'>$($_.State)</td>" 
     }
     "</tr>"
     }
     $g1+="</tbody>
     </table>
     </center>
     </body>
     </html>"
$g1|out-file -FilePath "c:\xampp\htdocs\server_decomm\decomm_logs\$sfcase\$destinationfile"
