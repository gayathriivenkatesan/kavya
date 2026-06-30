<!DOCTYPE html>
<html>
<head>
    <title>Server_Decomm Dashboard</title>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>

<style>
body{
    margin: 0;
    padding: 0;
    background-image: url('assets/background.jpg');
    background-size: cover;
    background-repeat: no-repeat;
    font-family: sans-serif;
}

.login-container{
    width: 370px;
    height: 550px;
    top: 50%;
    left: 50%;
    position: absolute;
    background: #f8f8f8;
    transform: translate(-50%, -50%);
    box-sizing: border-box;
    color: black;
    padding: 40px 20px;
}

.login-container img{
    width:200px;
    height: 150px; 
    border-radius: 30%;
	top: -20px;
	position: absolute;
    left: calc(30% - 50px);
}

.login-container h3{
    text-align: center;
    font-size: 15px;
}

.login-container label{
    display: block;
}

.login-container div{
    margin-bottom: 20px;
}

.login-container input[type="text"], input[type="password"]{
    width: 100%;
    border: none;
    outline: none;
    border-bottom: 1px solid #ffff;
    background: transparent;
    color:black;
    height: 40px;
}

.login-container input[type="submit"]{
    width: 100%;
    border: none;
    outline: none;
    height: 40px;
	background:#aaa9ad;
    /*background-image: linear-gradient(to right,#F26FC9, #8772EF);*/
    color: #ffff;
    
}
.login-container input[type="submit"]:hover{
    cursor: pointer;
    box-shadow: 1px 1px 10px #696969;
}


button[name="hello"]{
	color:#5bc0de;
}
</style>
</head>
<body>

<!--#1fb5ad;-->
  <!--div class="container-fluid">
	<!--div class="navbar-header">
	 <ul class="nav navbar-nav">
		<a class="navbar-brand" href="loginsa.php">
      <div class="logo-image">
            <img src="Blue_yonder_logo_0.jpg" class="img-fluid">
      </div>
	</a>
	</ul>
	.navbar-brand {
  width:600px;
  font-size:20px;

}
.navbar-brand img {
  height: 80px;
  /* put value of image height as your need */
  float: left;
  padding:3px 0 0 0 ;
  margin:0,auto;
  
}


<!--div> 
	<div class="row">
		<div class="col-md-3"><img src="BlueYonder-logo-4.png" style="width:300px;"></div>
	</div>
	</div-->
	   <div><center><p><h3><b>UPDATE PASSWORD FOR SERVICE ACCOUNT</b></h3></p></center></div>
	   <div class="login-container">

       <form action="" method="POST">
	   <img src="BlueYonder-logo-4.png" style="width:250px;">
	   	<br>
           <h3>LOGIN</h3>

           <div>
               <label>Username</label>
               <input type="text" name="username" placeholder="Enter your username here" value="" required>
           </div>
           <div>
               <label>Password</label>
               <input type="password" name="password" placeholder="Enter your password here" value="" required>
           </div>
		   <div>
               <label>Service Account Name</label>
               <input type="text" name="passwordgg" value="Decom_Task" readonly>
           </div>
		    <div>
               <label>Service Account Credential</label>
               <input type="password" name="sfcase" placeholder="Enter service acoount credential" value="" required>
           </div>
           <input type="submit" name="submit" value="LOGIN">
		   <br>
		 
		   <br>
       </form>
	   </div>
 <?php
if(isset($_POST['submit'])){
	$username=$_POST['username'];
	$password=$_POST['password'];
	$password1=$_POST['sfcase'];
	$_SESSION["username"] = $username;
	$_SESSION["password"] = $password;

	#echo $_SESSION["sfcase"];
	$dbhost = 'localhost';
	$dbuser = 'root';
	$dbpass = '';	
	$db = 'server_decomm';
	$psScriptPath1 = "C:\\xampp\\htdocs\\server_decomm\\Ldap_authentication1.ps1";
	$s="powershell.exe -command $psScriptPath1 -username $username -password $password -Verb RunAs";
	#powershell.exe -command D:\xampp\htdocs\server_decomm\newproj\Ldap_authentication1.ps1 -username "jdadelivers\1029311" -password "" -verb RunAs
	$query1 = shell_exec($s);
	#echo $query1;
	if(strpos($query1, 'Authentication')!==false) {
		echo '<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><center style="color:black;"><b><h5>"'.$query1.'"</h5></b></center><br>';
	}
	else{
	$usernames='jdadelivers\Decom_Task';
	$_SESSION["sfcase"] = $password1;
	$s1="powershell.exe -command $psScriptPath1 -username $usernames -password $password1 -Verb RunAs";
	echo $s1;
	#FlAsH@330093939
	$query2 = shell_exec($s1);
	echo $query2;
	if(strpos($query2, 'Authentication')!==false){
		echo '<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><center style="color:black;"><b><h5>"Authentication Failed for service account"</h5></b></center><br>';
	}
	else{	
	$ciphering = "AES-128-CTR";

	// Use OpenSSl Encryption method
	$iv_length = openssl_cipher_iv_length($ciphering);
	$options = 0;

	// Non-NULL Initialization Vector for encryption
	$encryption_iv = '1234567891011121';

	// Store the encryption key
	$encryption_key = "serverdecommission";

	// Use openssl_encrypt() function to encrypt the data
	$encryption = openssl_encrypt($password1, $ciphering,$encryption_key, $options, $encryption_iv);
	// Display the encrypted string
	$dbhost = 'localhost';
	$dbuser = 'root';
	$dbpass = '';	
	$db = 'server_decomm';
	$dbconn = mysqli_connect($dbhost,$dbuser,$dbpass,$db);
	$query2= ("UPDATE `logg` SET `decomm`='".$encryption."',username='".$username."' WHERE 1");
	$res=mysqli_query($dbconn,$query2);
	#echo $res;
	$path1="c:\\xampp\\htdocs\\server_decomm\\mailsend.ps1";
	$query8="powershell.exe -command $path1 -username $username -verb RunAs";
	$query3= shell_exec($query8);
	echo $query3;
	}
	}
}
?>


</body>
</html>





