  #$path1 = "C:\Storage_Healthcheck_dashboard"
  #$date = Get-date -Format "dd-MM-yyyy-HH:mm:ss"
  #$Logfile = "$path\logs\error\StorageDeviceHealthCheck_$date"

Import-Module posh-SSH

$input_data = Import-Csv -Path "C:\Storage_Healthcheck_dashboard\Input_data.csv"

Write-Host "Hence creating folder to Export the csv file."
 #$foldername = Get-Date -Format "dd-MM-yyyy-HH:mm:ss"
 #mkdir -path "C:\Storage_Healthcheck_dashboard\Logs" -Name $foldername

$foldername = Get-Date -Format "dd-MM-yyyy-HH-mm-ss"
$folderpath = "C:\Storage_Healthcheck_dashboard\Logs\$foldername"

New-Item -Path $folderpath -ItemType Directory


$fullpath = "C:\Storage_Healthcheck_dashboard\Logs"

$path = Get-ChildItem $fullpath | Sort-Object CreationTime -desc | Select-Object -First 1
#starting Transcript
Start-Transcript -Path "$($path.FullName)\StorageDeviceHealthCheck.txt" 

 #$IsiolonResult=@()
 $resultStatus=@()

 foreach ($line in $input_data) {
    $DeviceType = $line.DeviceType.Trim()
    $DeviceName = $line.DeviceName.Trim()
    $UserName = $line.UserName.Trim()
    $userPassword = $line.Password.Trim()

# PureStorageDevices
function PureStorageDevices {
        param(
            [Parameter(Mandatory = $true)]
            [string]$Device,

            [Parameter(Mandatory = $true)]
            [string]$User,

            [Parameter(Mandatory = $true)]
            [string]$Password

           
            
        )

Write-Host "###############################################################################"
Write-Host "Device Name:$Device"

[securestring]$secStringPassword = ConvertTo-SecureString $Password -AsPlainText -Force
[pscredential]$cred = New-Object System.Management.Automation.PSCredential ($user, $secStringPassword)
$cred

 $session = New-SSHSession -ComputerName $Device -Credential $cred -ConnectionTimeout 120 -AcceptKey

 if($session)
 {
   $command = "purehw list"
   $output = Invoke-SSHCommand -SessionId $session.SessionId -Command $command
   $data= $output.output

   $lines = $data -split "`n" | Select-Object -Skip 1
   $result=@()
   $resultStatus = @()
   foreach ($line in $lines) 
  {

    $columns = $line -split "\s+"
    $status = $columns[1]

  
    $result += New-Object psobject -Property @{

    Status = $status

   }
 }

   if($result.Status -eq "unhealthy") 
   {
     $finalresult = "UnHealthy"
     Write-Output $finalresult
     $Remarks=$finalresult
     Write-Host $Remarks

   }
   else
   {
    $finalresult = "Healthy"
    Write-Output $finalresult
    $Remarks='NA'
    Write-Host $Remarks
   }

    Remove-SSHSession -SessionId $session.SessionId

   if ($null -eq $session.Connected) 
   {
          Write-Host "Hence $Device removed the SSH connection"
                
    } else 
    {
       Write-Host "Unable to remove the SSH session for this $Device"
    }

    sleep 20

   $resultStatus += New-Object psobject -Property @{

   Technology = "PURE STORAGE DEVICES"
   DeviceName = $Device
   Status = $finalresult
   Remarks=$Remarks
  

   }

$resultStatus | Select-Object Technology,DeviceName,Status,Remarks | Export-Csv -Path "C:\Storage_Healthcheck_dashboard\Logs\$path\Status.csv" -Append -Force -NoTypeInformation


}

else
{
 Write-Host "unable to establish the connection $Device"
}
}

#BrocadeSwitches

function BrocadeSwitches{

param(
    [Parameter(Mandatory=$true)]
    [string]$Device,

    [Parameter(Mandatory=$true)]
    [string]$User,

    [Parameter(Mandatory=$true)]
    [string]$Password
       
  )
Write-Host "###############################################################################"
Write-Host "Device Name:$Device"
Write-Host $User,$Password
[securestring]$secStringPassword = ConvertTo-SecureString $Password -AsPlainText -Force
[pscredential]$cred = New-Object System.Management.Automation.PSCredential ($user, $secStringPassword)
#$cred


  
    $session = New-SSHSession -ComputerName $Device -Credential $cred -ConnectionTimeout 500 -AcceptKey
    if($session){
    Write-Host $session
    
    
     Write-Host "Checking for PSshow"
     Write-Host "########################################"

     $command = "psshow"
     $output = Invoke-SSHCommand -SessionId $session.SessionId -Command $command
     $data= $output.output
     write-Host $data
   
     #$lines = $data -split "`n" | Select-Object -Skip 1
     $result1=@()
     $resultStatus = @()
     foreach ($line in $data) 
     {
       Write-Host $line
     if($line -like '*ok*' -or 'Not supported*')
       { 

         $finalresult1 = "Healthy"
         Write-Host $finalresult1
    
       }
      else
       {
        $finalresult1 = "UnHealthy"
        Write-Output $finalresult1
       }
              $result1 += New-Object psobject -Property @{

              Status = $finalresult1

       }

   }


   
     Write-Host "Checking for fanshow"
     Write-Host "########################################"

     $command = "fanshow"
     $output = Invoke-SSHCommand -SessionId $session.SessionId -Command $command
     $data= $output.output
     Write-Host $data

     #$lines = $data -split "`n" | Select-Object -Skip 1
     $result2=@()
     $resultStatus = @()
    foreach ($line in $data) 
    {

        if($line -like '*ok*' -or 'Not supported*')
       { 
         $finalresult2 = "Healthy"
         Write-Host $finalresult2
    
       }
       else
       {
        $finalresult2 = "UnHealthy"
        Write-Host $finalresult2
       }
  
       $result2 += New-Object psobject -Property @{

       Status = $finalresult2

       }

   
   }

   

    
     Write-Host "Checking for tempshow"
      Write-Host "########################################"

     $command = "tempshow"
        $output = Invoke-SSHCommand -SessionId $session.SessionId -Command $command
       $data= $output.output

       $lines = $data -split "`n" 
       $result3=@()
       $resultStatus = @()
  foreach ($line in $lines) 
  {

    $columns = $line -split "\s+"
    #$status = $columns[2]

  if($columns -notlike "Not Ok"){
    #if($status -eq 'ok') 
    $finalresult3 = "Healthy"
    Write-Output $finalresult3

   }else{
    $finalresult3 = "UnHealthy"
    Write-Output $finalresult3
    }
   $result3 += New-Object psobject -Property @{

   Status = $finalresult3

   }

   
}



 Write-Host "Checking for sensorshow"
  Write-Host "########################################"

    $command = "sensorshow"
    $output = Invoke-SSHCommand -SessionId $session.SessionId -Command $command
   $data= $output.output

   $lines = $data -split "`n" 
   $result4=@()
   $resultStatus = @()
  foreach ($line in $lines) 
  {

     if($line -like '*ok*' -or $line -like '*Absent*')
   { 
     $finalresult4 = "Healthy"
     Write-Output $finalresult4
    
   }
   else
   {
    $finalresult4 = "UnHealthy"
    Write-Output $finalresult4
   }
  
   $result4 += New-Object psobject -Property @{

   Status = $finalresult4

   }

   
}



 Write-Host "Checking for Switchshow"
 Write-Host "########################################"

    $command = "switchshow"
    $output = Invoke-SSHCommand -SessionId $session.SessionId -Command $command
   $data= $output.output

   $lines = $data -split "`n" 
   $result5=@()
   $resultStatus = @()
    # Process each line to find switch state
    #$line='switchState:	Online   '
foreach ($line in $data) {
    if ($line -like "switchState:*") {
        $switchState = ($line -split ":")[1].Trim()
         $finalresult5 = New-Object psobject -Property @{
         Status = $switchState
   }

    }
}

# Determine the status and display the result
if ($finalresult5.Status -eq "Online") {
    $result5='Healthy'
    Write-Host  $result5
    $Remarks='NA'
   Write-Host $Remarks
} else {
    $result5='UnHealthy'
  Write-Host  $result5
  $Remarks=$finalresult5.Status
   Write-Host $Remarks
 
}
 Remove-SSHSession -SessionId $session.SessionId

   if ($null -eq $session.Connected) {
                    Write-Host "Hence $Device removed the SSH connection"
                } else {
                    Write-Host "Unable to remove the SSH session for this $Device"
                }

    sleep 20

 if($result1.Status  -eq 'Healthy' -and $result2.Status -eq 'Healthy' -and $result3.Status -like 'Healthy' -and $result4.Status -eq 'Healthy' -and $result5 -eq 'Healthy' )
   {
    $finalresult='Healthy'
   }
   else
   {
    $finalresult='UnHealthy'
    $Remarks
   }

 }  
   else
   {
    Write-Host "unable to establish the connection $Device"
    $finalresult = "Connection Failed"

   }

   $Result  += New-Object psobject -Property @{
  Technology = "BROCADE DEVICES"
  DeviceName = $Device
  Status = $finalresult
  Remarks=$Remarks
  }

$Result | Select-Object Technology,DeviceName,Status,Remarks | Export-Csv -Path "C:\Storage_Healthcheck_dashboard\Logs\$path\Status.csv" -Append -Force -NoTypeInformation


}

# DellEMCIsilonDevices
function DellEMCIsilonDevices {
        param(
            [Parameter(Mandatory = $true)]
            [string]$Device,

            [Parameter(Mandatory = $true)]
            [string]$User,

            [Parameter(Mandatory = $true)]
            [string]$Password

            
        )

        Write-Host $Device

        $pythonScriptPath = & python.exe "C:\Storage_Healthcheck_dashboard\isolon.py"  $Device $User $Password 
        Write-Output $pythonScriptPath 
        
        
        }

# DellEMC Unity Storage Devices
function DellEMCDevices {
        param(
            [Parameter(Mandatory = $true)]
            [string]$Device,

            [Parameter(Mandatory = $true)]
            [string]$User,

            [Parameter(Mandatory = $true)]
            [string]$Password

            
        )
        
        $Device = $Device.trim()
        $User = $User.trim()
        $Password = $Password.trim()

Write-Host "###############################################################################"
Write-Host "Device Name:$Device"

$AllHost_details = & "C:\Program Files (x86)\Dell EMC\Unity\Unisphere CLI\uemcli.exe" -d $Device -u $User -p $Password  -sslPolicy accept /sys/general show -detail

$AllHost_details

$attribute = "Health state "
$results1 = $AllHost_details | Select-String -Pattern "$attribute\s+=\s+(.+)"

$Result =@()

if($results1){

$lineString = $results1.ToString()
$HealthStatus = $lineString.Split('=')[1].Trim()
 
}
else{

Write-Host "Hence the HealthStatus not found."
$HealthStatus = "NA"

}
if($HealthStatus -like 'ok*')
{
 
 $Status='Healthy'
 Write-Host  $Status
 $Remarks='NA'
 Write-Host $Remarks
 }
 else
 {
  $Status='UnHealthy'
  Write-Host  $Status
  $Remarks=$HealthStatus
   Write-Host $Remarks
 }

$Result  += New-Object psobject -Property @{
  Technology = "DELL _ EMC UNITY DEVICES"
  DeviceName = $Device
  Status = $Status
  Remarks=$Remarks


  }

$Result | Select-Object Technology,DeviceName,Status,Remarks | Export-Csv -Path "C:\Storage_Healthcheck_dashboard\Logs\$path\Status.csv" -Append -Force -NoTypeInformation

   }
if($DeviceType -eq "DellEMC Devices"){
        Write-Host "DellEMC Devices"
        DellEMCDevices -Device $DeviceName  -User $UserName -Password $userPassword 
}


elseif ($DeviceType -eq "Pure Storage Devices") {
        Write-Host "Pure Storage Devices"
        PureStorageDevices -Device $DeviceName  -User $UserName -Password $userPassword 

 }
elseif ($DeviceType -eq "Brocade Switches") {
        Write-Host "Brocade Switches"
        BrocadeSwitches -Device $DeviceName  -User $UserName -Password $userPassword 
        Write-host $UserName,$userPassword
    }
    

elseif($DeviceType -eq "Isiolon Devices"){
       Write-Host "DellEMC Isilon Devices"
       $IsiolonResult = DellEMCIsilonDevices -Device $DeviceName  -User $UserName -Password $userPassword 
  
   $outputPS = $IsiolonResult | ConvertFrom-Json 

    write-Host $outputPS

    $resultStatus  += New-Object psobject -Property @{
    Technology = "ISIOLON DEVICES"
    DeviceName = $outputps.DeviceName
    Status = $outputps.output_status
    Remarks=$outputps.Remark


  }
  }


 }

     $resultStatus | Select-Object Technology,DeviceName,Status,Remarks | Export-Csv -Path "C:\Storage_Healthcheck_dashboard\Logs\$path\Status.csv" -Append -Force -NoTypeInformation





