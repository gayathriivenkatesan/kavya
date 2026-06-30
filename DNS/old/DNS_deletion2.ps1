############################################################
#
# REMOVE DNS Server FROM DNS
# 
############################################################

Param([string]$filepath,[string]$destinationfile,[string]$username,[string]$sfcase,[string]$password)
$filepath="\\vincromi0019\C$\Decommissioning\decomm_portal\server_cleanup_common_input.csv"
$destinationfile="test.html"
$sfcase="123"
$Username = "1028742"
$Password = "SMPrs!@140495"
#$path="\\vincromi0019\C$\xampp\htdocs\server_decomm\decomm_logs\$sfcase\"
$date=Get-Date -Format "dd_MM_yyy_HH_mm_ss"
Start-Transcript -Path "$path\Report_$date.txt"

$pass = ConvertTo-SecureString -AsPlainText $Password -Force
$Cred = New-Object System.Management.Automation.PSCredential -ArgumentList $Username,$pass
Invoke-Command -ComputerName localhost -Credential $Cred -ArgumentList $filepath,$destinationfile,$sfcase,$username,$password -ScriptBlock{
$filepath=$args[0]
$destinationfile=$args[1]
$sfcase=$args[2]
$username=$args[3]
$password=$args[4]

import-module DNSServer

######## FORMAT DATE #############

$date = Get-Date -Format "dd_MM_yyyy_hh_mm_ss"
$date2 = Get-Date -Format "dd-MM-yyyy hh:mm:ss"

#$secureCreds = New-Object -typename System.Management.Automation.PSCredential -argumentlist @($username,(ConvertTo-SecureString -String $password -AsPlainText -Force))
############# CREATION OF LOG FOLDER #############

if(!(Test-Path -Path "\\vincromi0019\C$\xampp\htdocs\server_decomm\decomm_logs\$sfcase\")){
    New-Item "\\vincromi0019\C$\xampp\htdocs\server_decomm\decomm_logs\$sfcase" -ItemType Directory
}


############# READING A INPUT FILE  ###############
$us=whoami
write-host $us
$a=import-csv -Path $filepath
$a1=@()
# To  loop  through  the  csv list 
foreach($i in $a){
    $hostname=($i.servername).Trim()
    $domainname=($i.domainname).Trim()
    $dns_host_Ip=($i.serverip).Trim()
    $comp=($i.dnsservername).Trim()
        
############# REMOVING DNS SERVER FROM DNS #########
    try{
        $dns=Get-DnsServerResourceRecord -ZoneName $domainname -ComputerName  $comp -Name $hostname -ErrorAction Ignore|where {$_.RecordData.IPv4Address.IPAddressToString -eq $dns_host_Ip} 
        if($dns -ne $null -or $dns -ne ""){
            write-host "Pre-check $hostname is found in $domainname" -ForegroundColor Cyan 
            Write-host "Preparing to Remove DNS from  the Domain server....." -ForegroundColor Green
           # Remove-DnsServerResourceRecord -ZoneName $domainname -ComputerName $comp -RRType $dns.RecordType -Name $hostname -Force -Confirm:$false 
            $dns1=Get-DnsServerResourceRecord -ZoneName $domainname -ComputerName $comp -Name $hostname -ErrorAction SilentlyContinue
            if($dns1 -eq $null){
               write-host "Post-check $hostname is removed from $domainname" -Foregroundcolor Cyan
               $b="$hostname is removed from $domainname"
            }
            else{
               write-host "Failed to remove $hostname from $domainname" -ForegroundColor Red
               $b="Failed to remove $hostname from $domainname"
            }
        }
        else{
               Write-host "$hostname not found in DNS server" -ForegroundColor Red
               $b="Failed $hostname not found in DNS server"
        }
    }
    catch{
         write-host "Catch: $_" -ForegroundColor Red 
         $b="$_"
    }
   $a1+=$b
   $b=$null

  <#  try{
        #$s=new-pssession -ComputerName "vincromi0019.jdadelivers.com" -Credential $securecreds
        #$dns1=get-dnsserver -ComputerName $comp 
        #$dns1
        #$dns=Invoke-Command -Session $s -ScriptBlock{Get-DnsServerResourceRecord -ZoneName $domainname -ComputerName  $comp -Name $hostname} -ErrorAction Ignore
        #$s1=Invoke-Command -Session $s -ScriptBlock{Get-DnsServerResourceRecord -ZoneName jdadelivers.com -ComputerName scdc02 -Name dlwmtpsrdbn1v} -ErrorAction Ignore
        #write-host $s1
        # -CimSession $s -ErrorAction Ignore|where {$_.RecordData.IPv4Address.IPAddressToString -eq $dns_host_Ip}}
        #$s1
        $s=New-CimSession -ComputerName "vincromi0019.jdadelivers.com" -Credential $secureCreds
        $dns=Get-DnsServerResourceRecord -ZoneName $domainname -ComputerName  $comp -Name $hostname -ErrorAction Ignore -CimSession $s |where {$_.RecordData.IPv4Address.IPAddressToString -eq $dns_host_Ip}
        #$dns=Get-DnsServerResourceRecord -ZoneName jdadelivers.com -ComputerName  scdc02 -Name dlwmtpsrdbn1v #CimSession $s -ErrorAction Ignore
        #|where {$_.RecordData.IPv4Address.IPAddressToString -eq $dns_host_Ip}
        if($dns -ne $null){
            #write-host "Pre-check $hostname is found in $domainname" -ForegroundColor Cyan 
            #Write-host "Preparing to Remove DcureNS from  the Domain server....." -ForegroundColor Green
            #Remove-DnsServerResourceRecord -ZoneName $domainname -ComputerName $comp -RRType $dns.RecordType -Name $hostname -Force -Confirm:$false -cimsession $s.id
            $dns1=Get-DnsServerResourceRecord -ZoneName $domainname -ComputerName $comp -Name $hostname -ErrorAction SilentlyContinue -CimSession $s.id
            if($dns1 -eq $null){
               write-host "Post-check $hostname is removed from $domainname" -Foregroundcolor Cyan
               $b="$hostname is removed from $domainname"
            }
            else{
               write-host "Failed to remove $hostname from $domainname" -ForegroundColor Red
               $b="Failed to remove $hostname from $domainname"
            }
        }
        else{
               Write-host "$hostname not found in DNS server" -ForegroundColor Red
               $b="Failed $hostname not found in DNS server"
        }
    }
    catch{
         write-host "$_" -ForegroundColor Red 
         $b="$_"
    }
   $a1+=$b
   $b=$null#>
}
#$a1
$output=@()
$count=$a1.count
for($i1=0;$i1 -lt $count;$i1++){
$d=New-Object -TypeName psobject  
 Add-Member -InputObject $d  -MemberType NoteProperty -Name 'Sfcase' -Value $sfcase;
 Add-Member -InputObject $d  -MemberType NoteProperty -Name 'dns_HostName' -Value $a[$i1].servername;
 Add-Member -InputObject $d  -MemberType NoteProperty -Name 'dns_HostIP' -Value $a[$i1].serverip;
 Add-Member -InputObject $d  -MemberType NoteProperty -Name 'domainname' -Value $a[$i1].domainname;
 Add-Member -InputObject $d  -MemberType NoteProperty -Name 'server' -Value $a[$i1].dnsservername;
 Add-Member -InputObject $d  -MemberType NoteProperty -Name 'Status' -Value $a1[$i1];
  
 $output+= $d
}
#$output
$g="<html>
    <head>
    <style>
    table, th, td {
     border: 1px solid black;
    }
</style>
</head>
     <body>
     <center>
     <h1 ><b>DNS_DECOMM REPORT</b></h1>
     <h4 ><b>Execution time:<span >$date2</span></b></h3>
     <h4 ><b>Executed by:<span >$username</span></b></h3>
    
     <table>
     <thead>
     <tr>
	 <th>SF Case</th>
     <th>Server Name</th>
     <th>Server IP</th>
     <th>Domain Name</th>
     <th>DNS ServerName</th>
     <th>Result</th>
     </tr>
     </thead>
     <tbody>"
     $g+= $output|%{
     "<tr>
	 <td>$($_.Sfcase)</td>
     <td>$($_.dns_HostName)</td>
     <td>$($_.dns_HostIP)</td>
     <td>$($_.domainname)</td>
     <td>$($_.server)</td>"
     if($_.Status -like "Failed*"){
     "<td style='color:red;'>$($_.Status)</td>"
     }
     else{
     "<td style='color:green;'>$($_.Status)</td>" 
     }
     "</tr>"
     }
     $g+="</tbody>
     </table>
     </center>
     </body>
     </html>"
$g|out-file -FilePath "\\vincromi0019\C$\xampp\htdocs\server_decomm\decomm_logs\$sfcase\$destinationfile"

}

Stop-Transcript