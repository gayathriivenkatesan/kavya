<html>
<head>
<script type="text/javascript" charset="utf8" src="http://ajax.aspnetcdn.com/ajax/jQuery/jquery-1.7.1.min.js"></script>
   <script src="https://cdn.datatables.net/1.10.20/js/jquery.dataTables.min.js"></script>
	<script src="https://cdn.datatables.net/fixedcolumns/3.3.0/js/dataTables.fixedColumns.min.js"></script>
	<script src="https://cdn.datatables.net/1.10.20/css/jquery.dataTables.min.css"></script>
	<script src="https://cdn.datatables.net/fixedcolumns/3.3.0/css/fixedColumns.dataTables.min.css"></script>
	<script src="https://cdn.datatables.net/1.10.20/js/jquery.dataTables.min.js"></script>
   <meta name="viewport" content="width=device-width, initial-scale=1">
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
<script src='https://kit.fontawesome.com/a076d05399.js'></script>
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
<link rel="stylesheet" type="text/css" href="http://ajax.aspnetcdn.com/ajax/jquery.dataTables/1.9.0/css/jquery.dataTables.css">
   <link rel="stylesheet" type="text/css" href="http://ajax.aspnetcdn.com/ajax/jquery.dataTables/1.9.0/css/jquery.dataTables_themeroller.css">
   <script type="text/javascript" charset="utf8" src="http://ajax.aspnetcdn.com/ajax/jquery.dataTables/1.9.0/jquery.dataTables.min.js"></script>
<style>
 input,th{
	  text-align:center;
  }
.nav-side-menu {
  overflow: auto;
  font-family: verdana;
  font-size: 12px;
  font-weight: 200;
  background-color:#2e353d;
  position: fixed;
  top: 0px;
  width: 300px;
  height: 100%;
  color: #e1ffff;
}
.nav-side-menu .brand {
  background-color: #23282e;
  line-height: 50px;
  display: block;
  text-align: center;
  font-size: 14px;
}
.nav-side-menu .toggle-btn {
  display: none;
}
.nav-side-menu ul,
.nav-side-menu li {
  list-style: none;
  padding: 0px;
  margin: 0px;
  line-height: 35px;
  cursor: pointer;
  /*    
    .collapsed{
       .arrow:before{
                 font-family: FontAwesome;
                 content: "\f053";
                 display: inline-block;
                 padding-left:10px;
                 padding-right: 10px;
                 vertical-align: middle;
                 float:right;
            }
     }
*/
}
.nav-side-menu ul :not(collapsed) .arrow:before,
.nav-side-menu li :not(collapsed) .arrow:before {
  font-family: FontAwesome;
  content: "\f078";
  display: inline-block;
  padding-left: 10px;
  padding-right: 10px;
  vertical-align: middle;
  float: right;
}
.nav-side-menu ul .active,
.nav-side-menu li .active {
  border-left: 3px solid #d19b3d;
  background-color: #4f5b69;
}
.nav-side-menu ul .sub-menu li.active,
.nav-side-menu li .sub-menu li.active {
  color: #d19b3d;
}
.nav-side-menu ul .sub-menu li.active a,
.nav-side-menu li .sub-menu li.active a {
  color: #d19b3d;
}
.nav-side-menu ul .sub-menu li,
.nav-side-menu li .sub-menu li {
  background-color: #181c20;
  border: none;
  line-height: 28px;
  border-bottom: 1px solid #23282e;
  margin-left: 0px;
}
.nav-side-menu ul .sub-menu li:hover,
.nav-side-menu li .sub-menu li:hover {
  background-color: #020203;
}
.nav-side-menu ul .sub-menu li:before,
.nav-side-menu li .sub-menu li:before {
  font-family: FontAwesome;
  content: "\f105";
  display: inline-block;
  padding-left: 10px;
  padding-right: 10px;
  vertical-align: middle;
}
.nav-side-menu li {
  padding-left: 0px;
  border-left: 3px solid #2e353d;
  border-bottom: 1px solid #23282e;
}
.nav-side-menu li a {
  text-decoration: none;
  color: #e1ffff;
}
.nav-side-menu li a i {
  padding-left: 10px;
  width: 20px;
  padding-right: 20px;
}
.nav-side-menu li:hover {
  border-left: 3px solid #d19b3d;
  background-color: #4f5b69;
  -webkit-transition: all 1s ease;
  -moz-transition: all 1s ease;
  -o-transition: all 1s ease;
  -ms-transition: all 1s ease;
  transition: all 1s ease;
}
@media (max-width: 767px) {
  .nav-side-menu {
    position: relative;
    width: 100%;
    margin-bottom: 10px;
  }
  .nav-side-menu .toggle-btn {
    display: block;
    cursor: pointer;
    position: absolute;
    right: 10px;
    top: 10px;
    z-index: 10 !important;
    padding: 3px;
    background-color: #ffffff;
    color: #000;
    width: 40px;
    text-align: center;
  }
  .brand {
    text-align: left !important;
    font-size: 22px;
    padding-left: 20px;
    line-height: 50px !important;
  }
}
@media (min-width: 767px) {
  .nav-side-menu .menu-list .menu-content {
    display: block;
  }
}
body {
  margin: 0px;
  padding: 0px;
}
.glyphicon {
    font-size: 50px;
}
img[name="hello"]{
  border-radius: 60%;
}
table.dataTable thead tr {
  background-color: #f5f5f0;
}

