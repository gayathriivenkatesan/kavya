<html>
<head>

<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
<link rel="stylesheet" type="text/css" href="./styles.css">
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
  background-color: #2e353d;
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
<center><h3><b>GLPI DASHBOARD</b></h3></center>
<button style="float: right;"><a  class="btn" href="glpi_serverlist.csv" download> DOWNLOAD REPORT</a></button>
<br>
<br>
<hr/>
<table id="example">
</table>
</body>
<script>
let inputElement = document.getElementById("a"),
    csvs = ["text/csv", "application/vnd.ms-excel"],
    example = null;
    //alert("hi");
	handleFiles();

inputElement.addEventListener("onclick", handleFiles, false);

function handleFiles() {
	let file="glpi_serverlist.csv";
    //let file = "C:\\Decommissioning\\GLPI\\glpi_serverlist.csv";
	alert(file);
    if (window.File && window.FileReader && window.FileList && window.Blob) {
        //if (csvs.indexOf(file.type) === -1) {
        //    alert("Please only upload CSV files.")
        //} else {
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
						alert("hii");
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
        }
    //}
}
</script>
</html>