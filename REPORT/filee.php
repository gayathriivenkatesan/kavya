<?php
if(isset($_REQUEST["a"]))
{ 
?>
<html>
<head>
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
   <script type="text/javascript" charset="utf8" src="http://ajax.aspnetcdn.com/ajax/jQuery/jquery-1.7.1.min.js"></script>
   <script type="text/javascript" charset="utf8" src="http://ajax.aspnetcdn.com/ajax/jquery.dataTables/1.9.0/jquery.dataTables.min.js"></script>
</head>
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
tr,td{
	background-color:white;
}
</style>
<script>
$(document).ready(function(){
	$('#example1').DataTable();
});
</script>	
</head>
<?php
ini_set('display_errors', 0);
error_reporting(~E_ALL | ~E_WARNING | ~E_NOTICE);
session_start();
?>
<?php
$a= $_REQUEST["a"];
$target_dir = "C:/xampp/htdocs/server_decomm/decomm_logs/$a/"; 
$files1=scandir($target_dir);
 ?>
<body>	 
<center><h4> REPORTS OF SFCASE : <?php echo $a;?></h4></center>
		  <table id="example1" class= "table table-light table-sm" width="90%">
		    <thead>
			  <tr>
				<th>SFcase</th>
				<th>Files</th>
				<th>Download</th>
			</tr>
          </thead>
		  <tbody>
		  <?php
			foreach($files1 as $values){
								if($values != '.'){
					if($values != '..'){
				if($values){
					#$indi = explode(";", $values);
				   ?>
				   <tr>
				   <td><?php echo $a;?></td>				   
				   <td><?php print_r($values); ?></td>
				   <td><a href="http:\\localhost:80\server_decomm\decomm_logs\<?php echo $a; ?>\<?php print_r($values);?>" download>download</a></td>
				   </tr>
			
			<?php }}}} ?>	 			   
		 </tbody>
		 
     </table>
	 <br>
	 <br>
	 <hr>
	 <br>
</body>
</html>
 <?php }
else{
 echo "<meta http-equiv=\"refresh\" content=\"0; url=dash10.php\">";
}
?>


