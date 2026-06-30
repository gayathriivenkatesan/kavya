#Param([string]$filepath,[string]$destinationfile,[string]$username,[string]$sfcase,[string]$password)
#$filepath="\\vincromi0019\C$\Decommissioning\decomm_portal\server_cleanup_common_input.csv"
#$destinationfile="test.html"
#$sfcase="00123"
#$Username = "jdadelivers\1028742"
#$Password = "SMPrs!@140495"
#$counta="5"
#$filepath,$destinationfile,$sfcase,$username,$password

$data=$args[0] -split ","
$filepath=$data[0]
$destinationfile=$data[1]
$sfcase=$data[2]
$username=$data[3]
#$password=$data[4]
$counta=$data[4]
#[string]$sf=$sfcase

#$path="\\vincromi0019\C$\xampp\htdocs\server_decomm\decomm_logs\$sfcase"
$date=Get-Date -Format "dd_MM_yyy_HH_mm_ss"

#write-host $data
#write-host $sfcase.length
##write-host $data[2]
#write-host count
#write-host $counta

If (-NOT  (([int]($sfcase.ToString()).length) -eq [int]$counta)){
#$ss=[int]$counta - [int]($sfcase.ToString()).length
$sfcases=$sfcase.padleft($counta,'0')
$path="\\vincromi0019\C$\xampp\htdocs\server_decomm\decomm_logs\$sfcases"
write-host $path
}
else{
$path="\\vincromi0019\C$\xampp\htdocs\server_decomm\decomm_logs\$sfcase"
write-host $path
}
Start-Transcript -Path "$path\Report2_$($sfcase)_$($date).txt"
#$pass = ConvertTo-SecureString -AsPlainText $Password -Force
#$Cred = New-Object System.Management.Automation.PSCredential -ArgumentList $Username,$pass
import-module DNSServer
#[void][system.reflection.Assembly]::LoadWithPartialName("MySql.Data")
#$MySQLHost="localhost"
#$user="root"
#$pass=""
#$database="server_decomm"
#$connStr = "server=" + $MySQLHost + ";port=3306;uid=" + $user + ";pwd=" + $pass + ";database="+$database+";Pooling=FALSE" 
#$conn = New-Object MySql.Data.MySqlClient.MySqlConnection($connStr) 
#$conn.Open()
#$query = "INSERT INTO dns_tracker (status) VALUES ('Started')" 
#$command = $conn.CreateCommand()                 
#$command.CommandText = $query                     
#$RowsInserted = $command.ExecuteNonQuery() 
#$sno=$command.LastInsertedId

######## FORMAT DATE #############

$date = Get-Date -Format "dd_MM_yyyy_hh_mm_ss"
$date2 = Get-Date -Format "dd-MM-yyyy hh:mm:ss"

#$secureCreds = New-Object -typename System.Management.Automation.PSCredential -argumentlist @($username,(ConvertTo-SecureString -String $password -AsPlainText -Force))
############# CREATION OF LOG FOLDER #############

#if(!(Test-Path -Path "\\vincromi0019\C$\xampp\htdocs\server_decomm\decomm_logs\$sfcase\")){
#    New-Item "\\vincromi0019\C$\xampp\htdocs\server_decomm\decomm_logs\$sfcase" -ItemType Directory
#}
if(!(Test-Path -Path $path)){
    New-Item $path -ItemType Directory
}

############# READING A INPUT FILE  ###############
$us=whoami
write-host $us
#$filepathh = "c:\xampp\htdocs\server_decomm\DNS\decomminp_DNS.csv"
$a=import-csv -Path $filepath
$a1=@()
$counts=0
# To  loop  through  the  csv list 
foreach($i in $a){
	$counts+=1
    #$query2 = "UPDATE dns_tracker SET count=$counts WHERE sno=$sno" 
    #$command.CommandText = $query2                     
    #$RowsInserted = $command.ExecuteNonQuery()
	#$command.Dispose()
    $hostname=($i.servername).Trim()
    $domainname=($i.domainname).Trim()
    $dns_host_Ip=($i.serverip).Trim()

    $comp=($i.dnsservername).Trim()
    $pp=Get-DnsServerResourceRecord -ZoneName $domainname -ComputerName  $comp -Name $hostname -ErrorAction Ignore|where {$_.RecordData.IPv4Address.IPAddressToString -eq $dns_host_Ip} 
    Write-Output $pp

    #Displaying the hostname in Reverse look up Zones

    $mix=$dns_host_Ip.Split(".")

    $domain1=$mix[1]+"."+$mix[0]+"."+"in-addr.arpa"

    $host1=$mix[3]+"."+$mix[2]

    $dns2=Get-DnsServerResourceRecord -ZoneName $domain1    -ComputerName  $comp  -Name $host1 







    if($pp)
    {
############# REMOVING DNS SERVER FROM DNS #########
    try{
        $dns=Get-DnsServerResourceRecord -ZoneName $domainname -ComputerName  $comp -Name $hostname -ErrorAction Ignore|where {$_.RecordData.IPv4Address.IPAddressToString -eq $dns_host_Ip} 
        if($dns -ne $null -or $dns -ne ""){
            write-host "Pre-check $hostname is found in $domainname" -ForegroundColor Cyan 
            Write-host "Preparing to Remove DNS from  the Domain server....." -ForegroundColor Green
            Remove-DnsServerResourceRecord -ZoneName $domainname -ComputerName $comp -RRType $dns.RecordType -Name $hostname -Force  -Confirm:$false 
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
        #Removing Hostname in Reverse Lookup Zones 
        if($dns2 -ne $null -or $dns2 -ne ""){
            write-host "Pre-check $host1 is found in $domain1" -ForegroundColor Cyan 
            Write-host "Preparing to Remove Hostname from Reverse Lookup Zone....." -ForegroundColor Green
            Remove-DnsServerResourceRecord -ZoneName $domain1 -ComputerName $comp -RRType $dns2.RecordType -Name $host1 -Force  -Confirm:$false 

            $dns3=Get-DnsServerResourceRecord -ZoneName $domain1 -ComputerName $comp -Name $host1 -ErrorAction SilentlyContinue
            if($dns3 -eq $null){
               write-host "Post-check $host1 is removed from $domain1" -Foregroundcolor Cyan
               
            }
            else{
               write-host "Failed to remove $host1 from $domain1" -ForegroundColor Red
               
            }
        }

        else{
               Write-host "$hostname not found in DNS server" -ForegroundColor Red
               $b="Failed $hostname not found in DNS server"
        }
    }
    catch{
         write-host "Catch: $_" -ForegroundColor Red 
         $b="Catch: $_"
    }
    }
    else
    {
    Write-host "$hostname not found in DNS server" -ForegroundColor Red
    $b="Failed $hostname not found in DNS server."
    }

   $a1+=$b
   $b=$null
}
$a1
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
$output
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
     if($_.Status -like "Failed*" -or $_.Status -like "Catch*"){
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
$g|out-file -FilePath "$path\$destinationfile"
#$g | out-file -FilePath  "C:\xampp\htdocs\server_decomm\decomm_logs\"+$sfcases+"\"+$destinationfile
$sfcases
$destinationfile


#"Hi" | out-file -FilePath  "C:\xampp\htdocs\server_decomm\decomm_logs\1029311\Report2.txt"








$g
#$query1 = "UPDATE dns_tracker SET status='Completed' WHERE sno=$sno" 
#$command.CommandText = $query1                     
#$RowsInserted = $command.ExecuteNonQuery() 
#$command.Dispose()
#$conn.close()

Stop-Transcript
