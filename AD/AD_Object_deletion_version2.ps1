############################################################
#
# REMOVE COMPUTER FROM AD
# 
############################################################
Param([string]$filepath,[string]$destinationfile,[string]$username,[string]$password,[string]$sfcase)
import-module activedirectory

######## FORMAT DATE #############

$date = Get-Date -Format "dd_MM_yyyy_hh_mm_ss"
$date1= Get-Date -Format "dd-MM-yyyy hh:mm:ss"
$usernames="jdadelivers\Decom_Task"
$secureCreds = New-Object -typename System.Management.Automation.PSCredential -argumentlist @($usernames,(ConvertTo-SecureString -String $password -AsPlainText -Force))


############# CREATION OF LOG FOLDER #############

if(!(Test-Path -Path "C:\xampp\htdocs\server_decomm\decomm_logs\$sfcase\")){
    New-Item "C:\xampp\htdocs\server_decomm\decomm_logs\$sfcase\" -ItemType Directory
}
#set-executionpolicy -ExecutionPolicy Unrestricted -Confirm:$false -Force
#Start-Transcript "$env:USERPROFILE\Desktop\decomm_logs\ADstatus_log_$date.txt"

############# READING A INPUT FILE  ###########
#$a=Import-csv -Path "$env:USERPROFILE\Desktop\decomminp_AD.csv"
$a=Import-csv -Path "C:\xampp\htdocs\server_decomm\AD\AD_input.csv"
$a2=@()
# To  loop  through  the  csv list 
foreach($i in $a)
{
    #$server=$i.server
    $domainname=($i.domainname).Trim()
    $computername=($i.servername).Trim()
    
    ############# REMOVING COMPUTER FROM AD USING DOMAIN  ###########
 
    $d1=$domainname.split('.')[0]
    $d2=$domainname.split('.')[1]
    #$dnsname=$computername.Toupper()+"."+$domainname

        $computer1=$computername+"-c"
        #write-host "Pre-check before removing AD COMPUTER AND GROUP" -ForegroundColor Cyan
        $ad1 = Get-ADComputer -Filter "Name -eq '$computername' -or Name -eq '$computer1' " -SearchBase "DC=$d1,DC=$d2" -ErrorAction Ignore -Properties name,DistinguishedName,DNSHostName,ObjectClass,SID,IPV4Address,OperatingSystem
        if(($ad1.Name -ne $null -and $ad1.name -ne '')) # -or ($ad2.Name -ne $null -and $ad2.name -ne ''))
        {
            #Write-host "$computername found from $domainname" -ForegroundColor Green
            if($ad1.OperatingSystem -like "Windows*")
            {
                $ad1.OperatingSystem
                try{
                        Get-ADComputer -Identity $ad1.SamAccountName | Remove-ADObject -Recursive -confirm:$false -ErrorAction SilentlyContinue -credential $secureCreds
                        #Remove-ADComputer -Identity $ad1.SamAccountName  -Confirm:$false -ErrorAction Ignore
                        #write-host "Removing $computername from $domainname" -ForegroundColor Green
                        $adcom1=Get-ADComputer -Filter "Name -eq '$computername'"  -SearchBase "DC=$d1,DC=$d2" -ErrorAction Ignore -Properties name,DistinguishedName,DNSHostName,ObjectClass,SID,IPV4Address,OperatingSystem 
                        #write-host "Post-check after removing AD COMPUTER" -ForegroundColor Cyan
                        if($adcom1.Name -eq $computername)
                        { 
                            #write-host "Failed to remove $computername" -ForegroundColor Red
                            $b2="Failed to remove $computername"
                        }
                        else
                        {
                            #Write-host "$computername removed from $domainname" -ForegroundColor Green
                            $b2="$computername removed from $domainname"
                        }
                }
                catch
                {
                        #Write-Host "$_" -ForegroundColor Red
                    $b2="Failed -$_"
                    
                }
            }
            else
            {
                 #Write-Host "Operating System = Linux\Unix Server"
                 #Write-Host "Removing computer"
                 $computer1=$computername+"-c"
                 try{
                     
                        Remove-ADComputer -Identity $ad1.SamAccountName -Confirm:$false -ErrorAction Ignore -credential $securecreds
                        #write-host "Removing $computername from $domainname" -ForegroundColor Green
                        start-sleep -seconds 5
                        $adcom1 = Get-ADComputer -Filter "Name -like '$computer1'" -SearchBase "DC=$d1,DC=$d2" -ErrorAction Ignore -Properties name,DistinguishedName,DNSHostName,ObjectClass,SID,IPV4Address,OperatingSystem
                        #$adcom1=Get-ADComputer -Filter "Name -like '$computer1'" 
                        #write-host "Post-check after removing AD COMPUTER" -ForegroundColor Cyan
                        #if($adcom1.Name -eq $computer1)
                        if($adcom1 -ne $null -and $adcom1.name -ne $null)
                        { 
                            #write-host "Failed to remove $computername" -ForegroundColor Red
                            $b2="Failed to  remove $computername from linux\unix computer"
                        }
                        else
                        {
                            #Write-host "$computername removed from $domainname" -ForegroundColor Green
                            $b2="$computername removed from linux\unix computer"
                        }
                    }
                    catch
                    {
                        #Write-Host "$_" -ForegroundColor Red
                        $b2="Failed $Computername Not Found from linux\unixcomputer"
                    
                    }
                 #Write-Host "Removing Group"
                 $ad12 = Get-ADGroup -Filter "Name -like '$computername-access*' -and GroupCategory -eq 'Security'" -Properties * 
                 #-SearchBase "OU=Security Groups,DC=$DC1,DC=$DC2"
                 if($ad12.Name -ne $null -and $ad12.CanonicalName -like "$domainname/UnixServers/*$computername*-Access")
                 {
                       #Write-Host "Precheck- $computername found in security group" -ForegroundColor Green
                       try{
                               Get-ADGroup -Filter "Name -like '$computername-access' -and GroupCategory -eq 'Security'" -Properties * -SearchBase "DC=$d1,DC=$d2"|Remove-Adgroup  -Confirm:$False -credential $secureCreds
                               #write-host "Preparing to remove Security group $computername from $domainname ....." -ForegroundColor Cyan
                               start-sleep -seconds 5
                               $adl12a=Get-ADGroup -Filter "Name -like '$computername-access' -and GroupCategory -eq 'Security'" -Properties * -SearchBase "DC=$d1,DC=$d2"
                               $adl12a
                               if($adl12a -ne $null -and $adl12a.name -ne $null)
                               {
                                   #Write-host "Postcheck- Failed to $computername remove from $domainname" -ForegroundColor red
                                   $b2="Failed to  removed $computername and object group from $domainname"
                               }
                               else
                               {
                                   #Write-host "Postcheck-  removed $computername from $domainname" -ForegroundColor green
                                   $b2="$computername and object group is removed from $domainname "
                                  
                               }
                           }
                       catch
                       {
                          #Write-Host "$_" -ForegroundColor Red
                         $b2="Failed $Computername Not Found"
                       }
                  }
                  else
                  {
                       #write-host "Precheck- $computername not found in  security group" -ForegroundColor Red
                       $b2="Failed $computername not found in  security group. Deleted from Computer object"
                  }
             }
        }
        else
        {
        #Write-host "$computername not found from $domainname" -ForegroundColor Red 
        $b2="Failed $computername not found from $domainname"
        }
    #Write-host "**********************************************************"
    $a2+=$b2
    $b2=$null
}
$output1=@()
$count=$a2.count
for($i1=0;$i1 -lt $count;$i1++){
$d=New-Object -TypeName psobject 
 Add-Member -InputObject $d  -MemberType NoteProperty -Name 'sfcase' -Value $sfcase;  
 Add-Member -InputObject $d  -MemberType NoteProperty -Name 'ComputerName' -Value $a[$i1].servername;
 Add-Member -InputObject $d  -MemberType NoteProperty -Name 'DomainName' -Value $a[$i1].domainname;
 Add-Member -InputObject $d  -MemberType NoteProperty -Name 'Status' -Value $a2[$i1]
 $output1+= $d
}
#$output1|out-file -filepath "D:\xampp\htdocs\server_decomm\newproj\decomm_logs\$destinationfile.xlsx"
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
     <h1 ><b>AD-OBJECT_DELETION_DECOMM REPORT</b></h1>
     <h4 ><b>Execution time: <span >$date1</span></b></h3>
     <h4 ><b>Executed by: <span >$username</span></b></h3>
     <table>
     <thead>
     <tr>
	 <th>SFcase</th>
     <th>Computer Name</th>
     <th>Domain Name</th>
     <th>Result</th>
     </tr>
     </thead>
     <tbody>"
     $g1+= $output1|%{ 
     "<tr>
	 <td>$($_.sfcase)</td>
     <td>$($_.ComputerName)</td>
     <td>$($_.DomainName)</td>"
     if($_.Status -like "Failed*"){
     "<td style='color:red;'>$($_.Status)</td>"
     }
     else{
     "<td style='color:green;'>$($_.Status)</td>" 
     }
     "</tr>"
     }
     $g1+="</tbody>
     </table>
     </center>
     </body>
     </html>"
$g1|out-file -FilePath "c:\xampp\htdocs\server_decomm\decomm_logs\$sfcase\$destinationfile"



