from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
from .models import Trial_Table,Scheduled_dr,Configuration_details,Login_details
from .serializers import Trailserializer,Filterserializer,Configuration_details_serializer,Configuration_details_cus,Configuration_details_app,YourSerializer
from django.shortcuts import render
from rest_framework import viewsets
from itertools import chain
from django.http import JsonResponse
from rest_framework import views
from .excel_file import GetGlci as ef
from .api_zabbix  import Zabbix_Api
import json
import pymssql
from .mssql_instance import mssql_ as ms
from .get_TransferReport import AS2_Transfer_Report
from .handleRequests import  handleData as hD
from .api_maintenance import maintenance_theme
from .api_rollout import rollout_actions
from .api_start_stop import start_stop_actions
from .api_refresh_rollback import refresh_actions
from .api_f5 import F5_Api
from .schemaInfo import getSchemaInfo
from .scpoPostJenkinsActivity import scpopostdb
global con
import time
import datetime
import ldap3
import base64
from pathlib import Path
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import ensure_csrf_cookie
from zipfile import ZipFile
import pytz
import threading
import requests
from requests.auth import HTTPBasicAuth
import  tarfile
import json

#######################################
### LAST UPDATED DATE & TIME : 3/3/2022 12:47 AM (as per server time)
### LAST UPDATED BY: SIVAKUMAR.V
### CHANGES DESCRIPTION : ADDED NEW  FUNCTION FOR BIGFIX INTEGRATION

#####################################

postdb= scpopostdb()
obj =ef()
mssql = ms()
mssql1 = ms()
handleD= hD()
F5_obj = F5_Api()
zabbix_obj = Zabbix_Api()
rollout_obj = rollout_actions()
start_stop_obj = start_stop_actions()
refresh_obj = refresh_actions()
main_obj = maintenance_theme()
as2 = AS2_Transfer_Report()
sinfo = getSchemaInfo()
con = mssql.connect_db(server="10.120.78.123", port="1433", user="hu_automationdb", password="bxkrCkvkA9q94cnN", database="automationdb_test")
con1 = mssql1.connect_db(server="10.120.78.123", port="1433", user="hu_automationdb", password="bxkrCkvkA9q94cnN", database="automationdb_UAT")
# Create your views here.

def login(request):
    print('hello')
    return HttpResponse('Hello Loging in');

def role_list(request):
    user = request.GET['user']
    output = mssql.get_user_role(user)
    return JsonResponse(output,safe=False)

def login_validation(request):
    user = request.GET['user']
    password = request.GET['pass']
    password = (base64.b64decode(password)).decode('utf-8')
    user_dn = user+'@jdadelivers.com'
    output = {}
    try:
        conn = ldap3.Connection('ldap://Scdc02.jdadelivers.com:3268', user=user_dn, password=password,auto_bind=True)
        conn.search('dc=JDADELIVERS,dc=com', '(&(sAMAccountName={user}))'.format(user=user),attributes=['sn', 'objectclass','Displayname','mail'])
        dp = conn.entries[0]['displayName']
        em = conn.entries[0]['mail']
        if conn.result['description'] == 'success':
            output['result'] = 'Success'
            output['user'] = (str(dp)).split(':')
            output['email'] = (str(em)).split(':')
    except:
        output['result'] = 'Failure'
        output['user']  = 'Unknown'
        output['email'] = 'Unknown'
##    output['result'] = 'Success'
##    output['user'] = 'User'
    return JsonResponse(output,safe=False)

def GetCustomer(request):
    pid = int(request.GET['pid'])
    data = mssql.getCustomer(pid)
    return JsonResponse(data, safe=False)

def GetCustomer1(request):
    pid = int(request.GET['pid'])
    data = mssql.getCustomer1(pid)
    return JsonResponse(data, safe=False)

def GetSubregion(request):
    
    c_name=request.GET['c_name'].strip()
    env=request.GET['env']
    print('#'*10)
    print(c_name,env)
    data= mssql.getSubregion(c_name,env)
    print(data)
    return JsonResponse(data,safe=False)


def GetWMSMaintenancelogs(request):
    data= mssql.getWMSMaintenancelogs()
    return JsonResponse(data,safe=False)

def GetWMSCustomer(request):
    data= mssql.getWmsCustomer()
    return JsonResponse(data,safe=False)

def GetWMSCustomer3(request):
    print('+'*20)
    data= mssql.getWmsCustomer3()
    return JsonResponse(data,safe=False)

def getEnvironment(request):
    cid=int(request.GET['cid'])
    data= mssql.getEnvironment(cid)
    return JsonResponse(data,safe=False)

def GetServerCatgeory(request):
    cid=int(request.GET['cid'])
    pid=int(request.GET['pid'])
    data= mssql.getServerCatgeory(cid,pid)
    return JsonResponse(data,safe=False)

def GetWEnv(request):
    cid=request.GET['cid']
    sid=int(request.GET['sid'])
    pid=int(request.GET['pid'])
    data= mssql.getWenv (cid=cid,sid=sid,pid=pid)
    return JsonResponse(data,safe=False)  
    
def GetProduct(request):
    cname=request.GET['cus_name']
    data= obj.get_product(customer_name=cname)
    return JsonResponse(data['product'],safe=False) 

def GetEnv(request):
	cname=request.GET['cname']
	pname=request.GET['pname']
	server=request.GET['server']
	data= obj.get_env(customer_name=cname,solution=pname,server_cat=server)
	return JsonResponse(data['environment'],safe=False) 

def GetServer(request):
	cname=request.GET['cname']
	pname=request.GET['pname']
	server=request.GET['server']
	env=request.GET['env']
	data= obj.get_server(customer_name=cname,solution=pname,server_cat=server,environment=env)
	return JsonResponse(data['server_list'],safe=False)
    
def GetWServer(request):
    cid=request.GET['cid']
    sid=int(request.GET['sid'])
    eid=int(request.GET['eid'])
    pid=int(request.GET['pid'])
    data= mssql.getWserver(cid=cid,sid=sid,eid=eid,pid=pid)
    return JsonResponse(data,safe=False)

def GetWServer1(request):
    cid=request.GET['cid']
    sid=int(request.GET['sid'])
    eid=int(request.GET['eid'])
    pid=int(request.GET['pid'])
    sub=request.GET['sub']
    print(sub)
    data= mssql.getWserver1(cid=cid,sid=sid,eid=eid,pid=pid,sub=sub)
    return JsonResponse(data,safe=False)

def GetWServer2(request):
    cid=request.GET['cid']
    sid=int(request.GET['sid'])
    eid=int(request.GET['eid'])
    pid=int(request.GET['pid'])
    data= mssql.getWserver(cid=cid,sid=sid,eid=eid,pid=pid)
    return JsonResponse(data,safe=False)



########### AS2 ##################
def get_as2accountType(request):
    cname=request.GET['cus_name']
    prod_id=int(request.GET['pid'])
    accType = mssql.get_as2_accountType(prod_id=prod_id,customer=cname)
    return JsonResponse(accType,safe=False)

def get_as2accountName(request):
    cname=request.GET['cus_name']
    prod_id=int(request.GET['pid'])
    as2ACType=request.GET['as2acType']
    accName = mssql.get_as2_accountName(prod_id=prod_id,customer=cname,acctype=as2ACType)
    return JsonResponse(accName,safe=False)

def get_as2CustomerUI(request):
    accName = mssql.get_dbas2Customer()
    return JsonResponse(accName,safe=False)

def get_as2envUI(request):
    cid=request.GET['cid']
    accName = mssql.get_dbas2env(cid)
    return JsonResponse(accName,safe=False)

def get_as2outboxUI(request):
    cid=request.GET['cid']
    env=request.GET['env']
    accName = mssql.get_dboutboxenv(cid,env)
    return JsonResponse(accName,safe=False)

def get_as2accountUI(request):
    cid=request.GET['cid']
    env=request.GET['env']
    outbox=request.GET['outbox']
    accName = mssql.get_dbaccountenv(cid,env,outbox)
    return JsonResponse(accName,safe=False)

def get_as2accounttypeUI(request):
    cid=request.GET['cid']
    env=request.GET['env']
    outbox=request.GET['outbox']
    accname=request.GET['accname']
    acctype = mssql.get_dbaccounttypeenv(cid,env,outbox,accname)
    return JsonResponse(acctype,safe=False)

#### Big fix ADDED ####
def getIdDetails(request):
    cname = request.GET['cname']
    env = request.GET['env']
    cid = mssql.getLikeCustomerid(cname=cname)
    eid = mssql.getLikeEnvid(env=env)
    output= {'cid':cid[0],'eid':eid[0]}
    return JsonResponse(output,safe=False)

def getBigfixserver(request):
    cid=int(request.GET['cid'])
    eid=int(request.GET['eid'])
    data= mssql.getBigfixserver(cid=cid,eid=eid)
    return JsonResponse(data,safe=False)
#### Big fix ADDED ####

def get_as2Report(request):
    #cid=302&env=Dev&outbox=\\dlseeldevapp1v.jdadelivers.com\SFTP&accname=7elescdldev&acctype=SFTP&starttime=2022/03/02&endtime=2022/03/03&mail=a@jda.com
    cid=request.GET['cid']
    env=request.GET['env']
    outbox=request.GET['outbox']
    accname=request.GET['accname']
    acctype=request.GET['acctype']
    starttime=request.GET['starttime']
    endtime=request.GET['endtime']
    mail=request.GET['mail']
    my_dict = {'prod':env,'customerids':cid,'outboxs':outbox,'account_type':acctype,'account_names':accname,'start_date':starttime,'end_date':endtime,'email':mail}
    print(my_dict)
    t = threading.Thread(target=as2.get_transfer_report, kwargs=my_dict,daemon=True)
    t.start()
    return JsonResponse("AS2/SFTP report triggered and EMail would be sent",safe=False)

########### AS2 ##################

########### Customer Onboarding ##################
def get_unique_cm_customer(request):
    customer = mssql.get_db_unique_cm_customer()
    return JsonResponse(customer,safe=False)

def get_sub_region_cm(request):
    cid = request.GET['cid']
    subregion = mssql.get_db_subregion_cm(cid)
    return JsonResponse(subregion,safe=False)

def get_envby_subRegion_cm(request):
    cid = request.GET['cid']
    subregion = request.GET['subregion']
    environment = mssql.get_environment_cm(cid,subregion)
    return JsonResponse(environment,safe=False)

def insert_cm_details(request):
    cid = request.GET['cid']
    subregion = request.GET['subregion']
    env = request.GET['env']
    taskname = request.GET['taskname']
    tmscusname = request.GET['tmscusname']
    insert_id = mssql.insert_cm_db(cid,subregion,env,taskname,tmscusname)
    return JsonResponse(insert_id,safe=False)

def update_cm_details(request):
    oid = request.GET['oid']
    subregion = request.GET['subregion']
    env = request.GET['env']
    taskname = request.GET['taskname']
    tmscusname = request.GET['tmscusname']
    insert_id = mssql.update_cm_db(oid,subregion,env,taskname,tmscusname)
    return JsonResponse(insert_id,safe=False)

########### Customer Onboarding ##################

def GetActivity(request):

	pid =request.GET['pid']
	data = mssql.getActivity(product_id=pid)
	return JsonResponse(data,safe=False)

def GetActivity1(request):

	pid =request.GET['pid']
	data = mssql.getActivity1(product_id=pid)
	return JsonResponse(data,safe=False)
	
def GetTask(request):

	aid =request.GET['aid']
	data = mssql.getTask(activity_id=aid)
	return JsonResponse(data,safe=False)

def GetTask1(request):

	aid =request.GET['aid']
	data = mssql.getTask(activity_id=aid)
	return JsonResponse(data,safe=False)

def getSsl(request): # For Ssl Activity
    data = mssql.getSsl()
    return JsonResponse(data,safe=False)

def getServerHost(request):
    data = mssql.getServerHost()
    return JsonResponse(data,safe=False)

def getZabbixServerHost(request):
    data = mssql.getZabbixServerHost()
    return JsonResponse(data,safe=False)


def getZabbixServer(request):
    eid = request.GET['eid']
    sid = request.GET['sid']
    data = mssql.get_zabbix_server(eid,sid)      
    return JsonResponse(data,safe=False)

def getZabbixHG(request):
    zserver = request.GET['zserver']
    result = zabbix_obj.get_host_groups_zabbix(zserver)
    output = [{'groupid':i['groupid'],'name':i['name']} for i in result['result']]
    return JsonResponse(output,safe=False)

def getZabbixHost(request):
    zhg = request.GET['zhg']
    zserver = request.GET['zserver']
    zhg_list = zhg.split(',')
    result = zabbix_obj.get_hosts_zabbix(zserver,zhg_list)
    if(len(result) > 1):
            result.insert(0,{'hostid': '', 'host': 'SELECT ALL'})
    return JsonResponse(result,safe=False)

def getZabbixMaintenance(request):
    zserver = request.GET['zserver']
    zmname = request.GET['zmname']
    if zmname:
        result = zabbix_obj.get_maintenance_zabbix(zserver,zmname)
    else:
        epoch_time = int(time.time())
        result = zabbix_obj.get_maintenance_zabbix(zserver,zmname)
    return JsonResponse(result,safe=False)

#### SCPO POST DB REFRESH ####
def getSchemaDetails(request):
    server = request.GET['zserver']
    os_name = str.lower(mssql.get_os_name(server)[0]['os_name'])
    print(os_name)
    outValues=sinfo.getSchemaForLinux(serverName=server)
    return JsonResponse(outValues,safe=False)
#POST_DB SCRIPT
def getpostdbexitsornot(request):
    os=''
    appserver = request.GET['appserver']
    os_name = str.lower(mssql.get_os_name(appserver)[0]['os_name'])
    if 'WINDOWS' in os_name.upper():
        os='Windows'
    else:
        os='Linux'
    
    outValues=sinfo.getfileExists(os=os,serverName=appserver)
    return JsonResponse(outValues,safe=False)
    
#Send email
def sendEmailforScpoPostdb(request):
    appserver = request.GET['appserver']
    user = request.GET['user']
    email = request.GET['email']
    rid = request.GET['rid']
    os=''
    os_name = str.lower(mssql.get_os_name(appserver)[0]['os_name'])
    if 'WINDOWS' in os_name.upper():
      os='Windows'
    else:
      os='Linux'
    Buildbody = {
    "APPSERVER": appserver,
    "OS": os,
    "ACTION": "SendEmail",
    "REQUESTOR": email,
    "RID": rid
    }
    values=postdb.setscpoPostDb(Buildbody)
    return JsonResponse("Request has been initiated, Logs will send to "+email,safe=False)

#SCPO POST
def postDBRefreshtrigger(request):
    server = request.GET['appserver']
    cid = int(request.GET['cid'])
    env = request.GET['env']
    schema = request.GET['schema']
    user = request.GET['user']
    email = request.GET['email'] 
    os=''
    os_name = str.lower(mssql.get_os_name(server)[0]['os_name'])
    if 'WINDOWS' in os_name.upper():
      os='Windows'
    else:
      os='Linux'
    rid=int(time.time())
    Buildbody = {
	"APPSERVER": server,
	"SCHEMANAME": schema,
	"OS": os,
	"RID": int(rid),
	"ACTION": "Postdbrefresh",
	"REQUESTOR": email,
	"CID": cid,
	"ENV": env
    }
    checkpreviousbeforeSubmit=postdb.getsecrver(servername=server)
    if 'True' in checkpreviousbeforeSubmit:
        return JsonResponse("Request has Already InProgress "+server+" please wait to complete Previous Request",safe=False)
    else:
        values=postdb.setscpoPostDb(Buildbody)
        return JsonResponse("Request has been initiated with id:"+str(rid),safe=False)
#### SCPO POST DB REFRESH ####
    
def doZabbixActivity(request):
    main_output = {}
    user = request.GET['user']
    jid = request.GET['jid']
    zserver = request.GET['zserver']
    data = mssql.get_zabbix_server("","",zserver)
    hostnames = request.GET['hostnames']
    hostids = request.GET['hostids']
    ticket = request.GET['ticket']
    taskname = request.GET['taskname']
    tasktitle = request.GET['tasktitle']
    cr_mname = request.GET['crmname']
    cr_mname = ticket+'_'+cr_mname
    start_date = request.GET['startdate']
    if start_date:
        start_date = datetime.strptime(start_date, "%d/%m/%Y, %H:%M:%S")
        start_con = mssql.convertTZ(start_date,'Asia/Kolkata',data[0]['time_zone'])
        start_epoch = int(start_con.timestamp())
        start_date = start_con.strftime("%Y-%m-%d %H:%M:%S")
    end_date = request.GET['enddate']
    if end_date:
        end_date = datetime.strptime(end_date, "%d/%m/%Y, %H:%M:%S")
        end_con = mssql.convertTZ(end_date,'Asia/Kolkata',data[0]['time_zone'])
        end_epoch = int(end_con.timestamp())
        end_date = end_con.strftime("%Y-%m-%d %H:%M:%S")
    up_mname = request.GET['upmname']
    up_mid = request.GET['upmid']
    before_date = request.GET['beforedate']
    if before_date:
        before_date = datetime.strptime(before_date, "%d/%m/%Y, %H:%M:%S")
        before_con = mssql.convertTZ(before_date,'Asia/Kolkata',data[0]['time_zone'])
        before_epoch = int(before_con.timestamp())
        before_date = before_con.strftime("%Y-%m-%d %H:%M:%S")
    after_date = request.GET['afterdate']
    if after_date:
        after_date = datetime.strptime(after_date, "%d/%m/%Y, %H:%M:%S")
        after_con = mssql.convertTZ(after_date,'Asia/Kolkata',data[0]['time_zone'])
        after_epoch = int(after_con.timestamp())
        after_date = after_con.strftime("%Y-%m-%d %H:%M:%S")
    columns='(username,taskname,zabbix_server,hostnames,hostids,ticket,maintenance_name,maintenance_id,startdate,enddate,beforedate,afterdate,state,output,datetime,jid)'
    
    if taskname == 'enable_monitor' or taskname == 'disable_monitor':
        host_list = hostnames.split(',')
        hostid_list = hostids.split(',')
        output = {'Task':tasktitle,'Host Names':hostnames}
        function = 'zabbix_obj.'+taskname+'_zabbix'+'(zserver,hostid_list)'
        output.update(eval(function))
        main_output['header'] = list(output.keys())
        main_output['result'] = [output]
        if output['Status'] == 'Failed':
            values = (user,tasktitle,data[0]['display_name'],hostnames,hostids,ticket,"","","","","","",output['Status'],(eval(output['Output']))['data'],datetime.now().strftime("%Y-%m-%d %H:%M:%S"),jid)
        else:
            values = (user,tasktitle,data[0]['display_name'],hostnames,hostids,ticket,"","","","","","",output['Status'],output['Output'],datetime.now().strftime("%Y-%m-%d %H:%M:%S"),jid) 
        ins = mssql.insert_query('dbo.zabbix_logs',columns,values)
        
    elif taskname == 'create_maintenance':
        host_list = hostnames.split(',')
        hostid_list = hostids.split(',')
        period = end_epoch - start_epoch
        output = {'Task':tasktitle,'Host Names':hostnames}
        output.update(eval('zabbix_obj.create_maintenance_zabbix(zserver,cr_mname,start_epoch,end_epoch,"",hostid_list,period)'))
        main_output['header'] = list(output.keys())
        main_output['result'] = [output]
        if output['Status'] == 'Failed':
            values = (user,tasktitle,data[0]['display_name'],hostnames,hostids,ticket,cr_mname,"",start_date,end_date,"","",output['Status'],(eval(output['Output']))['data'],datetime.now().strftime("%Y-%m-%d %H:%M:%S"),jid)
        else:
            values = (user,tasktitle,data[0]['display_name'],hostnames,hostids,ticket,cr_mname,(output['Output'].split(': ')[1]),start_date,end_date,"","",output['Status'],output['Output'],datetime.now().strftime("%Y-%m-%d %H:%M:%S"),jid)
        ins = mssql.insert_query('dbo.zabbix_logs',columns,values)

    elif taskname == 'update_maintenance':
        output = {'Task':tasktitle,'Maintenance Name':up_mname}
        period = after_epoch - start_epoch
        output.update(eval('zabbix_obj.update_maintenance_zabbix(zserver,up_mid,start_epoch,after_epoch,period)'))
        main_output['header'] = list(output.keys())
        main_output['result'] = [output]
        if output['Status'] == 'Failed':
            values = (user,tasktitle,data[0]['display_name'],"","",ticket,up_mname,up_mid,start_date,"",before_date,after_date,output['Status'],(eval(output['Output']))['data'],datetime.now().strftime("%Y-%m-%d %H:%M:%S"),jid)
        else:
            values = (user,tasktitle,data[0]['display_name'],"","",ticket,up_mname,up_mid,start_date,"",before_date,after_date,output['Status'],output['Output'],datetime.now().strftime("%Y-%m-%d %H:%M:%S"),jid)
        ins = mssql.insert_query('dbo.zabbix_logs',columns,values)
    
    return JsonResponse(main_output,safe=False)

def test(request):
    test=request.GET['test']
    test1 = request.GET['test1']
    output = [{'test':test,'test1':test1}]
    return JsonResponse(output,safe=False)

def ValidateName(request):
    snames = request.GET['sname']
    prod =request.GET['prod']
    name =request.GET['name']
    print(prod)
    print("sdvgrgt4rtnthykytuk5ki")
    for sname in snames.split(','):
        output=zabbix_obj.validate_name_zabbix(sname,prod,name)
        if output['Output']==1:
             
            return JsonResponse({'exist':1},safe=False)
    return JsonResponse({'exist':0},safe=False)


##### Time zone Changes ####
def convertTZ(start_date,fromtzone,totzone):
        timezone = pytz.timezone(fromtzone)
        start_date = timezone.localize(start_date)
        data = start_date.astimezone(pytz.timezone(totzone))
        return data
##### Time zone Changes ####
    
def getWmaintenance(request):
    mid = request.GET['mid']
    output = {}
    outpu = mssql.select_query('*','wms_maintenance_logs',"maintenance_id ='{}'".format(mid))
    if(outpu):
        output['id'] = outpu[0][0]
        output['mid'] = outpu[0][1]
        output['name'] = outpu[0][2]
        output['zabbix_server'] = outpu[0][3]
        ##### Time zone Changes ####
        time_zone = mssql.get_zabbix_time_zone(outpu[0][3])
        s_time = datetime. datetime. fromtimestamp(int(outpu[0][4])).strftime('%Y/%m/%d,%H:%M')
        s_time = datetime.datetime.strptime(s_time, "%Y/%m/%d,%H:%M")
        e_time = datetime. datetime. fromtimestamp(int(outpu[0][5])).strftime('%Y/%m/%d,%H:%M')
        e_time = datetime.datetime.strptime(e_time, "%Y/%m/%d,%H:%M")
        start_time = convertTZ(s_time,time_zone[0]['time_zone'],'Asia/Kolkata')
        end_time = convertTZ(e_time,time_zone[0]['time_zone'],'Asia/Kolkata')
        start_time = (str(start_time).split('+')[0]).replace('-','/')
        end_time = (str(end_time).split('+')[0]).replace('-','/')
        print(start_time)
        print(end_time)
        output['start_time'] = (datetime.datetime.strptime(start_time, "%Y/%m/%d %H:%M:%S")).strftime('%Y/%m/%d %H:%M')
        output['end_time'] = (datetime.datetime.strptime(end_time, "%Y/%m/%d %H:%M:%S")).strftime('%Y/%m/%d %H:%M')
        print(output)
        #datetime.datetime.strptime(str(start_time), "%Y/%m/%d %H:%M")
        ##### Time zone Changes ####
    return JsonResponse(output,safe=False)

def UpdateWmaintenance(request):
    mid = request.GET['mid']
    cid = request.GET['cid']
    ##### Time zone Changes ####
    start_time = datetime.datetime.strptime(request.GET['start_time'], "%Y/%m/%d %H:%M")
    end_time = datetime.datetime.strptime( request.GET['end_time'], "%Y/%m/%d %H:%M")
    zserver = request.GET['zserver']
    time_zone = mssql.get_zabbix_time_zone(zserver)
    start_time = convertTZ(start_time,'Asia/Kolkata',time_zone[0]['time_zone'])
    end_time = convertTZ(end_time,'Asia/Kolkata',time_zone[0]['time_zone'])
    start_time = int(start_time.timestamp())
    end_time =int(end_time.timestamp())
    period = (int(start_time) - int(end_time))
    ##### Time zone Changes ####
    zabbixoutput = zabbix_obj.get_update_maintenance(zserver=zserver,maintenance_id=mid,start_time=start_time,end_time=end_time,period=period)
    output = {'output':[]}
    if zabbixoutput['Status'] == "Success":
        out = mssql.updateWmaintence(cid=cid,start_time=start_time,end_time=end_time)
        output['output'].append({'Output Status':zabbixoutput['Output']})
    else:
        output['output'].append({'Output Status':'Error Updating Maintenance'})
    return JsonResponse(output,safe=False)

def RolloutZabbix(request):
    snames = request.GET['sname']
    prod =int(request.GET['prod'])
    if prod != 1:
        prod = 2
    zabbix_server = zabbix_obj.get_zabbix_server_host(sname,prod)
    return zabbix_server

