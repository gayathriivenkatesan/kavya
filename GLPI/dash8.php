<!--#https://jsfiddle.net/annoyingmouse/56ao9ow2/-->
<?php
session_start();
?>
<?php
 if (isset($_SESSION["username"]))
{ 
?>
<html>
<head>

<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
<link rel="stylesheet" type="text/css" href="./styles/PapaParse.js">
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
<script type="text/javascript" charset="utf8" src="//cdn.datatables.net/1.10.15/js/jquery.dataTables.js"></script>
<link rel="stylesheet" type="text/css" href="//cdn.datatables.net/1.10.15/css/jquery.dataTables.css">
<script src="https://code.jquery.com/jquery-2.2.4.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/4.2.0/papaparse.min.js"></script>
<script src="https://cdn.datatables.net/1.10.13/css/jquery.dataTables.min.css"></script>
<script src="https://cdn.datatables.net/1.10.13/js/jquery.dataTables.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery.blockUI/2.70/jquery.blockUI.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/alasql/0.3.9/alasql.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.18.1/moment-with-locales.min.js"></script>
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
img {
  border-radius: 60%;
}
table.dataTable thead tr {
  background-color: #f5f5f0;
}

input[name=execute]{
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
<body>
<div class="login-container">
	<div class="row">
		<div class="col-md-3">
		<div class="nav-side-menu">
    <!--div class="brand"><img src="D:\xampp\htdocs\server_decomm\newproj\BlueYonder-logo-4.png"></div-->
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
                  <a href="../IPAM/dash5.php">IP RECLAIM</a>
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
			    <li data-toggle="collapse" data-target="#new"  class="collapsed">
                  <a href="../AD_SER/dash7.php">AD SERVICE ACCOUNT DELETION</a>
                </li>
				<li data-toggle="collapse" data-target="#new" class="collapsed active">
                  <a href="dash8.php">GLPI</a>
                </li>
				<li data-toggle="collapse" data-target="#new" class="collapsed">
                  <a href="../NOTIFICATION/dash9.php">NOTIFICATION</a>
                </li>
				<li data-toggle="collapse" data-target="#new" class="collapsed">
                  <a href="../REPORT/dash10.php">OVERALL REPORT</a>
                </li>
				<li data-toggle="collapse" data-target="#new" class="collapsed">
                  <a href="../bigfix_server_decomm/dash11.php">BIGFIX SERVER DECOMMISSION</a>
                </li>
				<li data-toggle="collapse" data-target="#new" class="collapsed">
                  <a href="../CP/changepass1.php">RESET SERVICE ACCOUNT PASSWORD</a>
                </li>
            </ul>

     </div>
</div>
		</div>
		<div class="col-md-9">
			<center>
			<h3><b>GLPI</b></h3>
			<br>
			<form action="fileup.php" method="post" enctype="multipart/form-data"> 
			<h5> Please upload the input csv file</h5>
			<input type="file" name="file" id="file" required>
			<!--input type="file" id="input" required-->
			<h5>mandate columns servername</h5>
			<br>
			</center>
			<?php
			$date=date('d_m_Y_h_i');
			$file="GLPI_status_log_".$date.".csv";
			$_SESSION["file"]=$file;
			?>
			<input type="hidden" name="file1" value='<?php echo "$file"; ?>'>
			<center><input type="submit" id="submit" name="execute" value="EXECUTE">  <input type="button" name="exit" onClick="window.location.href=window.location.href" value=" CANCEL"></center>
			<hr/>
			</form>
			<center><p>Preview your csv inputs</p></center>
			<table id="example">
			</table>
		</div>
	</div>
</div>

<script>
let inputElement = document.getElementById("file"),
    csvs = ["text/csv", "application/vnd.ms-excel"],
    example = null;
	

inputElement.addEventListener("change", handleFiles, false);

function handleFiles() {
    let file = this.files[0];
	alert("Loading the file");
    if (window.File && window.FileReader && window.FileList && window.Blob) {
        //if (csvs.indexOf(file.type) === -1) {
        //    alert("Please only upload CSV files")
        //} else {
			//document.getElementById('#sub1').style.visibility = 'visible';
        	$.blockUI();
        	let timer = {
            	start: moment()
            };
			$.fn.dataTable.ext.errMode = 'none';
            Papa.parse(file, {
                "download": true,
                "header": true,
                "dynamicTyping": true,
                "complete": results => {
                    if ($.fn.DataTable.isDataTable("#example")) {
                        example.destroy();
                        $('#example').empty();
                    }
                    example = $("#example").DataTable({
                        "responsive": true,
                        "columns": results.meta.fields.map(c => ({
                            "title": c,
                            "data": c,
                            "visible": c.toLowerCase() !== "id",
                            "default": ""

                        })),	
						
				
                        "data": results.data,
                        "drawCallback": function(settings) {
                        	$.unblockUI();
                            timer.end = moment();
                            let duration = moment.duration(timer.end.diff(timer.start));
                            console.log("timer", timer);
                            console.log("duration", duration.asSeconds());
							
							
							
                        }
						

                    });
                }
            });
        //}
    }
}
</script>
<script>
function change() {
  document.getElementById('but').style.display = "block"
  //document.getElementById('butother').style.display = "block"
}
</script>
</body>
</html>
<?php }
else{
 echo "<meta http-equiv=\"refresh\" content=\"0; url=..\index.php\">";
}
?>

 