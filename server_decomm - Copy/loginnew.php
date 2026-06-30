<!--https://codepen.io/ranjitha-duraisamy/details/YzwjKmQ-->
<?php
session_start();
?>
<!DOCTYPE html>
<html>
<head>
    <title>Server_Decomm Dashboard</title>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
    <link rel="stylesheet" type="text/css" href="./styles.css">
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
    height: 400px;
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
    width: 100px;
    height: 100px;
    position: absolute;
    left: calc(50% - 50px);
    border-radius: 50%;
    top: -50px;
}

.login-container h1{
    text-align: center;
    font-size: 20px;
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
	background:#428BCA;
    /*background-image: linear-gradient(to right,#F26FC9, #8772EF);*/
    color: #ffff;
    
}
.login-container input[type="submit"]:hover{
    cursor: pointer;
    box-shadow: 1px 1px 10px #696969;
}
a{
    display: block;
    text-align: right;
    text-decoration: none;
    color: #fff;
    font-size: 12px;
    margin-top: 10px;
}

a:hover{
    color: #d3d3d3;
    
}


</style>
</head>
<body>
<nav class="navbar navbar-default" style="background:#428BCA;">
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
	 </div-->
	 <div class="container-fluid">
	
<a class="navbar-brand" href="loginsa.php"><p style="color:white;"><b>SERVER DECOMMISSION DASHBOARD</b></p></a>
    </div>
	<!--/div-->
 
</nav>

<div> 
	<div class="row">
		<div class="col-md-3"><img src="blue_yonder_logo_0.jpg" style="width:300px;"></div>
	</div>
	   <div class="login-container">
       <form action="" method="POST">
           <h1>LOGIN</h1>
           <div>
               <label>Username</label>
               <input type="text" name="username" placeholder="Enter your username here" value="" required>
           </div>
           <div>
               <label>Password</label>
               <input type="password" name="password" placeholder="Enter your password here" value="" required>
           </div>
           <input type="submit" name="submit" value="LOGIN">
       </form>
	   </div>
</div>
 <?php
if(isset($_POST['submit'])){
	$username=$_POST['username'];
	$password=$_POST['password'];
	$_SESSION["username"] = $username;
	$_SESSION["password"] = $password;
	$psScriptPath1 = "D:\\xampp\\htdocs\\server_decomm\\newproj\\Ldap_authentication1.ps1";
	$s="powershell.exe -command $psScriptPath1 -username $username -password $password -Verb RunAs";
	#powershell.exe -command D:\xampp\htdocs\server_decomm\newproj\Ldap_authentication1.ps1 -username "jdadelivers\1029311" -password "" -verb RunAs
	$query1 = shell_exec($s);
	$_SESSION["validate"]=$query1;
	if (strpos($query1, 'Authentication')!==false) {
	echo '<br><br><br><br><br><BR><BR><br><br><br><br><br><br><br><br><center style="color:black;"><b><h5>"'.$query.'"</h5></b></center>';
	}
	else{
		header("Location:AD/dash1.php");
	}	
}
?>
    
</body>
</html>