def CreateHostMaintenance(request):
    snames = request.GET['sname']
    pid = int(request.GET['pid'])
    prod =int(request.GET['prod'])
    name =request.GET['name']
    
    ##### Time zone Changes ####
    end_epoch = datetime.datetime.strptime(request.GET['etime'], "%Y/%m/%d %H:%M")
    start_epoch = datetime.datetime.strptime(request.GET['stime'], "%Y/%m/%d %H:%M")
    ##### Time zone Changes ####
    user= 'test'
    if prod != 1:
        prod=2
    zserver={}
    output = []
    zoutput = {}
    for sname in snames.split(','):
        zabbix_server = zabbix_obj.get_zabbix_server_host(sname,prod)
        {'servername':'','status':''}
        if zabbix_server['zabbixserver'] in zserver.keys():
            zserver[zabbix_server['zabbixserver']].append({'host_id':zabbix_server['host_id'],'server_name':zabbix_server['server']})
            
        else:
            zserver[zabbix_server['zabbixserver']]=[{'host_id':zabbix_server['host_id'],'server_name':zabbix_server['server']}]
    for zser,value in zserver.items():
        print('zssss',zser)
        host = [zid['host_id'] for zid  in value]
        servernames = ','.join([zid['server_name'] for zid  in value])
        ##### Time zone Changes ####
        time_zone = mssql.get_zabbix_time_zone(zser)
        #print(time_zone[0]['time_zone'])
        start_time = convertTZ(start_epoch,'Asia/Kolkata',time_zone[0]['time_zone'])
        end_time = convertTZ(end_epoch,'Asia/Kolkata',time_zone[0]['time_zone'])
        start_epoch = int(start_time.timestamp())
        end_epoch =int(end_time.timestamp())
        period = (int(end_epoch) - int(start_epoch))
        print(start_epoch,end_epoch)
        ##### Time zone Changes ####
        #http://127.0.0.1:8000/api/CreateHostMaintenance?name=Maintenance_test&etime=1636643640&stime=1636643100&prod=2&sname=DLJDATNFWFMW1V,DLJDATNFWFMW1V&pid=18
        out=zabbix_obj.get_create_hostmaintenance(zserver = zser,maintenance_name = name,start_time = start_epoch,end_time = end_epoch,period = period,hostid = host)
        print(out)
        if(out['Status'] == "Success"):
            output.append({'Server Name': servernames,'Output Status' :"In "+zser+out['Output']})
            host = ','.join(host)
            mid = out['Output'].split(':')[1]
            mssql.insert_query(columnname = ['name','zabbix_server','start_time','end_time','host_id','maintenance_id','created_by','server_name','status','product_id'],columnvalue = [name,zser,start_epoch,end_epoch,host,mid,user,servernames,'Success',pid],tablename = 'wms_maintenance_logs')
        else:
            output.append({'Server Name': servernames,'Output Status':" Error Creating Maintnenance in "+zser})
            host = ','.join(host)
            mid = '0'
            mssql.insert_query(columnname = ['name','zabbix_server','start_time','end_time','host_id','maintenance_id','created_by','server_name','status','product_id'],columnvalue = [name,zser,start_epoch,end_epoch,host,mid,user,servernames,'Failure',pid],tablename = 'wms_maintenance_logs')
    #output.append( {'Output Status':" Error Creating Maintnenance in "+zser})
    zoutput['output'] = output
    return JsonResponse(zoutput,safe=False)

def startservice(request):
    snames = request.GET['sname']
    servicearr = request.GET['servicearr']
    customer = request.GET['customer']
    pid = request.GET['pid']
    user = request.GET['user']
    #snames = ['DLBYAUTDEVWA1V','SL1SMCDEVWA1V']
    snames = ['DLBYAUTDEVWA1V']
    #servicearr = ['MOCA']
    output = []
    routput = {}
    moutput = []
    for sname in snames: #.split(','):
        output.extend(main_obj.get_start_app_service(servername = sname,service_arr=servicearr.split(',')))
        for out in output:
            e = datetime.datetime.now()
            now = e.strftime("%Y-%m-%d %H:%M:%S")
            tablename = 'wms_service_logs'
            coloumns = ['activity','customer_name','server_name','service_name','status','product_id','created_by','created_on']
            values = ['Start Service',customer,out['server name'],out['Service Name'],out['Status'],pid,user,now]
            mssql.insert_query(columnname = coloumns,columnvalue = values,tablename = tablename)
##    print(output)
##    for out in output:
##        for ser,sta in out.items():
##            moutput.append({'Server Name':ser,'Output Status':','.join(str(s) for s in sta)})
    routput['output']=output
    return JsonResponse(routput,safe=False)

def anisible_trigger(request):
    output = []
    routput = {}
    output.extend(main_obj.trigger_anisible())
    routput['output'] = output
    return JsonResponse(routput,safe=False)

def stopservice(request):
    snames = request.GET['sname']
    servicearr = request.GET['servicearr']
    customer = request.GET['customer']
    pid = request.GET['pid']
    user = request.GET['user']
    #snames = ['DLBYAUTDEVWA1V','SL1SMCDEVWA1V']
    snames = ['DLBYAUTDEVWA1V']
    #servicearr = ['MOCA']
    output = []
    routput = {}
    moutput = []
    for sname in snames: #.split(','):
        output.extend(main_obj.get_stop_app_service(servername = sname,service_arr=servicearr.split(',')))
        for out in output:
            e = datetime.datetime.now()
            now = e.strftime("%Y-%m-%d %H:%M:%S")
            tablename = 'wms_service_logs'
            coloumns = ['activity','customer_name','server_name','service_name','status','product_id','created_by','created_on']
            values = ['Stop Service',customer,out['server name'],out['Service Name'],out['Status'],pid,user,now]
            mssql.insert_query(columnname = coloumns,columnvalue = values,tablename = tablename)
    routput['output'] = output
    return JsonResponse(routput,safe=False)

def MaintenanceLog(request):
    returnOutput={'headers':[],'output':[]}
    mid = int(request.GET['id'])
    if mid == 1:
       output =  mssql.getWMSMaintenancelogs()
       returnOutput['headers'].extend(['CreationID','MaitenanceName','StartTime','EndTime','ServerNames','Status','CreatedBy'])
       returnOutput['output'].extend(output)
    if mid == 0:
       output =  mssql.getWMSEnablelogs()
       returnOutput['headers'].extend(['ID','Activity','CustomerName','Status','ServerNames','CreatedBy','CreatedOn'])
       returnOutput['output'].extend(output)
    #### service start/stop ####
    if mid == 2:
       output =  mssql.getWMSServicelogs()
       returnOutput['headers'].extend(['ID','Activity','CustomerName','ServerNames','ServiceName','Status','CreatedBy','CreatedOn'])
       returnOutput['output'].extend(output)
    #### server reboot ####
    if mid == 3:
       output =  mssql.getWMSServerRebootlogs()
       returnOutput['headers'].extend(['ID','Activity','CustomerName','Status','ServerNames','CreatedBy','CreatedOn','Action'])
       returnOutput['output'].extend(output)
    #### RollOut ####
    if mid == 4:
       output =  mssql.getWMSRolloutlogs()
       returnOutput['headers'].extend(['ID','Customer Name','Rollout Name','Server Name','Status','CreatedBy','CreatedOn','Action'])
       returnOutput['output'].extend(output)
    #### Upgrade ####
    if mid == 5:
       output =  mssql.getWMSUpgradelog()
       returnOutput['headers'].extend(['ID','Customer Name','Server Name','Job ID','Maintenance ID','Maintenance End Time','Stage','Status','CreatedBy','CreatedOn'])
       returnOutput['output'].extend(output)

    #### Start & Stop ####
    if mid == 6:
       output =  mssql.getStartStoplogs()
       returnOutput['headers'].extend(['ID','Customer Name','Server Name','Status','CreatedBy','CreatedOn','Action'])
       returnOutput['output'].extend(output)

    if mid == 7:
       output =  mssql.getRefreshlogs()
       returnOutput['headers'].extend(['ID','Customer Name','Activity','App_type','Status','CreatedBy','CreatedOn','Action'])
       returnOutput['output'].extend(output)
    
    return JsonResponse(returnOutput,safe=False)

#### RollOut ####


def RolloutServerLog(request):
    returnOutput={'headers':[],'output':[]}
    mid = int(request.GET['id'])
    output =  mssql.getWMSRolloutServerlogs(mid)
    returnOutput['headers'].extend(['ID','Server Name','Status','Updated On','Action'])
    returnOutput['output'].extend(output)
    return JsonResponse(returnOutput,safe=False)

def StartStopServerLog(request):
    returnOutput={'headers':[],'output':[]}
    mid = int(request.GET['id'])
    output =  mssql.getWMSStartStoplogs(mid)
    returnOutput['headers'].extend(['ID','Env','Server Name','App','Action','Status','Moca_Server','Moca_instance','Refs_server','Refs_instance','Maintenance_Id','Start_time','End_time','Action'])
    returnOutput['output'].extend(output)
    return JsonResponse(returnOutput,safe=False)

def RefreshServerLog(request):
    returnOutput={'headers':[],'output':[]}
    mid = int(request.GET['id'])
    
    output =  mssql.getWMSRefreshlogs(mid)
    returnOutput['headers'].extend(['ID','Activity','App_type','AWX_Job_id','Source_Server','Source_Env','Destination_Server','Destination_Env','OS_type','Instance_type','Backupfilename','Start_time','End_time','Error','Status','Action'])
    returnOutput['output'].extend(output)
    return JsonResponse(returnOutput,safe=False)

def RolloutDetailedLog(request):
    returnOutput={'headers':[],'output':[]}
    mid = int(request.GET['id'])
    output =  mssql.getWMSRolloutDetailedlogs(mid)
    returnOutput['headers'].extend(['ID','Rollout Name','Activity','Status','Updated On'])
    returnOutput['output'].extend(output)
    return JsonResponse(returnOutput,safe=False)

def getRefreshid(request):
    returnOutput={'headers':[],'output':[]}
    rid = int(request.GET['rid'])
    
    output =  mssql.getWMSRefreshlogs(rid)
    
    returnOutput['headers'].extend(['ID','Activity','App_type','AWX_Job_id','Source_Server','Source_Env','Destination_Server','Destination_Env','OS_type','Instance_type','Backupfilename','Start_time','End_time','Action'])
    returnOutput['output'].extend(output)
    return JsonResponse(returnOutput,safe=False)
    
    

def StartStopDetailedLog(request):
    returnOutput={'headers':[],'output':[]}
    mid = int(request.GET['id'])
    output =  mssql.getWMSStartStopDetailedlogs(mid)
    returnOutput['headers'].extend(['ID','Server Name','Action','Status'])
    returnOutput['output'].extend(output)
    return JsonResponse(returnOutput,safe=False)

def RefreshRollbackDetailedLog(request):
    returnOutput={'headers':[],'output':[]}
    mid = int(request.GET['id'])
    output =  mssql.getWMSRefreshDetailedlogs(mid)
    returnOutput['headers'].extend(['ID','Current_task','Status','Error'])
    returnOutput['output'].extend(output)
    return JsonResponse(returnOutput,safe=False)

def handleRollout(request):
    returnOutput=[]
    filezip=request.GET['filezip']
    app=request.GET['app'].lower()
    server_type=request.GET['server_type']
    maintenance_end_time=request.GET['maintenance_end_time']
    
    server=request.GET['server']
    customer=request.GET['customer']
    rollouts=request.GET['rollouts']
    env=request.GET['env']
    user=request.GET['user']
    moca_password=''
    refs_password=''
    activity=request.GET['activity']
    if request.GET['moca_password']:
        moca_password=request.GET['moca_password']
    if request.GET['refs_password']:
        refs_password=request.GET['refs_password']
   
   
    
    main_output = {'output':[]}
    e = datetime.datetime.now()
    now = e.strftime("%Y-%m-%d %H:%M:%S")
    
    rolloutid = mssql.insert_query_with_id(columnname = ['customer_name','server_list','rollout_list','status','jobidlist','created_by','created_on'],columnvalue = [customer,server,rollouts,'In Progress','',user,now],tablename = 'wms_rollout_customer_view')
    my_dict = {'Filezip':filezip,'App':app,'Server_type':server_type,'Maintenance End time':maintenance_end_time,'Customer':customer,'Environment':env,'Moca Password':moca_password,'Refs password':refs_password,'Rolloutid':rolloutid }
    print("*"*50,'Inputs from Form',"*"*50)
    print(my_dict)
    print("Printing Rolloutid:",rolloutid[0][0])
    #t = threading.Thread(target=rollout_obj.trigger_rollout, kwargs=my_dict ,daemon=True)
    #t.start()
    if env!='linux':
        rollout_obj.trigger_rollout(filezip,app,server_type,maintenance_end_time,server,customer,rollouts,env,rolloutid[0][0],activity=activity)
    else:
        rollout_obj.trigger_rollout(filezip,app,server_type,maintenance_end_time,server,customer,rollouts,env,rolloutid[0][0],moca_password,refs_password,activity=activity)
    main_output['output'] = [{'output':'Rollout is in Progress Please check Logs for progress With ID : {}'.format(rolloutid[0][0])}]
    return JsonResponse(main_output,safe=False)

def refresh(request):
    returnOutput=[]
    if request.GET['activity']=='Refresh':
        instance=request.GET['instance']
        app=request.GET['app'].lower()
        env=request.GET['server_type']
        customer_name=request.GET['customer']
        activity=request.GET['activity']
        senv=request.GET['env']
        conn = pymssql.connect(server="DLBYSQLPRAUT1V.JDADELIVERS.COM", port="1433", user="hu_automationdb", password="bxkrCkvkA9q94cnN", database="automationdb_UAT")
        cursor = conn.cursor()
        
        
        print('select * from environment where id={}'.format(senv))
        cursor.execute('select * from environment where id={}'.format(senv))
        output1=cursor.fetchall()
        senv2=output1[0][2]
        print(senv2)
        print("*************")
        
        senv1=request.GET['env1']

        print('select * from environment where id={}'.format(senv1))
        cursor.execute('select * from environment where id={}'.format(senv1))
        output1=cursor.fetchall()
        senv3=output1[0][2]
        print(senv3)
        print("*************")

        
        s_server=request.GET['sourceserver']
        #env1=request.GET['env1']
        d_server=request.GET['targetserver']
        user=request.GET['user']
        if env == "linux" and app == "refs":
            refs_user_pass=request.GET['source_password']
            refs_user_pass1=request.GET['target_password']
            moca_user_pass=''
            moca_user_pass1=''
        elif env == "linux" and app == "moca":
            moca_user_pass=request.GET['source_password']
            moca_user_pass1=request.GET['target_password']
            refs_user_pass=''
            refs_user_pass1=''
        else:
            moca_user_pass=''
            moca_user_pass1=''
            refs_user_pass=''
            refs_user_pass1=''
        print("+"*50)
        print(instance,app,env,customer_name,s_server,d_server,moca_user_pass,moca_user_pass1,refs_user_pass,refs_user_pass1)
        main_output = {'output':[]}
        e = datetime.datetime.now()
        now = e.strftime("%Y-%m-%d %H:%M:%S")
        refreshid = mssql.insert_query_with_id1(columnname = ['awx_job_id','Activity','Customer','App_Type','source_server','source_environment','target_server','target_environment','os_type','Instance','backup_file_name','overall_status','error_message','Start_time','End_time','created_by'],columnvalue = ['',activity,customer_name,app,s_server,senv,d_server,senv1,env,instance,'','In Progress','',now,'',user],tablename = 'App_Refresh_Overall_Status')
        
        print("Printing Refreshid:",refreshid[0][0])

        refresh_obj.refresh(instance,app,env,customer_name,s_server,d_server,moca_user_pass,moca_user_pass1,refs_user_pass,refs_user_pass1,refreshid[0][0],senv3)
    else:
        activity=request.GET['activity']
        refreshid=request.GET['id']
        output =  mssql.getWMSRefreshlogs1(refreshid)
        print(output)
        customer_name=output[0]['Customer_name']
        app=output[0]['App_type']
        s_server=output[0]['Source_Server']
        senv=output[0]['Source_Env']
        d_server=output[0]['Destination_Server']
        senv1=output[0]['Destination_Env']
        env=output[0]['OS_type']
        instance=output[0]['Instance_type']
        bkpfilename=output[0]['Backupfilename']
        main_output = {'output':[]}
        user=request.GET['user']
        if app=="moca":
           moca_user_pass=request.GET['target_password']
           refs_user_pass=''
        else:
           moca_user_pass=''
           refs_user_pass=request.GET['target_password']
        refreshid = mssql.insert_query_with_id1(columnname = ['awx_job_id','Activity','Customer','App_Type','source_server','source_environment','target_server','target_environment','os_type','Instance','backup_file_name','overall_status','error_message','Start_time','End_time','created_by'],columnvalue = ['',activity,customer_name,app,s_server,senv,d_server,senv1,env,instance,bkpfilename,'In Progress','','','',user],tablename = 'App_Refresh_Overall_Status')
        jobids=refresh_obj.rollback(customer_name,env,d_server,app,instance,bkpfilename,moca_user_pass,refs_user_pass,refreshid[0][0])
        
    main_output['output'] = [{'output':'Refresh is in Progress Please check Logs for progress With ID : {}'.format(refreshid[0][0])}]
    return JsonResponse(main_output,safe=False)
    

    
    
    

def start_stop(request):
    returnOutput=[]

    server=request.GET['server']
    
    app=request.GET['app'].lower()
    
    server_type=request.GET['env']
    env=request.GET['server_type']
    c_name=request.GET['customer']
    
    
    
    instance=request.GET['instance']
    action=request.GET['action']

    if action!='start':
       maintenance_end_time=request.GET['maintenance_end_time']
       a=str(maintenance_end_time)
       maintenance_end_time=a.split(" ")[0].split("/")[2]+"/"+a.split(" ")[0].split("/")[1]+"/"+a.split(" ")[0].split("/")[0]+" "+a.split(" ")[1]+":"+"00"
    
    user=request.GET['user']
    moca_password=''
    refs_password=''
    
    if request.GET['moca_password']:
        moca_password=request.GET['moca_password']
    if request.GET['refs_password']:
        refs_password=request.GET['refs_password']
   
   
    
    main_output = {'output':[]}
    e = datetime.datetime.now()
    now = e.strftime("%Y-%m-%d %H:%M:%S")
    
    rolloutid = mssql.insert_query_with_id1(columnname = ['customer_name','server_list','status','jobidlist','created_by','created_on'],columnvalue = [c_name,server,'In Progress','',user,now],tablename = 'start_stop_customer_view')
    
    print("Printing Startstopid:",rolloutid[0][0])
    #t = threading.Thread(target=rollout_obj.trigger_rollout, kwargs=my_dict ,daemon=True)
    #t.start()
    if env!='linux':
        print('Windows')
        if action!='start':
            print("Stop & Restart")
            start_stop_obj.trigger_start_stop(action=action,app=app,customer_name=c_name,env=env,instance=instance,maintenance_end_time=maintenance_end_time,server=server,server_type=server_type,rolloutid=rolloutid[0][0])
        else:
            print("Start")
            start_stop_obj.trigger_start_stop(action=action,app=app,customer_name=c_name,env=env,instance=instance,server=server,server_type=server_type,rolloutid=rolloutid[0][0])
    else:
        print("Linux")
        if action!='start':
            print("Stop & Restart")
            start_stop_obj.trigger_start_stop(action=action,app=app,customer_name=c_name,env=env,instance=instance,maintenance_end_time=maintenance_end_time,server=server,server_type=server_type,rolloutid=rolloutid[0][0],moca_password=moca_password,refs_password=refs_password)
        else:
            print("Start")
            start_stop_obj.trigger_start_stop(action=action,app=app,customer_name=c_name,env=env,instance=instance,server=server,server_type=server_type,rolloutid=rolloutid[0][0],moca_password=moca_password,refs_password=refs_password)


            
    main_output['output'] = [{'output':'Start/Stop  is in Progress Please check Logs for progress With ID : {}'.format(rolloutid[0][0])}]
    return JsonResponse(main_output,safe=False)





def rollout(request):
    #print("FILE!!!", request.FILES)
    file = request.FILES['file']
    fs = FileSystemStorage('media/')
    print("="*50)
    print(file)
    filesave = fs.save(file.name, file)
    listOfiles=[]
    if (str(file).split('.')[-1]=='zip'):
        #print('########################################',file) 
        #print(filesave)	
        #test = ZipFile('C:\\Centralized_Dashboard\\blueyonder_centralized_dashboard\\blueyonder\\media\\{}'.format(filesave), 'r')	
        #print(test)
        #print('C:\\Centralized_Dashboard\\blueyonder_centralized_dashboard\\blueyonder\\media\\{}'.format(filesave))
        with ZipFile('C:\\Centralized_Dashboard\\blueyonder_centralized_dashboard\\blueyonder\\media\\{}'.format(filesave), 'r') as zipObj:
            listOfiles = [name for name in zipObj.namelist() if name.endswith('.zip')]
        #print(listOfiles)
    if (str(file).split('.')[-1]=='tar'):
        tar = tarfile.open('C:\\Centralized_Dashboard\\blueyonder_centralized_dashboard\\blueyonder\\media\\{}'.format(str(file)))
        listOfiles.append(tar.getnames()[0])
    print("*"*50)
    print(listOfiles)
    returnOutput={'foldername':[],'output':[]}
    returnOutput['foldername'] = filesave
    returnOutput['output'] = [{'filename':i.split('.')[0]} for i in listOfiles]
    #print(data)
    return JsonResponse(returnOutput,safe=False)

def get_rollout_status(request):
    headers = {
            "Content-Type": "application/json",
            }
    output =  mssql.getWMSRolloutlogs()
    for out in output:
        print(out)
        completion_count = 0
        joblist = out['Jobid'].split(',')
        print(joblist)
        if(len(joblist) > 0):
            for jobid in joblist:
                if (jobid != ''):
                    
                    response = requests.get('http://10.120.78.130/api/v2/jobs/{}/'.format(int(jobid)), auth = HTTPBasicAuth('1031359', 'Blueyonder@1509$'),headers=headers)
                    print(response)
                    if((json.loads(response.text)['status'] == 'successful') or (json.loads(response.text)['status'] == 'failed')):
                        print(out['ID'])
                        completion_count = completion_count + 1
            if(completion_count == len(joblist)):
                updatestatus = mssql.updateRolloutStatus(out['ID'])
            else:
                print(out['ID'],'inprogress')
    
    return JsonResponse('Status Update',safe=False)


def get_start_stop_status(request):
    headers = {
            "Content-Type": "application/json",
            }
    output =  mssql.getStartStoplogs()
    for out in output:
        print(out)
        completion_count = 0
        joblist = out['Jobid'].split(',')
        print(joblist)
        if(len(joblist) > 0):
            for jobid in joblist:
                if (jobid != ''):
                    
                    response = requests.get('http://10.120.78.130/api/v2/jobs/{}/'.format(int(jobid)), auth = HTTPBasicAuth('1031359', 'Blueyonder@1509$'),headers=headers)
                    print(response)
                    if((json.loads(response.text)['status'] == 'successful') or (json.loads(response.text)['status'] == 'failed')):
                        print(out['ID'])
                        completion_count = completion_count + 1
            if(completion_count == len(joblist)):
                updatestatus = mssql.updateStartStopStatus(out['ID'])
            else:
                print(out['ID'],'inprogress')
    
    return JsonResponse('Status Update',safe=False)



#### RollOut ####

#### API's and  Function related to Application Upgrade ####

def file_upload(file_obj):
    '''
        Uploads files in the media folder
    '''
    #print("FILE!!!", request.FILES)
    file = file_obj
    fs = FileSystemStorage('media/')
    try:
        filesave = fs.save(file.name, file)
        output={'status':0,'file_name':filesave}
    except:
        output={'status':1,'file_name':filesave}
    return output

def doUpgrade(request):
    servername = request.GET['servername']
    customername = request.GET['customer']
    app =  request.GET['app']
    moca_service = request.GET['moca_servicename']
    refs_service = request.GET['refs_servicename']
    created_by = request.GET['suser']
    maintenance_end_time = request.GET['endtime']
    moca_prop_filename = request.GET['moca_propsfile']
    refs_prop_filename = request.GET['refs_propsfile']
    user = request.GET['suser']
    environment = request.GET['env']
    os_name = str.lower(mssql.get_os_name(servername)[0]['os_name'])
    data = {}
    main_output = {'output':[]}
    headers = {
        "Content-Type": "application/json",
        }
    output={'moca_file':{},'refs_file':{}}
    if app =='MOCA' or app =='REFS':
        #output={}
        #print(str(app.lower()+'_file'))
        file = request.FILES[(str(app.lower())+'_file')]
        output[app.lower()+'_file'] =  file_upload(file)
        if app == 'MOCA':
            output['refs_file']['file_name'] = 'NA'
            refs_prop_filename = 'NA'
            refs_service = 'NA'
        if app == 'REFS':
            output['moca_file']['file_name'] = 'NA'
            moca_prop_filename = 'NA'
            moca_service = 'NA'
    else:
        moca_file = request.FILES['moca_file']
        refs_file = request.FILES['refs_file']
        output['moca_file'] =  file_upload(moca_file)
        output['refs_file'] =  file_upload(refs_file)
##    print(output)
    data['extra_vars'] = {
        "moca_source_file": output['moca_file']['file_name'],
        "refs_source_file": output['refs_file']['file_name'],
        "moca_service": moca_service,
        "refs_service": refs_service,
        "moca_prop_filename": moca_prop_filename,
        "refs_prop_filename": refs_prop_filename,
        "customer": customername,
        "environment": environment,
        "maintenance_end_time": maintenance_end_time,
        "created_by": user,
        "app": app,
        "servername":servername
     }
    print(data)
##    if 'windows' in os_name:
##        response = requests.post('http://10.120.78.130/api/v2/job_templates/154/launch/', auth = HTTPBasicAuth('1030243', 'Susilanagaraj@14'),json= data ,headers=headers)
##        jid = (json.loads(response.text)['job'])
##        print(jid)
    response = requests.post('http://10.120.78.130/api/v2/job_templates/154/launch/', auth = HTTPBasicAuth('1030243', 'Susilanagaraj@14'),json= data ,headers=headers)
    jid = (json.loads(response.text)['job'])
    main_output['output'] = [{'output':'Application Upgrade is in Progress Please check Logs for progress With JOB ID : {}'.format(jid)}]
    return JsonResponse(main_output,safe=False)
        
def getWmsService(request):
    servername = request.GET['servername']
    app = str(request.GET['app']).lower()
    if 'both' in app:
        app = 'both'
    data = {}
    data['extra_vars'] = {
            "target_host": servername,
            "app": app}
    headers = {
        "Content-Type": "application/json",
        }
    print(data)
    response = requests.post('http://10.120.78.130/api/v2/job_templates/166/launch/', auth = HTTPBasicAuth('1030243', 'Susilanagaraj@14'),json= data ,headers=headers)
    jid = (json.loads(response.text)['job'])
    print(jid)
    job_status = True
    while  job_status:
        response_jobstatus = requests.get('http://10.120.78.130/api/v2/jobs/{}/'.format(int(jid)), auth = HTTPBasicAuth('1030243', 'Susilanagaraj@14'),headers=headers)
        print((json.loads(response_jobstatus.text)['status']))
        if((json.loads(response_jobstatus.text)['status'] == 'successful') or (json.loads(response_jobstatus.text)['status'] == 'failed')):
            job_status = False
            job_result_staus = json.loads(response_jobstatus.text)['status']
    print('out')
    if job_result_staus == 'successful':
        response_result = requests.get('http://10.120.78.130/api/v2/jobs/{}/job_events/?event__contains=runner_on_ok&task__contains=Get%20WMS%20Service'.format(int(jid)), auth = HTTPBasicAuth('1030243', 'Susilanagaraj@14'),headers=headers)
        data = response_result.json()
        result = (data['results'][0]['event_data']['res']['stdout_lines'][0]).split(',')
        output={'moca_service':[],'refs_service':[]}
        for service in result:
            if 'moca' in service:
                output['moca_service'].append(service)
            else:
                output['refs_service'].append(service)
        
    else:
        output = {'moca_service':['None'],'refs_service':['None']}
    return JsonResponse(output,safe=False)
