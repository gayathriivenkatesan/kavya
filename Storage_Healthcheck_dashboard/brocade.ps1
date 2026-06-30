$Device = "FR1BCD01-B1"
Write-Host "Brocade sanswitch"
$userPassword = "GGNh83wWVZK&EjGC"
$userName = "ro_api_sanswitch"
[securestring]$secStringPassword = ConvertTo-SecureString $userPassword -AsPlainText -Force
[pscredential]$cred = New-Object System.Management.Automation.PSCredential ($userName, $secStringPassword)
$cred

 $session = New-SSHSession -ComputerName $Device -Credential $cred -ConnectionTimeout 120 -AcceptKey

 $commands =@("psshow","fanshow","tempshow","sensorshow","switchshow")
  #$command ="switchshow"

 foreach($command in $commands)
 {

$output = Invoke-SSHCommand -SessionId $session.SessionId -Command $command
    $data= $output.output
    $data
}

    

