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