$domain1="27.10.in-addr.arpa"
$comp1="scdc02"
$host1="1.143"
$dns2=Get-DnsServerResourceRecord -ZoneName $domain1    -ComputerName  $comp1  -Name $host1 
$dns2

#$dns=Get-DnsServerResourceRecord -ZoneName $domainname -ComputerName  $comp -Name $hostname -RRType A
Remove-DnsServerResourceRecord -ZoneName $domain1 -ComputerName $comp1 -RRType $dns2.RecordType -Name $host1 -Force  -Confirm:$false 

#10.27.143.1