#### End of Application  Upgrade  Functions ###

#### server reboot ####
def ServerrebootLog(request):
    returnOutput={'headers':[],'output':[]}
    mid = int(request.GET['id'])
    output =  mssql.getWMSServerRebootdetails(mid)
    #print(output)
    returnOutput['headers'].extend(['ID','Activity','ServerNames','Status','CreatedOn'])
    returnOutput['output'].extend(output)
    return JsonResponse(returnOutput,safe=False)

def handleServerreboot(request):
    returnOutput=[]
    servernames = request.GET['servername']
    product = request.GET['prod']
    customer = request.GET['customer']
    themeid = request.GET['theme_id']
    env =request.GET['env']
    servercat =request.GET['servercat']
    pid = request.GET['pid']
    user = request.GET['user']
    main_output = {'output':[]}
    taskname = 'Server Reboot'
    e = datetime.datetime.now()
    now = e.strftime("%Y-%m-%d %H:%M:%S")
    rebootid = mssql.insert_query_with_id(columnname = ['activity','customer_name','server_name','status','product_id','created_by','created_on'],columnvalue = [taskname,customer,servernames,'In Progress',pid,user,now],tablename = 'wms_serverreboot_details')
    my_dict = {'servernames':servernames, 'rebootid':str(rebootid[0][0])}
    print(my_dict)
    t = threading.Thread(target=main_obj.get_reboot_server, kwargs=my_dict ,daemon=True)
    t.start()
    #main_obj.get_reboot_server(servernames,str(rebootid[0][0]))
    main_output['output'] = [{'output':'Server Reboot is in Progress Please check Logs for progress With ID : {}'.format(rebootid[0][0])}]
    return JsonResponse(main_output,safe=False)
#### server reboot ####

#### brick ftp mail ####
def brickftpuserdeletion(request):
    pid = int(request.GET['id'])
    output =  mssql.deleteBrickftpmail(pid)
    return JsonResponse(output,safe=False)

def createBrickftpmail(request):
    username = request.GET['username']
    email = request.GET['mail']
    insertedid = mssql.insert_query_with_id(columnname = ['recipient_name','email'],columnvalue = [username,email],tablename = 'brick_ftp_recipient')
    return JsonResponse(insertedid,safe=False)
#### brick ftp mail ####

def OutputLog(request):
    returnOutput={'headers':[],'output':[]}
    mid = int(request.GET['id'])
    pid = int(request.GET['pid'])
    if mid == 1:
        output =  mssql.getOutputMaintenancelogs(pid)
        returnOutput['headers'].extend(['CreationID','MaintenanceId','MaitenanceName','StartTime','EndTime','ServerNames','Status','CreatedBy'])
        returnOutput['output'].extend(output)
    if mid == 0:
        output =  mssql.get_output_logs(pid)
        returnOutput['headers'].extend(['id','Customer Name','server Name','Theme Name','Task Name','Name','Status','Last Updated Time','Viewed By','Date'])
        returnOutput['output'].extend(output)
    #### brick ftp ####
    if mid == 2:
        output =  mssql.get_brickftp_monitoring()
        returnOutput['headers'].extend(['URL','Connection','Upload','Download','Delete File','Last Checked Time(IST)'])
        returnOutput['output'].extend(output)
    #### server reboot ####
    if mid == 3:
       output =  mssql.getTMSServerRebootlogs()
       returnOutput['headers'].extend(['ID','Activity','CustomerName','Status','ServerNames','CreatedBy','CreatedOn','Action'])
       returnOutput['output'].extend(output)
    #### brick ftp mail ####
    if mid == 4:
       output =  mssql.get_brickftp_monitoring_mail()
       returnOutput['headers'].extend(['ID','UserName','MailId','Action'])
       returnOutput['output'].extend(output)
    #### process level logs ####
    if mid == 5:
       output =  mssql.get_processlevel_main_logs()
       returnOutput['headers'].extend(['ProcessID','CustomerName','Status','SubmittedBy','DateTime'])
       returnOutput['output'].extend(output)
    #### SCPO POST DB REFRESH ####
    if mid == 7:
       output =  mssql.get_scpo_post_db()
       returnOutput['headers'].extend(['RID','CustomerName','Environment','ServerName','Schema','Requestor','RequestorDate','Description','Status'])
       returnOutput['output'].extend(output)
    return JsonResponse(returnOutput,safe=False)

#### process level logs ####
def ProcessLevelSubLog(request):
    returnOutput={'headers':[],'output':[]}
    pid = int(request.GET['id'])
    output =  mssql.get_processlevel_sub_logs(pid)
    #print(output)
    returnOutput['headers'].extend(['ID','MainID','ProcessID','CheckType','Customer','P1','P2','P3','P4','Server','Result','Status','CheckTime','Expected'])
    returnOutput['output'].extend(output)
    return JsonResponse(returnOutput,safe=False)
#### process level logs ####

#### Customer On Boarding ####
def get_tmscustomerdata(request):
    returnOutput={'headers':[],'output':[]}
    output =  mssql.getTMSCustomerdata()
    #print(output)
    returnOutput['headers'].extend(['ID','CustomerName','SubRegion','Environment','TaskName','TMSCustomerName'])
    returnOutput['output'].extend(output)
    return JsonResponse(returnOutput,safe=False)

def get_tmssinglecustomerdata(request):
    cid = int(request.GET['id'])
    output =  mssql.getTMSSingleCustomerdata(cid)
    #print(output)
    return JsonResponse(output,safe=False)
#### Customer On Boarding ####

#### Customer_server Subregion ####
def get_subregionData(request):
    returnOutput={'headers':[],'output':[]}
    output =  mssql.get_subregion_db()
    #print(output)
    returnOutput['headers'].extend(['ID','ServerName','CustomerName','Location','EnvironmentName','CloudEnvironment','SubRegion'])
    returnOutput['output'].extend(output)
    return JsonResponse(returnOutput,safe=False)

def update_subRegion(request):
    returnOutput={'headers':[],'output':[]}
    rid = request.GET['id']
    sub_region = request.GET['sub_region']
    success = 0
    failed = 0
    ids = []
    #print("before for")
    for i in rid.split(","):
        output =  mssql.update_subRegionData(i,sub_region)
        #print("here for loop")
        if output == 'Success':
            success = success+1
        else:
            failed = failed+1
            ids.extend(i)
    if failed > 0:
        msg = "Some Id's failed to update ("+str(', '.join(ids))+")"
    else:
        msg = "Successfully updated"
    #print(msg)
    return JsonResponse(msg,safe=False)
#### Customer_server Subregion ####

##def handleRequest(request):
##    returnOutput=[]
##    servernames = request.GET['servername']
##    product = request.GET['prod']
##    customer = request.GET['customer']
##    tasknames = request.GET['task_id']    
##    themeid = request.GET['theme_id']
##    funcname= [mssql.func_name(task) for task in tasknames.split(',')]
##    output ={'header':tasknames.split(',')}
##    for server in servernames.split(','):
##        output = {'servname':server}
##        for func in funcname:
##            output.update(handleD.callfunction(server,func['func_name'][0][0]))
##        returnOutput.append(output)
##            
##    return JsonResponse(returnOutput,safe=False)

def handleRequest111(request):
    returnOutput=[]
    servernames = request.GET['servername']
    product = request.GET['prod']
    customer = request.GET['customer']
    tasknames = request.GET['task_id']
    themeid = request.GET['theme_id']
    env = int(request.GET['env'])
    servercat =request.GET['servercat']
    pid = request.GET['pid']
    accountType = request.GET['as2acctype']
    accountName = request.GET['as2acc']
    start_date = request.GET['as2starttime']
    end_date = request.GET['as2endtime']
    #print(customer,pid)
    main_output = {'header':[],'output':[]}
    for taskname in tasknames.split(','):

        if 'ICMP Ping' == taskname:
            main_output['header'].extend(['ICMP Last Value','ICMP Last Clock'])
        elif 'CPU Utilization' == taskname:
            main_output['header'].extend(['CPU Utilization Last Value','CPU Utilization Last Clock'])
        elif 'Memory Utilization' == taskname:
            main_output['header'].extend(['Memory Utilization Last Value','Memory Utilization Last Clock'])
        elif 'Service Status' == taskname:
            main_output['header'].extend(['Service Name','Service Last Value','Service Last Clock'])
        elif 'Port Status' == taskname:
            main_output['header'].extend(['Port Name', 'Port Last Value','Port Last Clock'])
        elif 'Internal URL Status' == taskname:
            main_output['header'].extend(['Internal URL Name','Internal URL Value','Internal URL Clock'])
        elif 'Public URL Status' == taskname:
            main_output['header'].extend(['Public URL Name','Public URL Value','Public URL Clock'])
        elif 'Database Growth' == taskname:
            main_output['header'].extend(['Servername','DBName','OWNER','TABLE_NAME','NUM_ROWS'])
        elif 'Database Session Count' == taskname:
            main_output['header'].extend(['Database Session Name','Database Session Value','Database Session Clock'])
        elif 'CIS Adapter Status' == taskname:
            main_output['header'].extend(['CIS Adapter Name','CIS Adapter Status','CIS Adapter Last time'])
        elif 'Web Services Status' == taskname:
            main_output['header'].extend(['Web Services Name','Web Services Status','Web Services Last Time'])
        elif 'File Age Monitor' == taskname:
            main_output['header'].extend(['File Age customer','File Age Good Count','File Age Bad Count'])
        elif 'Database Monitor' == taskname:
            main_output['header'].extend(['DB customer','DB Good Count','DB Bad Count'])
        elif 'Process Level' == taskname:
            main_output['header'].extend(['Process Name','Number of Process','Process Last checked Time'])
        elif 'Start App Service' == taskname or 'Stop App Service' == taskname:
            main_output['header'].extend(['Service Name','Status'])
        elif 'UI Sanity Checks' == taskname:
            main_output['header'].extend(['Name','Test Name','Status','node'])
        elif 'UI Availability' == taskname:
            main_output['header'].extend(['Name','Test Name','Check Name','Status','node'])
        elif 'I/O Rate' == taskname:
            main_output['header'].extend(['IO Name','IO Value','Last checked Time'])
        elif 'AS2/SFTP' == taskname:
            main_output['header'].extend(['Gateway Server','Zabbix Location','Gateway URL Name','Gateway URL Value','Gateway URL Last Clock'])
            main_output['header'].extend(['Mailbox','Transport','Start_Date','End_Date','Direction','Status','File_Name','File_Size_Bytes'])
        elif 'Server Reboot' == taskname:
            main_output['header'].extend(['status'])
        else:
            main_output['header'].append(taskname)
    if env == 1:
        prod=1
    else:
        prod=2
    funcname= [mssql.func_name(task) for task in tasknames.split(',')]    
##    main_output['header'] = tasknames.split(',')
    func_name = [a['func_name'][0][0]  for a in funcname]
    #print(func_name)
    # or func['func_name'][0][0] == "" or func['func_name'][0][0] == ""
    variable = []
    strHtml = ""
    if 'main' in func_name :
        result = (handleD.callfunction('',themeid,customer,pid,servercat,prod,'main','','','',''))
        #print(result)
        func_name.remove('main')
        variable.extend(a for a in result)
    if 'ui_availability' in func_name :
        result = (handleD.callfunction('',themeid,customer,pid,servercat,prod,'ui_availability','','','',''))
        #print(result)
        func_name.remove('ui_availability')
        variable.extend(a for a in result)
    if 'gateway_details' in func_name :
        result1 = (handleD.callfunction('',themeid,customer,pid,servercat,prod,'gateway_details','','','',''))
        #print(result1)
        variable.extend(a for a in result1)
        result2 = (handleD.callfunction('',themeid,customer,pid,servercat,prod,'transfer_report',accountType,accountName,start_date,end_date))
        variable.extend(a for a in result2)
        func_name.remove('gateway_details')
    if 'file_monitorDetails' in func_name :
        result = (handleD.callfunction('',themeid,customer,pid,servercat,prod,'file_monitorDetails','','','',''))
        #print(result) 'File Age customer','File Age Good Count','File Age Bad Count'
        strHtml += "<table><thead><th>File Age customer</th><th>File Age Good Count</th><th>File Age Bad Count</th></thead>"
        for res in result:
            strHtml += "<tr><td>"+res["File Age customer"]+"</td><td>"+str(res["File Age Good Count"])+"</td><td>"+str(res["File Age Bad Count"])+"</td></tr>"
        strHtml += "</table>"
        func_name.remove('file_monitorDetails')
        variable.extend(a for a in result)
    if 'db_monitorDetails' in func_name :
        result_1 = (handleD.callfunction('',themeid,customer,pid,servercat,prod,'db_monitorDetails','','','',''))
        #'DB customer','DB Good Count','DB Bad Count'
        table = '''<TableContainer className={classes.container}>
            <Table stickyHeader aria-label="sticky table" responsive>
              <TableHead style={{backgroundColor:'rgb(92 147 217)'}}>
           
                <TableRow >              
                <TableCell
                  style={{ minWidth: column.minWidth }}
                >
                  'DB customer'
                </TableCell>
                <TableCell
                  style={{ minWidth: column.minWidth }}
                >
                  'DB Good Count'
                </TableCell>
                <TableCell
                  style={{ minWidth: column.minWidth }}
                >
                  'DB Bad Count'
                </TableCell>
            </TableRow>
           
              </TableHead>
             
             
              <TableBody>
                <TableRow hover role="checkbox" tabIndex={-1} key={row.code}>'''
        for res in result_1:
            table += '''
                      <TableCell key="'''+res["DB customer"]+'''" align={column.align}>
                            '''+res["DB customer"]+'''
                      </TableCell>
                      <TableCell key="'''+str(res["DB Good Count"])+'''" align={column.align}>
                            '''+str(res["DB Good Count"])+'''
                      </TableCell>
                      <TableCell key="'''+str(res["DB Bad Count"])+'''" align={column.align}>
                            '''+str(res["DB Bad Count"])+'''
                      </TableCell>'''
        table +='''</TableRow>
          </TableBody>
            </Table>
          </TableContainer>'''
        table = table.replace("\n",'')
        '''strHtml += "<table><thead><th>DB customer</th><th>DB Good Count</th><th>DB Bad Count</th></thead>"
        for res in result_1:
            strHtml += "<tr><td>"+res["DB customer"]+"</td><td>"+str(res["DB Good Count"])+"</td><td>"+str(res["DB Bad Count"])+"</td></tr>"
        strHtml += "</table>"'''
        func_name.remove('db_monitorDetails')
        variable.extend(a for a in result_1)
    if 'reboot_server_tms' in func_name:
        result_1 = (handleD.callfunction(servernames,themeid,customer,pid,servercat,prod,'reboot_server_tms','','','',''))
        func_name.remove('reboot_server_tms')
        variable.extend(a for a in result_1)
    if 'file_monitorDetails' not in func_name or 'db_monitorDetails' not in func_name:
        print(func_name)
        for server in servernames.split(','):
            output = {'server name':server}
            for func in func_name:
                if (func == "public_url" or func == "internal_url" or func == "service_status" or func == "port_status" or func == "db_session" or func == "db_growth" or func == "cis_Adapter" or func == "web_service" or func == "start_app_service" or func == "stop_app_service" or func == "process_validation" or func == "IO_rate"):
                    #print(server)
                    result = (handleD.callfunction(server,themeid,customer,pid,servercat,prod,func,'','','',''))
                    #print(result)
                    variable.extend(a for a in result)
                else:
                    output.update(handleD.callfunction(server,themeid,customer,pid,servercat,prod,func,'','','',''))
            if output != {'server name':server}:
                variable.insert(0,output)
            #returnOutput.append(variable)
            
    main_output['output'] = table
    return JsonResponse(main_output,safe=False)


