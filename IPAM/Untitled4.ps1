
$a='''<DEFTABLE xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="Folder.xsd">

<FOLDER DATACENTER="veus2core0620" VERSION="919" PLATFORM="UNIX" FOLDER_NAME="CS_DXL_DMS_TEST" MODIFIED="False" LAST_UPLOAD="20220915071102UTC" FOLDER_ORDER_METHOD="UD4USESTAM" REAL_FOLDER_ID="280" TYPE="1" USED_BY_CODE="0">'''

$file = Import-Csv -Path "C:\Users\1033828\Downloads\template1.csv"
#C:\Users\1033828\Downloads\template1.xlsx
$job_dep=$null

$job_dep1=$null
$file=$file

foreach ($item in $file)
{
#$des=$item.'JOB DESCRIPTION'

 #if(!$item.'Job Parameter'){

 <#
 $condition=$null
 if($item.'Job Parameter' -ne ""){

 $param=$item.'Job Parameter'.split(",") 
 $param
 $i=1
 foreach($dat in $param){
 $condition='<VARIABLE NAME="%%PARM'+$i+'" VALUE="'+$dat+'"/>'
 $i++
    
 }

 }
 #>
 #####################################################
 
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
###########################################


$item.'JOB NAME'
if($item.'JOB NAME'){
$item.'Job Dependency'

}


$time=$null

 ###############3not working expected  TIMEFROM
if($item.'Execution time and Schedule (Specific day or Calendar Name)' -ne ""){

 $time="TIMEFROM ="+$timefrom

}
########################upto this


 $scriptname=$item.'Script Name'
 $scriptname
 $jobname=$item.'JOB NAME'
 $dec=$item.'JOB DESCRIPTION'
 $servername=$item.'Server Name'
 $scriptpath=$item.'Script path'
 $maxrun=$item.'Max Run Alarm'


 ############33333
 ########################

 $text1='<JOB JOBISN="10" APPLICATION="DXL_DMS_EST_TEST" SUB_APPLICATION="TEST_WEEKLY" MEMNAME="'+$scriptname+'" JOBNAME="'+$jobname+'" DESCRIPTION="'+$dec+'" 
CREATED_BY="J1016433" RUN_AS="SVC_DXLNPCONNMULE" CRITICAL="0" TASKTYPE="Job" CYCLIC="0" NODEID="'+$servername+'" INTERVAL="00001M" MEMLIB="'+$scriptpath+'"
CONFIRM="0" RETRO="0" MAXWAIT="1" MAXRERUN="0" AUTOARCH="0" MAXDAYS="0" MAXRUNS="0" "'+$time+'" WEEKDAYS="0" JAN="1" FEB="1" MAR="1" APR="1" MAY="1" JUN="1" JUL="1" AUG="1" 
SEP="1" OCT="1" NOV="1" DEC="1" DAYS_AND_OR="O" SHIFT="Ignore Job" SHIFTNUM="+00" SYSDB="0" IND_CYCLIC="S" CREATION_USER="j1016433" CREATION_DATE="20220629" CREATION_TIME="095938"
CHANGE_USERID="1027136" CHANGE_DATE="20220810" CHANGE_TIME="090200" RULE_BASED_CALENDAR_RELATIONSHIP="O" TIMEZONE="EST" APPL_TYPE="OS" MULTY_AGENT="N" USE_INSTREAM_JCL="N"
VERSION_OPCODE="N" IS_CURRENT_VERSION="Y" VERSION_SERIAL="2" VERSION_HOST="veus2core0622" CYCLIC_TOLERANCE="0" CYCLIC_TYPE="C" PARENT_FOLDER="CS_DXL_DMS_TEST">


<SHOUT WHEN="EXECTIME" TIME="+003" URGENCY="R" DEST="EM" MESSAGE="DMS-LONG_DXL_TEST_%%JOBNAME is running long more than 3 minutes of Average run time. Please check on priority."/>
<SHOUT WHEN="EXECTIME" TIME=">'+$maxrun+'" URGENCY="R" DEST="TODXLDMS" MESSAGE="DMS-LONG_DXL_TEST_%%JOBNAME is running long on %%NODEID. Please check on priority."/>
<SHOUT WHEN="EXECTIME" TIME=">'+$maxrun+'" URGENCY="R" DEST="EM" MESSAGE="DMS-LONG_DXL_TEST_%%JOBNAME is running long on %%NODEID. Please check on priority."/>' +$job_dep+ '<QUANTITATIVE NAME="BL_PATCH_DMS_DXL" QUANT="1" ONFAIL="R" ONOK="R"/>' +$job_dep1+ '</JOB>'
  write-host "HI"
 #}
  $text1
  #$data|Out-File "C:\Lavanya\convert.xml"
  
    
}

