<html>
<body>
<center>
<form action="" method="post">
<h3><b>CHANGE CREDENTIAL  FOR SERVICE ACCOUNT FOR DECOM PORTAL</b></h3>
<p>Enter the new password for service account-Decom_Task</p><input type="text" name="hi" id="hi" required><input type="submit" name="submit">
</form>
</center>
</body>
<?php
if(isset($_POST['submit'])){
	$simple_string=$_POST['hi'];
	$username="Decom_Task";
    $psScriptPath1 = "C:\\xampp\\htdocs\\server_decomm\\Ldap_authentication1.ps1";
	$s="powershell.exe -command $psScriptPath1 -username $username -password $simple_string -Verb RunAs";
	#$query1 = shell_exec($s);
	#$query2 = shell_exec("whoami");
	#echo $query2;
	#echo get_current_user();
	#exit;
	#echo $query1;
	if (strpos($query1, 'Authentication')!==false) {
	echo '<br><br><br><br><br><br><center style="color:red;"><b><h5>"'.$query1.'"</h5></b></center><br>';
	}
	else{
	// Display the original string
	//echo "Original String: " . $simple_string;

	// Store the cipher method
	$ciphering = "AES-128-CTR";

	// Use OpenSSl Encryption method
	$iv_length = openssl_cipher_iv_length($ciphering);
	$options = 0;

	// Non-NULL Initialization Vector for encryption
	$encryption_iv = '1234567891011121';

	// Store the encryption key
	$encryption_key = "serverdecommission";

	// Use openssl_encrypt() function to encrypt the data
	$encryption = openssl_encrypt($simple_string, $ciphering,
	$encryption_key, $options, $encryption_iv);
	// Display the encrypted string
	$dbhost = 'localhost';
	$dbuser = 'root';
	$dbpass = '';	
	$db = 'server_decomm';

	//powershell.exe -command D:\xampp\htdocs\server_decomm\newproj\Ldap_authentication1.ps1 -username "jdadelivers\1029311" -password "" -verb RunAs
	//$query1 = shell_exec($s);
	//$_SESSION["validate"]=$query1;
	$dbconn = mysqli_connect($dbhost,$dbuser,$dbpass,$db);
	$query2= ("UPDATE `logg` SET `decomm`='".$encryption."' WHERE 1");
	//echo $query2;
	$res=mysqli_query($dbconn,$query2);
	//print_r($res);
	#echo $res;
	echo '<br><br><br><br><br><br><center style="color:green;"><b><h5>"Successfully Updated"</h5></b></center><br>';
	//while($row=$res->fetch_assoc()){
	//echo "<tr><td>".$row["decomm"]."</td></tr>";
	//}
	}
}
?>
</html>
<?php }
else{
 echo "<meta http-equiv=\"refresh\" content=\"0; url=..\index.php\">";
}
?>