def get_tms_html_report(request):
    '''
        Function created by Aravindhghosh P (1027319)
        Function Details: get_tms_html_report() this function will generate reports and share the file to UI
    '''
    jsonFile = request.POST['customers']
    downloadType = request.POST['overall_type']
    print(downloadType)
    jsonFile=jsonFile.split(';')
    jsonFile=jsonFile[:-1]

    output = []
    print(jsonFile)
    for i in jsonFile:
        try:
            output.append(json.loads(i))
        except Exception as e:
            print(e)
    
    #html_input = open(jsonFile)
    #print(html_input)
    #output = json.load(jsonFile)
    # print(output)
    if (downloadType == "overall"):
        htmlFileName = "html_report_"+ str((datetime.datetime.now()).strftime("%Y_%m_%d_%H_%M_%S"))
        finalReportFile = "D:\\TMS_Prod\\UI_HTML_Report\\{}.html".format(htmlFileName)

    html = ""
    html += """<html>
    <title>
        TMS Report
    </title>
    <style>
        /* Style the tab */
        .tab {
            overflow-y: auto;
            border: 1px solid #ccc;
            background-color: #107bd3;
        }

        /* Style the buttons inside the tab */
        .tab button {
            background-color: inherit;
            float: left;
            border: none;
            outline: none;
            cursor: pointer;
            padding: 14px 16px;
            transition: 0.3s;
            font-size: 17px;
            color: white;
            font-weight: bolder;
            border: 2px solid #ABB2B9;
        }

        /* Change background color of buttons on hover */
        .tab button:hover {
            background-color: rgb(176, 240, 176);
        }

        /* Create an active/current tablink class */
        .tab button.active {
            background-color: #0c4c80;
            color: white;
            font-weight: bolder;
        }

        /* Style the tab content */
        .tabcontent {
            display: none;
            padding: 6px 12px;
            border-top: none;
            background-color: #ffffff;
            height: 90%;
            overflow-y: auto;
            border: 2px solid rgb(104, 104, 104);
        }

        .taskTitle {
            text-align: center;
            background-color: #04AA6D;
            border-radius: 5px;
            color: #ffffff;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-top: 5px;
        }

        .tableDiv {
            align-items: center;
            padding: 15px;
            overflow-x: auto;
        }

        .tablecontent {
            font-family: Arial, Helvetica, sans-serif;
            border-collapse: collapse;
            width: 100%;
            padding: 5px;
            margin-top: 10px;
        }

        .tablecontent th,
        .tablecontent td {
            border: 1px solid rgb(146, 146, 146);
            padding: 8px;
        }

        .tablecontent th {
            padding-top: 12px;
            padding-bottom: 12px;
            text-align: center;
            background-color: #107bd3;
            color: white;
            border: 2px solid rgb(64, 64, 64);
        }

        .tablecontent tr:nth-child(even) {
            background-color: #f2f2f2;
        }

        .tablecontent tr:hover {
            background-color: rgb(232, 237, 191);
        }

        .tablecontent tr[data-stat="Good"] {
            background-color: #CEF3D3 !important;
        }

        .tablecontent tr[data-stat="Bad"] {
            background-color: rgb(242, 150, 150) !important;
        }

        .tablecontent tr[data-stat="NA"] {
            background-color: rgb(200, 199, 199) !important;
        }
        
        /* width */
        ::-webkit-scrollbar {
            width: 10px;
        }

        /* Track */
        ::-webkit-scrollbar-track {
            background: #f1f1f1; 
            border-radius: 10px; 
        }
        
        /* Handle */
        ::-webkit-scrollbar-thumb {
            background: #00B7F1; 
            border-radius: 10px; 
        }

        /* Handle on hover */
        ::-webkit-scrollbar-thumb:hover {
            background: #107bd3; 
            border-radius: 10px; 
        }
    </style>
    <body style="background-color:rgb(231, 231, 231)">
        <h2 style="text-align: center;">TMS Health check Report</h2>

        <div class="tab">"""

    ## print("Length of the output:")
    count = 0
    for x in output:
        customer_name = mssql.tmscustomerbyid(str(x['customer_id']))
        count = count + 1
        if count == 1:
            html += '''
            <button class="tablinks" onclick="openCustomer(event, 'customer''' + str(count) + '''')" id="defaultOpen">''' + customer_name + '''</button>'''
        else:
            html += '''
            <button class="tablinks" onclick="openCustomer(event, 'customer''' + str(count) + '''')">''' + customer_name + '''</button>'''

    html += """
        </div>"""

    count = 0
    for x in output:
        count = count + 1
        #print(len(x['value']['Summary Table']))
        html += '''
        <div id="customer''' + str(count) + '''" class="tabcontent">
        '''
        # Start App Service
        try:
            if len(x['value']['Start App Service']) > 0:
                html += '''
                <div class="taskTitle">
                    <h4 class="taskTitleh4">Start App Service</h4>
                </div>
                <div class="tableDiv">
                    <table class="tablecontent">
                        <thead>
                            <tr>
                '''
                for y in x['headers']['Start App Service']:
                    html += '''                        <th>'''+str(y)+'''</th>
                            '''
                html += '''                    </tr>
                        </thead>
                        <tbody>'''
                for y in x['value']['Start App Service']:
                    html += '''
                            <tr>
                                <td>'''+str(y['Server Name'])+'''</td>
                                <td>'''+str(y['Service Name'])+'''</td>
                                <td>'''+str(y['Status'])+'''</td>
                            </tr>'''
                html += '''
                        </tbody>
                    </table>
                </div>'''
        except Exception as e:
            print(e)
            
        # Summary Table
        try:
            if len(x['value']['Summary Table']) > 0:
                html += '''
                <div class="taskTitle">
                    <h4 class="taskTitleh4">Summary Table</h4>
                </div>
                <div class="tableDiv">
                    <table class="tablecontent">
                        <thead>
                            <tr>
                '''
                for y in x['headers']['Summary Table']:
                    html += '''                        <th>'''+str(y)+'''</th>
                            '''
                html += '''                    </tr>
                        </thead>
                        <tbody>'''
                for y in x['value']['Summary Table']:
                    html += """
                            <tr>
                                <td>"""+str(y['Task Name'])+"""</td>
                                <td>"""+str(y['Good Count'])+"""</td>
                                <td>"""+str(y['Bad Count'])+"""</td>
                                <td>"""+str(y['NA Count'])+"""</td>
                            </tr>"""
                html += '''
                        </tbody>
                    </table>
                </div>'''
        except Exception as e:
            print(e)

        # ICMP Ping
        try:
            if len(x['value']['ICMP Ping']) > 0:
                html += '''
                <div class="taskTitle">
                    <h4 class="taskTitleh4">ICMP Ping</h4>
                </div>
                <div class="tableDiv">
                    <table class="tablecontent">
                        <thead>
                            <tr>
                '''
                for y in x['headers']['ICMP Ping']:
                    html += '''                        <th>'''+str(y)+'''</th>
                            '''
                html += '''                    </tr>
                        </thead>
                        <tbody>'''
                for y in x['value']['ICMP Ping']:
                    html += '''
                            <tr data-stat="'''+str(y['Status'])+'''">
                                <td>'''+str(y['Server Name'])+'''</td>
                                <td>'''+str(y['ICMP Last Value'])+'''</td>
                                <td>'''+str(y['ICMP Last Clock'])+'''</td>
                                <td>'''+str(y['Last Checked'])+'''</td>
                                <td>'''+str(y['Status'])+'''</td>
                            </tr>'''
                html += '''
                        </tbody>
                    </table>
                </div>'''
        except Exception as e:
            print(e)

        # Service Status
        try:
            if len(x['value']['Service Status']) > 0:
                html += '''
                <div class="taskTitle">
                    <h4 class="taskTitleh4">Service Status</h4>
                </div>
                <div class="tableDiv">
                    <table class="tablecontent">
                        <thead>
                            <tr>
                '''
                for y in x['headers']['Service Status']:
                    html += '''                        <th>'''+str(y)+'''</th>
                            '''
                html += '''                    </tr>
                        </thead>
                        <tbody>'''
                for y in x['value']['Service Status']:
                    html += '''
                            <tr data-stat="'''+str(y['Status'])+'''">
                                <td>'''+str(y['Server Name'])+'''</td>
                                <td>'''+str(y['Service Name'])+'''</td>
                                <td>'''+str(y['Service Last Value'])+'''</td>
                                <td>'''+str(y['Service Last Clock'])+'''</td>
                                <td>'''+str(y['Last Checked'])+'''</td>
                                <td>'''+str(y['Status'])+'''</td>
                            </tr>'''
                html += '''
                        </tbody>
                    </table>
                </div>'''
        except Exception as e:
            print(e)

        # Port Status
        try:
            if len(x['value']['Port Status']) > 0:
                html += '''
                <div class="taskTitle">
                    <h4 class="taskTitleh4">Port Status</h4>
                </div>
                <div class="tableDiv">
                    <table class="tablecontent">
                        <thead>
                            <tr>
                '''
                for y in x['headers']['Port Status']:
                    html += '''                        <th>'''+str(y)+'''</th>
                            '''
                html += '''                    </tr>
                        </thead>
                        <tbody>'''
                for y in x['value']['Port Status']:
                    html += '''
                            <tr data-stat="'''+str(y['Status'])+'''">
                                <td>'''+str(y['Server Name'])+'''</td>
                                <td>'''+str(y['Port Name'])+'''</td>
                                <td>'''+str(y['Port Last Value'])+'''</td>
                                <td>'''+str(y['Port Last Clock'])+'''</td>
                                <td>'''+str(y['Last Checked'])+'''</td>
                                <td>'''+str(y['Status'])+'''</td>
                            </tr>'''
                html += '''
                        </tbody>
                    </table>
                </div>'''
        except Exception as e:
            print(e)

        # CIS Adapter Statuss
        try:
            if len(x['value']['CIS Adapter Status']) > 0:
                html += '''
                <div class="taskTitle">
                    <h4 class="taskTitleh4">CIS Adapter Status</h4>
                </div>
                <div class="tableDiv">
                    <table class="tablecontent">
                        <thead>
                            <tr>
                '''
                for y in x['headers']['CIS Adapter Status']:
                    html += '''                        <th>'''+str(y)+'''</th>
                            '''
                html += '''                    </tr>
                        </thead>
                        <tbody>'''
                for y in x['value']['CIS Adapter Status']:
                    html += '''
                            <tr data-stat="'''+str(y['Status'])+'''">
                                <td>'''+str(y['Server Name'])+'''</td>
                                <td>'''+str(y['CIS Adapter Name'])+'''</td>
                                <td>'''+str(y['CIS Adapter Status'])+'''</td>
                                <td>'''+str(y['CIS Adapter Duration'])+'''</td>
                                <td>'''+str(y['CIS Adapter Last time'])+'''</td>
                                <td>'''+str(y['Status'])+'''</td>
                            </tr>'''
                html += '''
                        </tbody>
                    </table>
                </div>'''
        except Exception as e:
            print(e)

        # Web Services Status
        try:
            if len(x['value']['Web Services Status']) > 0:
                html += '''
                <div class="taskTitle">
                    <h4 class="taskTitleh4">Web Services Status</h4>
                </div>
                <div class="tableDiv">
                    <table class="tablecontent">
                        <thead>
                            <tr>
                '''
                for y in x['headers']['Web Services Status']:
                    html += '''                        <th>'''+str(y)+'''</th>
                            '''
                html += '''                    </tr>
                        </thead>
                        <tbody>'''
                for y in x['value']['Web Services Status']:
                    html += '''
                            <tr data-stat="'''+str(y['Status'])+'''">
                                <td>'''+str(y['Server Name'])+'''</td>
                                <td>'''+str(y['Web Services Name'])+'''</td>
                                <td>'''+str(y['Web Services Status'])+'''</td>
                                <td>'''+str(y['Web Services URL'])+'''</td>
                                <td>'''+str(y['Web Services Last Time'])+'''</td>
                                <td>'''+str(y['Status'])+'''</td>
                            </tr>'''
                html += '''
                        </tbody>
                    </table>
                </div>'''
        except Exception as e:
            print(e)

        # Internal URL Status
        try:
            if len(x['value']['Internal URL Status']) > 0:
                html += '''
                <div class="taskTitle">
                    <h4 class="taskTitleh4">Internal URL Status</h4>
                </div>
                <div class="tableDiv">
                    <table class="tablecontent">
                        <thead>
                            <tr>
                '''
                for y in x['headers']['Internal URL Status']:
                    html += '''                        <th>'''+str(y)+'''</th>
                            '''
                html += '''                    </tr>
                        </thead>
                        <tbody>'''
                for y in x['value']['Internal URL Status']:
                    html += '''
                            <tr data-stat="'''+str(y['Status'])+'''">
                                <td>'''+str(y['Server Name'])+'''</td>
                                <td>'''+str(y['Internal URL Name'])+'''</td>
                                <td>'''+str(y['Internal URL Value'])+'''</td>
                                <td>'''+str(y['Internal URL Clock'])+'''</td>
                                <td>'''+str(y['Last Checked'])+'''</td>
                                <td>'''+str(y['Status'])+'''</td>
                            </tr>'''
                html += '''
                        </tbody>
                    </table>
                </div>'''
        except Exception as e:
            print(e)

        # Public URL Status
        try:
            if len(x['value']['Public URL Status']) > 0:
                html += '''
                <div class="taskTitle">
                    <h4 class="taskTitleh4">Public URL Status</h4>
                </div>
                <div class="tableDiv">
                    <table class="tablecontent">
                        <thead>
                            <tr>
                '''
                for y in x['headers']['Public URL Status']:
                    html += '''                        <th>'''+str(y)+'''</th>
                            '''
                html += '''                    </tr>
                        </thead>
                        <tbody>'''
                for y in x['value']['Public URL Status']:
                    html += '''
                            <tr data-stat="'''+str(y['Status'])+'''">
                                <td>'''+str(y['Public URL Name'])+'''</td>
                                <td>'''+str(y['Public URL Value'])+'''</td>
                                <td>'''+str(y['Public URL Clock'])+'''</td>
                                <td>'''+str(y['Last Checked'])+'''</td>
                                <td>'''+str(y['Status'])+'''</td>
                            </tr>'''
                html += '''
                        </tbody>
                    </table>
                </div>'''
        except Exception as e:
            print(e)

        # UI Availability
        try:
            if len(x['value']['UI Availability']) > 0:
                html += '''
                <div class="taskTitle">
                    <h4 class="taskTitleh4">UI Availability</h4>
                </div>
                <div class="tableDiv">
                    <table class="tablecontent">
                        <thead>
                            <tr>
                '''
                for y in x['headers']['UI Availability']:
                    html += '''                        <th>'''+str(y)+'''</th>
                            '''
                html += '''                    </tr>
                        </thead>
                        <tbody>'''
                print(x['value']['UI Availability'])
                for y in x['value']['UI Availability']:
                    html += '''
                            <tr data-stat="'''+str(y['Status'])+'''">
                                <td>'''+str(y['Name'])+'''</td>
                                <td>'''+str(y['Test Name'])+'''</td>
                                <td>'''+str(y['Test_Status'])+'''</td>
                                <td>'''+str(y['node'])+'''</td>
                                <td>'''+str(y['Time'])+'''</td>
                                <td>'''+str(y['Status'])+'''</td>
                            </tr>'''
                html += '''
                        </tbody>
                    </table>
                </div>'''
        except Exception as e:
            print(e)

        # File Age Monitor
        try:
            if len(x['value']['File Age Monitor']) > 0:
                html += '''
                <div class="taskTitle">
                    <h4 class="taskTitleh4">File Age Monitor</h4>
                </div>
                <div class="tableDiv">
                    <table class="tablecontent">
                        <thead>
                            <tr>
                '''
                for y in x['headers']['File Age Monitor']:
                    html += '''                        <th>'''+str(y)+'''</th>
                            '''
                html += '''                    </tr>
                        </thead>
                        <tbody>'''
                for y in x['value']['File Age Monitor']:
                    html += '''
                            <tr>
                                <td>'''+str(y['File Age customer'])+'''</td>
                                <td>'''+str(y['File Age Good Count'])+'''</td>
                                <td>'''+str(y['File Age Bad Count'])+'''</td>
                            </tr>'''
                html += '''
                        </tbody>
                    </table>
                </div>'''
        except Exception as e:
            print(e)

        # Database Monitor
        try:
            if len(x['value']['Database Monitor']) > 0:
                html += '''
                <div class="taskTitle">
                    <h4 class="taskTitleh4">Database Monitor</h4>
                </div>
                <div class="tableDiv">
                    <table class="tablecontent">
                        <thead>
                            <tr>
                '''
                for y in x['headers']['Database Monitor']:
                    html += '''                        <th>'''+str(y)+'''</th>
                            '''
                html += '''                    </tr>
                        </thead>
                        <tbody>'''
                for y in x['value']['Database Monitor']:
                    html += '''
                            <tr>
                                <td>'''+str(y['DB customer'])+'''</td>
                                <td>'''+str(y['DB Good Count'])+'''</td>
                                <td>'''+str(y['DB Bad Count'])+'''</td>
                            </tr>'''
                html += '''
                        </tbody>
                    </table>
                </div>'''
        except Exception as e:
            print(e)

        # Process Level
        try:
            if len(x['value']['Process Level']) > 0:
                print("Process Level")
                for y in x['value']['Process Level']:
                    if (y['Request_Id'] != 'NA'):
                        output =  mssql.get_processlevel_sub_logs(y['Request_Id'])
                        if len(output) > 0:
                            html += '''
                            <div class="taskTitle">
                                <h4 class="taskTitleh4">Process Level</h4>
                            </div>
                            <div class="tableDiv">
                                <table class="tablecontent">
                                    <thead>
                                        <tr>
                            '''
                            html += '''                        <th>ProcessID</th>
                                                                   <th>Check Type</th>
                                                                   <th>Customer</th>
                                                                   <th>P1</th>
                                                                   <th>P2</th>
                                                                   <th>P3</th>
                                                                   <th>P4</th>
                                                                   <th>Server</th>
                                                                   <th>Result</th>
                                                                   <th>Status</th>
                                                                   <th>CheckTime</th>
                                                                   <th>Expected</th>
                                        '''
                            html += '''                    </tr>
                                    </thead>
                                    <tbody>'''
                            for z in output:
                                html += '''
                                        <tr data-stat="'''+str(z['Result']).capitalize()+'''">
                                            <td>'''+str(z['ProcessID'])+'''</td>
                                            <td>'''+str(z['CheckType'])+'''</td>
                                            <td>'''+str(z['Customer'])+'''</td>
                                            <td>'''+str(z['P1'])+'''</td>
                                            <td>'''+str(z['P2'])+'''</td>
                                            <td>'''+str(z['P3'])+'''</td>
                                            <td>'''+str(z['P4'])+'''</td>
                                            <td>'''+str(z['Server'])+'''</td>
                                            <td>'''+str(z['Result']).capitalize()+'''</td>
                                            <td>'''+str(z['Status'])+'''</td>
                                            <td>'''+str(z['CheckTime'])+'''</td>
                                            <td>'''+str(z['Expected'])+'''</td>
                                        </tr>'''
                            html += '''
                                    </tbody>
                                </table>
                            </div>'''
                        else:
                            html += '''
                            <div class="taskTitle">
                                <h4 class="taskTitleh4">Process Validation</h4>
                            </div>
                            <div class="tableDiv">
                                <table class="tablecontent">
                                    <thead>
                                        <tr>
                                                    <th>Request Id</th><th>Status</th>
                                                            </tr>
                                    </thead>
                                    <tbody>
                                        <tr">
                                            <td>'''+str(y['Request_Id'])+'''</td>
                                            <td>'''+str(y['Status'])+'''</td>
                                        </tr>'''
                            html += '''
                                    </tbody>
                                </table>
                            </div>'''
                    else:
                        html += '''
                        <div class="taskTitle">
                            <h4 class="taskTitleh4">Process Validation</h4>
                        </div>
                        <div class="tableDiv">
                            <table class="tablecontent">
                                <thead>
                                    <tr>
                                                <th>Request Id</th><th>Status</th>
                                                        </tr>
                                </thead>
                                <tbody>
                                    <tr">
                                        <td>'''+str(y['Request_Id'])+'''</td>
                                        <td>'''+str(y['Status'])+'''</td>
                                    </tr>'''
                        html += '''
                                </tbody>
                            </table>
                        </div>'''
        except Exception as e:
            print(e)

        #CPU Utilization
        try:
            if len(x['value']['CPU Utilization']) > 0:
                html += '''
                <div class="taskTitle">
                    <h4 class="taskTitleh4">CPU Utilization</h4>
                </div>
                <div class="tableDiv">
                    <table class="tablecontent">
                        <thead>
                            <tr>
                '''
                for y in x['headers']['CPU Utilization']:
                    html += '''                        <th>'''+str(y)+'''</th>
                            '''
                html += '''                    </tr>
                        </thead>
                        <tbody>'''
                print(x['value']['CPU Utilization'])
                for y in x['value']['CPU Utilization']:
                    html += '''
                            <tr data-stat="'''+str(y['Status'])+'''">
                                <td>'''+str(y['Server Name'])+'''</td>
                                <td>'''+str(y['CPU Utilization Last Value'])+'''</td>
                                <td>'''+str(y['CPU Utilization Last Clock'])+'''</td>
                                <td>'''+str(y['Last Checked'])+'''</td>
                                <td>'''+str(y['Threshold'])+'''</td>
                                <td>'''+str(y['Status'])+'''</td>
                            </tr>'''
                html += '''
                        </tbody>
                    </table>
                </div>'''
        except Exception as e:
            print(e)

        #Memory Utilization
        try:
            if len(x['value']['Memory Utilization']) > 0:
                html += '''
                <div class="taskTitle">
                    <h4 class="taskTitleh4">Memory Utilization</h4>
                </div>
                <div class="tableDiv">
                    <table class="tablecontent">
                        <thead>
                            <tr>
                '''
                for y in x['headers']['Memory Utilization']:
                    html += '''                        <th>'''+str(y)+'''</th>
                            '''
                html += '''                    </tr>
                        </thead>
                        <tbody>'''
                print(x['value']['Memory Utilization'])
                for y in x['value']['Memory Utilization']:
                    html += '''
                            <tr data-stat="'''+str(y['Status'])+'''">
                                <td>'''+str(y['Server Name'])+'''</td>
                                <td>'''+str(y['Free Memory Last Value'])+'''</td>
                                <td>'''+str(y['Free Memory Last Clock'])+'''</td>
                                <td>'''+str(y['Last Checked'])+'''</td>
                                <td>'''+str(y['Threshold'])+'''</td>
                                <td>'''+str(y['Status'])+'''</td>
                            </tr>'''
                html += '''
                        </tbody>
                    </table>
                </div>'''
        except Exception as e:
            print(e)
        
        # Database Tablespace
        try:
            if len(x['value']['Database Tablespace']) > 0:
                html += '''
                <div class="taskTitle">
                    <h4 class="taskTitleh4">Database Tablespace</h4>
                </div>
                <div class="tableDiv">
                    <table class="tablecontent">
                        <thead>
                            <tr>
                '''
                for y in x['headers']['Database Tablespace']:
                    html += '''                        <th>'''+str(y)+'''</th>
                            '''
                html += '''                    </tr>
                        </thead>
                        <tbody>'''
                for y in x['value']['Database Tablespace']:
                    html += '''
                            <tr data-stat="'''+str(y['STATUS'])+'''">
                                <td>'''+str(y['ServerName'])+'''</td>
                                <td>'''+str(y['DBName'])+'''</td>
                                <td>'''+str(y['TABLESPACE'])+'''</td>
                                <td>'''+str(y['STATUS'])+'''</td>
                                <td>'''+str(y['TOTAL_MB'])+'''</td>
                                <td>'''+str(y['USED_MB'])+'''</td>
                                <td>'''+str(y['FREE_MB'])+'''</td>
                                <td>'''+str(y['PCT_USED'])+'''</td>
                            </tr>'''
                html += '''
                        </tbody>
                    </table>
                </div>'''
        except Exception as e:
            print(e)
        
        # Table Indexes Health Status
        try:
            if len(x['value']['Table Indexes Health Status']) > 0:
                html += '''
                <div class="taskTitle">
                    <h4 class="taskTitleh4">Table Indexes Health Status</h4>
                </div>
                <div class="tableDiv">
                    <table class="tablecontent">
                        <thead>
                            <tr>
                '''
                for y in x['headers']['Table Indexes Health Status']:
                    html += '''                        <th>'''+str(y)+'''</th>
                            '''
                html += '''                    </tr>
                        </thead>
                        <tbody>'''
                for y in x['value']['Table Indexes Health Status']:
                    html += '''
                            <tr>
                                <td>'''+str(y['ServerName'])+'''</td>
                                <td>'''+str(y['DBName'])+'''</td>
                                <td>'''+str(y['OWNER'])+'''</td>
                                <td>'''+str(y['DATETIME(LAST_ANALYZED)'])+'''</td>
                                <td>'''+str(y['COUNT'])+'''</td>
                            </tr>'''
                html += '''
                        </tbody>
                    </table>
                </div>'''
        except Exception as e:
            print(e)
        
        # System global area Program global Area
        try:
            if len(x['value']['System global area Program global Area']) > 0:
                html += '''
                <div class="taskTitle">
                    <h4 class="taskTitleh4">System global area Program global Area</h4>
                </div>
                <div class="tableDiv">
                    <table class="tablecontent">
                        <thead>
                            <tr>
                '''
                for y in x['headers']['System global area Program global Area']:
                    html += '''                        <th>'''+str(y)+'''</th>
                            '''
                html += '''                    </tr>
                        </thead>
                        <tbody>'''
                for y in x['value']['System global area Program global Area']:
                    html += '''
                            <tr>
                                <td>'''+str(y['Servername'])+'''</td>
                                <td>'''+str(y['INSTANCE_NAME'])+'''</td>
                                <td>'''+str(y['NAME'])+'''</td>
                                <td>'''+str(y['GB'])+'''</td>
                            </tr>'''
                html += '''
                        </tbody>
                    </table>
                </div>'''
        except Exception as e:
            print(e)
        
        # Blocking Sessions trend
        try:
            if len(x['value']['Blocking Sessions trend']) > 0:
                html += '''
                <div class="taskTitle">
                    <h4 class="taskTitleh4">Blocking Sessions trend</h4>
                </div>
                <div class="tableDiv">
                    <table class="tablecontent">
                        <thead>
                            <tr>
                '''
                for y in x['headers']['Blocking Sessions trend']:
                    html += '''                        <th>'''+str(y)+'''</th>
                            '''
                html += '''                    </tr>
                        </thead>
                        <tbody>'''
                for y in x['value']['Blocking Sessions trend']:
                    html += '''
                            <tr>
                                <td>'''+str(y['ServerName'])+'''</td>
                                <td>'''+str(y['DBName'])+'''</td>
                                <td>'''+str(y['LOGIN_TIME'])+'''</td>
                                <td>'''+str(y['inst_id'])+'''</td>
                                <td>'''+str(y['sid'])+'''</td>
                                <td>'''+str(y['serial'])+'''</td>
                                <td>'''+str(y['sql_id'])+'''</td>
                                <td>'''+str(y['username'])+'''</td>
                                <td>'''+str(y['status'])+'''</td>
                                <td>'''+str(y['module'])+'''</td>
                                <td>'''+str(y['machine'])+'''</td>
                                <td>'''+str(y['event'])+'''</td>
                                <td>'''+str(y['program'])+'''</td>
                                <td>'''+str(y['blocking_Session'])+'''</td>
                                <td>'''+str(y['blocking_instance'])+'''</td>
                                <td>'''+str(y['blocking_session_status'])+'''</td>
                                <td>'''+str(y['WAIT_TIME'])+'''</td>
                                <td>'''+str(y['SECONDS_IN_WAIT'])+'''</td>
                            </tr>'''
                html += '''
                        </tbody>
                    </table>
                </div>'''
        except Exception as e:
            print(e)
        
        # Backup Status
        try:
            if len(x['value']['Backup Status']) > 0:
                html += '''
                <div class="taskTitle">
                    <h4 class="taskTitleh4">Backup Status</h4>
                </div>
                <div class="tableDiv">
                    <table class="tablecontent">
                        <thead>
                            <tr>
                '''
                for y in x['headers']['Backup Status']:
                    html += '''                        <th>'''+str(y)+'''</th>
                            '''
                html += '''                    </tr>
                        </thead>
                        <tbody>'''
                for y in x['value']['Backup Status']:
                    html += '''
                            <tr>
                                <td>'''+str(y['ServerName'])+'''</td>
                                <td>'''+str(y['DBName'])+'''</td>
                                <td>'''+str(y['SESSION_KEY'])+'''</td>
                                <td>'''+str(y['INPUT_TYPE'])+'''</td>
                                <td>'''+str(y['STATUS'])+'''</td>
                                <td>'''+str(y['START_TIME'])+'''</td>
                                <td>'''+str(y['END_TIME'])+'''</td>
                                <td>'''+str(y['HRS'])+'''</td>
                                <td>'''+str(y['INPUT_GB'])+'''</td>
                                <td>'''+str(y['OUTPUT_GB'])+'''</td>
                                <td>'''+str(y['AUTOBACKUP_DONE'])+'''</td>
                            </tr>'''
                html += '''
                        </tbody>
                    </table>
                </div>'''
        except Exception as e:
            print(e)
        
        # Reindexing
        try:
            if len(x['value']['Reindexing']) > 0:
                html += '''
                <div class="taskTitle">
                    <h4 class="taskTitleh4">Reindexing</h4>
                </div>
                <div class="tableDiv">
                    <table class="tablecontent">
                        <thead>
                            <tr>
                '''
                for y in x['headers']['Reindexing']:
                    html += '''                        <th>'''+str(y)+'''</th>
                            '''
                html += '''                    </tr>
                        </thead>
                        <tbody>'''
                for y in x['value']['Reindexing']:
                    html += '''
                            <tr>
                                <td>'''+str(y['ServerName'])+'''</td>
                                <td>'''+str(y['DBName'])+'''</td>
                                <td>'''+str(y['OWNER'])+'''</td>
                                <td>'''+str(y['TABLE_NAME'])+'''</td>
                                <td>'''+str(y['INDEX_NAME'])+'''</td>
                                <td>'''+str(y['INDEX_TYPE'])+'''</td>
                            </tr>'''
                html += '''
                        </tbody>
                    </table>
                </div>'''
        except Exception as e:
            print(e)
        
        # I/O Rate
        try:
            if len(x['value']['I/O Rate']) > 0:
                html += '''
                <div class="taskTitle">
                    <h4 class="taskTitleh4">I/O Rate</h4>
                </div>
                <div class="tableDiv">
                    <table class="tablecontent">
                        <thead>
                            <tr>
                '''
                for y in x['headers']['I/O Rate']:
                    html += '''                        <th>'''+str(y)+'''</th>
                            '''
                html += '''                    </tr>
                        </thead>
                        <tbody>'''
                for y in x['value']['I/O Rate']:
                    html += '''
                            <tr>
                                <td>'''+str(y['Server Name'])+'''</td>
                                <td>'''+str(y['IO Name'])+'''</td>
                                <td>'''+str(y['IO Value'])+'''</td>
                                <td>'''+str(y['Last checked Time'])+'''</td>
                                <td>'''+str(y['Last Checked'])+'''</td>
                            </tr>'''
                html += '''
                        </tbody>
                    </table>
                </div>'''
        except Exception as e:
            print(e)
        
        # Database Session Count
        try:
            if len(x['value']['Database Session Count']) > 0:
                html += '''
                <div class="taskTitle">
                    <h4 class="taskTitleh4">Database Session Count</h4>
                </div>
                <div class="tableDiv">
                    <table class="tablecontent">
                        <thead>
                            <tr>
                '''
                for y in x['headers']['Database Session Count']:
                    html += '''                        <th>'''+str(y)+'''</th>
                            '''
                html += '''                    </tr>
                        </thead>
                        <tbody>'''
                for y in x['value']['Database Session Count']:
                    html += '''
                            <tr>
                                <td>'''+str(y['Servername'])+'''</td>
                                <td>'''+str(y['INSTANCE_NAME'])+'''</td>
                                <td>'''+str(y['SESSION_COUNT'])+'''</td>
                            </tr>'''
                html += '''
                        </tbody>
                    </table>
                </div>'''
        except Exception as e:
            print(e)
        
        # Database Growth
        try:
            if len(x['value']['Database Growth']) > 0:
                html += '''
                <div class="taskTitle">
                    <h4 class="taskTitleh4">Database Growth</h4>
                </div>
                <div class="tableDiv">
                    <table class="tablecontent">
                        <thead>
                            <tr>
                '''
                for y in x['headers']['Database Growth']:
                    html += '''                        <th>'''+str(y)+'''</th>
                            '''
                html += '''                    </tr>
                        </thead>
                        <tbody>'''
                for y in x['value']['Database Growth']:
                    html += '''
                            <tr>
                                <td>'''+str(y['Servername'])+'''</td>
                                <td>'''+str(y['DBName'])+'''</td>
                                <td>'''+str(y['OWNER'])+'''</td>
                                <td>'''+str(y['TABLE_NAME'])+'''</td>
                                <td>'''+str(y['NUM_ROWS'])+'''</td>
                            </tr>'''
                html += '''
                        </tbody>
                    </table>
                </div>'''
        except Exception as e:
            print(e)

        html += '''
        </div>'''

    html += '''
        <script>
            function openCustomer(evt, cityName) {
                var i, tabcontent, tablinks;
                tabcontent = document.getElementsByClassName("tabcontent");
                for (i = 0; i < tabcontent.length; i++) {
                    tabcontent[i].style.display = "none";
                }
                tablinks = document.getElementsByClassName("tablinks");
                for (i = 0; i < tablinks.length; i++) {
                    tablinks[i].className = tablinks[i].className.replace(" active", "");
                }
                document.getElementById(cityName).style.display = "block";
                evt.currentTarget.className += " active";
            }
            document.getElementById("defaultOpen").click();
        </script>
    </body>
    </html>'''

    #print(html)

    text_file = open(r"D:\\TMS_Prod\\UI_HTML_Report\\{}.html".format(htmlFileName), "w")
    text_file.write(html)
    text_file.close()

    filename_Download = {"path":"D:\\TMS_Prod\\UI_HTML_Report\\","filename":"{}.html".format(htmlFileName)}
    return JsonResponse(html,safe=False)

