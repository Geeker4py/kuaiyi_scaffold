import os
import re
import time
import ConfigParser
import shutil


def colored(text, color=None, on_color=None, attrs=None):
    fmt_str = '\x1B[;%dm%s\x1B[0m'
    if color is not None:
        text = fmt_str % (color, text)

    if on_color is not None:
        text = fmt_str % (on_color, text)

    if attrs is not None:
        for attr in attrs:
            text = fmt_str % (color, text)

    return text

def printError(msg):
    print colored(msg, color=36)

def printWarning(msg):
    print colored(msg, color=33)

def printInfo(msg):
    print colored(msg, color=37)
      

header = '''\
_____\ \ \___   _____     ___    ___    \_\ \     __     __      __    ___
/\ '__`\ \  _ `\/\ '__`\  /'___\ / __`\  /'_` \  /'__`\ /'_ `\  /'__`\/' _ `\ \\
\ \ \L\ \ \ \ \ \ \ \L\ \/\ \__//\ \L\ \/\ \L\ \/\  __//\ \L\ \/\  __//\ \/\ \ \\
 \ \ ,__/\ \_\ \_\ \ ,__/\ \____\ \____/\ \___,_\ \____\ \____ \ \____\ \_\ \_\ \\
  \ \ \/  \/_/\/_/\ \ \/  \/____/\/___/  \/__,_ /\/____/\/___L\ \/____/\/_/\/_/ \\
   \ \_\           \ \_\                                  /\____/ \\
    \/_/            \/_/                                  \_/__/ For leyue with Library v. 0.0.1 \\
        author and idea : yaojialu \\
        e-mail : yaojialu@leyue100.com \\
        site : https://github.com/Geeker4py/leyue-phpcodegen.git | www.leyue100.com 
'''
path=''
token=''
current_project=''
ext=''
clone_project=''
def init():
    cf = ConfigParser.ConfigParser() 
    cf.read("gen_config.conf")
    secs = cf.sections() 
    global path
    path = cf.get("base", "path") 
    global token
    token= cf.get("base","bootstrap_file")
    global current_project
    current_project=cf.get("base","current_project")
    global ext
    ext=cf.get("base","ext")
    global clone_project
    clone_project=cf.get("base","clone_project_name")
    #print path
    #return
    f = file('header')
    # if no mode is specified, 'r'ead mode is assumed by default
    while True:
        line = f.readline()
        if len(line) == 0: # Zero length indicates EOF
            break
        print line,
        #printWarning(line)
        # Notice comma to avoid automatic newline added by Python
    f.close() # close the file
    getCommand()

def getCommand():
    command=raw_input('>>>')
    if command!='exit':
    	command_lines=command.split() 
    	#print command_lines
    	makeCommand(command_lines)
        getCommand()
    else:    	
        print '>>>Now is exit'

def makeCommand(params):
    if params!='':
        if params[0]=='create':
        	second_params=params[1]
        	p = re.compile('^([a-z]+):([A-Za-z]+)$')
        	match=p.findall(second_params)
        	if match:
        	    action=match[0][0]
                name=match[0][1]                        
                if action=='project':
                    #print name
                    createProject(name)
                elif(action=='adapter'):	
                    createAdapter(name)
                elif(action=='test'):            
                    createTest(name)
                elif(action=='crontab'):
                    print name
                elif(action=='api'):	
                    print name
        elif(params[0]=='init'):
            print 'init'
        elif(params[0]=='help'):	
            print 'help'


def createProject(name):
    global current_project
    global clone_project
    global path    
    folder_path='/library/Adapter/Platform/'
    current_project_path=path+folder_path+name
    if os.path.exists(current_project_path):
    	_error('This project already exists ,you can change anothor name')
    else:
        if clone_project!='':
            os.mkdir(current_project_path)  
            if os.path.exists(current_project_path):            	
                current_clone_project_path=path+folder_path+clone_project
                #createAllDir(current_clone_project_path) 
                createAllFile(current_clone_project_path,current_project_path)                                                            	

    

def createAdapter(name):
    global current_project
    global path
    global ext

    folder_path='/library/Adapter/Platform/'
    base_path=path+folder_path
    current_file_path=os.path.join(base_path, current_project) +'/'+name+ext
    if os.path.exists(current_file_path):
        _error('This test file already exists , you can change anothor one')
    else:
        time= getTime()  
        name=getFirstUpper(name)  
        parent_file_path=base_path+'/'+name+ext
        adapter_body='''
<?php

/**
 * '''+name+'''.php
 * author: [yourname@leyue100]
 * date: ['''+time+''']
 */
class Adapter_Platform_'''+current_project+'''_'''+name+''' extends Adapter_Platform_'''+current_project+'''_Base 
    implements Adapter_Platform_'''+name+''' {
'''
        adapter_parent_body='''
<?php
/**
 * '''+name+'''.php
 *
 * author: [yourname@leyue100]
 * date: ['''+time+''']
 */

interface Adapter_Platform_'''+name+''' {
    
} 
'''

        if os.path.exists(parent_file_path):
            createFile(current_file_path,adapter_body)
        else:	
            createFile(parent_file_path,adapter_parent_body)
            createFile(current_file_path,adapter_body)                         
        
