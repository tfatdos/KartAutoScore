import os
import configparser
import win32con
import win32clipboard as wincld

global player_name
global player_total
global player_point
global player_number


#获取本局信息
def get_message(file,line):
    return '\n'.join(open(file,'r', encoding='UTF-16').readlines()[line:])


#获取当局地图
def get_map(message):
    #查找地图名前 
    index_f = message.find(' ')
    map_f = message[1:index_f]
    #查找地图名后
    index_l = message.find(' ',index_f+1,-1)
    map_l = message[index_f+1:index_l]
    #print(map_l)
    print(map_f)
    return map_f + map_l


# 获取分数
def get_score(message):
    no_complete = message.count('         未完成	')
    for i in range(player_number):
        if message.find(player_name[i]) == -1:
            print("can't find ID :"+player_name[i])
            return -1
        rank = int(message[message.find(player_name[i])-3])
        if rank <= player_number - no_complete:
            player_total[i] = player_total[i] + player_point[rank]
            print(player_name[i]+"，本局名次："+str(rank) +",得分："+ str(player_point[rank]) + ",总分：" + str(player_total[i]))
        else: 
            player_total[i] = player_total[i] + player_point[9]
            print(player_name[i]+"，本局名次：未完成,得分："+str(player_point[9])+ ",总分："+str(player_total[i]))

#将比分复制到粘贴板
def set_text(info):
    wincld.OpenClipboard()
    wincld.EmptyClipboard()
    wincld.SetClipboardData(win32con.CF_UNICODETEXT, info)
    wincld.CloseClipboard()

def get_id(file):
    message_tmp = open(file,'r', encoding='UTF-16').readlines()
    index = len(message_tmp) - 1
    # 过滤空行
    while (index > 0) :
        if message_tmp[index].strip() == "" :
            index -= 1
        else :
            break
    # 最后一行肯定是 ----
    player_name = []
    index -= 1
    while (index > 0 ) :
        line = message_tmp[index].split(" \t")
        player_name.append(line[1].strip())
        # 读到第一名结束
        if (line[0] == '1') :
            break
        index -= 2
    return player_name[::-1]

if __name__ == '__main__':
    #info
    print("*-----------------------------------------*")
    print("|      written by : tfatdos丶             |")
    print("|本软件不得用于商业用途,仅做学习交流使用。   |")
    print("*-----------------------------------------*")
    #config
    print("获取配置文件...")
    config=configparser.ConfigParser()
    config.read("config.ini", encoding='UTF-16')
    game_name = config.get("game","name")
    print("本次比赛名称为："+game_name)

    file_path = config.get("file","path")
    print("文件路径为："+ file_path)
    file_name = config.get("file","name")
    print("文件名为:"+file_name)
    
    #每局得分录入
    player_point = [10,7,5,4,3,2,1,0,-1,-5]
    player_point[1] = config.get("game","1stscore")
    print("本次比赛第1名得分为："+player_point[1])
    player_point[2] = config.get("game","2ndscore")
    print("本次比赛第2名得分为："+player_point[2])
    player_point[3] = config.get("game","3rdscore")
    print("本次比赛第3名得分为："+player_point[3])
    player_point[4] = config.get("game","4thscore")
    print("本次比赛第4名得分为："+player_point[4])
    player_point[5] = config.get("game","5thscore")
    print("本次比赛第5名得分为："+player_point[5])
    player_point[6] = config.get("game","6thscore")
    print("本次比赛第6名得分为："+player_point[6])
    player_point[7] = config.get("game","7thscore")
    print("本次比赛第7名得分为："+player_point[7])
    player_point[8] = config.get("game","8thscore")
    print("本次比赛第8名得分为："+player_point[8])
    player_point[9] = config.get("game","incompletescore")
    print("本次比赛未完成得分为："+player_point[9])
    for i in range(len(player_point)):
        player_point[i] = int(player_point[i])

    while True:
        #选择输入ID还是导入ID
        print("请选择ID导入方式：")
        print("1.config.ini录入（必须与游戏ID完全一致）")
        print("2.通过OB账号完成一局测试局")
        switch = input()
        if switch == '1':
            player_number = int(config.get("player","count"))
            player_name = ['','','','','','','','']

            player_name[0] = config.get("player","name1")
            player_name[1] = config.get("player","name2")
            player_name[2] = config.get("player","name3")
            player_name[3] = config.get("player","name4")
            player_name[4] = config.get("player","name5")
            player_name[5] = config.get("player","name6")
            player_name[6] = config.get("player","name7")
            player_name[7] = config.get("player","name8")
            break
        elif switch == '2':
            print("由于选择通过测试局录入ID，请在测试局结束后按“任意键”并“回车”继续")
            input()
            player_name = get_id(file_path+file_name)
            player_number = len(player_name)
            print("由于ID录入方式为测试局ID，现已将参赛ID复制到剪切板")
            set_text('  '.join(player_name))
            break
        else:
            print("输入错误，请重新输入！！！")
    print("本次参赛选手ID为：")
    for i in range(player_number):
        print(player_name[i])


    player_total = [0,0,0,0,0,0,0,0]
    line = -1*(5+2*player_number)

    while True:
        print("等待本局比赛结束返回游戏界面后，按“任意键”并“回车”开始统计本局分数，若输入“-1”则程序退出")
        if input() == '-1' :
            break
        message = get_message(file_path+file_name,line)
        print(message)
        map = get_map(message)
        print("本张地图："+map)
        score = get_score(message)
        if score == -1:
            print("ID查找错误 程序退出")
            exit()
        text = ""
        for i in range(player_number):
            text = text + str(player_total[i]) + "    "
        #将结果复制到粘贴板
        set_text(text)
        print("得分复制到粘贴板成功")