Stop-Transcript | out-null



 

################Send-Email##########################

try
{


$fullpath = "C:\Storage_Healthcheck_dashboard\Logs"

$path = Get-ChildItem $fullpath | sort CreationTime -desc | select -f 1

$filepath = "C:\Storage_Healthcheck_dashboard\Logs\$path\*.csv"


# Load the CSV file using Import-Csv
$csvData = Import-Csv -Path $filepath

# Convert the CSV data to an HTML table with conditional formatting
$htmlContent = @"
<style>
    table {
        border-collapse: collapse;
        width: 80%;
    }

    th, td {
        border: 2px solid black;
        padding: 6px;
        text-align: center;
    }

    th {
        background-color: #87CEEB;
    }

    .healthy {
        background-color: #2dbd58;
        color: black;
    }

    .unhealthy {
        background-color: #fa645f;
        color: black;
    }
    

</style>
<table>
"@

# Create table headers using the first row of the CSV (assuming it contains headers)
$htmlContent += "<tr>"
$csvData[0].PSObject.Properties | ForEach-Object {
    $htmlContent += "<th>$($_.Name)</th>"
}
$htmlContent += "</tr>"

# Add table rows for each row in the CSV with conditional formatting
$csvData | ForEach-Object {
    $statusValue = $_.'status'
    $statusClass = if ($statusValue -eq 'Healthy') { 'healthy' } else { 'unhealthy' }

    $htmlContent += "<tr>"
    $_.PSObject.Properties | ForEach-Object {
        if ($_.Name -eq 'status') {
            $htmlContent += "<td class='$statusClass'>$($_.Value)</td>"
        } else {
            $htmlContent += "<td>$($_.Value)</td>"
        }
    }
    $htmlContent += "</tr>"
}

$htmlContent += "</table>"

    # Replace the following email settings with your SMTP server and recipient details
    $smtpServer = 'mailout.jdadelivers.com'
    $fromEmail = 'StoragehealthCheckDashboard@jdadelivers.com'
    $toEmail = 'CSStorage@blueyonder.com'
    #$toEmail = 'karnatisiva.kavyasree@blueyonder.com'
    $CcEmail = 'karnatisiva.kavyasree@blueyonder.com', 'ashok.damerla@blueyonder.com'
    $subject = 'Storage Device Health Check Report'

    # Custom message to be included in the email body
    $emailBody = "<br>Hi Team,<br><br>Please find the report for the Storage Device health check.<br>"
    # Combine the custom message with the HTML table content
    $emailBody += "<html>$($htmlContent)<html>"
    $emailBody +="<br><br><b>Regards,<br>Automation Team.</b><br><br><b>Note:</b> This is a system generated email please do not reply to this email."


# Send the email with the HTML table in the body
Send-MailMessage -SmtpServer $smtpServer -From $fromEmail -To $toEmail -Cc $CcEmail -Subject $subject  -BodyAsHtml -Body   $emailBody

Write-Host "HTML report generated and email sent successfully."
    }
   catch
     {
$errormessage = $_.Exception.Message
Write-Output $errormessage

     }



