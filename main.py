import sys

import demjson
import requests
import xlwt
from PyQt5.QtWidgets import QApplication, QMainWindow
import load_path
import uidesign
from functools import partial
import proxy
import shutil
import os
import re
import json

def open_info(ui):
    try:
        with open("user.json", "r", encoding='utf-8') as load_f:
            load_dict = json.load(load_f)
            print(load_dict)
            ui.label_3.setText(str(load_dict['path']))
            ui.lineEdit.setText(str(load_dict['number']))
    except:
        with open("user.json", "w", encoding='utf-8') as w_f:
            result = {"path": "", "number": ""}
            w_dict = w_f.write(json.dumps(result))

def remove_dir(root,title):
    list = os.listdir(root)
    #print(list)
    for item in list:
        if title in item:
            shutil.rmtree(root + '/'+item)
            print('找到重复游戏，进行更新！')

def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title

def convert(ui):
    path = load_path.get()
    ui.label_3.setText(str(path))
    with open("user.json", "w",encoding='utf-8') as w_f:
        result = {"path": str(path),"number": ""}
        w_dict = w_f.write(json.dumps(result))
    ui.textBrowser.append('当前存储地址:'+str(path))
    if ui.lineEdit.text() == '':
        ui.textBrowser.append('请输入游戏编号！')
    else:
        pass

def download(num,link,root,game_dir_name):
    pic = proxy.get_pic(link,ui.lineEdit_3.text())
    dir =root+'/'+game_dir_name+'/'+str(num) + '.' + str(link.split('.')[-1])
    fp = open(dir, 'wb')
    fp.write(pic.content)
    fp.close()

def write_excel(workbook,root,new_sheet,j,content):
    new_sheet.write(1, j, content)  # 在索引为i, j处写入content
    workbook.save(root)  # 保存

def make_sheet():
    workbook = xlwt.Workbook(encoding='utf-8')  # 创建 workbook 即新建 excel 文件/工作簿，
    new_sheet = workbook.add_sheet('游戏列表')  # 创建工作表，如果想创建多个工作表，直接在后面再 add_sheet
    # 添加表头

    workbook.save('游戏列表.xlsx')

def get_data(link,port):
    try:
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.41',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        if port=='':
            r = requests.get(link, headers=headers)
        else:
            proxies = {'http': 'http://localhost:'+port, 'https': 'http://localhost:'+port}
            r = requests.get(link, headers=headers,proxies=proxies)
        r.encoding = 'utf-8-sig'
        result = r.text
    except Exception as e:
        error_line = e.__traceback__.tb_lineno
        error_info = '第{error_line}行发生error为: {e}'.format(error_line=error_line, e=str(e))
        print(error_info)
        result = ''
    return result

