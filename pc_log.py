#
#筛选思路：ETC车道所有交易成功的OBU，从隔壁的混合车道查找所有的车牌识别的过车信息，是否在短时间内（1 min）有记录，有的话则一辆有嫌疑发生邻道干扰的车辆
#
import os
import tkinter as tk
import fnmatch
import threading
import time
import xlsxwriter
from datetime import datetime
from  excel_style import *  #引用其他Python文件

version ='V1.0.1'
gui_width  = 900
gui_height = 600

def str2ms(time_str):
    # 根据字符串获得时间戳，单位是ms
    timeArray = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S.%f")
    return int(time.mktime(timeArray.timetuple()) * 1000.0 + timeArray.microsecond / 1000.0)

class struct_car_info():
    def __init__(self):
        self.lane_name = '' #车道目录名称，由路径借去
        self.plate_num = '' #车牌号
        self.date_time = '' #日期时间

class parser_handle(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.records = dict();
        self.records['ETC'] = []
        self.records['MTC'] = []

    def run(self):
        self.create_gui()

    def create_gui(self):
        self.win = tk.Tk()
        self.win.title('新软日志分析工具%s' % version)
        self.win.geometry('%dx%d+100+100' % (gui_width, gui_height))
        self.win.resizable(False, False)

        #信息提示框
        self.print_obj = tk.StringVar()
        self.print_obj.set('开始分析日志嗲哇......')
        self.hint_info_label = tk.Label(
            self.win,
            textvariable=self.print_obj,
            #text = 'what???', ##这个变量无论先后位置，都是textvariable起作用
            bg = 'gray',
            fg = 'cyan',
            wraplength = gui_width - 4,
            font=('宋体', 13),
            justify = 'left',
            anchor = 'nw')
        self.hint_info_label.place(x=1, y=1, width=gui_width-2, height=gui_height-2)

        self.win.mainloop()

    def create_excel_file(self):
        date_tmp = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())
        self.excel_book = xlsxwriter.Workbook(os.path.join(os.getcwd(), '发生邻道交易嫌疑车辆_' + date_tmp + '.xlsx'))
        # exel标题正文的一些样式设置
        style_setting = excel_style()
        self.style_head = style_setting.get_highest_head_style(self.excel_book.add_format())
        self.style_title = style_setting.get_title_style(self.excel_book.add_format())
        self.style_light = style_setting.get_text_style_light(self.excel_book.add_format())
        self.style_dark = style_setting.get_text_style_dark(self.excel_book.add_format())
        self.style_pink = style_setting.get_text_style_pink(self.excel_book.add_format())
        self.style_left_dark = style_setting.get_text_style_left_dark(self.excel_book.add_format())

        self.result_sheet = self.excel_book.add_worksheet('result')
        self.result_sheet.set_row(0, 30)
        self.result_sheet.set_row(1, 20)


    def parse_all_files(self):
        self.get_records_from_file()
        self.log_print('提取信息成功，开始分析')
        self.create_excel_file()
        self.parse_records()
        self.log_print('分析完成')
        self.excel_book.close()

    def log_print(self, new_line):
        if new_line[-1] != '\n':
            new_line += '\n'

        text_tmp = self.print_obj.get()
        if text_tmp[-1] != '\n':
            text_tmp += '\n'
        text_tmp += new_line

        self.print_obj.set(text_tmp)

    def get_records_from_file(self):
        for root, dirs, files in os.walk(os.getcwd()):
            for filename in files:
                if fnmatch.fnmatch(filename, '*.txt*'):
                    self.get_need_info(root, filename)

    def get_need_info(self, root, file):
        #读取ETC，MTC的日志，提取需要的信息
        file_dir = os.path.join(root, file)
        f = open(file_dir, 'r', encoding='gb18030', errors='ignore')
        if f:
            self.log_print('Start getting info:' + file_dir )

            for line in f:
                #ETC交易的日志
                if fnmatch.fnmatch(line, '*ETC：车牌:*'):
                    carinfo = struct_car_info()
                    trade_time = line.split(' ')[3][0:11]
                    plate_num = line.split(':')[3][0:7]
                    carinfo.plate_num = plate_num
                    carinfo.date_time = '2020-11-' + file.split('.')[0] + ' ' + trade_time #手动加了个假的年月信息给他(车道日志没有这个信息)
                    carinfo.lane_name = root.split('\\')[-2]
                    self.records['ETC'].append(carinfo)

                #MTC过车的日志
                if fnmatch.fnmatch(line, '*原始车牌识别结果*'):
                    carinfo = struct_car_info()
                    trade_time = line.split(' ')[3][0:11]
                    plate_num = line.split(':')[3][0:7]
                    carinfo.plate_num = plate_num
                    carinfo.date_time = '2020-11-' + file.split('.')[0] + ' ' + trade_time
                    carinfo.lane_name = root.split('\\')[-2]
                    self.records['MTC'].append(carinfo)

            f.close()

    def parse_records(self):
        self.column_cnt = 0  #纵列
        write_account = dict()
        old_plate = ''  #已经记录过的车牌
        if self.records['ETC'] and self.records['MTC']:
            for record in self.records['ETC']:
                for reference in self.records['MTC']:
                    if (record.plate_num == reference.plate_num) \
                            and (record.lane_name != reference.lane_name)\
                            and (record.plate_num != old_plate):
                        time1 = str2ms(record.date_time)
                        time2 = str2ms(reference.date_time)
                        if abs(time1 - time2) < 60*1000:  #60秒内
                            old_plate = record.plate_num
                            if record.lane_name in write_account:
                                write_account[record.lane_name] += 1
                                row = write_account[record.lane_name]
                                self.result_sheet.write(row, self.column_cnt - 1, record.plate_num + ' ' + record.date_time, self.style_left_dark)
                            else:
                                self.result_sheet.set_column(self.column_cnt, self.column_cnt, 40) #设置一下列宽
                                self.result_sheet.write(0, self.column_cnt, record.lane_name, self.style_head)
                                write_account[record.lane_name] = 1
                                row = write_account[record.lane_name]
                                self.result_sheet.write(row, self.column_cnt, record.plate_num + ' ' + record.date_time, self.style_left_dark)
                                self.column_cnt += 1

if __name__ == '__main__':
    parser = parser_handle()
    parser.start()
    parser.parse_all_files()
    parser.join()