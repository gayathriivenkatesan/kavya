Param([string]$oldpassword,[string]$newpassword)
#$oldpassword="Welcome@2k22"
#$newpassword="Jesusgod@9876"
$usernames="Decom_Task"
$CurrentDomain = "LDAP://" + ([ADSI]"").distinguishedName
$domain = New-Object System.DirectoryServices.DirectoryEntry($CurrentDomain,$UserNames,$oldPassword)
if ($domain.name -eq $null)
	{
	write-host "Failed - please verify your old password!"
	exit #terminate the script.
	}
else
{
	$s=Set-ADAccountPassword -Identity $usernames -OldPassword (ConvertTo-SecureString -AsPlainText $oldpassword -Force) -NewPassword (ConvertTo-SecureString -AsPlainText $newpassword -Force)	
	if($s){
		$s3=aduser -Identity $usernames -Properties passwordlastset
		$s1=($s3.passwordlastset).AddHours(24)
		$s2=get-date 
		if($s2 -lt $s1){
		Write-host "Failed - Try reset password after $s1"
		write-host "$_"
	}
	else{
		$domain = New-Object System.DirectoryServices.DirectoryEntry($CurrentDomain,$UserNames,$newPassword)
		if ($domain.name -eq $null)
		{
		write-host "Failed - Unable to  reset password"
		exit #terminate the script.
		}
		else{
			write-host "Reset Successfully"
		}
	}
}