def createTest(name):
    ishas=checkFolder()
    global current_project
    global path
    global ext
    if ishas:
        if current_project=='null':
            print 'current project maybe is NULL , Please check a project for checkout:xxxx or create it'
        else:        	
            isOk=checkFolder('/tests/Adapter/')
            if isOk:
                time=getTime()
                name=getFirstUpper(name)            	
                test_body='''
<?php
/**
 * '''+name+'''.php
 *
 * author: [yourname@leyue100.com]
 * date: ['''+time+''']
 */
ini_set('display_errors',1);
error_reporting(E_ALL);
include_once(__DIR__.'/../../../indexc.php');

try {

    $adapter = Adapter_Client::getInstance();
    $reg = $adapter->getModule('your_project_code', DispatchModel::MODULE_REGISTERED);
    $reg->test('1','2','3',array());
}catch (Exception $e){
    var_dump($e->getMessage());
}
'''

                folder_path='/tests/Adapter/'
                base_path=path+folder_path

                current_file_path=os.path.join(base_path, current_project) +'/'+name+ext
                if os.path.exists(current_file_path):
                    _error('This test file is exists , you can change anothor file name')
                else:
                	createFile(current_file_path,test_body)
            else:
            	_error('The project is not exists . First your must be create it')

            #print test_body	
	        
def createCrontab(name):
    global path
    global token
    global current_project
    folder_path='/queue/crontab/'
    base_path=path+folder_path
    current_file_path=path+folder_path+'/'+name+ext
    if os.path.exists(current_file_path):
        _error('This test file is exists , you can change anothor file name')
    else:
    	time=getTime()
        crontab_body='''
<?php
/**
 * '''+name+'''.php
 *
 * author: [yourname@leyue100]
 * data: ['''+time+''']
 *
 */

define('APPLICATION_PATH', dirname(__FILE__) . '/../..');

if (!extension_loaded("yaf")) {
    include(APPLICATION_PATH . '/framework/loader.php');
}
$application = new Yaf_Application(APPLICATION_PATH . "/conf/application.ini");
$application->bootstrap()->getDispatcher()->dispatch();


'''  
        createFile(current_file_path,crontab_body)  


def createAPI(name):
    global path
    global token
    global current_project

    folder_path='/application/modules/Api/'
    current_file_path=path+folder_path+'/'+name+ext
    if os.path.exists(current_file_path):
        _error('The file is exists . you can change anothor file name')
    else:
    	time=getTime()
    	name=getFirstUpper(name)
        api_body='''
<?php

/**
 * '''+name+'''.php
 *
 * author: [yourname@leyue100]
 * date: ['''+time+''']
 */
class '''+name+'''Controller extends AControllerModel {

}
'''
        createFile(current_file_path,api_body)                


def checkFile(name):
    pass

def createFile(file_path,file_body):
    if file_path!='':
        file_handle=open(file_path,'w') 
        file_handle.write(file_body)
        file_handle.close()    

def checkFolder(folder_path=''):
    global path
    global token
    global current_project
    if path!='' and token!='' and folder_path=='':
        current_path=os.path.join(path, token)
        if os.path.exists(current_path):
            return 1                 
        else:
            return 0
    else:
        base_path=path+folder_path
        current_path=os.path.join(base_path, current_project)            	
        if os.path.exists(current_path):
            return 1
        else:
            return 0   
            

def getFirstUpper(params):
    if params!='':
        params = params.lower()
        params = params[0].upper() + params[1:]
        return params

def getTime():
    ISOTIMEFORMAT='%Y-%m-%d %X'
    return time.strftime( ISOTIMEFORMAT, time.localtime() )

def help():
    pass 

def _error(msg):
    print msg

def getFileList(p):
        p = str(p)
        if p=="":
            return []
        #p = p.replace( "/","\\")
        if p[ -1] != "/":
            p = p+"/"
        a = os.listdir(p)
        b = [ x  for x in a if os.path.isfile( p + x ) ]
        return b

def getDirList(p):
        p = str( p )
        if p=="":
              return []
        #p = p.replace( "/","\\")
        if p[ -1] != "/":
            p = p+"/"
        a = os.listdir(p)
        b = [ x for x in a if os.path.isdir( p + x ) ]
        return b

def createAllDir(path):
    global clone_project
    global current_project
    dir_list=getDirList(path)
    for i in xrange(len(dir_list)):
        if dir_list[i]:
            current_path=path+'/'+dir_list[i]
            #print path+'/'+dir_list[i]
            current_folder_path=current_path.replace(clone_project,current_project)
            if os.path.exists(current_folder_path) and os.path.isdir(current_folder_path):
                pass
            else:
                #print current_folder_path
                os.mkdir(current_folder_path)
            
            file_list=getFileList(current_path)
            for f in xrange(len(file_list)):
                #print current_path+'/'+file_list[f]
                if os.path.isfile(current_path+'/'+file_list[f]):
                    file_path=current_path+'/'+file_list[f]
                    file_path=file_path.replace(clone_project,current_project)
                    #print file_path
                    if not os.path.exists(file_path):
                        shutil.copyfile(current_path+'/'+file_list[f],file_path)                     
                    #current_file=open(file_path,'w') 


            createAllDir(current_path)


               
def createAllFile(clone_path,_path):
    file_list=getFileList(clone_path)
    global path
    global current_project
    global clone_project

    for i in xrange(len(file_list)):
        file_path=clone_path+'/'+file_list[i]
        clone_path=file_path
        file_path=file_path.replace(clone_project,current_project)
        if not os.path.exists(file_path):
            shutil.copyfile(clone_path,file_path) 
       
        with open(file_path,"r+") as f:
            d = f.read()
            d.replace(clone_project, current_project)
            f.write(d)           


if __name__=="__main__":
    init()