def handleRequest1(request):
   
    print("&"*50)
    print(request)
    rows=request.POST['rows']
    print(rows)
    print("&"*50)
    rows=rows.split(';')
    rows=rows[:-1]

    inputJson = []
    print(rows)
    for i in rows:
        try:
            print("################")
            print(i)
            inputJson.append(json.loads(i))
        except Exception as e:
            print(e)
        
    print(inputJson)    
    returnOutput=[]

    for i in inputJson:
        print(i)    
        customerid = i['customer']
        env = i['env']
        servernames = i['server']
        tasknames = i['task']
        themename = i['activity']
        pid = '8'
        servercat = 'Private'
        subregion = i['subregion']
        if themename == 'Maintenance':
            if 'Create Maintenance' in tasknames:
                mname = i['mname']
                start_epoch = i['starttime']
                end_epoch = i['endtime']
            elif 'Update Maintenance' in tasknames:
                mid = i['mname']
                cid = i['mcrid']
                start_time = i['starttime']
                end_time = i['endtime']
                zserver = i['zserver']

        if themename == 'Availability':
            print("######Availability######")
            themeid = 1
        elif themename == 'Performance':
            themeid = 2
        elif themename == 'Maintenance':
            themeid = 3
        elif themename == 'Integration':
            themeid = 10

        if subregion == 'No Subregion':
            subregion = ''
        #print(themeid)

        customer = mssql.tmscustomerbyid(customerid)
        
        main_output = {'customer_name':customer,'customer_id':customerid,'funcnames':[],'headers':{},'value':{}}
        if themeid == 1 or themeid == 2:
            main_output['funcnames'].extend(['Summary Table'])
            main_output['headers']['Summary Table'] = ["Task Name",'Good Count','Bad Count','NA Count']
            main_output['value']['Summary Table'] = []
            ## Summary Count - Availability/Performance##
            summ_tasknames = tasknames.split(',')
            icmp_ping_good = 0
            icmp_ping_na = 0
            icmp_ping_bad = 0
            cpu_utl_good = 0
            cpu_utl_na = 0
            cpu_utl_bad = 0
            mem_utl_good = 0
            mem_utl_na = 0
            mem_utl_bad = 0
            serv_status_good = 0
            serv_status_bad = 0
            serv_status_na = 0
            port_good = 0
            port_bad = 0
            port_na = 0
            cis_good = 0
            cis_bad = 0
            cis_na = 0
            web_serv_gd = 0
            web_serv_bd = 0
            web_serv_na = 0
            int_url_gd = 0
            int_url_bd = 0
            int_url_na = 0
            pub_url_gd = 0
            pub_url_bd = 0
            pub_url_na = 0
            ui_avail_gd = 0
            ui_avail_bd = 0
            ui_avail_na = 0
            fa_mon_gd = 0
            fa_mon_bd = 0
            fa_mon_na = 0
            db_mon_gd = 0
            db_mon_bd = 0
            db_mon_na = 0
            ## Summary Count - Availability/Performance##
        for taskname in tasknames.split(','):
            if 'ICMP Ping' == taskname:
                main_output['funcnames'].extend(['ICMP Ping'])
                main_output['headers']['ICMP Ping'] = ["Server Name",'ICMP Last Value','ICMP Last Clock','Last Checked','Status']
                main_output['value']['ICMP Ping'] = []
                
            elif 'CPU Utilization' == taskname:
                main_output['funcnames'].extend(['CPU Utilization'])
                main_output['headers']['CPU Utilization'] = ["Server Name", "CPU Utilization Last Value", "CPU Utilization Last Clock",'Last Checked', "Threshold" , "Status"]
                main_output['value']['CPU Utilization'] = []
                
            elif 'Memory Utilization' == taskname:
                main_output['funcnames'].extend(['Memory Utilization'])
                main_output['headers']['Memory Utilization'] = ["Server Name",'Free Memory Last Value','Free Memory Last Clock', 'Last Checked', "Threshold" , "Status"]
                main_output['value']['Memory Utilization'] = []
                
            elif 'Service Status' == taskname:
                main_output['funcnames'].extend(['Service Status'])
                main_output['headers']['Service Status'] = ["Server Name", "Service Name", "Service Last Value", "Service Last Clock",'Last Checked','Status']
                main_output['value']['Service Status'] = []
                
            elif 'Port Status' == taskname:
                main_output['funcnames'].extend(['Port Status'])
                main_output['headers']['Port Status'] = ["Server Name", 'Port Name', 'Port Last Value','Port Last Clock','Last Checked','Status']
                main_output['value']['Port Status'] = []
                
            elif 'Internal URL Status' == taskname:
                main_output['funcnames'].extend(['Internal URL Status'])
                main_output['headers']['Internal URL Status'] = ['Server Name','Internal URL Name','Internal URL Value','Internal URL Clock','Last Checked','Status']
                main_output['value']['Internal URL Status'] = []
                
            elif 'Public URL Status' == taskname:
                main_output['funcnames'].extend(['Public URL Status'])
                main_output['headers']['Public URL Status'] = ['Public URL Name','Public URL Value','Public URL Clock','Last Checked','Status']
                main_output['value']['Public URL Status'] = []
                
            elif 'Database Growth' == taskname:
                main_output['funcnames'].extend(['Database Growth'])
                main_output['headers']['Database Growth'] = ['Servername','DBName','OWNER','TABLE_NAME','NUM_ROWS']
                main_output['value']['Database Growth'] = []
                
            elif 'Database Session Count' == taskname:
                main_output['funcnames'].extend(['Database Session Count'])
                main_output['headers']['Database Session Count'] = ['Servername','INSTANCE_NAME','SESSION_COUNT']
                main_output['value']['Database Session Count'] = []
                
            elif 'Database Tablespaces' == taskname:
                main_output['funcnames'].extend(['Database Tablespace'])
                main_output['headers']['Database Tablespace'] = ['ServerName','DBName','TABLESPACE','STATUS','TOTAL_MB','USED_MB','FREE_MB','PCT_USED']
                
                main_output['funcnames'].extend(['Table Indexes Health Status'])
                main_output['headers']['Table Indexes Health Status'] = ['ServerName','DBName','OWNER','DATETIME(LAST_ANALYZED)','COUNT']
                
            elif 'System global area Program global Area' == taskname:
                main_output['funcnames'].extend(['System global area Program global Area'])
                main_output['headers']['System global area Program global Area'] = ['Servername','INSTANCE_NAME','NAME','GB']
                main_output['value']['System global area Program global Area'] = []
                
            elif 'Blocking Sessions trend' == taskname:
                main_output['funcnames'].extend(['Blocking Sessions trend'])
                main_output['headers']['Blocking Sessions trend'] = ['ServerName','DBName','LOGIN_TIME','inst_id','sid','serial','sql_id','username','status','module','machine','event','program','blocking_Session','blocking_instance','blocking_session_status','WAIT_TIME','SECONDS_IN_WAIT']
                main_output['value']['Blocking Sessions trend'] = []
                
            elif 'Database maintnenace jobs and duration' == taskname:
                main_output['funcnames'].extend(['Backup Status'])
                main_output['headers']['Backup Status'] = ['ServerName','DBName','SESSION_KEY','INPUT_TYPE','STATUS','START_TIME','END_TIME','HRS','INPUT_GB','OUTPUT_GB','AUTOBACKUP_DONE']
                
                main_output['funcnames'].extend(['Reindexing'])
                main_output['headers']['Reindexing'] = ['ServerName','DBName','OWNER','TABLE_NAME','INDEX_NAME','INDEX_TYPE']
                
            elif 'CIS Adapter Status' == taskname:
                main_output['funcnames'].extend(['CIS Adapter Status'])
                main_output['headers']['CIS Adapter Status'] = ['Server Name','CIS Adapter Name','CIS Adapter Status','CIS Adapter Duration','CIS Adapter Last time','Status']
                main_output['value']['CIS Adapter Status'] = []
                
            elif 'Web Services Status' == taskname:
                main_output['funcnames'].extend(['Web Services Status'])
                main_output['headers']['Web Services Status'] = ['Server Name','Web Services Name','Web Services Status','Web Services URL','Web Services Last Time','Status']
                main_output['value']['Web Services Status'] = []
                
            elif 'File Age Monitor' == taskname:
                main_output['funcnames'].extend(['File Age Monitor'])
                main_output['headers']['File Age Monitor'] = ['File Age customer','File Age Good Count','File Age Bad Count']
                main_output['value']['File Age Monitor'] = []
                
            elif 'Database Monitor' == taskname:
                main_output['funcnames'].extend(['Database Monitor'])
                main_output['headers']['Database Monitor'] = ['DB customer','DB Good Count','DB Bad Count']
                main_output['value']['Database Monitor'] = []
                
            elif 'Process Level' == taskname:
                main_output['funcnames'].extend(['Process Level'])
                main_output['headers']['Process Level'] = ['Request_Id','Status']
                main_output['value']['Process Level'] = []
                
            elif 'Start App Service' == taskname:
                main_output['funcnames'].extend([taskname])
                main_output['headers'][taskname] = ['Server Name','Service Name','Status']
                main_output['value']['Start App Service'] = []
                ################### Start App Service ###############################
                main_output['funcnames'].extend(['Summary Table'])
                main_output['headers']['Summary Table'] = ["Task Name",'Good Count','Bad Count','NA Count']
                main_output['value']['Summary Table'] = []
                ## Summary Count - Availability/Performance##
                summ_tasknames = "ICMP Ping,Service Status,Port Status,CIS Adapter Status,Web Services Status,Internal URL Status,Public URL Status,UI Availability,Process Level,File Age Monitor,Database Monitor".split(',')
                icmp_ping_good = 0
                icmp_ping_na = 0
                icmp_ping_bad = 0
                cpu_utl_good = 0
                cpu_utl_na = 0
                cpu_utl_bad = 0
                mem_utl_good = 0
                mem_utl_na = 0
                mem_utl_bad = 0
                serv_status_good = 0
                serv_status_bad = 0
                serv_status_na = 0
                port_good = 0
                port_bad = 0
                port_na = 0
                cis_good = 0
                cis_bad = 0
                cis_na = 0
                web_serv_gd = 0
                web_serv_bd = 0
                web_serv_na = 0
                int_url_gd = 0
                int_url_bd = 0
                int_url_na = 0
                pub_url_gd = 0
                pub_url_bd = 0
                pub_url_na = 0
                ui_avail_gd = 0
                ui_avail_bd = 0
                ui_avail_na = 0
                fa_mon_gd = 0
                fa_mon_bd = 0
                fa_mon_na = 0
                db_mon_gd = 0
                db_mon_bd = 0
                db_mon_na = 0
                ##### Run Availability Theme #####
                # ICMP PING
                main_output['funcnames'].extend(['ICMP Ping'])
                main_output['headers']['ICMP Ping'] = ["Server Name",'ICMP Last Value','ICMP Last Clock','Last Checked','Status']
                main_output['value']['ICMP Ping'] = []
                # Service Status
                main_output['funcnames'].extend(['Service Status'])
                main_output['headers']['Service Status'] = ["Server Name", "Service Name", "Service Last Value", "Service Last Clock",'Last Checked','Status']
                main_output['value']['Service Status'] = []
                # Port Status
                main_output['funcnames'].extend(['Port Status'])
                main_output['headers']['Port Status'] = ["Server Name", 'Port Name', 'Port Last Value','Port Last Clock','Last Checked','Status']
                main_output['value']['Port Status'] = []
                # Internal URL Status
                main_output['funcnames'].extend(['Internal URL Status'])
                main_output['headers']['Internal URL Status'] = ['Server Name','Internal URL Name','Internal URL Value','Internal URL Clock','Last Checked','Status']
                main_output['value']['Internal URL Status'] = []
                # Public URL Status
                main_output['funcnames'].extend(['Public URL Status'])
                main_output['headers']['Public URL Status'] = ['Public URL Name','Public URL Value','Public URL Clock','Last Checked','Status']
                main_output['value']['Public URL Status'] = []
                # CIS Adapter
                main_output['funcnames'].extend(['CIS Adapter Status'])
                main_output['headers']['CIS Adapter Status'] = ['Server Name','CIS Adapter Name','CIS Adapter Status','CIS Adapter Duration','CIS Adapter Last time','Status']
                main_output['value']['CIS Adapter Status'] = []
                # Web Service status
                main_output['funcnames'].extend(['Web Services Status'])
                main_output['headers']['Web Services Status'] = ['Server Name','Web Services Name','Web Services Status','Web Services URL','Web Services Last Time','Status']
                main_output['value']['Web Services Status'] = []
                # File Age Monitor
                main_output['funcnames'].extend(['File Age Monitor'])
                main_output['headers']['File Age Monitor'] = ['File Age customer','File Age Good Count','File Age Bad Count']
                main_output['value']['File Age Monitor'] = []
                # DB Monitor
                main_output['funcnames'].extend(['Database Monitor'])
                main_output['headers']['Database Monitor'] = ['DB customer','DB Good Count','DB Bad Count']
                main_output['value']['Database Monitor'] = []
                # UI Availability
                main_output['funcnames'].extend(['UI Availability'])
                main_output['headers']['UI Availability'] = ['Name','Test Name','Test_Status','node','Time','Status']
                main_output['value']['UI Availability'] = []
                # process Validation
                main_output['funcnames'].extend(['Process Level'])
                main_output['headers']['Process Level'] = ['Request_Id','Status']
                main_output['value']['Process Level'] = []
                ##### Run Availability Theme #####
                
            elif 'Stop App Service' == taskname:
                main_output['funcnames'].extend(['Create Maintenance'])
                main_output['headers']['Create Maintenance'] = ['Server Name','Output Status']
                main_output['value']['Create Maintenance'] = []
                main_output['funcnames'].extend([taskname])
                main_output['headers'][taskname] = ['Server Name','Service Name','Status']
                main_output['value']['Stop App Service'] = []
                
            elif 'UI Sanity Checks' == taskname:
                main_output['funcnames'].extend(['UI Sanity Checks'])
                main_output['headers']['UI Sanity Checks'] = ['Name','Test Name','Status','node']
                main_output['value']['UI Sanity Checks'] = []
                
            elif 'UI Availability' == taskname:
                main_output['funcnames'].extend(['UI Availability'])
                main_output['headers']['UI Availability'] = ['Name','Test Name','Test_Status','node','Time','Status']
                main_output['value']['UI Availability'] = []
                
            elif 'I/O Rate' == taskname:
                main_output['funcnames'].extend(['I/O Rate'])
                main_output['headers']['I/O Rate'] = ['Server Name','IO Name','IO Value','Last checked Time','Last Checked']
                main_output['value']['I/O Rate'] = []
                
            elif 'AS2/SFTP' == taskname:
                main_output['funcnames'].extend(['AS2/SFTP Gateways'])
                main_output['headers']['AS2/SFTP Gateways'] = ['Customer','Gateway Server','Zabbix Location','Gateway URL Name','Gateway URL Value','Gateway URL Last Clock']
                main_output['funcnames'].extend(['AS2/SFTP'])
                main_output['headers']['AS2/SFTP'] = ['Customer','Mailbox','Transport','Start_Date','End_Date','Direction','Status','File_Name','File_Size_Bytes']
                
            elif 'Server Reboot' == taskname:
                main_output['funcnames'].extend(['Server Reboot'])
                main_output['headers']['Server Reboot'] = ['status']
                
            elif 'Create Maintenance' == taskname:
                main_output['funcnames'].extend(['Create Maintenance'])
                main_output['headers']['Create Maintenance'] = ['Server Name','Output Status']
                
            elif 'Update Maintenance' == taskname:
                main_output['funcnames'].extend(['Update Maintenance'])
                main_output['headers']['Update Maintenance'] = ['Output Status']

            else:
                main_output['headers'].append(taskname)
                
        if env == 'Prod':
            prod=1
        else:
            prod=2
        funcname = [mssql.func_name(task) for task in tasknames.split(',')]
        
        func_name = [a['func_name'][0][0]  for a in funcname]
        
        variable = []
        
        if 'main' in func_name :
            result = (handleD.callfunction('',themeid,customer,pid,servercat,prod,env,subregion,'main','','','','','','','','','','','','','',''))
            #print(result)
            func_name.remove('main')
            main_output['value']['UI Sanity Checks'] = result
            variable.extend(a for a in result)
            
        if 'ui_availability' in func_name :
            result = (handleD.callfunction('',themeid,customer,pid,servercat,prod,env,subregion,'ui_availability','','','','','','','','','','','','','',''))
            #print(result)
            func_name.remove('ui_availability')
            for tmp in result:
                if (tmp['Test_Status'] == 'PASS'):
                    ui_avail_gd = ui_avail_gd + 1
                elif (tmp['Test_Status'] == 'NA'):
                    ui_avail_na = ui_avail_na + 1
                else:
                    ui_avail_bd = ui_avail_bd + 1
            main_output['value']['UI Availability'] = result
            
        if 'public_url' in func_name:
            result = (handleD.callfunction((servernames.split(","))[0],themeid,customer,pid,servercat,prod,env,subregion,'public_url','','','','','','','','','','','','','',''))
            #print(result)
            func_name.remove('public_url')
            for tmp in result:
                if (tmp['Status'] == 'Good'):
                    pub_url_gd = pub_url_gd + 1
                elif (tmp['Status'] == 'NA'):
                    pub_url_na = pub_url_na + 1
                else:
                    pub_url_bd = pub_url_bd + 1
            main_output['value']['Public URL Status'] = result
            
        if 'gateway_details' in func_name :
            result1 = (handleD.callfunction('',themeid,customer,pid,servercat,prod,env,subregion,'gateway_details','','','','','','','','','','','','','',''))
            #print(result1)
            main_output['value']['AS2/SFTP Gateways'] = result1
            variable.extend(a for a in result1)
            result2 = (handleD.callfunction('',themeid,customer,pid,servercat,prod,env,subregion,'transfer_report',accountType,accountName,start_date,end_date,'','','','','','','','',result1,emailid))
            main_output['value']['AS2/SFTP'] = result2
            variable.extend(a for a in result2)
            func_name.remove('gateway_details')
            
        if 'file_monitorDetails' in func_name :
            result = (handleD.callfunction('',themeid,customer,pid,servercat,prod,env,subregion,'file_monitorDetails','','','','','','','','','','','','','',''))
            #print(result)
            func_name.remove('file_monitorDetails')
            for tmp in result:
                if (tmp['File Age Good Count'] == 'NA' or tmp['File Age Bad Count'] == 'NA'):
                    fa_mon_na = fa_mon_na + 1
                else:
                    fa_mon_gd = fa_mon_gd + int(tmp['File Age Good Count'])
                    fa_mon_bd = fa_mon_bd + int(tmp['File Age Bad Count'])
            main_output['value']['File Age Monitor'] = result
            
        if 'db_monitorDetails' in func_name :
            result_1 = (handleD.callfunction('',themeid,customer,pid,servercat,prod,env,subregion,'db_monitorDetails','','','','','','','','','','','','','',''))
            func_name.remove('db_monitorDetails')
            for tmp in result_1:
                if (tmp['DB Good Count'] == 'NA' or tmp['DB Bad Count'] == 'NA'):
                    db_mon_na = db_mon_na + 1
                else:
                    db_mon_gd = db_mon_gd + int(tmp['DB Good Count'])
                    db_mon_bd = db_mon_bd + int(tmp['DB Bad Count'])
            main_output['value']['Database Monitor'] = result_1
            
        if "process_validation" in func_name:
            tempout = handleD.callfunction('',themeid,customer,pid,servercat,prod,env,subregion,'process_validation','','','','','','','','','','','','','','')
            main_output['value']['Process Level'].extend(tempout)
            
        if 'create_maintenance' in func_name:
            end_epoch = datetime.datetime.strptime(end_epoch, "%Y/%m/%d %H:%M")
            start_epoch = datetime.datetime.strptime(start_epoch, "%Y/%m/%d %H:%M")
            result = (handleD.callfunction(servernames,themeid,customer,pid,servercat,prod,env,subregion,'create_maintenance','','','','',mname,start_epoch,end_epoch,'','','','','','',''))
            #func_name.remove('create_maintenance')
            main_output['value']['Create Maintenance'] = result
            
        if 'reboot_server_tms' in func_name:
            if 'create_maintenance' not in func_name:
                func_name.insert(0,'create_maintenance')
                main_output['funcnames'].extend(['Create Maintenance'])
                main_output['headers']['Create Maintenance'] = ['Server Name','Output Status']
                IST = pytz.timezone('Asia/Kolkata') 
                end_epoch = datetime.datetime.strptime((datetime.datetime.now(IST) + datetime.timedelta(minutes=15)).strftime("%Y/%m/%d %H:%M"),  "%Y/%m/%d %H:%M")
                start_epoch = datetime.datetime.strptime(datetime.datetime.now(IST).strftime("%Y/%m/%d %H:%M"),  "%Y/%m/%d %H:%M")
                mname = customer + '_reboot_server_' +str(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
                result = (handleD.callfunction(servernames,themeid,customer,pid,servercat,prod,'create_maintenance','','','','',mname,start_epoch,end_epoch,'','','','','','',''))
                main_output['value']['Create Maintenance'] = result
            result_1 = (handleD.callfunction(servernames,themeid,customer,pid,servercat,prod,env,subregion,'reboot_server_tms','','','','','','','','','','','','','',''))
            
            main_output['value']['Server Reboot'] = result_1
            
        if "start_app_service" in func_name:
            '''if 'create_maintenance' not in func_name:
                func_name.insert(0,'create_maintenance')
                main_output['funcnames'].extend(['Create Maintenance'])
                main_output['headers']['Create Maintenance'] = ['Server Name','Output Status']
                IST = pytz.timezone('Asia/Kolkata') 
                end_epoch = datetime.datetime.strptime((datetime.datetime.now(IST) + datetime.timedelta(minutes=15)).strftime("%Y/%m/%d %H:%M"),  "%Y/%m/%d %H:%M")
                start_epoch = datetime.datetime.strptime(datetime.datetime.now(IST).strftime("%Y/%m/%d %H:%M"),  "%Y/%m/%d %H:%M")
                mname = customer + '_start_stop_serv_' + str(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
                result = (handleD.callfunction(servernames,themeid,customer,pid,servercat,prod,'create_maintenance','','','','',mname,start_epoch,end_epoch,'','','','','','',''))
                main_output['value']['Create Maintenance'] = result'''
            func_name = ["icmp_ping","service_status","internal_url","port_status","cis_Adapter","web_service","process_validation"]
            for server in servernames.split(','):
                result = (handleD.callfunction(server,themeid,customer,pid,servercat,prod,env,subregion,'start_app_service','','','','','','','','','','','','','',''))
                main_output['value']['Start App Service'].extend(result)
                ######### Availability Theme #########
            ## UI Availability ##
            result = (handleD.callfunction('',themeid,customer,pid,servercat,prod,env,subregion,'ui_availability','','','','','','','','','','','','','',''))
            main_output['value']['UI Availability'] = result
            for tmp in result:
                if (tmp['Test_Status'] == 'PASS'):
                    ui_avail_gd = ui_avail_gd + 1
                elif (tmp['Test_Status'] == 'NA'):
                    ui_avail_na = ui_avail_na + 1
                else:
                    ui_avail_bd = ui_avail_bd + 1
                    
            ## PUBLIC URL ##
            result = (handleD.callfunction((servernames.split(","))[0],themeid,customer,pid,servercat,prod,env,subregion,'public_url','','','','','','','','','','','','','',''))
            main_output['value']['Public URL Status'] = result
            for tmp in result:
                if (tmp['Status'] == 'Good'):
                    pub_url_gd = pub_url_gd + 1
                elif (tmp['Status'] == 'NA'):
                    pub_url_na = pub_url_na + 1
                else:
                    pub_url_bd = pub_url_bd + 1
                    
            ## File Age Monitor ##
            result = (handleD.callfunction('',themeid,customer,pid,servercat,prod,env,subregion,'file_monitorDetails','','','','','','','','','','','','','',''))
            main_output['value']['File Age Monitor'] = result
            for tmp in result:
                if (tmp['File Age Good Count'] == 'NA' or tmp['File Age Bad Count'] == 'NA'):
                    fa_mon_na = fa_mon_na + 1
                else:
                    fa_mon_gd = fa_mon_gd + int(tmp['File Age Good Count'])
                    fa_mon_bd = fa_mon_bd + int(tmp['File Age Bad Count'])
                    
            ## DB Monitor ##
            result_1 = (handleD.callfunction('',themeid,customer,pid,servercat,prod,env,subregion,'db_monitorDetails','','','','','','','','','','','','','',''))
            main_output['value']['Database Monitor'] = result_1
            for tmp in result_1:
                if (tmp['DB Good Count'] == 'NA' or tmp['DB Bad Count'] == 'NA'):
                    db_mon_na = db_mon_na + 1
                else:
                    db_mon_gd = db_mon_gd + int(tmp['DB Good Count'])
                    db_mon_bd = db_mon_bd + int(tmp['DB Bad Count'])
                    
            ## Process Validation ##
            tempout = handleD.callfunction('',themeid,customer,pid,servercat,prod,env,subregion,'process_validation','','','','','','','','','','','','','','')
            main_output['value']['Process Level'].extend(tempout)
            ## ------ Server Based Tasks ------ ##
            for server in servernames.split(','):
                print("sample")
                for func in func_name:
                    tempout = None
                    #ICMP Ping
                    if (func == "icmp_ping"):
                        tempout = handleD.callfunction(server,themeid,customer,pid,servercat,prod,env,subregion,func,'','','','','','','','','','','','','','')
                        main_output['value']['ICMP Ping'].append(tempout)
                        if (tempout['ICMP Last Value'] == 'Available'):
                            icmp_ping_good = icmp_ping_good + 1
                        elif (tempout['ICMP Last Value'] == 'NA'):
                            icmp_ping_na = icmp_ping_na + 1
                        else:
                            icmp_ping_bad = icmp_ping_bad + 1   
                    #Service Status
                    if func == "service_status":
                        tempout = handleD.callfunction(server,themeid,customer,pid,servercat,prod,env,subregion,func,'','','','','','','','','','','','','','')
                        main_output['value']['Service Status'].extend(tempout)
                        for tmp in tempout:
                            if (tmp['Service Last Value'] == 'Running'):
                                serv_status_good = serv_status_good + 1
                            elif (tmp['Service Last Value'] == 'NA'):
                                serv_status_na = serv_status_na + 1
                            else:
                                serv_status_bad = serv_status_bad + 1
                    #Internal url
                    if func == "internal_url":
                        tempout = handleD.callfunction(server,themeid,customer,pid,servercat,prod,env,subregion,func,'','','','','','','','','','','','','','')
                        main_output['value']['Internal URL Status'].extend(tempout)
                        for tmp in tempout:
                            if (tmp['Status'] == 'Good'):
                                int_url_gd = int_url_gd + 1
                            elif (tmp['Status'] == 'NA'):
                                int_url_na = int_url_na + 1
                            else:
                                int_url_bd = int_url_bd + 1 
                    # port Status
                    if func == "port_status":
                        tempout = handleD.callfunction(server,themeid,customer,pid,servercat,prod,env,subregion,func,'','','','','','','','','','','','','','')
                        main_output['value']['Port Status'].extend(tempout)
                        for tmp in tempout:
                            if (tmp['Port Last Value'] == 'Up'):
                                port_good = port_good + 1
                            elif (tmp['Port Last Value'] == 'NA'):
                                port_na = port_na + 1
                            else:
                                port_bad = port_bad + 1
                    #CIS Adapter
                    if func == "cis_Adapter":
                        tempout = handleD.callfunction(server,themeid,customer,pid,servercat,prod,env,subregion,func,'','','','','','','','','','','','','','')
                        main_output['value']['CIS Adapter Status'].extend(tempout)
                        for tmp in tempout:
                            if (tmp['CIS Adapter Status'] == 'Available'):
                                cis_good = cis_good + 1
                            elif (tmp['CIS Adapter Status'] == 'NA'):
                                cis_na = cis_na + 1
                            else:
                                cis_bad = cis_bad + 1
                    # Web Service
                    if func == "web_service":
                        tempout = handleD.callfunction(server,themeid,customer,pid,servercat,prod,env,subregion,func,'','','','','','','','','','','','','','')
                        main_output['value']['Web Services Status'].extend(tempout)
                        for tmp in tempout:
                            if (tmp['Web Services Status'] == 'Available'):
                                web_serv_gd = web_serv_gd + 1
                            elif (tmp['Web Services Status'] == 'NA'):
                                web_serv_na = web_serv_na + 1
                            else:
                                web_serv_bd = web_serv_bd + 1
                    # Process Level
            func_name = []
            ######### Availability Theme #########
            
        if "stop_app_service" in func_name:
            if 'create_maintenance' not in func_name:
                func_name.insert(0,'create_maintenance')
                summ_tasknames = "ICMP Ping,Service Status,Port Status,CIS Adapter Status,Web Services Status,Internal URL Status,Public URL Status,UI Availability,Process Level,File Age Monitor,Database Monitor".split(',')
                
                IST = pytz.timezone('Asia/Kolkata') 
                end_epoch = datetime.datetime.strptime((datetime.datetime.now(IST) + datetime.timedelta(minutes=15)).strftime("%Y/%m/%d %H:%M"),  "%Y/%m/%d %H:%M")
                start_epoch = datetime.datetime.strptime(datetime.datetime.now(IST).strftime("%Y/%m/%d %H:%M"),  "%Y/%m/%d %H:%M")
                mname = customer + '_start_stop_serv_' + str(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
                result = (handleD.callfunction(servernames,themeid,customer,pid,servercat,prod,env,subregion,'create_maintenance','','','','',mname,start_epoch,end_epoch,'','','','','','',''))
                main_output['value']['Create Maintenance'] = result
            for server in servernames.split(','):
                result = (handleD.callfunction(server,themeid,customer,pid,servercat,prod,env,subregion,'stop_app_service','','','','','','','','','','','','','',''))
                main_output['value']['Stop App Service'].extend(result)
                
        if 'update_maintenance' in func_name:
            start_time = datetime.datetime.strptime(str(start_time), "%Y/%m/%d %H:%M")
            end_time = datetime.datetime.strptime(str(end_time), "%Y/%m/%d %H:%M")
            result = (handleD.callfunction(servernames,themeid,customer,pid,servercat,prod,env,subregion,'update_maintenance','','','','','','','',mid,cid,start_time,end_time,zserver,'',''))
            func_name.remove('update_maintenance')
            main_output['value']['Update Maintenance'] = result
            
        if "Backup_Reindexing" in func_name:
            result1 = handleD.callfunction(servernames,themeid,customer,pid,servercat,prod,env,subregion,'db_backup_status','','','','','','','','','','','','','','')
            #print(result1)
            main_output['value']['Backup Status'] = result1
            
            result2 = handleD.callfunction(servernames,themeid,customer,pid,servercat,prod,env,subregion,'db_reindexing','','','','','','','','','','','','','','')
            main_output['value']['Reindexing'] = result2
            func_name.remove('Backup_Reindexing')
            
        if "db_tablespace" in func_name:
            result1 = handleD.callfunction(servernames,themeid,customer,pid,servercat,prod,env,subregion,'db_tablespace','','','','','','','','','','','','','','')
            #print(result1)
            main_output['value']['Database Tablespace'] = result1
            
            result2 = handleD.callfunction(servernames,themeid,customer,pid,servercat,prod,env,subregion,'DB_index_Healthstat','','','','','','','','','','','','','','')
            main_output['value']['Table Indexes Health Status'] = result2
            func_name.remove('db_tablespace')

        if "disk_free_space" in func_name:
            tempout = handleD.callfunction(servernames,themeid,customer,pid,servercat,prod,env,subregion,"disk_free_space",'','','','','','','','','','','','','','')
            main_output['value']['Free Disk Space'].extend(tempout)

        for server in servernames.split(','):
            output = {'server name':server}
            for func in func_name:
                if (func == "internal_url" or func == "service_status" or func == "port_status" or func == "db_session" or func == "db_growth" or func == "cis_Adapter" or func == "web_service" or func == "start_app_service" or func == "stop_app_service" or func == "process_validation" or func == "IO_rate"  or func =="SGA_PGA" or func == "Blocking_Sessions" ):

                    if func == "service_status":
                        tempout = handleD.callfunction(server,themeid,customer,pid,servercat,prod,env,subregion,func,'','','','','','','','','','','','','','')
                        for tmp in tempout:
                            if (tmp['Service Last Value'] == 'Running'):
                                serv_status_good = serv_status_good + 1
                            elif (tmp['Service Last Value'] == 'NA'):
                                serv_status_na = serv_status_na + 1
                            else:
                                serv_status_bad = serv_status_bad + 1 
                        main_output['value']['Service Status'].extend(tempout)
                        
                    if func == "internal_url":
                        tempout = handleD.callfunction(server,themeid,customer,pid,servercat,prod,env,subregion,func,'','','','','','','','','','','','','','')
                        for tmp in tempout:
                            if (tmp['Status'] == 'Good'):
                                int_url_gd = int_url_gd + 1
                            elif (tmp['Status'] == 'NA'):
                                int_url_na = int_url_na + 1
                            else:
                                int_url_bd = int_url_bd + 1 
                        main_output['value']['Internal URL Status'].extend(tempout)
                        
                    if func == "port_status":
                        tempout = handleD.callfunction(server,themeid,customer,pid,servercat,prod,env,subregion,func,'','','','','','','','','','','','','','')
                        for tmp in tempout:
                            if (tmp['Port Last Value'] == 'Up'):
                                port_good = port_good + 1
                            elif (tmp['Port Last Value'] == 'NA'):
                                port_na = port_na + 1
                            else:
                                port_bad = port_bad + 1
                        main_output['value']['Port Status'].extend(tempout)
                        
                    if func == "port_status_wms":
                        tempout = handleD.callfunction(server,themeid,customer,pid,servercat,prod,env,subregion,func,'','','','','','','','','','','','','','')
                        for tmp in tempout:
                            if (tmp['Port Last Value'] == 'Up'):
                                port_good = port_good + 1
                            elif (tmp['Port Last Value'] == 'NA'):
                                port_na = port_na + 1
                            else:
                                port_bad = port_bad + 1
                        main_output['value']['Port Status'].extend(tempout)
                        
                    if func == "db_session":
                        tempout = handleD.callfunction(server,themeid,customer,pid,servercat,prod,env,subregion,func,'','','','','','','','','','','','','','')
                        main_output['value']['Database Session Count'].extend(tempout)
                        
                    if func == "db_growth":
                        tempout = handleD.callfunction(server,themeid,customer,pid,servercat,prod,env,subregion,func,'','','','','','','','','','','','','','')
                        main_output['value']['Database Growth'].extend(tempout)
                        
                    if func == "SGA_PGA":
                        tempout = handleD.callfunction(server,themeid,customer,pid,servercat,prod,env,subregion,func,'','','','','','','','','','','','','','')
                        main_output['value']['System global area Program global Area'].extend(tempout)
                        
                    if func == "Blocking_Sessions":
                        tempout = handleD.callfunction(server,themeid,customer,pid,servercat,prod,env,subregion,func,'','','','','','','','','','','','','','')
                        main_output['value']['Blocking Sessions trend'].extend(tempout)
                        
                    if func == "IO_rate":
                        tempout = handleD.callfunction(server,themeid,customer,pid,servercat,prod,env,subregion,func,'','','','','','','','','','','','','','')
                        main_output['value']['I/O Rate'].extend(tempout)
                    
                    if func == "web_service":
                        tempout = handleD.callfunction(server,themeid,customer,pid,servercat,prod,env,subregion,func,'','','','','','','','','','','','','','')
                        for tmp in tempout:
                            if (tmp['Web Services Status'] == 'Available'):
                                web_serv_gd = web_serv_gd + 1
                            elif (tmp['Web Services Status'] == 'NA'):
                                web_serv_na = web_serv_na + 1
                            else:
                                web_serv_bd = web_serv_bd + 1
                        main_output['value']['Web Services Status'].extend(tempout)
                        
                    if func == "cis_Adapter":
                        tempout = handleD.callfunction(server,themeid,customer,pid,servercat,prod,env,subregion,func,'','','','','','','','','','','','','','')
                        for tmp in tempout:
                            if (tmp['CIS Adapter Status'] == 'Available'):
                                cis_good = cis_good + 1
                            elif (tmp['CIS Adapter Status'] == 'NA'):
                                cis_na = cis_na + 1
                            else:
                                cis_bad = cis_bad + 1
                        main_output['value']['CIS Adapter Status'].extend(tempout)
                        
                else:
                    if (func == "cpu_utilization"):
                        tempout = handleD.callfunction(server,themeid,customer,pid,servercat,prod,env,subregion,func,'','','','','','','','','','','','','','')
                        if (tempout['Status'] == 'Good'):
                            cpu_utl_good = cpu_utl_good + 1
                        elif (tempout['Status'] == 'NA'):
                            cpu_utl_na = cpu_utl_na + 1
                        else:
                            cpu_utl_bad = cpu_utl_bad + 1 
                        main_output['value']['CPU Utilization'].append(tempout)
                        
                    if (func == "icmp_ping"):
                        tempout = handleD.callfunction(server,themeid,customer,pid,servercat,prod,env,subregion,func,'','','','','','','','','','','','','','')
                        if (tempout['ICMP Last Value'] == 'Available'):
                            icmp_ping_good = icmp_ping_good + 1
                        elif (tempout['ICMP Last Value'] == 'NA'):
                            icmp_ping_na = icmp_ping_na + 1
                        else:
                            icmp_ping_bad = icmp_ping_bad + 1           
                        main_output['value']['ICMP Ping'].append(tempout)
                        
                    if (func == "free_memory"):
                        tempout = handleD.callfunction(server,themeid,customer,pid,servercat,prod,env,subregion,func,'','','','','','','','','','','','','','')
                        if (tempout['Status'] == 'Good'):
                            mem_utl_good = mem_utl_good + 1
                        elif (tempout['Status'] == 'NA'):
                            mem_utl_na = mem_utl_na + 1
                        else:
                            mem_utl_bad = mem_utl_bad + 1
                        main_output['value']['Memory Utilization'].append(tempout)
                        
        ### Last Clock NA Sorting ###
        if themeid == 1 or themeid == 2 or "Start App Service" in tasknames:
            if 'ICMP Ping' in summ_tasknames:
                icmp_ping = main_output['value']['ICMP Ping']
                icmp_ping = sorted(icmp_ping, key=lambda d: d['ICMP Last Clock'], reverse=True)
                main_output['value']['ICMP Ping'] = icmp_ping
            if 'CPU Utilization' in summ_tasknames:
                cpu_util = main_output['value']['CPU Utilization']
                cpu_util = sorted(cpu_util, key=lambda d: d['CPU Utilization Last Clock'], reverse=True)
                main_output['value']['CPU Utilization'] = cpu_util
            if 'Memory Utilization' in summ_tasknames:
                mem_util = main_output['value']['Memory Utilization']
                mem_util = sorted(mem_util, key=lambda d: d['Free Memory Last Clock'], reverse=True)
                main_output['value']['Memory Utilization'] = mem_util
            if 'Service Status' in summ_tasknames:
                service_Status = main_output['value']['Service Status']
                service_Status = sorted(service_Status, key=lambda d: d['Service Last Clock'], reverse=True)
                main_output['value']['Service Status'] = service_Status
            if 'Internal URL Status' in summ_tasknames:
                iurl = main_output['value']['Internal URL Status']
                iurl = sorted(iurl, key=lambda d: d['Internal URL Clock'], reverse=True)
                main_output['Internal URL Status'] = iurl
            if 'Public URL Status' in summ_tasknames:
                purl = main_output['value']['Public URL Status']
                purl = sorted(purl, key=lambda d: d['Public URL Clock'], reverse=True)
                main_output['value']['Public URL Status'] = purl
            if 'Port Status' in summ_tasknames:
                port_status = main_output['value']['Port Status']
                port_status = sorted(port_status, key=lambda d: d['Port Last Clock'], reverse=True)
                main_output['value']['Port Status'] = port_status
            if 'CIS Adapter Status' in summ_tasknames:
                cis = main_output['value']['CIS Adapter Status']
                cis = sorted(cis, key=lambda d: d['CIS Adapter Last time'], reverse=True)
                main_output['value']['CIS Adapter Status'] = cis
            if 'Web Services Status' in summ_tasknames:
                web = main_output['value']['Web Services Status']
                web = sorted(web, key=lambda d: d['Web Services Last Time'], reverse=True)
                main_output['value']['Web Services Status'] = web
        ### Last Clock NA Sorting ###
        if themeid == 1 or themeid == 2 or "Start App Service" in tasknames:
            print("Summary Table")
            if 'ICMP Ping' in summ_tasknames:
                temp = [{'Task Name':'ICMP Ping','Good Count':icmp_ping_good,'Bad Count':icmp_ping_bad,'NA Count':icmp_ping_na}]
                main_output['value']['Summary Table'].extend(temp)
            if 'CPU Utilization' in summ_tasknames:
                temp = [{'Task Name':'CPU Utilization','Good Count':cpu_utl_good,'Bad Count':cpu_utl_bad,'NA Count':cpu_utl_na}]
                main_output['value']['Summary Table'].extend(temp)
            if 'Memory Utilization' in summ_tasknames:
                temp = [{'Task Name':'Memory Utilization','Good Count':mem_utl_good,'Bad Count':mem_utl_bad,'NA Count':mem_utl_na}]
                main_output['value']['Summary Table'].extend(temp)
            if 'Service Status' in summ_tasknames:
                temp = [{'Task Name':'Service Status','Good Count':serv_status_good,'Bad Count':serv_status_bad,'NA Count':serv_status_na}]
                main_output['value']['Summary Table'].extend(temp)
            if 'Internal URL Status' in summ_tasknames:
                temp = [{'Task Name':'Internal URL Status','Good Count':int_url_gd,'Bad Count':int_url_bd,'NA Count':int_url_na}]
                main_output['value']['Summary Table'].extend(temp)
            if 'Public URL Status' in summ_tasknames:
                temp = [{'Task Name':'Public URL Status','Good Count':pub_url_gd,'Bad Count':pub_url_bd,'NA Count':pub_url_na}]
                main_output['value']['Summary Table'].extend(temp)
            if 'UI Availability' in summ_tasknames:
                temp = [{'Task Name':'UI Availability','Good Count':ui_avail_gd,'Bad Count':ui_avail_bd,'NA Count':ui_avail_na}]
                main_output['value']['Summary Table'].extend(temp)
            if 'Port Status' in summ_tasknames:
                temp = [{'Task Name':'Port Status','Good Count':port_good,'Bad Count':port_bad,'NA Count':port_na}]
                main_output['value']['Summary Table'].extend(temp)
            if 'Public URL Status WMS' in summ_tasknames:
                temp = [{'Task Name':'Public URL Status','Good Count':pub_url_gd,'Bad Count':pub_url_bd,'NA Count':pub_url_na}]
                main_output['value']['Summary Table'].extend(temp)
            if 'Port Status WMS' in summ_tasknames:
                temp = [{'Task Name':'Port Status','Good Count':port_good,'Bad Count':port_bad,'NA Count':port_na}]
                main_output['value']['Summary Table'].extend(temp)
            if 'File Age Monitor' in summ_tasknames:
                temp = [{'Task Name':'File Age Monitor','Good Count':fa_mon_gd,'Bad Count':fa_mon_bd,'NA Count':fa_mon_na}]
                main_output['value']['Summary Table'].extend(temp)
            if 'Database Monitor' in summ_tasknames:
                temp = [{'Task Name':'Database Monitor','Good Count':db_mon_gd,'Bad Count':db_mon_bd,'NA Count':db_mon_na}]
                main_output['value']['Summary Table'].extend(temp)
            if 'CIS Adapter Status' in summ_tasknames:
                temp = [{'Task Name':'CIS Adapter Status','Good Count':cis_good,'Bad Count':cis_bad,'NA Count':cis_na}]
                main_output['value']['Summary Table'].extend(temp)
            if 'Web Services Status' in summ_tasknames:
                temp = [{'Task Name':'Web Services Status','Good Count':web_serv_gd,'Bad Count':web_serv_bd,'NA Count':web_serv_na}]
                main_output['value']['Summary Table'].extend(temp)
                
        #main_output['output'] = variable
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print(main_output)
        time.sleep(3)
        returnOutput.append(main_output)
    return JsonResponse(returnOutput,safe=False)
    

   





def handleRequest(request):
    returnOutput=[]
    servernames = request.GET['servername']
    product = request.GET['prod']
    customer = request.GET['customer']
    tasknames = request.GET['task_id']
    themeid = request.GET['theme_id']
    env = int(request.GET['env'])
    servercat =request.GET['servercat']
    pid = request.GET['pid']
    accountType = request.GET['as2acctype']
    accountName = request.GET['as2acc']
    start_date = request.GET['as2starttime']
    end_date = request.GET['as2endtime']
    
    #print(customer,pid)
    

    mname =request.GET['name']
    mid = request.GET['mid']
    cid = request.GET['cid']
    #start_time = datetime.datetime.strptime(request.GET['start_time'], "%Y/%m/%d %H:%M")
    #end_time = datetime.datetime.strptime( request.GET['end_time'], "%Y/%m/%d %H:%M")
    zserver = request.GET['zserver']
    emailid = request.GET['as2email']
    #emailid = 'thangamari.gnanaguru@blueyonder.com'
    print('mailid')
    print(emailid)

    ## Summary Count - Availability/Performance##
    summ_tasknames = tasknames.split(',')
    icmp_ping_good = 0
    icmp_ping_na = 0
    icmp_ping_bad = 0
    cpu_utl_good = 0
    cpu_utl_na = 0
    cpu_utl_bad = 0
    mem_utl_good = 0
    mem_utl_na = 0
    mem_utl_bad = 0
    serv_status_good = 0
    serv_status_bad = 0
    serv_status_na = 0
    port_good = 0
    port_bad = 0
    port_na = 0
    cis_good = 0
    cis_bad = 0
    cis_na = 0
    web_serv_gd = 0
    web_serv_bd = 0
    web_serv_na = 0
    int_url_gd = 0
    int_url_bd = 0
    int_url_na = 0
    pub_url_gd = 0
    pub_url_bd = 0
    pub_url_na = 0
    ui_avail_gd = 0
    ui_avail_bd = 0
    ui_avail_na = 0
    fa_mon_gd = 0
    fa_mon_bd = 0
    fa_mon_na = 0
    db_mon_gd = 0
    db_mon_bd = 0
    db_mon_na = 0
    ## Summary Count - Availability/Performance##
    
    main_output = {'funcnames':[],'headers':{},'value':{}}
    if themeid == '1' or themeid == '2' or themeid == '15':
        main_output['funcnames'].extend(['Summary Table'])
        main_output['headers']['Summary Table'] = ["Task Name",'Good Count','Bad Count','NA Count']
        main_output['value']['Summary Table'] = []
        ## Summary Count - Availability/Performance##
        summ_tasknames = tasknames.split(',')
        icmp_ping_good = 0
        icmp_ping_na = 0
        icmp_ping_bad = 0
        cpu_utl_good = 0
        cpu_utl_na = 0
        cpu_utl_bad = 0
        mem_utl_good = 0
        mem_utl_na = 0
        mem_utl_bad = 0
        serv_status_good = 0
        serv_status_bad = 0
        serv_status_na = 0
        port_good = 0
        port_bad = 0
        port_na = 0
        cis_good = 0
        cis_bad = 0
        cis_na = 0
        web_serv_gd = 0
        web_serv_bd = 0
        web_serv_na = 0
        int_url_gd = 0
        int_url_bd = 0
        int_url_na = 0
        pub_url_gd = 0
        pub_url_bd = 0
        pub_url_na = 0
        ui_avail_gd = 0
        ui_avail_bd = 0
        ui_avail_na = 0
        fa_mon_gd = 0
        fa_mon_bd = 0
        fa_mon_na = 0
        db_mon_gd = 0
        db_mon_bd = 0
        db_mon_na = 0
        ## Summary Count - Availability/Performance##
    for taskname in tasknames.split(','):
        if 'ICMP Ping' == taskname:
            main_output['funcnames'].extend(['ICMP Ping'])
            main_output['headers']['ICMP Ping'] = ["Server Name",'ICMP Last Value','ICMP Last Clock','Last Checked','Status']
            main_output['value']['ICMP Ping'] = []
            #main_output['header'].extend(['ICMP Last Value','ICMP Last Clock'])
        elif 'CPU Utilization' == taskname:
            main_output['funcnames'].extend(['CPU Utilization'])
            main_output['headers']['CPU Utilization'] = ["Server Name", "CPU Utilization Last Value", "CPU Utilization Last Clock",'Last Checked', "Threshold" , "Status"]
            main_output['value']['CPU Utilization'] = []
            #main_output['header'].extend(['CPU Utilization Last Value','CPU Utilization Last Clock'])
        elif 'Memory Utilization' == taskname:
            main_output['funcnames'].extend(['Memory Utilization'])
            main_output['headers']['Memory Utilization'] = ["Server Name",'Free Memory Last Value','Free Memory Last Clock', 'Last Checked', "Threshold" , "Status"]
            main_output['value']['Memory Utilization'] = []
            #main_output['header'].extend(['Memory Utilization Last Value','Memory Utilization Last Clock'])
        elif 'Service Status' == taskname:
            main_output['funcnames'].extend(['Service Status'])
            main_output['headers']['Service Status'] = ["Server Name", "Service Name", "Service Last Value", "Service Last Clock",'Last Checked','Status']
            main_output['value']['Service Status'] = []
            #main_output['header'].extend(['Service Name','Service Last Value','Service Last Clock'])
        elif 'Port Status' == taskname:
            main_output['funcnames'].extend(['Port Status'])
            main_output['headers']['Port Status'] = ["Server Name", 'Port Name', 'Port Last Value','Port Last Clock','Last Checked','Status']
            main_output['value']['Port Status'] = []
            #main_output['header'].extend(['Port Name', 'Port Last Value','Port Last Clock'])
        elif 'Internal URL Status' == taskname:
            main_output['funcnames'].extend(['Internal URL Status'])
            main_output['headers']['Internal URL Status'] = ['Server Name','Internal URL Name','Internal URL Value','Internal URL Clock','Last Checked','Status']
            #main_output['header'].extend(['Internal URL Name','Internal URL Value','Internal URL Clock'])
            main_output['value']['Internal URL Status'] = []
        elif 'Public URL Status' == taskname:
            main_output['funcnames'].extend(['Public URL Status'])
            main_output['headers']['Public URL Status'] = ['Customer','Public URL Name','Public URL Value','Public URL Clock','Last Checked','Status']
            main_output['value']['Public URL Status'] = []
            #main_output['value']['Public URL Status'] = {}
            #main_output['header'].extend(['Public URL Name','Public URL Value','Public URL Clock'])
        elif 'Port Status WMS' == taskname:
            main_output['funcnames'].extend(['Port Status'])
            main_output['headers']['Port Status'] = ["Server Name", 'Port Name', 'Port Last Value','Port Last Clock','Last Checked','Status']
            main_output['value']['Port Status'] = []
        elif 'Public URL Status WMS' == taskname:
            main_output['funcnames'].extend(['Public URL Status'])
            main_output['headers']['Public URL Status'] = ['Customer','Public URL Name','Public URL Value','Public URL Clock','Last Checked','Status']
            main_output['value']['Public URL Status'] = []
        elif 'Database Growth' == taskname:
            main_output['funcnames'].extend(['Database Growth'])
            main_output['headers']['Database Growth'] = ['Servername','DBName','OWNER','TABLE_NAME','NUM_ROWS']
            main_output['value']['Database Growth'] = []
            #main_output['header'].extend(['Database Growth Name','Database Growth Value','Database Growth Clock'])
        elif 'Database Session Count' == taskname:
            main_output['funcnames'].extend(['Database Session Count'])
            main_output['headers']['Database Session Count'] = ['Servername','INSTANCE_NAME','SESSION_COUNT']
            main_output['value']['Database Session Count'] = []
            #main_output['header'].extend(['Database Session Name','Database Session Value','Database Session Clock'])
        elif 'Database Tablespaces' == taskname:
            main_output['funcnames'].extend(['Database Tablespace'])
            main_output['headers']['Database Tablespace'] = ['ServerName','DBName','TABLESPACE','STATUS','TOTAL_MB','USED_MB','FREE_MB','PCT_USED']
            main_output['funcnames'].extend(['Table Indexes Health Status'])
            main_output['headers']['Table Indexes Health Status'] = ['ServerName','DBName','OWNER','DATETIME(LAST_ANALYZED)','COUNT']
        elif 'System global area Program global Area' == taskname:
            main_output['funcnames'].extend(['System global area Program global Area'])
            main_output['headers']['System global area Program global Area'] = ['Servername','INSTANCE_NAME','NAME','GB']
            main_output['value']['System global area Program global Area'] = []
        elif 'Blocking Sessions trend' == taskname:
            main_output['funcnames'].extend(['Blocking Sessions trend'])
            main_output['headers']['Blocking Sessions trend'] = ['ServerName','DBName','LOGIN_TIME','inst_id','sid','serial','sql_id','username','status','module','machine','event','program','blocking_Session','blocking_instance','blocking_session_status','WAIT_TIME','SECONDS_IN_WAIT']
            main_output['value']['Blocking Sessions trend'] = []
        elif 'Database maintnenace jobs and duration' == taskname:
            main_output['funcnames'].extend(['Backup Status'])
            main_output['headers']['Backup Status'] = ['ServerName','DBName','SESSION_KEY','INPUT_TYPE','STATUS','START_TIME','END_TIME','HRS','INPUT_GB','OUTPUT_GB','AUTOBACKUP_DONE']
            main_output['funcnames'].extend(['Reindexing'])
            main_output['headers']['Reindexing'] = ['ServerName','DBName','OWNER','TABLE_NAME','INDEX_NAME','INDEX_TYPE']
        elif 'CIS Adapter Status' == taskname:
            main_output['funcnames'].extend(['CIS Adapter Status'])
            main_output['headers']['CIS Adapter Status'] = ['Server Name','CIS Adapter Name','CIS Adapter Status','CIS Adapter Duration','CIS Adapter Last time','Status']
            main_output['value']['CIS Adapter Status'] = []
            #main_output['header'].extend(['CIS Adapter Name','CIS Adapter Status','CIS Adapter Last time'])
        elif 'Web Services Status' == taskname:
            main_output['funcnames'].extend(['Web Services Status'])
            main_output['headers']['Web Services Status'] = ['Server Name','Web Services Name','Web Services Status','Web Services URL','Web Services Last Time','Status']
            main_output['value']['Web Services Status'] = []
            #main_output['header'].extend(['Web Services Name','Web Services Status','Web Services Last Time'])
        elif 'File Age Monitor' == taskname:
            main_output['funcnames'].extend(['File Age Monitor'])
            main_output['headers']['File Age Monitor'] = ['Customer','File Age customer','File Age Good Count','File Age Bad Count']
            main_output['value']['File Age Monitor'] = []
            #main_output['header'].extend(['File Age customer','File Age Good Count','File Age Bad Count'])
        elif 'Database Monitor' == taskname:
            main_output['funcnames'].extend(['Database Monitor'])
            main_output['headers']['Database Monitor'] = ['Customer','DB customer','DB Good Count','DB Bad Count']
            main_output['value']['Database Monitor'] = []
            #main_output['header'].extend(['DB customer','DB Good Count','DB Bad Count'])
        elif 'Process Level' == taskname:
            main_output['funcnames'].extend(['Process Level'])
            main_output['headers']['Process Level'] = ['Request_Id','Status']
            main_output['value']['Process Level'] = []
            #main_output['header'].extend(['Process Name','Number of Process','Process Last checked Time'])
        elif 'Start App Service' == taskname:
            main_output['funcnames'].extend([taskname])
            main_output['headers'][taskname] = ['Server Name','Service Name','Status']
            main_output['value']['Start App Service'] = []
            ##### Run Availability Theme #####
            # ICMP PING
            main_output['funcnames'].extend(['ICMP Ping'])
            main_output['headers']['ICMP Ping'] = ["Server Name",'ICMP Last Value','ICMP Last Clock','Last Checked','Status']
            main_output['value']['ICMP Ping'] = []
            # Service Status
            main_output['funcnames'].extend(['Service Status'])
            main_output['headers']['Service Status'] = ["Server Name", "Service Name", "Service Last Value", "Service Last Clock",'Last Checked','Status']
            main_output['value']['Service Status'] = []
            # Port Status
            main_output['funcnames'].extend(['Port Status'])
            main_output['headers']['Port Status'] = ["Server Name", 'Port Name', 'Port Last Value','Port Last Clock','Last Checked','Status']
            main_output['value']['Port Status'] = []
            # Internal URL Status
            main_output['funcnames'].extend(['Internal URL Status'])
            main_output['headers']['Internal URL Status'] = ['Server Name','Internal URL Name','Internal URL Value','Internal URL Clock','Last Checked','Status']
            main_output['value']['Internal URL Status'] = []
            # Public URL Status
            main_output['funcnames'].extend(['Public URL Status'])
            main_output['headers']['Public URL Status'] = ['Customer','Public URL Name','Public URL Value','Public URL Clock','Last Checked','Status']
            main_output['value']['Public URL Status'] = []
            # CIS Adapter
            main_output['funcnames'].extend(['CIS Adapter Status'])
            main_output['headers']['CIS Adapter Status'] = ['Server Name','CIS Adapter Name','CIS Adapter Status','CIS Adapter Duration','CIS Adapter Last time','Status']
            main_output['value']['CIS Adapter Status'] = []
            # Web Service status
            main_output['funcnames'].extend(['Web Services Status'])
            main_output['headers']['Web Services Status'] = ['Server Name','Web Services Name','Web Services Status','Web Services URL','Web Services Last Time','Status']
            main_output['value']['Web Services Status'] = []
            # File Age Monitor
            main_output['funcnames'].extend(['File Age Monitor'])
            main_output['headers']['File Age Monitor'] = ['Customer','File Age customer','File Age Good Count','File Age Bad Count']
            main_output['value']['File Age Monitor'] = []
            # DB Monitor
            main_output['funcnames'].extend(['Database Monitor'])
            main_output['headers']['Database Monitor'] = ['Customer','DB customer','DB Good Count','DB Bad Count']
            main_output['value']['Database Monitor'] = []
            # UI Availability
            main_output['funcnames'].extend(['UI Availability'])
            main_output['headers']['UI Availability'] = ['Name','Test Name','Test_Status','node','Time','Status']
            main_output['value']['UI Availability'] = []
            # process Validation
            main_output['funcnames'].extend(['Process Level'])
            main_output['headers']['Process Level'] = ['Request_Id','Status']
            main_output['value']['Process Level'] = []
            ##### Run Availability Theme #####
        elif 'Stop App Service' == taskname:
            main_output['funcnames'].extend([taskname])
            main_output['headers'][taskname] = ['Server Name','Service Name','Status']
            main_output['value']['Stop App Service'] = []
        elif 'UI Sanity Checks' == taskname:
            main_output['funcnames'].extend(['UI Sanity Checks'])
            main_output['headers']['UI Sanity Checks'] = ['Name','Test Name','Status','node']
            main_output['value']['UI Sanity Checks'] = []
            #main_output['header'].extend(['Name','Test Name','Status','node'])
        elif 'UI Availability' == taskname:
            main_output['funcnames'].extend(['UI Availability'])
            main_output['headers']['UI Availability'] = ['Name','Test Name','Test_Status','node','Time','Status']
            main_output['value']['UI Availability'] = []
            #main_output['header'].extend(['Name','Test Name','Check Name','Status','node'])
        elif 'I/O Rate' == taskname:
            main_output['funcnames'].extend(['I/O Rate'])
            main_output['headers']['I/O Rate'] = ['Server Name','IO Name','IO Value','Last checked Time','Last Checked']
            main_output['value']['I/O Rate'] = []
            #main_output['header'].extend(['IO Name','IO Value','Last checked Time'])
        elif 'AS2/SFTP' == taskname:
            main_output['funcnames'].extend(['AS2/SFTP Gateways'])
            main_output['headers']['AS2/SFTP Gateways'] = ['Customer','Gateway Server','Zabbix Location','Gateway URL Name','Gateway URL Value','Gateway URL Last Clock']
            #main_output['header'].extend(['Gateway Server','Zabbix Location','Gateway URL Name','Gateway URL Value','Gateway URL Last Clock'])
            main_output['funcnames'].extend(['AS2/SFTP'])
            main_output['headers']['AS2/SFTP'] = ['Customer','Mailbox','Transport','Start_Date','End_Date','Direction','Status','File_Name','File_Size_Bytes']
            #main_output['header'].extend(['Mailbox','Transport','Start_Date','End_Date','Direction','Status','File_Name','File_Size_Bytes'])
        elif 'Server Reboot' == taskname:
            main_output['funcnames'].extend(['Server Reboot'])
            main_output['headers']['Server Reboot'] = ['status']
            
            #main_output['header'].extend(['status'])
        elif 'Create Maintenance' == taskname:
            main_output['funcnames'].extend(['Create Maintenance'])
            main_output['headers']['Create Maintenance'] = ['Server Name','Output Status']
        elif 'Update Maintenance' == taskname:
            main_output['funcnames'].extend(['Update Maintenance'])
            main_output['headers']['Update Maintenance'] = ['Output Status']
        elif 'Free Disk Space' == taskname:
            main_output['funcnames'].extend(['Free Disk Space'])
            main_output['headers']['Free Disk Space'] = ["PSComputerName","DeviceID","SizeGB","FreeGB"]
            main_output['value']['Free Disk Space'] = []
        elif 'SKU and DFU count' == taskname:
            main_output['funcnames'].extend(['SKU and DFU count'])
            main_output['headers']['SKU and DFU count'] = ['Hostname','SKU','DFU']
            main_output['value']['SKU and DFU count'] = []
        elif 'Access check - for scpoadm user' == taskname:
            main_output['funcnames'].extend(['Access check - for scpoadm user'])
            main_output['headers']['Access check - for scpoadm user'] = ['Date','Hostname','Users','Total RAM','RAM Use','RAM Available']
            main_output['value']['Access check - for scpoadm user'] = []
        ### Cat Man ###
        elif 'Citrix Timeout' == taskname:
            main_output['funcnames'].extend(['Citrix Timeout'])
            main_output['headers']['Citrix Timeout'] = ['Server Name','Citrix Timeout']
            main_output['value']['Citrix Timeout'] = []
        elif 'Citrix Connections' == taskname:
            main_output['funcnames'].extend(['Citrix Connections'])
            main_output['headers']['Citrix Connections'] = ['Server Name','Citrix Connections']
            main_output['value']['Citrix Connections'] = []
        elif 'Citrix Profilepath' == taskname:
            main_output['funcnames'].extend(['Citrix Profilepath'])
            main_output['headers']['Citrix Profilepath'] = ['Server Name','Citrix Profilepath']
            main_output['value']['Citrix Profilepath'] = []
        ### Cat Man ###
        else:
            main_output['headers'].append(taskname)
    if env == 1:
        prod=1
    else:
        prod=2
    funcname= [mssql.func_name(task) for task in tasknames.split(',')]    
##    main_output['header'] = tasknames.split(',')
    func_name = [a['func_name'][0][0]  for a in funcname]
    #print(func_name)
    # or func['func_name'][0][0] == "" or func['func_name'][0][0] == ""
    variable = []
    if 'main' in func_name :
        result = (handleD.callfunction('',themeid,customer,pid,servercat,prod,env,'','main','','','','','','','','','','','','','',''))
        #print(result)
        func_name.remove('main')
        main_output['value']['UI Sanity Checks'] = result
        variable.extend(a for a in result)
    if 'ui_availability' in func_name :
        result = (handleD.callfunction('',themeid,customer,pid,servercat,prod,env,'ui_availability','','','','','','','','','','','','','',''))
        #print(result)
        func_name.remove('ui_availability')
        for tmp in result:
            if (tmp['Test_Status'] == 'PASS'):
                ui_avail_gd = ui_avail_gd + 1
            elif (tmp['Test_Status'] == 'NA'):
                ui_avail_na = ui_avail_na + 1
            else:
                ui_avail_bd = ui_avail_bd + 1
        main_output['value']['UI Availability'] = result
        variable.extend(a for a in result)
    if 'public_url' in func_name:
        result = (handleD.callfunction((servernames.split(","))[0],themeid,customer,pid,servercat,prod,env,'','public_url','','','','','','','','','','','','','',''))
        #print(result)
        func_name.remove('public_url')
        for tmp in result:
            if (tmp['Status'] == 'Good'):
                pub_url_gd = pub_url_gd + 1
            elif (tmp['Status'] == 'NA'):
                pub_url_na = pub_url_na + 1
            else:
                pub_url_bd = pub_url_bd + 1
        main_output['value']['Public URL Status'] = result
        #variable.extend(a for a in result)
    if 'public_url_wms' in func_name:
        result = (handleD.callfunction((servernames.split(","))[0],themeid,customer,pid,servercat,prod,env,'','public_url_wms','','','','','','','','','','','','','',''))
        #print(result)
        func_name.remove('public_url_wms')
        for tmp in result:
            if (tmp['Status'] == 'Good'):
                pub_url_gd = pub_url_gd + 1
            elif (tmp['Status'] == 'NA'):
                pub_url_na = pub_url_na + 1
            else:
                pub_url_bd = pub_url_bd + 1
        main_output['value']['Public URL Status'] = result
    if 'gateway_details' in func_name :
        result1 = (handleD.callfunction('',themeid,customer,pid,servercat,prod,env,'','gateway_details','','','','','','','','','','','','','',''))
        #print(result1)
        main_output['value']['AS2/SFTP Gateways'] = result1
        variable.extend(a for a in result1)
        result2 = (handleD.callfunction('',themeid,customer,pid,servercat,prod,env,'','transfer_report',accountType,accountName,start_date,end_date,'','','','','','','','',result1,emailid))
        main_output['value']['AS2/SFTP'] = result2
        variable.extend(a for a in result2)
        func_name.remove('gateway_details')
    if 'file_monitorDetails' in func_name :
        result = (handleD.callfunction('',themeid,customer,pid,servercat,prod,env,'','file_monitorDetails','','','','','','','','','','','','','',''))
        #print(result)
        func_name.remove('file_monitorDetails')
        for tmp in result:
            if (tmp['File Age Good Count'] == 'NA' or tmp['File Age Bad Count'] == 'NA'):
                fa_mon_na = fa_mon_na + 1
            else:
                fa_mon_gd = fa_mon_gd + int(tmp['File Age Good Count'])
                fa_mon_bd = fa_mon_bd + int(tmp['File Age Bad Count'])
        main_output['value']['File Age Monitor'] = result
        variable.extend(a for a in result)
    if 'db_monitorDetails' in func_name :
        result_1 = (handleD.callfunction('',themeid,customer,pid,servercat,prod,env,'','db_monitorDetails','','','','','','','','','','','','','',''))
        func_name.remove('db_monitorDetails')
        for tmp in result_1:
            if (tmp['DB Good Count'] == 'NA' or tmp['DB Bad Count'] == 'NA'):
                db_mon_na = db_mon_na + 1
            else:
                db_mon_gd = db_mon_gd + int(tmp['DB Good Count'])
                db_mon_bd = db_mon_bd + int(tmp['DB Bad Count'])
        main_output['value']['Database Monitor'] = result_1
        variable.extend(a for a in result_1)
    if "process_validation" in func_name:
        tempout = handleD.callfunction('',themeid,customer,pid,servercat,prod,env,'','process_validation','','','','','','','','','','','','','','')
        main_output['value']['Process Level'].extend(tempout)
    if 'create_maintenance' in func_name:
        end_epoch = datetime.datetime.strptime(request.GET['etime'], "%Y/%m/%d %H:%M")
        start_epoch = datetime.datetime.strptime(request.GET['stime'], "%Y/%m/%d %H:%M")
        result = (handleD.callfunction(servernames,themeid,customer,pid,servercat,prod,env,'','create_maintenance','','','','',mname,start_epoch,end_epoch,'','','','','','',''))
        #func_name.remove('create_maintenance')
        main_output['value']['Create Maintenance'] = result
        #variable.extend(a for a in result_1)
    if 'reboot_server_tms' in func_name:
        if 'create_maintenance' not in func_name:
            func_name.insert(0,'create_maintenance')
            main_output['funcnames'].extend(['Create Maintenance'])
            main_output['headers']['Create Maintenance'] = ['Server Name','Output Status']
            IST = pytz.timezone('Asia/Kolkata') 
            end_epoch = datetime.datetime.strptime((datetime.datetime.now(IST) + datetime.timedelta(minutes=15)).strftime("%Y/%m/%d %H:%M"),  "%Y/%m/%d %H:%M")
            start_epoch = datetime.datetime.strptime(datetime.datetime.now(IST).strftime("%Y/%m/%d %H:%M"),  "%Y/%m/%d %H:%M")
            mname = customer + '_reboot_server_' +str(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
            result = (handleD.callfunction(servernames,themeid,customer,pid,servercat,prod,'create_maintenance','','','','',mname,start_epoch,end_epoch,'','','','','','',''))
            main_output['value']['Create Maintenance'] = result
        result_1 = (handleD.callfunction(servernames,themeid,customer,pid,servercat,prod,env,'','reboot_server_tms','','','','','','','','','','','','','',''))
        #func_name.remove('reboot_server_tms')
        main_output['value']['Server Reboot'] = result_1
        variable.extend(a for a in result_1)
    if "start_app_service" in func_name:
        '''if 'create_maintenance' not in func_name:
            func_name.insert(0,'create_maintenance')
            main_output['funcnames'].extend(['Create Maintenance'])
            main_output['headers']['Create Maintenance'] = ['Server Name','Output Status']
            IST = pytz.timezone('Asia/Kolkata') 
            end_epoch = datetime.datetime.strptime((datetime.datetime.now(IST) + datetime.timedelta(minutes=15)).strftime("%Y/%m/%d %H:%M"),  "%Y/%m/%d %H:%M")
            start_epoch = datetime.datetime.strptime(datetime.datetime.now(IST).strftime("%Y/%m/%d %H:%M"),  "%Y/%m/%d %H:%M")
            mname = customer + '_start_stop_serv_' + str(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
            result = (handleD.callfunction(servernames,themeid,customer,pid,servercat,prod,'create_maintenance','','','','',mname,start_epoch,end_epoch,'','','','','','',''))
            main_output['value']['Create Maintenance'] = result'''
        func_name = ["icmp_ping","service_status","internal_url","port_status","cis_Adapter","web_service","process_validation"]
        for server in servernames.split(','):
            result = (handleD.callfunction(server,themeid,customer,pid,servercat,prod,env,'','start_app_service','','','','','','','','','','','','','',''))
            main_output['value']['Start App Service'].extend(result)
            ######### Availability Theme #########
        ## UI Availability ##
        result = (handleD.callfunction('',themeid,customer,pid,servercat,prod,env,'','ui_availability','','','','','','','','','','','','','',''))
        main_output['value']['UI Availability'] = result
        variable.extend(a for a in result)
        ## PUBLIC URL ##
        result = (handleD.callfunction((servernames.split(","))[0],themeid,customer,pid,servercat,prod,env,'','public_url','','','','','','','','','','','','','',''))
        main_output['value']['Public URL Status'] = result
        ## File Age Monitor ##
        result = (handleD.callfunction('',themeid,customer,pid,servercat,prod,env,'','file_monitorDetails','','','','','','','','','','','','','',''))
        main_output['value']['File Age Monitor'] = result
        variable.extend(a for a in result)
        ## DB Monitor ##
        result_1 = (handleD.callfunction('',themeid,customer,pid,servercat,prod,env,'','db_monitorDetails','','','','','','','','','','','','','',''))
        main_output['value']['Database Monitor'] = result_1
        variable.extend(a for a in result_1)
        ## Process Validation ##
        tempout = handleD.callfunction('',themeid,customer,pid,servercat,prod,env,'','process_validation','','','','','','','','','','','','','','')
        main_output['value']['Process Level'].extend(tempout)
        ## ------ Server Based Tasks ------ ##
        for server in servernames.split(','):
            print("sample")
            for func in func_name:
                tempout = None
                #ICMP Ping
                if (func == "icmp_ping"):
                    tempout = handleD.callfunction(server,themeid,customer,pid,servercat,prod,env,'',func,'','','','','','','','','','','','','','')
                    main_output['value']['ICMP Ping'].append(tempout)
                #Service Status
                if func == "service_status":
                    tempout = handleD.callfunction(server,themeid,customer,pid,servercat,prod,env,'',func,'','','','','','','','','','','','','','')
                    main_output['value']['Service Status'].extend(tempout)
                #Internal url
                if func == "internal_url":
                    tempout = handleD.callfunction(server,themeid,customer,pid,servercat,prod,env,'',func,'','','','','','','','','','','','','','')
                    main_output['value']['Internal URL Status'].extend(tempout)
                # port Status
                if func == "port_status":
                    tempout = handleD.callfunction(server,themeid,customer,pid,servercat,prod,env,'',func,'','','','','','','','','','','','','','')
                    main_output['value']['Port Status'].extend(tempout)
                #CIS Adapter
                if func == "cis_Adapter":
                    tempout = handleD.callfunction(server,themeid,customer,pid,servercat,prod,env,'',func,'','','','','','','','','','','','','','')
                    main_output['value']['CIS Adapter Status'].extend(tempout)
                # Web Service
                if func == "web_service":
                    tempout = handleD.callfunction(server,themeid,customer,pid,servercat,prod,env,'',func,'','','','','','','','','','','','','','')
                    main_output['value']['Web Services Status'].extend(tempout)
                # Process Level
        func_name = []
        ######### Availability Theme #########
    if "stop_app_service" in func_name:
        if 'create_maintenance' not in func_name:
            func_name.insert(0,'create_maintenance')
            main_output['funcnames'].extend(['Create Maintenance'])
            main_output['headers']['Create Maintenance'] = ['Server Name','Output Status']
            IST = pytz.timezone('Asia/Kolkata') 
            end_epoch = datetime.datetime.strptime((datetime.datetime.now(IST) + datetime.timedelta(minutes=15)).strftime("%Y/%m/%d %H:%M"),  "%Y/%m/%d %H:%M")
            start_epoch = datetime.datetime.strptime(datetime.datetime.now(IST).strftime("%Y/%m/%d %H:%M"),  "%Y/%m/%d %H:%M")
            mname = customer + '_start_stop_serv_' + str(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
            result = (handleD.callfunction(servernames,themeid,customer,pid,servercat,prod,env,'','create_maintenance','','','','',mname,start_epoch,end_epoch,'','','','','','',''))
            main_output['value']['Create Maintenance'] = result
        for server in servernames.split(','):
            result = (handleD.callfunction(server,themeid,customer,pid,servercat,prod,env,'','stop_app_service','','','','','','','','','','','','','',''))
            main_output['value']['Stop App Service'].extend(result)
    if 'update_maintenance' in func_name:
        start_time = datetime.datetime.strptime(request.GET['start_time'], "%Y/%m/%d %H:%M")
        end_time = datetime.datetime.strptime( request.GET['end_time'], "%Y/%m/%d %H:%M")
        result = (handleD.callfunction(servernames,themeid,customer,pid,servercat,prod,env,'','update_maintenance','','','','','','','',mid,cid,start_time,end_time,zserver,'',''))
        func_name.remove('update_maintenance')
        main_output['value']['Update Maintenance'] = result
    if "Backup_Reindexing" in func_name:
        result1 = handleD.callfunction(servernames,themeid,customer,pid,servercat,prod,env,'','db_backup_status','','','','','','','','','','','','','','')
        #print(result1)
        main_output['value']['Backup Status'] = result1
        variable.extend(a for a in result1)
        result2 = handleD.callfunction(servernames,themeid,customer,pid,servercat,prod,env,'','db_reindexing','','','','','','','','','','','','','','')
        main_output['value']['Reindexing'] = result2
        variable.extend(a for a in result2)
        func_name.remove('Backup_Reindexing')
    if "db_tablespace" in func_name:
##        tempout = handleD.callfunction(server,themeid,customer,pid,servercat,prod,func,'','','','','','','','','','','','')
##        main_output['value']['Database Tablespaces'] = tempout
        result1 = handleD.callfunction(servernames,themeid,customer,pid,servercat,prod,env,'','db_tablespace','','','','','','','','','','','','','','')
        #print(result1)
        main_output['value']['Database Tablespace'] = result1
        variable.extend(a for a in result1)
        result2 = handleD.callfunction(servernames,themeid,customer,pid,servercat,prod,env,'','DB_index_Healthstat','','','','','','','','','','','','','','')
        main_output['value']['Table Indexes Health Status'] = result2
        variable.extend(a for a in result1)
        func_name.remove('db_tablespace')

    if "disk_free_space" in func_name:
        tempout = handleD.callfunction(servernames,themeid,customer,pid,servercat,prod,env,'',"disk_free_space",'','','','','','','','','','','','','','')
        main_output['value']['Free Disk Space'].extend(tempout)
    if "scpoadm_users" in func_name:
        tempout = handleD.callfunction(servernames,themeid,customer,pid,servercat,prod,env,'',"scpoadm_users",'','','','','','','','','','','','','','')
        main_output['value']['Access check - for scpoadm user'].extend(tempout)

    if 'file_monitorDetails' not in func_name or 'db_monitorDetails' not in func_name:
        if 'create_maintenance' in func_name:
            func_name.remove('create_maintenance')
        print(func_name)
        for server in servernames.split(','):
            output = {'server name':server}
            for func in func_name:
                if (func == "port_status_wms" or func == "sku_dfu" or func == "disk_free_space" or func == "internal_url" or func == "service_status" or func == "port_status" or func == "db_session" or func == "db_growth" or func == "cis_Adapter" or func == "web_service" or func == "start_app_service" or func == "stop_app_service" or func == "process_validation" or func == "IO_rate"  or func =="SGA_PGA" or func == "Blocking_Sessions" ):
                    #print(server)
                    if func == "service_status":
                        tempout = handleD.callfunction(server,themeid,customer,pid,servercat,prod,env,func,'','','','','','','','','','','','','','')
                        for tmp in tempout:
                            if (tmp['Service Last Value'] == 'Running'):
                                serv_status_good = serv_status_good + 1
                            elif (tmp['Service Last Value'] == 'NA'):
                                serv_status_na = serv_status_na + 1
                            else:
                                serv_status_bad = serv_status_bad + 1 
                        main_output['value']['Service Status'].extend(tempout)
                    if func == "internal_url":
                        tempout = handleD.callfunction(server,themeid,customer,pid,servercat,prod,env,'',func,'','','','','','','','','','','','','','')
                        for tmp in tempout:
                            if (tmp['Status'] == 'Good'):
                                int_url_gd = int_url_gd + 1
                            elif (tmp['Status'] == 'NA'):
                                int_url_na = int_url_na + 1
                            else:
                                int_url_bd = int_url_bd + 1 
                        main_output['value']['Internal URL Status'].extend(tempout)
                    if func == "port_status":
                        tempout = handleD.callfunction(server,themeid,customer,pid,servercat,prod,env,'',func,'','','','','','','','','','','','','','')
                        for tmp in tempout:
                            if (tmp['Port Last Value'] == 'Up'):
                                port_good = port_good + 1
                            elif (tmp['Port Last Value'] == 'NA'):
                                port_na = port_na + 1
                            else:
                                port_bad = port_bad + 1
                        main_output['value']['Port Status'].extend(tempout)
                    if func == "port_status_wms":
                        tempout = handleD.callfunction(server,themeid,customer,pid,servercat,prod,env,'',func,'','','','','','','','','','','','','','')
                        for tmp in tempout:
                            if (tmp['Port Last Value'] == 'Up'):
                                port_good = port_good + 1
                            elif (tmp['Port Last Value'] == 'NA'):
                                port_na = port_na + 1
                            else:
                                port_bad = port_bad + 1
                        main_output['value']['Port Status'].extend(tempout)
                    if func == "db_session":
                        tempout = handleD.callfunction(server,themeid,customer,pid,servercat,prod,env,'',func,'','','','','','','','','','','','','','')
                        main_output['value']['Database Session Count'].extend(tempout)
                    if func == "db_growth":
                        tempout = handleD.callfunction(server,themeid,customer,pid,servercat,prod,env,'',func,'','','','','','','','','','','','','','')
                        main_output['value']['Database Growth'].extend(tempout)
##                    if func == "db_tablespace":
####                        tempout = handleD.callfunction(server,themeid,customer,pid,servercat,prod,func,'','','','','','','','','','','','')
####                        main_output['value']['Database Tablespaces'] = tempout
##                        result1 = handleD.callfunction(server,themeid,customer,pid,servercat,prod,'db_tablespace','','','','','','','','','','','','')
##                        #print(result1)
##                        main_output['value']['Database Tablespace'] = result1
##                        variable.extend(a for a in result1)
##                        result2 = handleD.callfunction(server,themeid,customer,pid,servercat,prod,'DB_index_Healthstat','','','','','','','','','','','','')
##                        main_output['value']['Table Indexes Health Status'] = result2
##                        variable.extend(a for a in result1)
##                        func_name.remove('db_tablespace')
                    if func == "SGA_PGA":
                        tempout = handleD.callfunction(server,themeid,customer,pid,servercat,prod,env,'',func,'','','','','','','','','','','','','','')
                        main_output['value']['System global area Program global Area'].extend(tempout)
                    if func == "Blocking_Sessions":
                        tempout = handleD.callfunction(server,themeid,customer,pid,servercat,prod,env,'',func,'','','','','','','','','','','','','','')
                        main_output['value']['Blocking Sessions trend'].extend(tempout)
                    if func == "IO_rate":
                        tempout = handleD.callfunction(server,themeid,customer,pid,servercat,prod,env,'',func,'','','','','','','','','','','','','','')
                        main_output['value']['I/O Rate'].extend(tempout)
                    '''if func == "start_app_service":
                        tempout = handleD.callfunction(server,themeid,customer,pid,servercat,prod,func,'','','','','','','','','','','','','','')
                        main_output['value']['Start App Service'].extend(tempout)
                    if func == "stop_app_service":
                        tempout = handleD.callfunction(server,themeid,customer,pid,servercat,prod,func,'','','','','','','','','','','','','','')
                        main_output['value']['Stop App Service'].extend(tempout)'''
                    if func == "web_service":
                        tempout = handleD.callfunction(server,themeid,customer,pid,servercat,prod,env,'',func,'','','','','','','','','','','','','','')
                        for tmp in tempout:
                            if (tmp['Web Services Status'] == 'Available'):
                                web_serv_gd = web_serv_gd + 1
                            elif (tmp['Web Services Status'] == 'NA'):
                                web_serv_na = web_serv_na + 1
                            else:
                                web_serv_bd = web_serv_bd + 1
                        main_output['value']['Web Services Status'].extend(tempout)
                    if func == "cis_Adapter":
                        tempout = handleD.callfunction(server,themeid,customer,pid,servercat,prod,env,'',func,'','','','','','','','','','','','','','')
                        for tmp in tempout:
                            if (tmp['CIS Adapter Status'] == 'Available'):
                                cis_good = cis_good + 1
                            elif (tmp['CIS Adapter Status'] == 'NA'):
                                cis_na = cis_na + 1
                            else:
                                cis_bad = cis_bad + 1
                        main_output['value']['CIS Adapter Status'].extend(tempout)
                    if func == "sku_dfu":
                        tempout = handleD.callfunction(server,themeid,customer,pid,servercat,prod,env,'',func,'','','','','','','','','','','','','','')
                        main_output['value']['SKU and DFU count'].extend(tempout)
                    else:
                        result = (handleD.callfunction(server,themeid,customer,pid,servercat,prod,env,'',func,'','','','','','','','','','','','','',''))
                        #print(result)
                        variable.extend(a for a in result)
                else:
                    if (func == "cpu_utilization"):
                        tempout = handleD.callfunction(server,themeid,customer,pid,servercat,prod,env,'',func,'','','','','','','','','','','','','','')
                        if (tempout['Status'] == 'Good'):
                            cpu_utl_good = cpu_utl_good + 1
                        elif (tempout['Status'] == 'NA'):
                            cpu_utl_na = cpu_utl_na + 1
                        else:
                            cpu_utl_bad = cpu_utl_bad + 1 
                        main_output['value']['CPU Utilization'].append(tempout)
                    if (func == "icmp_ping"):
                        tempout = handleD.callfunction(server,themeid,customer,pid,servercat,prod,env,'',func,'','','','','','','','','','','','','','')
                        if (tempout['ICMP Last Value'] == 'Available'):
                            icmp_ping_good = icmp_ping_good + 1
                        elif (tempout['ICMP Last Value'] == 'NA'):
                            icmp_ping_na = icmp_ping_na + 1
                        else:
                            icmp_ping_bad = icmp_ping_bad + 1           
                        main_output['value']['ICMP Ping'].append(tempout)
                    if (func == "free_memory"):
                        tempout = handleD.callfunction(server,themeid,customer,pid,servercat,prod,env,'',func,'','','','','','','','','','','','','','')
                        if (tempout['Status'] == 'Good'):
                            mem_utl_good = mem_utl_good + 1
                        elif (tempout['Status'] == 'NA'):
                            mem_utl_na = mem_utl_na + 1
                        else:
                            mem_utl_bad = mem_utl_bad + 1
                        main_output['value']['Memory Utilization'].append(tempout)
##                    if func == "service_status":
##                        tempout = handleD.callfunction(server,themeid,customer,pid,servercat,prod,func,'','','','','','','','','','','','','','')
##                        main_output['value']['Service Status'].extend(tempout)
                    ### Cat Man ###
                    if (func == "citrix_timeout"):
                        tempout = handleD.callfunction(server,user,themeid,customer,pid,servercat,prod,env,'',func,'','','','','','','','','','','','','','')
                        #,'','','','','','','','','','','','')
                        #print(tempout)
                        main_output['value']['Citrix Timeout'].append(tempout)
                    if (func == "citrix_connections"):
                        tempout = handleD.callfunction(server,user,themeid,customer,pid,servercat,prod,env,'',func,'','','','','','','','','','','','','','')
                        #,'','','','','','','','','','','','')
                        #print(tempout)
                        main_output['value']['Citrix Connections'].append(tempout)
                    if (func == "citrix_profilepath"):
                        tempout = handleD.callfunction(server,user,themeid,customer,pid,servercat,prod,env,'',func,'','','','','','','','','','','','','','')
                        #,'','','','','','','','','','','','')Citrix Profilepath
                        #print(tempout)
                        main_output['value']['Citrix Profilepath'].append(tempout)
                    ### Cat Man ###
                    #output.update(handleD.callfunction(server,themeid,customer,pid,servercat,prod,func,'','','',''))
            if output != {'server name':server}:
                variable.insert(0,output)
            #returnOutput.append(variable)
    ### Last Clock NA Sorting ###
    if 'ICMP Ping' in summ_tasknames:
        icmp_ping = main_output['value']['ICMP Ping']
        icmp_ping = sorted(icmp_ping, key=lambda d: d['ICMP Last Clock'], reverse=True)
        main_output['value']['ICMP Ping'] = icmp_ping
    if 'CPU Utilization' in summ_tasknames:
        cpu_util = main_output['value']['CPU Utilization']
        cpu_util = sorted(cpu_util, key=lambda d: d['CPU Utilization Last Clock'], reverse=True)
        main_output['value']['CPU Utilization'] = cpu_util
    if 'Memory Utilization' in summ_tasknames:
        mem_util = main_output['value']['Memory Utilization']
        mem_util = sorted(mem_util, key=lambda d: d['Free Memory Last Clock'], reverse=True)
        main_output['value']['Memory Utilization'] = mem_util
    if 'Service Status' in summ_tasknames:
        service_Status = main_output['value']['Service Status']
        service_Status = sorted(service_Status, key=lambda d: d['Service Last Clock'], reverse=True)
        main_output['value']['Service Status'] = service_Status
    if 'Internal URL Status' in summ_tasknames:
        iurl = main_output['value']['Internal URL Status']
        iurl = sorted(iurl, key=lambda d: d['Internal URL Clock'], reverse=True)
        main_output['Internal URL Status'] = iurl
    if 'Public URL Status' in summ_tasknames:
        purl = main_output['value']['Public URL Status']
        purl = sorted(purl, key=lambda d: d['Public URL Clock'], reverse=True)
        main_output['value']['Public URL Status'] = purl
    if 'Port Status' in summ_tasknames:
        port_status = main_output['value']['Port Status']
        port_status = sorted(port_status, key=lambda d: d['Port Last Clock'], reverse=True)
        main_output['value']['Port Status'] = port_status
    if 'CIS Adapter Status' in summ_tasknames:
        cis = main_output['value']['CIS Adapter Status']
        cis = sorted(cis, key=lambda d: d['CIS Adapter Last time'], reverse=True)
        main_output['value']['CIS Adapter Status'] = cis
    if 'Web Services Status' in summ_tasknames:
        web = main_output['value']['Web Services Status']
        web = sorted(web, key=lambda d: d['Web Services Last Time'], reverse=True)
        main_output['value']['Web Services Status'] = web
    ### Last Clock NA Sorting ###
    if themeid == '1' or themeid == '2' or themeid == '15':
        print("Summary Table")
        if 'ICMP Ping' in summ_tasknames:
            temp = [{'Task Name':'ICMP Ping','Good Count':icmp_ping_good,'Bad Count':icmp_ping_bad,'NA Count':icmp_ping_na}]
            main_output['value']['Summary Table'].extend(temp)
        if 'CPU Utilization' in summ_tasknames:
            temp = [{'Task Name':'CPU Utilization','Good Count':cpu_utl_good,'Bad Count':cpu_utl_bad,'NA Count':cpu_utl_na}]
            main_output['value']['Summary Table'].extend(temp)
        if 'Memory Utilization' in summ_tasknames:
            temp = [{'Task Name':'Memory Utilization','Good Count':mem_utl_good,'Bad Count':mem_utl_bad,'NA Count':mem_utl_na}]
            main_output['value']['Summary Table'].extend(temp)
        if 'Service Status' in summ_tasknames:
            temp = [{'Task Name':'Service Status','Good Count':serv_status_good,'Bad Count':serv_status_bad,'NA Count':serv_status_na}]
            main_output['value']['Summary Table'].extend(temp)
        if 'Internal URL Status' in summ_tasknames:
            temp = [{'Task Name':'Internal URL Status','Good Count':int_url_gd,'Bad Count':int_url_bd,'NA Count':int_url_na}]
            main_output['value']['Summary Table'].extend(temp)
        if 'Public URL Status' in summ_tasknames:
            temp = [{'Task Name':'Public URL Status','Good Count':pub_url_gd,'Bad Count':pub_url_bd,'NA Count':pub_url_na}]
            main_output['value']['Summary Table'].extend(temp)
        if 'UI Availability' in summ_tasknames:
            temp = [{'Task Name':'UI Availability','Good Count':ui_avail_gd,'Bad Count':ui_avail_bd,'NA Count':ui_avail_na}]
            main_output['value']['Summary Table'].extend(temp)
        if 'Port Status' in summ_tasknames:
            temp = [{'Task Name':'Port Status','Good Count':port_good,'Bad Count':port_bad,'NA Count':port_na}]
            main_output['value']['Summary Table'].extend(temp)
        if 'Public URL Status WMS' in summ_tasknames:
            temp = [{'Task Name':'Public URL Status','Good Count':pub_url_gd,'Bad Count':pub_url_bd,'NA Count':pub_url_na}]
            main_output['value']['Summary Table'].extend(temp)
        if 'Port Status WMS' in summ_tasknames:
            temp = [{'Task Name':'Port Status','Good Count':port_good,'Bad Count':port_bad,'NA Count':port_na}]
            main_output['value']['Summary Table'].extend(temp)
        if 'File Age Monitor' in summ_tasknames:
            temp = [{'Task Name':'File Age Monitor','Good Count':fa_mon_gd,'Bad Count':fa_mon_bd,'NA Count':fa_mon_na}]
            main_output['value']['Summary Table'].extend(temp)
        if 'Database Monitor' in summ_tasknames:
            temp = [{'Task Name':'Database Monitor','Good Count':db_mon_gd,'Bad Count':db_mon_bd,'NA Count':db_mon_na}]
            main_output['value']['Summary Table'].extend(temp)
        if 'CIS Adapter Status' in summ_tasknames:
            temp = [{'Task Name':'CIS Adapter Status','Good Count':cis_good,'Bad Count':cis_bad,'NA Count':cis_na}]
            main_output['value']['Summary Table'].extend(temp)
        if 'Web Services Status' in summ_tasknames:
            temp = [{'Task Name':'Web Services Status','Good Count':web_serv_gd,'Bad Count':web_serv_bd,'NA Count':web_serv_na}]
            main_output['value']['Summary Table'].extend(temp)
            
    #main_output['output'] = variable
    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    print(main_output)
    return JsonResponse(main_output,safe=False)

def handleEnabledisable(request):
    returnOutput=[]
    servernames = request.GET['servername']
    product = request.GET['prod']   
    
    customer = request.GET['customer']
    tasknames = request.GET['task_id']
    themeid = request.GET['theme_id']
    env =request.GET['env']
    servercat =request.GET['servercat']
    pid = request.GET['pid']
    main_output = {'header':[],'output':[]}
    for taskname in tasknames.split(','):
        main_output['header'].append(taskname)
    if env == 1:
        prod=1
    else:
        prod=2
    funcname= [mssql.func_name(task) for task in tasknames.split(',')]
    e = datetime.datetime.now()
    now = e.strftime("%Y-%m-%d %H:%M:%S")
    for server in servernames.split(','):
        output = {'server name':server}
        for func in funcname:
            output.update(handleD.callfunction(server,themeid,customer,pid,servercat,prod,func['func_name'][0][0],'','','','','','','','',''))
            #print(output[taskname])
            mssql.insert_query(columnname = ['activity','customer_name','server_name','status','product_id','created_by','created_on'],columnvalue = [taskname,customer,server,output[taskname],pid,'test',now],tablename = 'wms_enable_logs')
        returnOutput.append(output)
    main_output['output'] = returnOutput
    return JsonResponse(main_output,safe=False)

def testoutput(request):
    funcnames = ['CPU Utilization','Memory Utilization']
    headerdict = {'CPU Utilization':['Server Name','CPU Utilization Last Value','CPU Utilization Last Clock'],'Memory Utilization':['Server Name','Memory Utilization Last Value','Memory Utilization Last Clock']}
    valdict = {'CPU Utilization':[{'Server Name':'1','CPU Utilization Last Value':'1','CPU Utilization Last Clock':'1'},{'Server Name':'2','CPU Utilization Last Value':'2','CPU Utilization Last Clock':'2'}],'Memory Utilization':[{'Server Name':'1','Memory Utilization Last Value':'1','Memory Utilization Last Clock':'1'}]}
    main_output = {'funcnames':funcnames,'headers':headerdict,'value':valdict}
    return JsonResponse(main_output,safe=False)

############# APP VALIDATION ######

def getHmmEnv(request):
    data = mssql.hmmEnv()
    return JsonResponse(data,safe=False)

def getHmmCustomer(request):
    dc_id = request.GET['dcid']
    data = mssql.hmmCustomer(dc_id)
    return JsonResponse(data,safe=False)

def getHmmValCustomer(request):
    dc_id = request.GET['dcid']
    pid = request.GET['pid']
    eid = request.GET['eid']
    data = mssql.hmmValCustomer(dc_id,pid,eid)
    return JsonResponse(data,safe=False)

def getHmmProduct(request):
    data = mssql.hmmProduct()
    return JsonResponse(data,safe=False)

def getServerType(request):
    data = mssql.getServerType()
    return JsonResponse(data,safe=False)

def getHmmEnvironment(request):
    sid = request.GET['sid']
    data = mssql.hmmEnvironment(sid)
    return JsonResponse(data,safe=False)

def getHmmUrl(request):
    cusid = request.GET['cusid']
    url_type = request.GET['url_type']
    data = mssql.hmmUrl(cusid,url_type)
    return JsonResponse(data,safe=False)

def doHmmActivity(request):
    main_output = {}
    data = {}
    user = request.GET['user']
    jid = request.GET['jid']
    dc_id = request.GET['dcid']
    server = request.GET['server']
    cus_id = request.GET['cusid']
    headers = { "Content-Type": "application/json" }
    data['extra_vars'] = {
        "grp": server,
        "user": user,
        "jid": jid,
        "dc_id": dc_id,
        "cus_id": cus_id
        }
    response = requests.post('http://10.120.78.130/api/v2/job_templates/149/launch/', auth = HTTPBasicAuth('1029310', 'P@$$word@84529'),json= data ,headers=headers)
    if json.loads(response.text)['status']:
        main_output['result'] = "Success"
    else:
        main_output['result'] = "Fail"
    #main_output = [{'user':data,'jid':jid,'dc_id':dc_id,'server':server,'cus_id':cus_id}]
    return JsonResponse(main_output,safe=False)

def getHmmLogs(request):
    main_output = {}
    counter = 1
    user = request.GET['user']
    data = mssql.HmmLogs(user)
    for i in data:
        i['sno']=counter
        counter+=1
    main_output['header'] = list(data[0].keys())
    main_output['result'] = data
    return JsonResponse(main_output,safe=False)

def getHmmLog3(request):
    main_output = {}
    counter = 1
    user = request.GET['user']
    data = mssql.HmmLog(user)
    for i in data:
        i['sno']=counter
        counter+=1
    main_output['header'] = list(data[0].keys())
    main_output['result'] = data
    return JsonResponse(main_output,safe=False)

def getHmmSummaryLogs(request):
    main_output = {}
    summary_id = request.GET['id']
    data = mssql.HmmSummaryLogs(summary_id)
    main_output['header'] = list(data[0].keys())
    main_output['result'] = data
    return JsonResponse(main_output,safe=False)

def getHmmTable(request):
    main_output = {}
    counter = 1
    table = request.GET['table']
    data = mssql.HmmTable(table)
    for i in data:
        i['sno']=counter
        counter+=1
    main_output['header'] = list(data[0].keys())
    main_output['result'] = data
    main_output['table'] = table
    return JsonResponse(main_output,safe=False)
    
def doDelete(request):
    main_output={}
    user=request.GET['user']
    table = request.GET['table']
    delid=request.GET['id']
    delete = mssql.delete_query_hmm(table,delid)
    return JsonResponse(main_output,safe=False)	
	
	
def doEventEdit(request):
    main_output={}
    user=request.GET['user']
    db=request.GET['db']
    upid=request.GET['upid']
    eventid=request.GET['eventid']
    eventname=request.GET['eventname']
    up = mssql.HmmUpdateEvent(db,eventname,eventid,upid)
    main_output = [{'user':up,'db':db,'upid':upid,'evid':eventid,'evn':eventname}]
    return JsonResponse(main_output,safe=False)		
		
def doEventAdd(request):
    main_output={}
    user=request.GET['user']
    db=request.GET['db']
    eventid=request.GET['eventid']
    eventname=request.GET['eventname']
    ins = mssql.HmmAddEvent(db,eventname,eventid)
    main_output = [{'user':ins,'db':db,'evid':eventid,'evn':eventname}]
    return JsonResponse(main_output,safe=False)

def doUrlAdd(request):
    main_output={}
    user=request.GET['user']
    db=request.GET['db']
    dcid=request.GET['dcid']
    cid=request.GET['cid']
    urltype=request.GET['urltype']
    urlname=request.GET['urlname']
    ins = mssql.HmmAddUrl(db,dcid,cid,urltype,urlname)
    return JsonResponse(main_output,safe=False)
	

def doUrlEdit(request):
    main_output={}
    user=request.GET['user']
    db=request.GET['db']
    dcid=request.GET['dcid']
    upid=request.GET['upid']
    cid=request.GET['cid']
    urltype=request.GET['urltype']
    urlname=request.GET['urlname']
    up = mssql.HmmUpdateUrl(db,dcid,cid,urltype,urlname,upid)
    return JsonResponse(main_output,safe=False)

def doServerAdd(request):
    main_output={}
    user=request.GET['user']
    db=request.GET['db']
    dcid=request.GET['dcid']
    cid=request.GET['cid']
    servername=request.GET['servername']
    ins = mssql.HmmAddServer(db,dcid,cid,servername)
    return JsonResponse(main_output,safe=False)

def doServerEdit(request):
    main_output={}
    user=request.GET['user']
    db=request.GET['db']
    dcid=request.GET['dcid']
    upid=request.GET['upid']
    cid=request.GET['cid']
    servername=request.GET['servername']
    up = mssql.HmmUpdateServer(db,dcid,cid,servername,upid)
    return JsonResponse(main_output,safe=False)

def doFileAdd(request):
    main_output={}
    user=request.GET['user']
    db=request.GET['db']
    filepath=request.GET['filepath']
    filename=request.GET['filename']
    ins = mssql.HmmAddFile(db,filename,filepath)
    return JsonResponse(main_output,safe=False)

def doFileEdit(request):
    main_output={}
    user=request.GET['user']
    db=request.GET['db']
    upid=request.GET['upid']
    filepath=request.GET['filepath']
    filename=request.GET['filename']
    up = mssql.HmmUpdateFile(db,filename,filepath,upid)
    return JsonResponse(main_output,safe=False)


def doSsl(request):
    main_output={}
    dcid=request.GET['dcid']
    cus=request.GET['cus']
    ssl_ava=request.GET['sslava']
    counter=1
    data = mssql.doSsl(dcid,cus,ssl_ava)
    for i in data:
        i['sno']=counter
        counter+=1
    return JsonResponse(data,safe=False)

def doCustomerAdd(request):
    main_output={}
    user=request.GET['user']
    db=request.GET['db']
    dcid=request.GET['dcid']
    customername=request.GET['customername']
    alias=request.GET['alias']
    pid=request.GET['pid']
    eid=request.GET['eid']
    ins = mssql.HmmAddCustomer(db,dcid,customername,alias,pid,eid)
    return JsonResponse(main_output,safe=False)

def doCustomerEdit(request):
    main_output={}
    user=request.GET['user']
    db=request.GET['db']
    upid=request.GET['upid']
    dcid=request.GET['dcid']
    customername=request.GET['customername']
    alias=request.GET['alias']
    pid=request.GET['pid']
    eid=request.GET['eid']
    up = mssql.HmmUpdateCustomer(db,dcid,customername,alias,pid,eid,upid)
    return JsonResponse(main_output,safe=False)


############# END APP VALIDATION ######

############# F5 MAINTENANCE ######

def getHmmProductF5(request):
    dc_id=request.GET['dc_id']
    data = mssql.hmmProductF5(dc_id)
    return JsonResponse(data,safe=False)

def getHmmValCustomerF5(request):
    dc_id = request.GET['dc_id']
    pid = request.GET['pid']
    data = mssql.hmmValCustomerF5(dc_id,pid)
    return JsonResponse(data,safe=False)

def getHmmEnvironmentF5(request):
    dc_id = request.GET['dc_id']
    pid = request.GET['pid']
    cus = request.GET['cus']
    data = mssql.hmmEnvironmentF5(dc_id,pid,cus)
    return JsonResponse(data,safe=False)

def getHmmUrlF5(request):
    dc_id = request.GET['dc_id']
    pid = request.GET['pid']
    cus = request.GET['cus']
    eid = request.GET['eid']
    data = mssql.hmmUrlF5(dc_id,pid,cus,eid)
    return JsonResponse(data,safe=False)

def doF5Activity(request):
    main_output = {}
    user = request.GET['user']
    url_ids = request.GET['url_ids']
    urls = request.GET['urls']
    task = request.GET['task']
    url_ids_list = url_ids.split(',')
    url_list = urls.split(',')
    val_res = mssql.f5Validation(url_ids,task)
    if val_res[0]['url_id']:
        t=[]
        f=[]
        [f.append(i) if i['error']  else t.append(i)  for i in val_res]
        if f:
            for tmp in f:
                cur_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                ins = mssql.F5Addlogs("f5_maintenance_logs",user,tmp['url_id'],task,'Failed',tmp['error'],'Failed','NA','NA','Failed','NA','NA',cur_date)
        res = mssql.f5activity(t,"f5_maintenance_logs",user,task)
        main_output['status'] = "Success"
        main_output['msg'] = "Script had been executed.Please check logs for activity status"
    else:
        print("fail")
        main_output['status'] = "Failed"
        main_output['msg'] = "Validation Failed for urls {one}".format(one=val_res['msg'])
    
    return JsonResponse(main_output,safe=False)

def doF5Add(request):
    main_output={}
    user=request.GET['user'].strip()
    db=request.GET['db'].strip()
    dc_id=request.GET['dc_id'].strip()
    cus_id=request.GET['cus_id'].strip()
    url_id=request.GET['url_id'].strip()
    idns=request.GET['idns'].strip()
    edns=request.GET['edns'].strip()
    waf_be=request.GET['waf_be'].strip()
    fw_nat=request.GET['fw_nat'].strip()
    active_ip=request.GET['active_ip'].strip()
    standby_ip=request.GET['standby_ip'].strip()
    vip_ip=request.GET['vip_ip'].strip()
    vs_name=request.GET['vs_name'].strip()
    other_urls=request.GET['other_urls'].strip()
    mprule=request.GET['mprule'].strip()
    mpdg=request.GET['mpdg'].strip()
    vs_val=request.GET['vs_val'].strip()
    pre=request.GET['pre'].strip()
    taskact=request.GET['taskact'].strip()
    ins = mssql.HmmAddF5(db,dc_id,cus_id,url_id,idns,edns,waf_be,fw_nat,active_ip,standby_ip,vip_ip,vs_name,other_urls,mprule,mpdg,vs_val,pre,taskact)
    return JsonResponse(main_output,safe=False)

def doF5Edit(request):
    main_output={}
    user=request.GET['user'].strip()
    db=request.GET['db'].strip()
    upid=request.GET['upid'].strip()
    idns=request.GET['idns'].strip()
    edns=request.GET['edns'].strip()
    waf_be=request.GET['waf_be'].strip()
    fw_nat=request.GET['fw_nat'].strip()
    active_ip=request.GET['active_ip'].strip()
    standby_ip=request.GET['standby_ip'].strip()
    vip_ip=request.GET['vip_ip'].strip()
    vs_name=request.GET['vs_name'].strip()
    other_urls=request.GET['other_urls'].strip()
    mprule=request.GET['mprule'].strip()
    mpdg=request.GET['mpdg'].strip()
    vs_val=request.GET['vs_val'].strip()
    pre=request.GET['pre'].strip()
    taskact=request.GET['taskact'].strip()
    up = mssql.HmmUpdateF5(db,idns,edns,waf_be,fw_nat,active_ip,standby_ip,vip_ip,vs_name,other_urls,mprule,mpdg,vs_val,pre,taskact,upid)
    return JsonResponse(main_output,safe=False)

############# End F5 MAINTENANCE ######
		
	
##zabbix logs ##

def getZabbixLogs(request):
    main_output = {}
    counter = 1
    task = request.GET['task']
    data = mssql.getZabbixLogs(task)
    for i in data:
        i['sno']=counter
        counter+=1
    main_output['header'] = list(data[0].keys())
    main_output['result'] = data
    return JsonResponse(main_output,safe=False)

## end zabbix logs ##


def doRestartAdd(request):
    main_output={}
    db=request.GET['db']
    cus_id=request.GET['cus_id']
    url_id=request.GET['url_id']
    active_ip=request.GET['active_ip']
    standby_ip=request.GET['standby_ip']
    pool_name=request.GET['pool_name']
    res_type=request.GET['res_type']
    syncCheckSleepTime=request.GET['syncCheckSleepTime']
    syncCheckCount=request.GET['syncCheckCount']
    drain_timeout=request.GET['drain_timeout']
    typee=request.GET['type']
    bigfix_id=request.GET['bigfix_id']
    ins = mssql.RestartAdd(db,cus_id,url_id,active_ip,standby_ip,pool_name,res_type,syncCheckSleepTime,syncCheckCount,drain_timeout,typee,bigfix_id)
    return JsonResponse(main_output,safe=False)

def doRestartEdit(request):
    main_output={}
    db=request.GET['db']
    upid=request.GET['upid']
    cus_id=request.GET['cus_id']
    url_id=request.GET['url_id']
    active_ip=request.GET['active_ip']
    standby_ip=request.GET['standby_ip']
    pool_name=request.GET['pool_name']
    res_type=request.GET['res_type']
    syncCheckSleepTime=request.GET['syncCheckSleepTime']
    syncCheckCount=request.GET['syncCheckCount']
    drain_timeout=request.GET['drain_timeout']
    typee=request.GET['type']
    bigfix_id=request.GET['bigfix_id']
    ins = mssql.RestartUpdate(db,cus_id,url_id,active_ip,standby_ip,pool_name,res_type,syncCheckSleepTime,syncCheckCount,drain_timeout,typee,bigfix_id,upid)
    return JsonResponse(main_output,safe=False)

def ValidateValue(request):
    db=request.GET['db']
    name =request.GET['name']
    value =request.GET['value']
    res = mssql.ValidateValue(db,name,value)
    if res:
        return JsonResponse({'exist':1},safe=False)
    else:
        return JsonResponse({'exist':0},safe=False)
    


