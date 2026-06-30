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
$subnets

#$IPSubnet="172.20.4.0/22"  GroupId, Address
$Address="172.20.4.0"

$add=$Address.split(".")[0]+"."+$Address.split(".")[1]+"."+$Address.split(".")[2]



$idQuery =(Get-SwisData -SwisConnection $swis -Query "SELECT GroupId, Address FROM IPAM.IPHistorySubnetInfo WHERE (Address='$Address')").GroupID
$idQuery

#$qry="SELECT SubnetID, IPAddress, IPAddressN, Status FROM IPAM.IPNode WHERE Status = 2 AND SubnetID=$idQuery "
$qry="SELECT IPNodeId,SubnetID, IPAddress, IPAddressN, Status FROM IPAM.IPNode WHERE Status = 2 AND SubnetID=$idQuery  "


$nodeId =  Get-SwisData -SwisConnection $swis -Query $qry
$nodeId.IPNodeId
$data=$nodeId.IPAddress
#$data="172.20.4.65"
$data
foreach($ips in $data){
write-host "$ips" 
if($ips -match "$add"){
Write-Host "my name $ips"
$ips1= ping $ips
if($ips1 -imatch "100% loss"){
Write-Host "ping failed"

#################################################3
$ips

$idQuery = ("SELECT IpNodeId,DisplayName,DnsBackward FROM IPAM.IPNode where IPAddress = `'{0}`'" -f $ips)
$nodeId =  Get-SwisData -SwisConnection $swis -Query $idQuery
#----------------------
$nodeId.IPNodeId

<#
$nodeUri = ('swis://{0}/Orion/IPAM.IPNode/IpNodeId={1}' -f $ipamserver, $nodeId.IPnodeId)
			$CustomURI = $nodeuri + "/Custom"
			
			set-SwisObject -SwisConnection $swis -Uri $nodeUri -Properties @{'Status' = 4}
            #set-SwisObject -SwisConnection $swis -Uri $nodeUri -Properties @{'Type' = "Static"}
            #set-SwisObject -SwisConnection $swis -Uri $nodeUri -Properties @{'Hostname' = 4}
            set-SwisObject -SwisConnection $swis -Uri $nodeUri -Properties @{'Comments' = $null}
            set-SwisObject -SwisConnection $swis -Uri $nodeUri -Properties @{'Alias' = $null}
            set-SwisObject -SwisConnection $swis -Uri $nodeUri -Properties @{'DnsBackward' = $null}
			set-Swisobject -swisconnection $swis -uri $CustomURI -properties @{'AdditionalComments' = "  "}
            set-Swisobject -swisconnection $swis -uri $CustomURI -properties @{'Customer_Code' = "  "}
            set-Swisobject -swisconnection $swis -uri $CustomURI -properties @{'Customer_Name' = "  "}
            set-Swisobject -swisconnection $swis -uri $CustomURI -properties @{'NAT' = "  "}
            set-Swisobject -swisconnection $swis -uri $CustomURI -properties @{'Gateway' = "  "}
     
            $v=Get-SwisObject -SwisConnection $swis -Uri "$nodeUri"

Write-Host "nodeip is $($node)"

#>

################################################## Type,Hostname

}
else{
write-host "ping passed"
}

}
 
}

#$eq=$nodeId.IPAddress - $add
#$eq





#Invoke-SwisVerb $swis IPAM.SubnetManagement GetFirstAvailableIp @("199.10.1.0", "24")
#$ip="172.20.4.0/22"
#$idQuery = "SELECT TOP 10 I.Status, I.DisplayName FROM IPAM.IPNode I WHERE I.Status=2 "
#$idQuery = ("SELECT IpNodeId,DisplayName,DnsBackward FROM IPAM.IPNode where IPAddress = '$ip'")
#`'{0}`'" -f

#$subnets=Invoke-SwisVerb $swis IPAM.SubnetManagement GetAllAvailableIp @("172.20.4.0", "22")
#$subnets=Invoke-SwisVerb $swis IPAM.SubnetManagement GetFirstAvailableIp @("172.20.4.0", "22")