input[type=submit]{
  background-color: #4CAF50;
  border: none;
  color: white;
  padding: 10px 5px;
  margin: 4px 2px;
  text-decoration: none;
  text-align:center;
  cursor: pointer;
}
input[name=exit]{
  background-color: #e60000;
  border: none;
  color: white;
  padding: 10px 5px;
  margin: 4px 2px;
  text-decoration: none;
  cursor: pointer;
  text-align:center;
}
</style>

</head>

<?php
ini_set('display_errors', 0);
error_reporting(~E_ALL | ~E_WARNING | ~E_NOTICE);
session_start();
?>
<?php
if (isset($_POST["file1"]))
{ 
?>
<?php
$filename = $_POST["file1"];
$username = $_POST["file2"];
$password = $_SESSION["password"];
$sfcase = $_POST["file3"];
$res=$_POST["file4"];
$target_dir = "C:/xampp/htdocs/server_decomm/IPAM/"; 
$target_file = $target_dir.basename($_FILES["file"]["name"]); 
$target_file = "C:/xampp/htdocs/server_decomm/IPAM/ipreclaim.csv";
if (file_exists($target_file))unlink($target_file); { 
	move_uploaded_file($_FILES["file"]["tmp_name"],$target_file);
	$target_files="C:\\xampp\\htdocs\\server_decomm\\IPAM\\ipreclaim.csv";
	$psScriptPath1 = "C:\\xampp\\htdocs\\server_decomm\\IPAM\\ipam_precheck.ps1";
	$s1="powershell.exe -command $psScriptPath1 -filepath '".$target_files."' -destinationfile '".$filename."'-username1 '".$username."' -password '".$password."' -res '".$res."' -sfcase '".$sfcase."'-Verb RunAs";
	#echo $s1;
	$query1 = shell_exec($s1);
	#echo $query1;
	$iparr = array();
	$iparr = explode("@", $query1);
	$indi = array();
	$filename=$filename;
	#$file= split("\.", $filename);
	#echo $file; 	
	#$file=explode(".",$filename);
	#"powershell.exe -command C:\\xampp\\htdocs\\newproj\\AD.ps1 -filepath $target_file -verb RunAs"

}
?>

<div class="login-container">
	<div class="row">
		<div class="col-md-3">
		<div class="nav-side-menu">
    <!--div class="brand"><center><img src="..\Blue_Yonder_logo_0.jpg" style="height:100px;width:100px"></center></div-->
    <i class="fa fa-bars fa-2x toggle-btn" data-toggle="collapse" data-target="#menu-content"></i>
  
        <div class="menu-list">
  
            <ul id="menu-content" class="menu-content collapse out">
                <li>
				 <center>
			      <!--center><span class="glyphicon glyphicon-user"></span></center-->
				  <img src="..\avatar.png" width="100" height="80" alt="avatar.png" name="hello">
				  <a onclick='change()'><?php echo '<div>'.$_SESSION["username"].'</div>';?></a>
				  <a><?php echo 'SFCase Number: '. $_SESSION["sfcase"];?></a>
				  <a href="../logout.php" id="but" style="display:none";>logout</a>
				  </center>
                </li>

                <li  data-toggle="collapse" data-target="#products" class="collapsed">
                  <a href="../AD/dash1.php">AD USERS AND COMPUTER DELETION</a>
                </li>
                


                <li data-toggle="collapse" data-target="#service" class="collapsed">
                  <a href="../DNS/dash2.php"> DNS DELETION </a>
                </li>  
                
                <li data-toggle="collapse" data-target="#new" class="collapsed">
                  <a href="../SPO/dash3.php">SERVER POWEROFF</a>
                </li>
                

                 <li data-toggle="collapse" data-target="#new" class="collapsed">
                  <a href="../VM_DEL/dash4.php">VM DELETION</a>
                  </li>

                 <li data-toggle="collapse" data-target="#new" class="collapsed">
                  <a href="/IPAM/dash5.php">IP RECLAIM</a>
                </li>
				
				<li data-toggle="collapse" data-target="#new" class="collapsed">
                  <a href="../ZM/dash6.php">ZABBIX MONITOR</a>
                </li>
				
				<li data-toggle="collapse" data-target="#new" class="collapsed">
                  <a href="../ZM/dash6_1.php">ZABBIX URL</a>
                </li>
				
				<li data-toggle="collapse" data-target="#new" class="collapsed">
                  <a href="../ZM/dash6_2.php">ZABBIX HOST DELETION</a>
                </li>
				
				<li data-toggle="collapse" data-target="#new" class="collapsed">
                  <a href="../AD_SER/dash7.php">AD SERVICE ACCOUNT DELETION</a>
                </li>
				
				<li data-toggle="collapse" data-target="#new" class="collapsed">
                  <a href="../GLPI/dash8.php">GLPI</a>
                </li>
				
				<li data-toggle="collapse" data-target="#new" class="collapsed">
                  <a href="../NOTIFICATION/dash9.php">NOTIFICATION</a>
                </li>
			    <li data-toggle="collapse" data-target="#new" class="collapsed">
                  <a href="../REPORT/dash10.php">OVERALL REPORT</a>
                </li>
				<li data-toggle="collapse" data-target="#new" class="collapsed">
                  <a href="../CP/changepass1.php">RESET SERVICE ACCOUNT PASSWORD</a>
                </li>
            </ul>
     </div>
</div>
</div>
<div class="col-md-9">
<center><h3><b>IPRECLAIM</b></h3></center>
<br>
<center>
	<div id="hello"></div>	
	<div id="hello1"><a href="http:\\localhost:80\server_decomm\decomm_logs\<?php echo "$sfcase";?>\post_decomm_logs_<?php echo $filename; ?>" style="display:none"; download>Post Execution Report Download</a></div>
	<br>
	<center><h5><b>PRECHECK IPRECLAIM REPORT</b></h5></center>
	<div id="load" style="display:None"><b>EXECUTING...</b><img src="//s.svgbox.net/loaders.svg?fill=maroon&ic=tail-spin" style="width:50px"></div>
	<div class="table-responsive">			
		  <table id="example" class= "table table-light table-sm">
		    <thead>
			  <tr>
				<th><input type="checkbox" name="select-all" id="select-all" /></th>
				<th>SF Case</th>
				<th>Server Name</th>
				<th>DNSBackward</th>
				<th>Comments</th>
				<th>Alias</th>
				<th>Status</th>
				<th>State</th>
			</tr>
          </thead>
		  <tbody>
		  
		  <?php
			foreach($iparr as $values){
				$indi1 = explode(";", $values);
				if($indi1[1]){
				#if($values){
					$indi = explode(";", $values);
				   ?>
				   <tr>
					<td><input type="checkbox" name='test12' id="check12" class="check1" value='<?php print_r(explode("servername=", $indi[1])[1]);?>' onchange="myFunction()"></td>
				    <td><?php echo $sfcase; ?></td>
					<td><?php print_r(explode("servername=", $indi[1])[1]); ?></td>
					 <td><?php print_r(explode("DnsBackward=", $indi[2])[1]); ?></td>
					 <td><?php print_r(explode("Comments=", $indi[3])[1]); ?></td>
					 <td><?php print_r(explode("alias=", $indi[4])[1]); ?></td>
					  <td><?php print_r(explode("Status=", $indi[5])[1]); ?></td>
					<td><?php print_r(explode("State=",(explode("}", $indi[6])[0]))[1]); ?></td>
				   </tr>
			
			<?php }} ?>	 			   
		 </tbody>		 
     </table>
	 <br>
	<br>
	<div ><center><a href="http:\\localhost:80\server_decomm\decomm_logs\<?php echo "$sfcase";?>\<?php echo "$filename";?>" download>Precheck Report Download</a></center></div>
	<?php 
	$f = array();
	list($a11, $b)=explode('.',$filename); 
	#echo $a11;
	?>
	
	 <br>
	 <br>
<input type="submit" value="Execute" onclick="checking()"> <input type="button" name="exit" onClick="window.location.href='dash5.php';" value=" CANCEL"></center>
</div>
</div>
</div>

<script>
function myFunction(){
	//$('.check1').change(function(event){
	var a;
	var favorite = [];
        $.each($("input[name='test12']:checked"), function(){
        var a=favorite.push($(this).val());
		event.preventDefault();
        });
		//function  myfunction(){
		var a=(favorite.join(", "));
		console.log(a);
		return a;
}
// Function 2
	function checking(){
		//document.getElementById('load').style.display = "block";
	//$('#checking').on('click',function(event){
		var s = myFunction();
		var res='<?php echo $res; ?>';
		var sfcase='<?php echo $sfcase; ?>';
		var user1 ='<?php echo $username; ?>';
		var filename='<?php echo $filename; ?>';
		var filenames="c:\\xampp\\htdocs\\server_decomm\\decomm_logs\\"+sfcase+"\\pre_decomm_logs_"+filename;
		var filenames1="c:\\xampp\\htdocs\\server_decomm\\decomm_logs\\"+sfcase+"\\post_decomm_logs_"+filename;
		$.ajax({
		url:"fileupp.php",
		method:"post",
		data: {
			   s: s,
			   filename :filename,
			   filenames :filenames,
			   filenames1 :filenames1,
			   sfcase :sfcase,
			   user1 :user1,
			   res:res
			   },
		cache:false,
		beforeSend: function(){
		$("#load").show();
		},
		success:function(response,data){
			$("#hello").html(response);
			//$("#hello1").html(response);
			$("a").removeAttr("style");
			//alert(user1);
			//window.location = 'fileupp.php';
			//windows.location ='dash5.php';
		},
		complete: function(){
		$('#load').hide();
		}
		
		});
        console.log("hello world");
	 return false;
	}
	
	$('#select-all').click(function(event) {   
    if(this.checked) {
        // Iterate each checkbox
        $(':checkbox').each(function() {
            this.checked = true;                        
        });
    } else {
        $(':checkbox').each(function() {
            this.checked = false;                       
        });
    }
});
</script>

<script>
$(document).ready(function(){
	$('#example').DataTable();
	//document.getElementById('load').style.display = "None";
	
});
</script>
<script>
function change() {
  document.getElementById('but').style.display = "block"
  //document.getElementById('butother').style.display = "block"
}
</script>

</html>
<?php }
else{
 echo "<meta http-equiv=\"refresh\" content=\"0; url=dash5.php\">";
}
?>