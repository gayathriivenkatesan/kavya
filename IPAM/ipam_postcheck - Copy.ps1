############################################################
#
# IP RECLAIM -SERVER DECOMMISSION 
# 
############################################################
Param([string]$filename,[string]$user1,[string]$s,[string]$sfcase,[string]$res)
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
$username=$user1
############# CREATION OF LOG FOLDER #############

if(!(Test-Path -Path "c:\xampp\htdocs\server_decomm\decomm_logs\$sfcase\")){
    New-Item "c:\xampp\htdocs\server_decomm\decomm_logs\$sfcase\" -ItemType Directory
}

Import-Module SwisPowerShell
$ipamServer = 'dljdaprdswa1v.jdadelivers.com'


$username1="jdadelivers\Decom_Task"
$secureCreds = New-Object -typename System.Management.Automation.PSCredential -argumentlist @($username1,(ConvertTo-SecureString -String $res -AsPlainText -Force))


############# READING A INPUT FILE  ###########
$c=0
$a1=@()
$a=$s.split(",")
try{
	$swis =Connect-Swis -host $ipamServer -credential $secureCreds
	#$swis=Connect-Swis -host $ipamServer -trusted
	foreach($i in $a)
	{
		$ip=($i).Trim()
		#$swis=Connect-Swis -host $ipamServer -username $username -password $password
		$idQuery = ("SELECT IpNodeId,DisplayName,DnsBackward FROM IPAM.IPNode where IPAddress = `'{0}`'" -f $ip)
		$nodeId =  Get-SwisData -SwisConnection $swis -Query $idQuery -TimeOut 60 
        if($nodeId){
			$nodeUri = ('swis://{0}/Orion/IPAM.IPNode/IpNodeId={1}' -f $ipamserver, $nodeId.IPnodeId)
			$CustomURI = $nodeuri + "/Custom"
			
			set-SwisObject -SwisConnection $swis -Uri $nodeUri -Properties @{'Status' = 2}
            set-SwisObject -SwisConnection $swis -Uri $nodeUri -Properties @{'Comments' = $null}
            set-SwisObject -SwisConnection $swis -Uri $nodeUri -Properties @{'Alias' = $null}
            set-SwisObject -SwisConnection $swis -Uri $nodeUri -Properties @{'DnsBackward' = $null}
			set-Swisobject -swisconnection $swis -uri $CustomURI -properties @{'AdditionalComments' = "  "}
            set-Swisobject -swisconnection $swis -uri $CustomURI -properties @{'Customer_Code' = "  "}
            set-Swisobject -swisconnection $swis -uri $CustomURI -properties @{'Customer_Name' = "  "}
            set-Swisobject -swisconnection $swis -uri $CustomURI -properties @{'NAT' = "  "}
            set-Swisobject -swisconnection $swis -uri $CustomURI -properties @{'Gateway' = "  "}
     
            $v=Get-SwisObject -SwisConnection $swis -Uri "$nodeUri"
			if($v.status.ToString() -eq '2'){
				$a2=$v.DisplayName.Tostring()+","+$v.DnsBackward.Tostring()+","+$v.comments.Tostring()+","+$v.alias.Tostring()+","+$v.Status.Tostring()+","+"Success"
				#$a2=$v.DnsBackward.Tostring()+","+$v.Status.Tostring()+","+"Success"
				$a1+=$a2
			}
			else{
				$a2=$v.DisplayName.Tostring()+","+$v.DnsBackward.Tostring()+","+$v.comments.Tostring()+","+$v.alias.Tostring()+","+$v.Status.Tostring()+","+"Failed-Unable to change State"
				#$a2=$v.DnsBackward.Tostring()+","+$v.Status.Tostring()+","+"Failed-Unable to change State"
                $a1+=$a2
			}
        }
        else{
            $a1+=",,Failed not found"
        }
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
 Add-Member -InputObject $d  -MemberType NoteProperty -Name 'servername' -Value $a[$i1];
 Add-Member -InputObject $d  -MemberType NoteProperty -Name 'DnsBackward' -Value $a1[$i1].split(",")[1];
 Add-Member -InputObject $d  -MemberType NoteProperty -Name 'Comments' -Value $a1[$i1].split(",")[2];
 Add-Member -InputObject $d  -MemberType NoteProperty -Name 'alias' -Value $a1[$i1].split(",")[3];
 Add-Member -InputObject $d  -MemberType NoteProperty -Name 'Status' -Value $a1[$i1].split(",")[4];
 Add-Member -InputObject $d  -MemberType NoteProperty -Name 'State' -Value $a1[$i1].split(",")[-1];
 $output1+= $d
}
$output1
write-host $output1
$output2=$output1| Where-Object {$_.State -EQ "success"}
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
     <h4 ><b>IPAM Postcheck Report</b></h4>
     <h4 ><b>Execution time: <span >$date1</span></b></h4>
     <table>
     <thead>
     <tr>
	 <th>SFCase</th>
     <th>Server Name</th>
     <th>DNSBackward</th>
	 <th>Comments</th>
	 <th>Alias</th>
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
$g1|out-file -FilePath $filename
