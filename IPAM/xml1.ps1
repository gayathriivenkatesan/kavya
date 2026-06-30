
#C:\Users\1033828\Downloads\template1.csv
#$file = Import-Csv -Path "C:\Users\1033828\Downloads\template1.csv"
$file=Import-Csv -Path "C:\xampp\htdocs\server_decomm\IPAM\template1.csv"
$folder_name1=$file.'foldername'
$folder_name=$folder_name1[0]
$app1=$file.'Application'
$app=$app1[0]
$sub_app1=$file.'Sub Application'
$sub_app=$sub_app1[0]
$created_by1=$file.'Created by'
$created_by=$created_by1[0]
$prefix1=$file.prefix_name
$prefix=$prefix1[0]
$timezone1=$file.'Time zone'
$timezone=$timezone1[0]
$solution1=$file.'Solution queue'
$solution=$solution1[0]
$cust_name1=$file.'Customer name'
$cust_name=$cust_name1[0]
$env_name1=$file.'Environment name'
$env_name=$env_name1[0]
$shout_dest1=$file.'Shout destination'
$shout_dest=$shout_dest1[0]
$alert1=$file.'Alert window'
$alert=$alert1[0]
$var1=$file.'Variable'
$var=$var1[0]
$ser_timezone1=$file.'Server timezone'
$ser_timezone=$ser_timezone1[0]
$sub_prod1=$file.'Sub_Product'
$sub_prod=$sub_prod1[0]

#C:\Users\1033828\Downloads\template1.xlsx
$a='<DEFTABLE xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="Folder.xsd">
<FOLDER DATACENTER="veus2core0620" VERSION="919" PLATFORM="UNIX" FOLDER_NAME="'+$folder_name+'" MODIFIED="False" LAST_UPLOAD="20220915071102UTC" FOLDER_ORDER_METHOD="UD4USESTAM" REAL_FOLDER_ID="280" TYPE="1" USED_BY_CODE="0">'
$a
$job_dep=$null
$time=$null
$job_dep1=$null
$file=$file
$outjob=@()


