<?php
ini_set('display_errors', 0);
error_reporting(~E_ALL | ~E_WARNING | ~E_NOTICE);
session_start();
?>
<?php
if(isset($_POST["file1"]))
{ 
?>
<?php
$filename = $_POST['file1'];
$res = $_POST['file2'];
$username = $_SESSION["username"];
$sfcase= $_SESSION["sfcase"];
$target_dir = "C:/xampp/htdocs/server_decomm/AD_SER/"; 
$target_file = $target_dir.basename($_FILES["file"]["name"]); 
$target_file = "C:/xampp/htdocs/server_decomm/AD_SER/AD_input.csv";
if (file_exists($target_file))unlink($target_file); { 
	move_uploaded_file($_FILES["file"]["tmp_name"],$target_file);
	$target_files="C:\\xampp\\htdocs\\server_decomm\\AD_SER\\AD_input.csv";
	$psScriptPath1 = "C:\\xampp\\htdocs\\server_decomm\\AD_SER\\serviceaccount_version3.ps1";
	$filenames="C:\\xampp\\htdocs\\server_decomm\\decomm_logs\\$sfcase\\$filename";
	$s1="powershell.exe -command $psScriptPath1 -filepath '".$target_files."' -destinationfile '".$filenames."' -username '".$username."' -res '".$res."' -sfcase '".$sfcase."' -Verb RunAs";
	$query1 = shell_exec($s1);
	#"powershell.exe -command C:\\xampp\\htdocs\\newproj\\AD.ps1 -filepath $target_file -verb RunAs"
	ob_end_clean();
    ob_start();
	header("Cache-Control: public");
    header("Content-Description: File Transfer");
    header("Content-Disposition: attachment; filename=$filenames");
	header("Content-Type: text/html; charset=UTF-8");
    readfile($filenames);
} 
?>

<?php }
else{
 echo "<meta http-equiv=\"refresh\" content=\"0; url=dash7.php\">";
}
?>

