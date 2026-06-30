#$Device ='SL1BRSW01'
$Device='KCBRXSW04'
#$Device = 'SL1BRXSW01'
Write-Host "###############################################################################"
Write-Host "Device Name:$Device"
$User = 'ro_api_sanswitch'
$Password='GGNh83wWVZK&EjGC'
[securestring]$secStringPassword = ConvertTo-SecureString $Password -AsPlainText -Force
[pscredential]$cred = New-Object System.Management.Automation.PSCredential ($user, $secStringPassword)
#$cred


  
    $session = New-SSHSession -ComputerName $Device -Credential $cred -ConnectionTimeout 500 -AcceptKey
    if($session){
    <#Write-Host $session
    
    
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

   
   }#>

   

     Write-Host "Checking for tempshow"
      Write-Host "########################################"

     $command = "tempshow"
        $output = Invoke-SSHCommand -SessionId $session.SessionId -Command $command
       $data= $output.output

       $lines = $data -split "`n" | Select-Object -Skip 3
       $result3=@()
       $resultStatus = @()
  foreach ($line in $lines) 
  {

    $columns = $line -split "\s+"
    $status = $columns[2]

    if($status -eq 'ok') {
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


<#

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

     if($line -like '*ok*' )
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
   }#>

 }  