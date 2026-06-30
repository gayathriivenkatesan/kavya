Param([string]$filepath,[string]$destinationfile,[string]$username,[string]$sfcase)
$servers=get-content $filepath 
$path="\\vincromi0019\C$\Decommissioning\GLPI"
#$server_list=Import-Csv "$path\glpi_serverlist.csv"
$server_list=Import-Csv "c:\xampp\htdocs\server_decomm\glpi_serverlist.csv"

$overall=@()
$notfound=@()
foreach($server in $servers)
{
    $found=$server_list|Where-Object {$_.server_name -like "$server*"}|select server_name,status,SFDecomCase
    if($found)
    {$overall+=$found}
    else
    {$notfound+=$server}
}
$overall|Export-Csv $destinationfile -NoTypeInformation
if($notfound)
{
    foreach($nf in $notfound)
    {
    Add-Content -Path $destinationfile -Value "$nf,Not Found"
    }
}