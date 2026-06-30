#$cred = Get-Credential #Read credentials
 #$username = $cred.username
 #$password = $cred.GetNetworkCredential().password
 Param([string]$username,[string]$password)

 # Get current domain using logged-on user's credentials
 $CurrentDomain = "LDAP://" + ([ADSI]"").distinguishedName
 $domain = New-Object System.DirectoryServices.DirectoryEntry($CurrentDomain,$UserName,$Password)

if ($domain.name -eq $null)
{
 write-host "Authentication failed - please verify your username and password!"
 exit #terminate the script.
}
else
{
 write-host "Successfully"
}