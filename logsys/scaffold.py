# -*- coding: UTF-8 -*-
import os
import re
import time
import ConfigParser
import shutil
import sys

class Scaffold():
    """docstring for Scaffold"""
    def __init__(self):
        self.header='''\
_____\ \ \___   _____     ___    ___    \_\ \     __     __      __    ___
/\ '__`\ \  _ `\/\ '__`\  /'___\ / __`\  /'_` \  /'__`\ /'_ `\  /'__`\/' _ `\ \r
\ \ \L\ \ \ \ \ \ \ \L\ \/\ \__//\ \L\ \/\ \L\ \/\  __//\ \L\ \/\  __//\ \/\ \ \r
 \ \ ,__/\ \_\ \_\ \ ,__/\ \____\ \____/\ \___,_\ \____\ \____ \ \____\ \_\ \_\ \r
  \ \ \/  \/_/\/_/\ \ \/  \/____/\/___/  \/__,_ /\/____/\/___L\ \/____/\/_/\/_/ \r
   \ \_\           \ \_\                                  /\____/ \r
    \/_/            \/_/                                  \_/__/ For leyue with Library v. 0.0.1 \r
        author and idea : yaojialu \r
        e-mail : yaojialu@leyue100.com \r
        site : https://github.com/Geeker4py/leyue-phpcodegen-logsys.git | www.leyue100.com 
'''
        self.path=''
        self.token=''
        self.ext=''
    def showHeader(self):
        #print self.header
        self.printSelf(self.header,33)

    def initParams(self):
        config = ConfigParser.ConfigParser() 
        config.read("logsys_config.conf")
        config.sections() 
        self.path=config.get("base","path")
        self.token= config.get("base","bootstrap_file")
        self.ext=config.get("base","ext")
        self.getCommand() 

    def getCommand(self):
        command=raw_input('>>>')
        if command!='exit':
            command_lines=command.split() 
            #print command_lines
            self.makeCommand(command_lines)
            self.getCommand()
        else:       
            print '>>>Now is exit'
            sys.exit()

    def makeCommand(self,params):                        
        if params!='':
            if len(params)>=2:                
                second_params=params[1]
                p = re.compile('^([a-z]+):([A-Za-z]+)$')
                match=p.findall(second_params)
                if params[0]=='add':                
                    if match:
                        action=match[0][0]
                        name=match[0][1]                        
                        if action=='task':
                            #print name
                            self.createTask(name)
                        if action=='admin':
                            self.createAdmin(name,params)
                        if action=='model':
                            self.createModel(name,params)
                        if action=='test':
                            self.createTest(name,params)    
                        if action=='help':
                            self._help()                                                                                                 
                elif(params[0]=='update'):
                    if match:
                        action=match[0][0]
                        name=match[0][1]
                        if action=='admin':
                            self.updateAdminController(name,params)
                elif(params[0]=='help'):    
                    self._help()
            else:
                self._help()       

    def  createAdmin(self,name,params):
        admin_controller_path='application/modules/Admin/controllers/'
        admin_views_path='application/modules/Admin/views/'
        admin_path=self.path+admin_controller_path+name+self.ext
        admin_view_folder_path=self.path+admin_views_path+name
        time= self.getTime()
        if os.path.exists(admin_path):
            self._error('This admin controllers already exists ,you can change anothor name')
        else:          
            admin_php_body='''
<?php
            /**
 * '''+name+'''.php
 * author: [yourname@leyue100]
 * date: ['''+time+''']
 */

class Controller extends AdminControllerModel {
    /**
     * @author [yourname@leyue100]
     * @date ['''+time+''']
     * @return bool
     */
    public function indexAction(){
        //设置大区数据
        $this->assignWRegion();
        //设置医院WIFI数据
        $this->assignWList();
        //top数据
        $top_data = [];
        $today = date('Ymd');
        $yesterday = date("Ymd",strtotime("-1 day"));
        $top_data['today'] = $this->assignTopData($today);
        $top_data['yesterday']= $this->assignTopData($yesterday);
        $this->_view->assign('top_data', $top_data);
        //默认当前时间
        $this->_view->assign('now_date', date('Y年m月d日'));

        return TRUE;
    }

    /**
    * @author: [yourname@leyue100]
    * @date: ['''+time+''']
    * @return bool
    */
    public function detailAction(){
        //设置大区数据
        $this->assignWRegion();
        //设置医院WIFI数据
        $this->assignWList();

        $groupList = AnalyseModel::getWifiGroup();
        $this->_view->assign('groupList',$groupList);
        //默认当前时间
        $this->_view->assign('now_date', date('Y年m月d日'));
        $adsZones = $this->getAllZones(2);
        $this->_view->assign('zones', $adsZones);
        return TRUE;
    }
'''          
        self.createFile(admin_path,admin_php_body,"create admin controller "+name+".php")
        self.createviews(name,admin_view_folder_path)   
        self.createAdminFunc(admin_path,params)                                     
        #for i in xrange(0, len(params)):
        #    if i>=2:
        #        print params[i]         
    
    def createAdminFunc(self,admin_path,params):
        for i in xrange(0, len(params)):
            if i>=2:
                file_handle=open(admin_path,'a')
                time= self.getTime()
                func_body='''
    /**
     * @author [yourname@leyue100.com]
     * @date ['''+time+''']
     */
    public function '''+params[i]+'''Action(){}'''
                file_handle.write(func_body)
                self.printSelf("create Action "+params[i]+" in admin controller",36)
        end_body='''
}
'''
        file_handle.write(end_body)
        file_handle.close()

    def createviews(self,admin_view_folder_name,admin_view_folder_path):
        if(os.path.exists(admin_view_folder_path)):
            self._error('This views folder already exists ,you can change anothor name')
        else:
            os.mkdir(admin_view_folder_path) 
            self.printSelf("create views folder "+admin_view_folder_name,34)
            index_path=admin_view_folder_path+"/index.phtml"
            detail_path=admin_view_folder_path+"/detail.phtml"       
            self.createFile(index_path,"","create views default file index.phtml")
            self.createFile(detail_path,"","create views default file detail.phtml")                    

    def  createTask(self,name):
        tool_folder_path='Tools/'
        sh_mongojs_path='sh/mongo/'
        task_php_path=self.path+tool_folder_path+name+self.ext 
        task_js_path=self.path+sh_mongojs_path+name+".js"
        time= self.getTime()
        if os.path.exists(task_php_path):
            self._error('This task already exists ,you can change anothor name')
        else:
            task_php_body='''
            <?php
            /**
 * '''+name+'''.php
 * author: [yourname@leyue100]
 * date: ['''+time+''']
 */
include_once(__DIR__.'/../indexc.php');
echo 'begin!!!';echo /"\n\r/";

$category  = isset($argv[1]) ? $argv[1] : 3 ; //PEOPLE_CAT_DX:
$dateStart = isset($argv[2]) ? $argv[2] : 20160501 ; 
$dateEnd   = isset($argv[3]) ? $argv[3] : 20161101 ; 
$dateType  = isset($argv[4]) ? $argv[4] : 'all' ; 

$totalType      = 1;
$totalType2     = 2;
$collectionName = 'client_times_';

$ini_arr  = (new Yaf_Config_Ini(APPLICATION_PATH . "/conf/application.ini", $application->environ()))->toArray();

//print_r($dateStart);die;
if($dateStart == 'auto_h'){
$date = [
    date('YmdH',strtotime("-1 hours")),
    date('YmdH',strtotime("-2 hours")),
    date('Ymd'),
];
}else if($dateStart == 'auto_d'){
    for($i=0;$i<=7;$i++){
        $date[] = date("Ymd", strtotime(' -'. $i . 'day'));
    }
}else if($dateStart == 'auto_m'){
    $date = [
        date('Ym',strtotime("last month")),
        date('Ym',strtotime("-2 month"))
    ];
}else{
    $date = $Analysis_OnlineStatus->getDateRange($dateStart,$dateEnd,$dateType);
}

foreach($date as $dateVal) {
    if ($dateVal == date('Ymd', time())) {
        continue;
    }
    $varStr  = '';
    $varStr .= 'var dateVal='.$dateVal.';';
    
    $collection = $collectionName . $dateVal;
    $varStr    .= 'var collection=\'' . $collection . '\';';
    print_r($collection);
    //$mongoCLI = 'mongo --quiet 10.172.234.118:27017/rtls -eval '.$varStr.'" '.APPLICATION_PATH.' /sh/mongo/scan_user_total.js';

    //$result          = exec($mongoCLI);
    //$scan_user_total = json_decode($result);
}'''            
            task_js_body='''
// print(collection);
// print(category);
// print(totalType);
// print(dateType); 
// print(dateVal); 
// var table = db[collection];


var objCond = {};

if(dateType == 4){
    objCond._H = dateVal;
}else if(dateType == 3){
    objCond._D = dateVal;
}else if(dateType == 2){
    objCond._M = dateVal;
}else{

}

objCond.event = 1;
objCond.module_type = 1;
objCond.page = {'$in':['portal::home::login','portal::home::logined','portal::r::ishangwang']};

switch (category) {
    case 1 : 
        var key = 'extend.user_os';
        break;
    case 2 : 
        var key = 'extend.user_browser';
        break;
    default:
        var key = 'extend.user_os';
        break;
}

var distinct = db.runCommand({
    "distinct": collection,
    "key": key,
    "query": objCond
}).values;

// print(JSON.stringify(distinct));
var all = [];
for(x in distinct){


    switch (category) {
        case 1 :
            objCond['extend.user_os'] = distinct[x];
            break;
        case 2 : 
            objCond['extend.user_browser'] = distinct[x];
            break;
        default:
            objCond['extend.user_os'] = distinct[x];
            break;
    }


    var n = 0;
    var ret = [];

    var temp_name = 'temp_collections_os_' + dateVal + '_' + category;
    var drop = 'db.'+temp_name+'.drop()';
    eval(drop);


    db.runCommand({
        mapreduce : collection,
        map : function Map(){
            emit( {uid:this.uid,wid:this.extend.wid}, 1);
        },
        reduce : function Reduce(key, emits) {

        },
        finalize : function Finalize(key, value) {
            return key.wid;
        },
        query : objCond,
        out : temp_name,
    });

  
    db.runCommand(
        {"group": {
            "ns": temp_name,
            "key": {'value':true},
            "initial": {"count": 0},
            "$reduce": function(doc, prev) {
                prev.count++;
            }
        }}
    ).retval.forEach(function(data){
        ret[n] = [];
        ret[n].push(data.value);
        ret[n].push(data.count);
        ret[n].push(distinct[x]);
        n++;

    });
    all.push(ret);
    eval(drop);
}
print(JSON.stringify(all));'''
            self.createFile(task_php_path,task_php_body,"create task "+name+".php") 
            self.createFile(task_js_path,task_js_body,"create task javascript "+name+".js") 

    def createModel(self,name,params):
        model_path='application/models/'
        if(os.path.exists(self.path+model_path+name+self.ext)):
            self._error('This model already exists ,you can change anothor name')
        else:
            model_file_path=self.path+model_path+name+self.ext
            time=self.getTime()
            model_body='''
            <?php

/**
 * '''+name+'''.php
 * @author [yourname@leyue100.com]
 * @date: ['''+time+''']
 */

class '''+name+'''Model extends Object {

    public function __construct(){
        self::$setBase = 'default' ;
    }

    /**
     * @author [yourname@leyue100.com]
     * @description [类型demo 可以有(TYPE_STRING|TYPE_INT|TYPE_DATETIME|TYPE_HTML) 还可以指定必填和长度]
     */
    protected $def = [
        'table'       => 'table_name',
        'primary'     => '主键',
        'fields'      => [
            //设备属性
            'upId'            => ['type' => self::TYPE_STRING,'size' => 12,'required' => true],//主键ID
            'upUid'           => ['type' => self::TYPE_STRING,'size'=>60],//wifi认证过程中用户uid
            'upStatus'        => ['type' => self::TYPE_INT],//状态 1正常，6删除
            'upFrom'          => ['type' => self::TYPE_STRING,'size'=>30],//登陆来源
            'upCreateTime'    => ['type' => self::TYPE_DATETIME],//记录生成时间
            'upUpdateTime'    => ['type' => self::TYPE_DATETIME],//记录更新时间
            'upLoginTime'     => ['type' => self::TYPE_DATETIME],//登陆时间
            'upPlatform'      => ['type' => self::TYPE_STRING,'size'=>60],//操作系统
            'upBrowsers'      => ['type' => self::TYPE_HTML],//浏览器
        ],
        'status'      => 'upStatus',
        'skip_update' => ['upCreateTime']
    ];

    /**
     * @author [yourname@leyue100.com]
     * @description [生成id]
     * @return string|void
     */
    protected function idGen() {
        $id = $this->def['primary'];
        $this->$id = $this->id = Key::keyGen($this->idKeys());
        return $this->$id;
    }

    /**
     * @author [yourname@leyue100.com]
     * @description[可自定义生成主键的字段,这里只列举一个字段作为例子]
     * @return array
     */
    protected function idKeys() {
        $keys = [
            $this->upUid,
        ];

        return $keys;
    }

    /**
     * 新增时字段设置
     */
    protected function beforeAdd() {
        $id = $this->def['primary'];
        if (!isset($this->$id)) {
            $idv = $this->idGen();
            $this->setDatas([$this->def['primary'] => $idv]);
        }

        $this->upCreateTime = date('Y-m-d H:i:s');
        $this->status = self::INISERT_STATUS;
    }


    /**
     * 修改时字段设置
     */
    protected function beforeUpdate() {
        $this->upUpdateTime = date('Y-m-d H:i:s');
    }

    /**
     * 删除时字段设置
     */
    protected function beforeRemove() {
        $this->upUpdateTime = date('Y-m-d H:i:s');
        $this->status = self::DEL_STATUS;
    }
            '''
            self.createFile(model_file_path,model_body,"create model "+name+".php")
            self.createModelFunc(model_file_path,params)

    def createModelFunc(self,model_file_path,params):
        file_handle=open(model_file_path,'a')
        for i in xrange(0, len(params)):
            if i>=2:
                time= self.getTime()
                func_body='''
    /**
     * @author [yourname@leyue100.com]
     * @date ['''+time+''']
     */
    public function '''+params[i]+'''(){}'''
                file_handle.write(func_body)
                self.printSelf("create function "+params[i]+" in model",36)
        end_body='''
}
'''
        file_handle.write(end_body)
        file_handle.close()

    def updateAdminController(self,name,params):
        admin_controller_path='application/modules/Admin/controllers/'
        controller_file_path=self.path+admin_controller_path+name+self.ext
        if(os.path.exists(controller_file_path)):
            handle=open(controller_file_path)
            source_body=handle.readlines()[0:-1]
            handle.close()
            handle=open(controller_file_path,"wb")
            handle.writelines(source_body)
            handle.close() 

            for i in xrange(0, len(params)):
                if i>=2:
                    file_handle=open(controller_file_path,'a')
                    time= self.getTime()
                    func_body='''
    /**
     * @author [yourname@leyue100.com]
     * @date ['''+time+''']
     */
    public function '''+params[i]+'''Action(){}'''
                    file_handle.write(func_body)
                    self.printSelf("update function "+params[i]+" in admin controller",36)
            end_body='''
}
'''
            file_handle.write(end_body)
            file_handle.close() 
        else:
            self._error("This controller "+name+" has no exists and you must be choose anothor one")

    def createTest(self,name,params):
        test_path='tests/library/'
        test_file_path=self.path+test_path+name+self.ext
        if(os.path.exists(test_file_path)):
            self._error("This test "+name+" is exists you must be anothor one")
        else:
            test_body='''<?php
/**
 * '''+name+'''.php
 *
 * 作者: Bright (dannyzml@qq.com)
 * 创建日期: 16/5/26 下午3:53
 * 修改记录:
 *
 * $Id$
 */
ini_set('display_errors', 1);
error_reporting(E_ALL);
include_once(__DIR__ . '/../../indexc.php');

try{
    /*dosomething*/
}catch (Exception $e){
    var_dump($e->getMessage());
}
''' 
        self.createFile(test_file_path,test_body,"create test "+name+".php")                                                               

    def createFile(self,file_path,file_body,msg=''):
        if file_path!='':
            file_handle=open(file_path,'w') 
            file_handle.write(file_body)
            self.printInfo(msg)
            file_handle.close()                       

    def _error(self,msg):
        print self.printError(msg)
        self.getCommand() 

    def _help(self):    
        help_str='''
Do you want to this command ?
    add task:name [添加任务] \r
    add admin:name func1 func2 ......[添加后台admin 控制器和可选的自定义函数] \r
    add test:name [添加测试脚本]\r
    add model:name func1 func2 ......[添加model模块 和可选的自定义函数]\r
    update admin:name func1 func2 ......[追加admin控制器函数]
'''
        self.printSelf(help_str,31)

    def getTime(self):
        ISOTIMEFORMAT='%Y-%m-%d %X'
        return time.strftime( ISOTIMEFORMAT, time.localtime() )  

    def colored(self,text, color=None, on_color=None, attrs=None):
        fmt_str = '\x1B[;%dm%s\x1B[0m'
        if color is not None:
            text = fmt_str % (color, text)

        if on_color is not None:
            text = fmt_str % (on_color, text)

        if attrs is not None:
            for attr in attrs:
                text = fmt_str % (color, text)
        return text

    def printError(self,msg):
        print self.colored(msg, color=31)

    def printWarning(self,msg):
        print self.colored(msg, color=33)

    def printInfo(self,msg):
        print self.colored(msg, color=32)
    def printSelf(self,msg,color):
        print self.colored(msg,color)                                                     

if __name__=="__main__":
    scaffold=Scaffold()
    scaffold.showHeader() 
    scaffold.initParams()           
        
