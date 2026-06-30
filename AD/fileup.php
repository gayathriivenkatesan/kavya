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
$username = $_POST['file2'];
$password = $_POST['file3'];
$username = $_SESSION["username"];
$sfcase = $_SESSION["sfcase"];
$target_dir = "C:/xampp/htdocs/server_decomm/AD/"; 
$target_file = $target_dir.basename($_FILES["file"]["name"]); 
$target_file = "C:/xampp/htdocs/server_decomm/AD/AD_input.csv";
if (file_exists($target_file))unlink($target_file); { 
	move_uploaded_file($_FILES["file"]["tmp_name"],$target_file);
	$target_files="C:\\xampp\\htdocs\\server_decomm\\AD\\AD_input.csv";
	$psScriptPath1 = "C:\\xampp\\htdocs\\server_decomm\\AD\\AD_Object_deletion_version2.ps1";
	$s1="powershell.exe -command $psScriptPath1 -filepath '".$target_files."' -destinationfile '".$filename."' -username '".$username."' -password '".$password."' -sfcase '".$sfcase."' -Verb RunAs";
	$query1 = shell_exec($s1);
	#"powershell.exe -command C:\\xampp\\htdocs\\newproj\\AD.ps1 -filepath $target_file -verb RunAs"
	$filenames="C:\\xampp\\htdocs\\server_decomm\\decomm_logs\\$sfcase\\$filename";
	ob_end_clean();
    ob_start();
	header("Cache-Control: public");
    header("Content-Description: File Transfer");
    header("Content-Disposition: attachment; filename=$filenames");
	header("Content-Type: text/html; charset=UTF-8");
	#header("Content-Type: multipart/form-data; boundary=something");
	#header("Content-type:   application/x-msexcel; charset=utf-8");
	#header("Content-type:application/pdf");
    #header("Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet");
    #header("Content-Transfer-Encoding: binary");
    // read the file from disk
    readfile($filenames);
} 
?>
<?php }
else{
 echo "<meta http-equiv=\"refresh\" content=\"0; url=dash1.php\">";
}
?>


