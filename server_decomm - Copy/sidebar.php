            <ul id="menu-content" class="menu-content collapse out">
                <li>
			      <center>
			      <!--center><span class="glyphicon glyphicon-user"></span></center-->
				  <img src="http:\\localhost:80\server_decomm\avatar.png" width="100" height="80" alt="avatar.png" name="hello">
				  <?php echo '<div>'.$_SESSION["username"].'</div>';?>
				  </center>
                </li>

                <li  data-toggle="collapse" data-target="#products" class="collapsed active">
                  <a href="http://localhost/server_decom/pages/dash1.php">AD USERS AND COMPUTER DELETION</a>
                </li>
                


                <li data-toggle="collapse" data-target="#service" class="collapsed">
                  <a href="http://localhost/server_decom/pages/dash2.php"> DNS DELETION </a>
                </li>  
                


                <li data-toggle="collapse" data-target="#new" class="collapsed">
                  <a href="C:/xampp/htdocs/server_decomm/SPO/dash3.php">SERVER POWEROFF</a>
                </li>
                

                 <li data-toggle="collapse" data-target="#new" class="collapsed">
                  <a href="C:/xampp/htdocs/server_decomm/VM_DEL/dash4.php">VM DELETION</a>
                  </li>

                 <li data-toggle="collapse" data-target="#new" class="collapsed">
                  <a href="C:/xampp/htdocs/server_decomm/IPAM/dash5.php">IP RECLAIM</a>
                </li>
				<li data-toggle="collapse" data-target="#new" class="collapsed">
                  <a href="C:/xampp/htdocs/server_decomm/ZM/dash6.php">ZABBIX MONITOR</a>
                </li>
			    <li data-toggle="collapse" data-target="#new" class="collapsed">
                  <a href="C:/xampp/htdocs/server_decomm/AD_SER/dash7.php">AD SERVICE ACCOUNT DELETION</a>
                </li>
				<li data-toggle="collapse" data-target="#new" class="collapsed">
                  <a href="C:/xampp/htdocs/server_decomm/bigfix_server_decomm/dash11.php">BIGFIX SERVER DECOMMISSION</a>
                </li>
            </ul>
