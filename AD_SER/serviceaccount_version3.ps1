############################################################
#
# REMOVE SERVICEACCOUNT FROM AD
# 
############################################################
Param([string]$filepath,[string]$destinationfile,[string]$username,[string]$sfcase,[string]$res)
import-module activedirectory

######## FORMAT DATE #############

$date = Get-Date -Format "dd_MM_yyyy_hh_mm_ss"
$date1= Get-Date -Format "dd-MM-yyyy hh:mm:ss"
$user =(whoami).split("\")[1]
$usernames="Decom_Task"

$secureCreds = New-Object -typename System.Management.Automation.PSCredential -argumentlist @($usernames,(ConvertTo-SecureString -String $res -AsPlainText -Force))

############# CREATION OF LOG FOLDER #############

if(!(Test-Path -Path "C:\xampp\htdocs\server_decomm\decomm_logs\$sfcase")){
    New-Item "C:\xampp\htdocs\server_decomm\decomm_logs\$sfcase" -ItemType Directory
}
set-executionpolicy -ExecutionPolicy Unrestricted -Confirm:$false -Force
$a2=@()
$a1=Import-csv -Path $filepath
foreach($i in $a1)
{
    $serviceaccount=($i.user_security_group).Trim()
    $a=get-AdUser -filter "name -eq  '$serviceaccount'" -ErrorAction ignore
    $c=get-Adgroup -filter "name -eq '$serviceaccount'" -ErrorAction ignore
    $b=get-Adcomputer -filter "name -eq  '$serviceaccount'" -ErrorAction ignore
    

    if(($a.Name -ne $null -and $a.name -ne '')) {
        $a = Get-ADUser -Filter "Name -eq '$serviceaccount'" |Remove-ADUser -Credential $secureCreds -Confirm:$false
        $ad12 = Get-ADuser -identity $serviceaccount -ErrorAction Ignore
        if($ad12.name -eq $serviceaccount){
            write-host "Failed to remove user $serviceaccount" -ForegroundColor Red
            $b2="Failed to remove user $serviceaccount"
        }
        else{
            write-host "Successfully removed $serviceaccount" -ForegroundColor Green
            $b2="Successfully removed $serviceaccount"

        }
    }
    elseif(($c.Name -ne $null -and $c.name -ne '')){
        $c = Get-ADGroup -Filter "Name -eq '$serviceaccount'" |Remove-ADGroup -Credential $secureCreds -Confirm:$false
        $c12 = Get-ADGroup -identity $serviceaccount -ErrorAction Ignore
        if($c12.name -eq $serviceaccount){
            write-host "Failed to remove group $serviceaccount" -ForegroundColor Red
            $b2="Failed to remove group $serviceaccount"
        }
        else{
            write-host "Successfully removed $serviceaccount" -ForegroundColor Green
            $b2="Successfully removed $serviceaccount"
        }

    }
    elseif(($b.Name -ne $null -and $b.name -ne '')) {
        $b = Get-ADcomputer -Filter "Name -eq '$serviceaccount'" |Remove-ADComputer -credential $secureCreds -Confirm:$false
        $b12 = Get-ADcomputer -identity $serviceaccount -ErrorAction Ignore
        if($b12.name -eq $serviceaccount){
            write-host "Failed to remove computer $serviceaccount" -ForegroundColor Red
            $b2="Failed to remove computer $serviceaccount"
        }
        else{
            write-host "Successfully removed $serviceaccount" -ForegroundColor Green
            $b2="Successfully removed $serviceaccount"
        }
     
    }
    else{
        write-host "$serviceaccount Not found"
        $b2="$serviceaccount Not found"
    }
    $a2+=$b2
    $b2=$null

}
$output1=@()
$count=$a2.count
for($i1=0;$i1 -lt $count;$i1++){
$d=New-Object -TypeName psobject  
 Add-Member -InputObject $d  -MemberType NoteProperty -Name 'sfcase' -Value $sfcase; 
 Add-Member -InputObject $d  -MemberType NoteProperty -Name 'serviceaccount' -Value $a1[$i1].user_security_group;
 Add-Member -InputObject $d  -MemberType NoteProperty -Name 'Status' -Value $a2[$i1];
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
     <h1 ><b>ServiceAccount Deletion Report</b></h1>
     <h4 ><b>Execution time: <span >$date1</span></b></h3>
     <h4 ><b>Executed by: <span >$user</span></b></h3>
     <table>
     <thead>
     <tr>
	 <th>SFcase</th>
     <th>Service Account Name</th>
     <th>Result</th>
     </tr>
     </thead>
     <tbody>"
     $g1+= $output1|%{ 
     "<tr>
	 <td>$($_.sfcase)</td>
     <td>$($_.serviceaccount)</td>"
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
$g1|out-file -FilePath $destinationfile
