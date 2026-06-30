<?php
if(isset($_REQUEST['s']))
{ 
?>
<?php
ini_set('display_errors', 0);
error_reporting(~E_ALL | ~E_WARNING | ~E_NOTICE);
session_start();
?>
<?php 
	$s =  $_REQUEST['s'];
	$user1 = $_POST['user1'];
	$filename = $_REQUEST['filename'];
	$filenames = $_REQUEST['filenames'];
	$filenames1 = $_REQUEST['filenames1'];
	$sfcase = $_REQUEST['sfcase'];
	$res =$_REQUEST['res'];
	$psScriptPath1 = "C:\\xampp\\htdocs\\server_decomm\\IPAM\\ipam_postcheck.ps1";
	$s2="powershell.exe -command $psScriptPath1 -filename '".$filenames1."' -s '".$s."' -user1 '".$user1."' -sfcase '".$sfcase."' -res '".$res."' -Verb RunAs";
	$query2 = shell_exec($s2);
	ob_end_clean();
    ob_start();
	header("Cache-Control: public");
    header("Content-Description: File Transfer");
    header("Content-Disposition: attachment; filename=$filenames1");
	header("Content-Type: text/html; charset=UTF-8");
    readfile($filenames1);	
?>
<?php }
else{
 echo "<meta http-equiv=\"refresh\" content=\"0; url=fileup5.php\">";
}
?>





