<?php
ini_set('display_errors', 0);
error_reporting(~E_ALL | ~E_WARNING | ~E_NOTICE);
session_start();
?>
<?php
if(isset($_POST['file1']))
{ 
?>
<?php
$filename = $_POST['file1'];
$username = $_POST['file2'];
$password=$_POST['file3'];
$sfcase = $_POST['file4'];
#echo $sfcase;
$target_dir = "C:\\xampp\\htdocs\\server_decomm\\DNS\\"; 
$target_file = $target_dir.basename($_FILES["file"]["name"]); 
$target_file = "c:\\xampp\\htdocs\\server_decomm\\DNS\\decomminp_DNS.csv";
if (file_exists($target_file))unlink($target_file); { 
	move_uploaded_file($_FILES["file"]["tmp_name"],$target_file);
	$target_files="c:\\xampp\\htdocs\\server_decomm\\DNS\\decomminp_DNS.csv";
	$psScriptPath1 = "c:\\xampp\\htdocs\\server_decomm\\DNS\\DNS_deletion.ps1";
	$s1="powershell.exe -command $psScriptPath1 -filepath '".$target_files."' -destinationfile '".$filename."' -password '".$password."' -username '".$username."' -sfcase '".$sfcase."' -Verb RunAs";
	#echo $s1;
	$query1 = shell_exec($s1);
	#echo $query1;
	echo "<script>alert('Task scheduled successfully download the report from  Overall Page');window.location.href='dash2.php'</script>";
	#$filenames="C:\\xampp\\htdocs\\server_decomm\\decomm_logs\\$sfcase\\$filename";
} 
?>
<?php }
#else{
# echo "<meta http-equiv=\"refresh\" content=\"0; url=dash2.php\">";
#}
?>
<?php
if(isset($_POST['file6'])){
	$sfcase = $_POST['file6'];
	$filename = $_POST['file7'];
	#echo "Executing....";
	#exit;
	$dbhost = 'localhost';
	$dbuser = 'root';
	$dbpass = '';	
	$db = 'server_decomm';
    $dbconn = mysqli_connect($dbhost,$dbuser,$dbpass,$db);
	$query2= ("SELECT * FROM `dns_tracker` ORDER by sno DESC LIMIT 1");
	#$query2= ("SELECT * FROM dns_tracker WHERE sno=max(sno)");
	$filenames=json_encode($filename);
	$link="http:\\localhost:80\server_decomm\decomm_logs\\$sfcase\\$filename";
	#echo $link;
	$res=mysqli_query($dbconn,$query2);
	$row = $res->fetch_assoc();
	$row1=json_encode($row);
	$row1=implode("",$row);
	echo $row1;
	if (strpos($row1,'Started')!==false){
		echo  $row['count'] ."Servers execution completed";
	}
	else {
		#echo "completed";
		echo $link;
	}
}
?>