def get_info(appid,root,ui):
    result = get_data('https://store.steampowered.com/api/appdetails?appids='+ str(appid) +'&cc=cn',ui.lineEdit_3.text())
    json_data_demjson = demjson.decode(result)
    print(result)
    json_data = json.dumps(json_data_demjson,ensure_ascii=False)
    main_data = json.loads(json_data)[str(appid)]['data']
    required_list1 = [
    'steam_appid',
    'name',
    'required_age',
    'developers',
    'publishers',
    'supported_languages',
    'detailed_description',
    'header_image',
    'release_date',
    'price_overview',
    'categories',
    'metacritic',
    'genres',
    'screenshots']

    try:
        os.mkdir(root)
    except:
        pass
        # print('已存在根目录')
    try:
        os.mkdir(root + '/' + validateTitle(main_data['name']))
    except:
        pass
        # print('已存在文章标题目录')
    sheet=root + '/' + validateTitle(main_data['name'])+'/'+validateTitle(main_data['name'])+'.xlsx'
    workbook = xlwt.Workbook(encoding='utf-8')
    new_sheet = workbook.add_sheet('游戏详情')
    new_sheet.write(0, 0, 'Steam ID')
    new_sheet.write(0, 1, '游戏名称')
    new_sheet.write(0, 2, '适龄提示')
    new_sheet.write(0, 3, '开发商')
    new_sheet.write(0, 4, '发行商')
    new_sheet.write(0, 5, '支持语言')
    new_sheet.write(0, 6, '游戏描述')
    new_sheet.write(0, 7, '游戏缩略图')
    new_sheet.write(0, 8, '发布情况')
    new_sheet.write(0, 9, '发布日期')
    new_sheet.write(0, 10, '原价')
    new_sheet.write(0, 11, '折扣价')
    new_sheet.write(0, 12, '折扣')
    new_sheet.write(0, 13, '标签')
    new_sheet.write(0, 14, '分类')
    new_sheet.write(0, 15, '评分')

    for index,item in enumerate(required_list1):
        if item == 'publishers' :
            write_excel(workbook, sheet,new_sheet, 3, main_data[item][0])
            print(main_data[item][0])
        elif item == 'screenshots':
            limit_num = ui.lineEdit_2.text()
            print('图上线'+limit_num)
            if limit_num =='':
                list = main_data[item]
            else:
                list = main_data[item][0:int(limit_num)]
            for i in list:
                print(i['id'])
                print(i['path_full'].split('?')[0])
                download(i['id'],i['path_full'].split('?')[0], root, validateTitle(main_data['name']))
        elif item == 'developers':
            write_excel(workbook, sheet,new_sheet, 4, main_data[item][0])
            print(main_data[item][0])
        elif item == 'metacritic':
            try:
                write_excel(workbook, sheet,new_sheet, 15, main_data[item]['score'])
                print(main_data[item]['score'])
            except:
                write_excel(workbook, sheet, new_sheet, 15, '暂无')
                print('暂无')
        elif item == 'release_date':
            if main_data[item]['coming_soon']:
                write_excel(workbook, sheet,new_sheet, 8, '未发行')
                print('未发行')
                write_excel(workbook, sheet,new_sheet, 9, main_data[item]['date'])
                print(main_data[item]['date'])
            else:
                write_excel(workbook, sheet,new_sheet, 8, '已发行')
                print('已发行')
                write_excel(workbook, sheet,new_sheet, 9, main_data[item]['date'])
                print(main_data[item]['date'])
        elif item == 'supported_languages':
            support_str = ''
            support_lang = ['中文','英语','日语','韩语']
            for i in support_lang:
                if i in main_data[item]:
                    if i != '韩语':
                        support_str += i+'、'
                    else:
                        support_str += i
            support_str += '等'
            write_excel(workbook, sheet,new_sheet, 5, support_str)
            print(support_str)
        elif item =='price_overview':
            if main_data[item]['discount_percent'] == 0:
                write_excel(workbook, sheet, new_sheet, 10, main_data[item]['final_formatted'])
                write_excel(workbook, sheet, new_sheet, 11, main_data[item]['final_formatted'])
                write_excel(workbook, sheet, new_sheet, 12, main_data[item]['discount_percent'])
            else:
                write_excel(workbook, sheet,new_sheet, 10, main_data[item]['initial_formatted'])
                write_excel(workbook, sheet,new_sheet, 11, main_data[item]['final_formatted'])
                write_excel(workbook, sheet,new_sheet, 12, main_data[item]['discount_percent'])
            print(main_data[item]['initial_formatted'])
            print(main_data[item]['final_formatted'])
            print(main_data[item]['discount_percent'])
            ui.textBrowser.append('原价：'+str(main_data[item]['initial_formatted']))
            ui.textBrowser.append('折扣价：'+str(main_data[item]['final_formatted']))
            ui.textBrowser.append('折扣：'+str(main_data[item]['discount_percent'])+'%')
        elif item =='categories' or item =='genres':
            desc_list=[]
            str_desc=','
            for i in main_data[item]:
                desc_list.append(i['description'])
            if item =='categories':
                write_excel(workbook, sheet,new_sheet, 14, str_desc.join(desc_list))
            else:
                write_excel(workbook, sheet,new_sheet, 13, str_desc.join(desc_list))
            print(str_desc.join(desc_list))
        else:
            if item == 'steam_appid':
                write_excel(workbook, sheet, new_sheet, 0, main_data[item])
                print(main_data[item])
            if item == 'name':
                write_excel(workbook, sheet, new_sheet, 1, main_data[item])
                print('游戏名'+main_data[item])
                ui.textBrowser.append(main_data[item])
            if item == 'required_age':
                write_excel(workbook, sheet, new_sheet, 2, main_data[item])
                print(main_data[item])
            if item == 'detailed_description':
                write_excel(workbook, sheet, new_sheet, 6, main_data[item])
                print(main_data[item])
            if item == 'header_image':
                write_excel(workbook, sheet, new_sheet, 7, main_data[item])
                print(main_data[item])

def download_click(ui):
    ui.textBrowser.append('_____________________抓取开始______________________')
    number = ui.lineEdit.text()
    root = ui.label_3.text()
    get_info(number,root,ui)
    ui.textBrowser.append('_____________________抓取结束______________________')

def open_path(ui):
    os.startfile(ui.label_3.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = uidesign.Ui_Form()
    ui.setupUi(MainWindow)
    MainWindow.show()
    open_info(ui)
    ui.pushButton.clicked.connect(partial(convert, ui))
    ui.pushButton_2.clicked.connect(partial(download,ui))
    ui.pushButton_3.clicked.connect(partial)
    sys.exit(app.exec_())