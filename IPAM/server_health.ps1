$folder="C:\Sanmathi"
#############################################

##################################################

$offset3 =0
$inc3 =10000
$overall3 =@()
$flag3 =$false
while($flag3 -ne $true)
{
"Initial offset - $offset3"
$url3="https://blueyonderdev.service-now.com/api/now/table/cmdb_ci_win_server?sysparm_query=install_status=1&sysparm_limit=10000&sysparm_offset=$offset3"
$apikey = 'svc_notify_portal'
$password = 'india'

$global:headers = @{"Authorization" = "Basic "+[System.Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($apikey+":"+$password))}
$result3 = Invoke-RestMethod -Uri $url3 -Method Get -Headers $global:headers -ContentType "application/json"


#($result1.result).Count
$overall3+=$result3.result



"Data count - $($overall3.Count)"
$offset3+=$inc3
if(($result3.result).Count -eq 0 -or $overall3.Count -lt $offset3){$flag3=$true}
}

$overall3.name| Out-File $folder\servers.txt 
$servers=Get-Content "$folder\servers.txt"
$servers1=$servers[0..5]
$Error.Clear()
#$overall3.count at2blprrepa01v.jdadelivers.com]
#$date = get-date -Format "MM_dd_yyy" https://blueyonderdev.service-now.com/login.do
#$overall3 | Export-Csv "C:\Users\1031360\JDA_SNOW\SNOW_WINDOWS_SERVER_Table_$date.csv" -NoTypeInformation -Append -Force

#>
$username="1028742"
$password="JUne!@141995"
#$username="1033828"
#$password="Jnikhil321?**"

$passwordSecure = ConvertTo-SecureString ($password) -AsPlainText -Force
$Cred = New-Object System.Management.Automation.PSCredential ($username, $passwordSecure) 
$Cred


$finalout=@()
foreach($ser in $servers1){

$data=Invoke-Command -ComputerName $ser -Credential $Cred -ScriptBlock {
###### dljmfdevapp1v
#$status=(Get-CimInstance Win32_OperatingSystem).LastBootUpTime

$status=Get-WmiObject win32_operatingsystem | select @{LABEL='LastBootUpTime';EXPRESSION={$_.ConverttoDateTime($_.lastbootuptime)}}

$cpu = (Get-WmiObject -Class win32_processor -ErrorAction Stop | Measure-Object -Property LoadPercentage -Average | Select-Object Average).Average
 

$ComputerMemory = Get-WmiObject -Class win32_operatingsystem -ErrorAction Stop
$Memory = ((($ComputerMemory.TotalVisibleMemorySize - $ComputerMemory.FreePhysicalMemory)*100)/ $ComputerMemory.TotalVisibleMemorySize)
$RoundMemory = [math]::Round($Memory, 2)

Write-Host "nikhil"

#cpu
#memory  https://www.powershellbros.com/run-script-to-check-cpu-and-memory-utilization/

$obj=New-Object -TypeName PSObject
$obj|Add-member -MemberType NoteProperty -Name "computername" "$($env:COMPUTERNAME)"
$obj|Add-member -MemberType NoteProperty -Name "Uptime" "$status"
$obj|Add-member -MemberType NoteProperty -Name "CPU" "$cpu"
$obj|Add-member -MemberType NoteProperty -Name "Memory" "$RoundMemory"
#$obj|Add-member -MemberType NoteProperty -Name "free" "$status"

return $obj
}
$finalout+=$data
}


$data1=$finalout|select computername,uptime,cpu,Memory|export-csv "$folder\report1.csv" -NoTypeInformation

foreach($ser in $Error.targetobject)
{
Add-Content -Value "$ser,Not Reachable" -Path "$folder\report1.csv"
}
$path="$folder\report1.csv"
#Email -path $path

#Select -Property * -ExcludeProperty PSComputerName,RunSpaceID
#$data1|export-csv "$folder\report.csv" -NoTypeInformation

$res=import-csv $path

$SMTPMessage = New-Object System.Net.Mail.MailMessage
$SMTPServer = "mailout.jdadelivers.com"
$SMTPMessage.from="test@jadelivers.com"  
$to = "nikhileswarreddy.jonnavaram@blueyonder.com"#,"CS-India-Bladelogic@blueyonder.com","abhishek.kona@blueyonder.com")
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
$SMTPMessage.subject = "Server Health Check Report"
$SMTPMessage.IsBodyHTML = $true
$SMTPClient = New-Object Net.Mail.SmtpClient($SmtpServer, 25)
$SMTPClient.UseDefaultCredentials = $False
$messageBody = "<html><body><style>
      table {
        border-collapse: collapse;
      }
      th, td {
        border: 1px solid black;
        padding: 5px;
        text-align: left;
      }
    </style><p>Hi,</br>
    "
    if($res|?{$_.uptime -like "Not Reachable"})
    {
   $messageBody += "</br>Below are the list of Servers unreachable </br></p>
    <table>
    <tr bgcolor='C0C0C0'><th>ComputerName</th><th>Status</th></tr>"
    foreach($a in $res|?{$_.uptime -like "Not Reachable"})
    {$messageBody+="<tr><th>$($a.computername)</th><th>$($a.Uptime)</th></tr>"}
    $messageBody+="</table></br></br>"
    }


    if($res|?{$_.cpu -gt 80 -or $_.memory -gt 80})
    {
   $messageBody += "</br>Below are the list of Servers which has CPU or memory percentage greater than the threshold </br></p>
    <table>
    <tr bgcolor='C0C0C0'><th>ComputerName</th><th>Uptime</th><th>CPU</th><th>Memory</th></tr>"
    foreach($a in $res|?{$_.cpu -gt 80 -or $_.memory -gt 80})
    {$messageBody+="<tr><th>$($a.computername)</th><th>$($a.Uptime)</th><th>$($a.CPU)</th><th>$($a.Memory)</th></tr>"}
    $messageBody+="</table></br></br>"
    }
    $messageBody+="</body></html>"

$SMTPMessage.Body = $messageBody #body
$SMTPMessage.Attachments.Add($path)
$SMTPClient.Send($SMTPMessage)



#Attempting to perform the InitializeDefaultDrives operation on the 'FileSystem' provider failed.