foreach ($item in $file)
{
$item.'Job Parameter'
 ###############################parameter#######################
 $meter=$null
 if($item.'Job Parameter' -ne ""){
 $param=$item.'Job Parameter'.split(",") 
 $param
 $i=1
 $meter=$null
 $meter=@()
 foreach($dat in $param){
 $condition='<VARIABLE NAME="%%PARM'+$i+'" VALUE="'+$dat+'"/>'
 $i++
 $meter+=$condition 

 }
 }
 
 ##############################################################

 <#
############################################INCOND
if($item.'Job Dependency' -ne ""){
$job_dep='<INCOND NAME="DXL_DMS_TEST_WEEKLY_dms_prepare_stg_wk-TO-dms_checkdd_running" ODATE="ODAT" AND_OR="A"/>'
#$job_dep="'"+$job_dep+"'"
}
################################################



########################################OUTCOND
if($item.'Job Dependency' -ne ""){
$job_dep1='<OUTCOND NAME="DXL_DMS_TEST_WEEKLY_dms_prepare_stg_wk-TO-dms_checkdd_running" ODATE="ODAT" SIGN="-"/>'
#$job_dep1="'"+$job_dep1+"'"

}
$time="TIMEFROM ="+"`"$timefrom`""
###########################################


$set="`"Hi,00000090Job execution Failed on the Server %%NODEID running from Control-M,Please Check in to it.00000021Application: %%APPLIC0028Sub Application: %%APPLGROUP0019Job Name: %%JOBNAME0021Server Name: %%NODEID0022Script Name: %%MEMNAME0021Script Path: 
   %%MEMLIB0075Failure Time: %%DATE : %%TIME (in YYMMDD : HHMMSS format and timezone: UTC)00000096**While replying please remove the email ID csms@blueyonder.com if it is part of 
   recipient list.00000008Regards,0033BlueYonder Customer Success Team`""

$msg="`"0004$set`"" 
#>


#job dependency to job name

################################incond &&& outcond########################
$index1=$item.'JOB NAME'
$dep=$null
if($item.'JOB NAME' -ne "" -and $item.'Job Dependency' -ne ""){
$depend=$item.'Job Dependency'.Split(",") 
$dep=@()
foreach($depen in $depend){
$job_dep='<INCOND NAME="'+$prefix+'_'+$depen+'-TO-'+$index1+'" ODATE="ODAT" AND_OR="A"/>'
$dep+=$job_dep
}
}

$dep1=$null
if($item.'JOB NAME' -ne "" -and $item.'Job Dependency' -ne ""){
$depend1=$item.'Job Dependency'.Split(",") 
$dep1=@()
foreach($depen1 in $depend1){
$job_dep1='<OUTCOND NAME="'+$prefix+'_'+$depen1+'-TO-'+$index1+'" ODATE="ODAT" SIGN="-"/>'
$dep1+=$job_dep1
}
}

#################################################################################

#######################JOB Dependency###################
$jb_name=$item.'JOB NAME'
#$dep_jobs=$file | ?{$_.job_dependency -eq $jb_name}
$dep_jobs1=$file | ?{$_.'Job Dependency' -match $jb_name}
$dep_jobs1
#$dep_jobs1=$dep_jobs.Split(",")
#$dep_jobs
$full=@()
foreach($join2 in $dep_jobs1){
$depjob=$join2.'JOB NAME'
$outcond='<OUTCOND NAME="'+$prefix+'_'+$jb_name+'-TO-'+$depjob+'" ODATE="ODAT" SIGN="+"/>'

$full+=$outcond
}

##########################################################



############################################# TIMEFROM
$time=$null
$timefrom=$item.'Execution_time'
if($item.'Execution_time' -ne ""){
 
 $time="TIMEFROM ="+"`"$timefrom`""

}
else{

Write-Host "no time"
}
########################################################


 $scriptname=$item.'Script Name'
 $scriptname
 $jobname=$item.'JOB NAME'
 $dec=$item.'JOB DESCRIPTION'
 $servername=$item.'Server Name'
 $scriptpath=$item.'Script path'
 $maxrun=$item.'Max Run Alarm'
 $data='</JOB>'


 ############33333
 ########################

 $text1='<JOB JOBISN="10" APPLICATION="'+$app+'" SUB_APPLICATION="'+$sub_app+'" MEMNAME="'+$scriptname+'" JOBNAME="'+$jobname+'" DESCRIPTION="'+$dec+'" 
CREATED_BY="'+$created_by+'" RUN_AS="SVC_DXLNPCONNMULE" CRITICAL="0" TASKTYPE="Job" CYCLIC="0" NODEID="'+$servername+'" INTERVAL="00001M" MEMLIB="'+$scriptpath+'"
CONFIRM="0" RETRO="0" MAXWAIT="1" MAXRERUN="0" AUTOARCH="0" MAXDAYS="0" MAXRUNS="0" '+$time+' WEEKDAYS="0" JAN="1" FEB="1" MAR="1" APR="1" MAY="1" JUN="1" JUL="1" AUG="1" 
SEP="1" OCT="1" NOV="1" DEC="1" DAYS_AND_OR="O" SHIFT="Ignore Job" SHIFTNUM="+00" SYSDB="0" IND_CYCLIC="S" CREATION_USER="'+$created_by+'" CREATION_DATE="20220629" CREATION_TIME="095938"
CHANGE_USERID="1027136" CHANGE_DATE="20220810" CHANGE_TIME="090200" RULE_BASED_CALENDAR_RELATIONSHIP="O" TIMEZONE="'+$timezone+'" APPL_TYPE="OS" MULTY_AGENT="N" USE_INSTREAM_JCL="N"
VERSION_OPCODE="N" IS_CURRENT_VERSION="Y" VERSION_SERIAL="2" VERSION_HOST="veus2core0622" CYCLIC_TOLERANCE="0" CYCLIC_TYPE="C" PARENT_FOLDER="'+$folder_name+'">' +$meter+
'<SHOUT WHEN="EXECTIME" TIME="+003" URGENCY="R" DEST="'+$alert+'" MESSAGE="'+$solution+'-LONG_'+$cust_name+'_'+$sub_prod+'_'+$env_name+'_%%JOBNAME is running long more than 3 minutes of Average run time. Please check on priority."/>
<SHOUT WHEN="EXECTIME" TIME=">'+$maxrun+'" URGENCY="R" DEST="'+$shout_dest+'" MESSAGE="'+$solution+'-LONG_'+$cust_name+'_'+$sub_prod+'_'+$env_name+'_%%JOBNAME is running long on %%NODEID. Please check on priority."/>
<SHOUT WHEN="EXECTIME" TIME=">'+$maxrun+'" URGENCY="R" DEST="'+$alert+'" MESSAGE="'+$solution+'-LONG_'+$cust_name+'_'+$sub_prod+'_'+$env_name+'_%%JOBNAME is running long on %%NODEID. Please check on priority."/>' +$dep+ '<QUANTITATIVE NAME="BL_PATCH_'+$solution+'_'+$cust_name+'" QUANT="1" ONFAIL="R" ONOK="R"/>' +$dep1+' 
' +$full+ '<ON STMT="*" CODE="NOTOK">
   <DOMAIL URGENCY="U" DEST="%%'+$var+'" SUBJECT="'+$solution+'-FAIL_'+$cust_name+'_'+$sub_prod+'_'+$env_name+'_%%JOBNAME Failed." MESSAGE="0003Hi,00000090Job execution Failed on the Server %%NODEID running from Control-M, Please Check in to it.00000021Application: %%APPLIC0028Sub Application: %%APPLGROUP0019Job Name: %%JOBNAME0021Server Name: %%NODEID0022Script Name: %%MEMNAME0021Script Path: %%MEMLIB0075Failure Time: %%DATE : %%TIME (in YYMMDD : HHMMSS format and timezone: '+$ser_timezone+')00000096**While replying please remove the email ID csms@blueyonder.com if it is part of recipient list.00000008Regards,0032BlueYonder Customer Success Team" ATTACH_SYSOUT="Y"/>
 </ON>'   
 
  write-host "HI"
  $outjob+=$text1+$data
  #$data|Out-File "C:\Lavanya\convert.xml"
    
}


$end='</FOLDER>
    </DEFTABLE>'

$final_output=$a+$outjob+$end

$final_output| out-file -FilePath "C:\xampp\htdocs\server_decomm\IPAM\Control-M.xml"
#

<#
"0003Hi,00000090Job execution Failed on the Server %%NODEID running from Control-M, Please Check in to it.00000021Application: %%APPLIC0028Sub Application: %%APPLGROUP0019Job Name: %%JOBNAME0021Server Name: %%NODEID0022Script Name: %%MEMNAME0021Script Path: %%MEMLIB0075Failure Time: %%DATE : %%TIME (in YYMMDD : HHMMSS format and timezone: '+$ser_timezone+')00000096**While replying please remove the email ID csms@blueyonder.com if it is part of recipient list.00000008Regards,0032BlueYonder Customer Success Team" ATTACH_SYSOUT="Y"/>
#>



 <#
 MESSAGE="0004"Hi,00000090Job execution Failed on the Server %%NODEID running from Control-M,
   Please Check in to it.00000021Application: %%APPLIC0028Sub Application: %%APPLGROUP0019Job Name: %%JOBNAME0021Server Name: %%NODEID0022Script Name: %%MEMNAME0021Script Path: 
   %%MEMLIB0075Failure Time: %%DATE : %%TIME (in YYMMDD : HHMMSS format and timezone: UTC)00000096**While replying please remove the email ID csms@blueyonder.com if it is part of 
   recipient list.00000008Regards,0033BlueYonder Customer Success Team""
 
 #>

<#

#>

