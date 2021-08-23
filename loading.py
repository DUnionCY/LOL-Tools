import win32api, win32con
import time
import urllib.request
import ssl
import urllib.error as error
import json
import psutil
from urllib import parse



def mainprint(i):
    print("\r",i,end="",flush=False)




def proc_exist(pid,process_name):
    try:
        if psutil.Process(pid).name() == process_name:
            return True
    except:
        return False



def readLolconfig():
    configfile = "\\LeagueClient\\lockfile"
    try:
        key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, 'SOFTWARE\\Tencent\\LOL', 0,win32con.KEY_ALL_ACCESS)
    except Exception as e:
        key = None

    if key is None:
        mainprint("无法获取配置文件路径")
        return False;
    else:
        getfilepath = win32api.RegQueryValueEx(key, "InstallPath")[0]
        configpath = getfilepath+configfile
    try:
        configread = open(configpath, 'r').read()
        config = configread.split(':')
    except:
        mainprint("无法读取配置文件路径，请检测是否有权限读取或请打开游戏客户端")

    return config



def csconfig(re):
    config["protocol"] = re[4]
    config["port"] = re[2]
    config["password"] = re[3]
    url["domain"]=config["protocol"]+"://"+config["host"]+":"+config["port"]
    print("\r url",url["domain"])
    print("\n 账号", config["username"])
    print("\n 密码", config["password"],"\n ")



def status(name):
    if name == "None":
        return "启动器界面中"
    elif name == "Lobby":
        return "游戏队伍中"
    elif name == "Matchmaking":
        return "匹配中"
    elif name == "ReadyCheck":
        return "找到对局"
    elif name == "ChampSelect":
        return "选择英雄中"
    elif name == "InProgress":
        return "游戏中"
    elif name == "WaitingForStats":
        return "等待结算"
    elif name == "PreEndOfGame":
        return "结算中"
    elif name == "EndOfGame":
        return "游戏结束"
    elif name == "Reconnect":
        return "游戏断开等待重新连接"
    elif name == "Error":
        return "异常"
    else:
        return "未知状态"




def getjson(file):
    with file as f:  # 打开url请求（如同打开本地文件一样）
        return json.loads(f.read().decode('utf-8'))


def reason(re):
    if re == "QUEUE_DODGER":
        return "由于玩家在英雄选择过程中退出了游戏，或者拒绝了过多场游戏，导致你无法加入队列。"
    else:
        return re



def Initializes():
    while True:
        mainprint("读取配置信息")
        time.sleep(1)
        re = readLolconfig()
        if not re:
            continue
        mainprint("读取配置信息成功")
        time.sleep(1)
        if not proc_exist(int(re[1]), re[0] + ".exe"):
            mainprint("无法获取到客户端，请启动游戏")
            time.sleep(5)
            continue
        mainprint("获取客户端成功")
        time.sleep(1)
        csconfig(re)
        break
    time.sleep(1)
    while True:
        if not proc_exist(int(re[1]), re[0] + ".exe"):
            mainprint("无法获取到客户端,可能客户端已被关闭")
            config["protocol"] = None
            config["port"] = None
            config["password"] = None
            url["domain"]=""
            return False


        ssl._create_default_https_context = ssl._create_unverified_context

        passman = urllib.request.HTTPPasswordMgrWithDefaultRealm()  # 创建域验证对象
        passman.add_password(None, url["domain"], config["username"],config["password"])  # 设置域地址，用户名及密码
        auth_handler = urllib.request.HTTPBasicAuthHandler(passman)  # 生成处理与远程主机的身份验证的处理程序
        opener = urllib.request.build_opener(auth_handler)  # 返回一个openerDirector实例
        urllib.request.install_opener(opener)  # 安装一个openerDirector实例作为默认的开启者。

        while True:
            try:
                searchfile = urllib.request.urlopen(url["domain"]+url["matchmakingsearch"])
                gameflowfile = urllib.request.urlopen(url["domain"] + url["gameflow"])
                gameflow = gameflowfile.read().decode().replace("\"", "")
                jsonData = getjson(searchfile)
                if jsonData["searchState"] == "Error":
                    if not jsonData["errors"]:
                        print("\r", '当前状态:', status(gameflow), '处罚状态：暂无处罚',
                              end="", flush=True)
                    else:
                        print("\r", '当前状态:', status(jsonData["searchState"]), '被惩罚的召唤师:',
                              jsonData["errors"][0]["penalizedSummonerId"], '惩罚剩余时间:',
                              jsonData["errors"][0]["penaltyTimeRemaining"], '惩罚原因:',
                              reason(jsonData["errors"][0]["message"]), end="", flush=True)
                else:
                    mainprint("当前状态:{0}".format(status(gameflow)))
            except error.URLError as err:
                mainprint('访问url错误:{0}'.format(err))
                return False
            if gameflow == "ReadyCheck":
                mainprint("当前状态:已自动接受对局")
                time.sleep(0.5)
                a = {}
                b = bytes(parse.urlencode(a), encoding="utf-8")
                try:
                    urllib.request.urlopen(url["domain"] + url["ready"], data=b)
                except error.URLError as err:
                    mainprint('访问url错误:{0}'.format(err))
            if gameflow == "ChampSelect":
                mainprint("当前状态:{0}".format(status(gameflow)))
                while True:
                    gameflowfile = urllib.request.urlopen(url["domain"] + url["gameflow"])
                    gameflow = gameflowfile.read().decode().replace("\"", "")
                    mainprint("当前状态:{0}".format(status(gameflow)))
                    if jsonData == "Lobby":
                        break
            time.sleep(0.5)



print("\nWELCOME TO USE LEAGUE OF LEGENDS TOOLS\n")
print("TOOLS [Version 1.0.1 ]\n")
print("BY ZAI02 POWERED BY CANYUE API PROVIDED BY LEAGUE OF LEGENDS LCU\n")
print("THIS PROGRAM COMPLIES WITH GPL-3.0 LICENSE\n")

mainprint("启动中")
time.sleep(1)
config ={
    "protocol":"",
    "port":"",
    "username":"riot",
    "password":"",
    "host":"127.0.0.1",
}
url={
    "domain":"",
    "matchmakingsearch":"/lol-lobby/v2/lobby/matchmaking/search-state",
    "ready":"/lol-matchmaking/v1/ready-check/accept",
    "startgame":"/lol-champ-select-legacy/v1/implementation-active",
    "gameflow":"/lol-gameflow/v1/gameflow-phase"
}
while True:
    mainprint("主程序初始化")
    Initializes()
    time.sleep(0.5)



