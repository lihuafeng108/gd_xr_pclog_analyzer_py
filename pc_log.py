import os
import tkinter as tk
import fnmatch

version ='V1.0.1'
gui_width  = 900
gui_height = 600

class parser_handle():
    def __init__(self):
        pass

    def create_gui_and_start_parsing(self):
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
            bg = 'black',
            fg = 'white',
            wraplength = gui_width - 4,
            justify = 'left',
            anchor = 'nw')
        self.hint_info_label.place(x=1, y=1, width=gui_width-2, height=gui_height-2)

        self.check_files()

        self.win.mainloop()

    def print(self, new_line):
        if new_line[-1] != '\n':
            new_line += '\n'

        text_tmp = self.print_obj.get()
        if text_tmp[-1] != '\n':
            text_tmp += '\n'
        text_tmp += new_line

        self.print_obj.set(text_tmp)

    def check_files(self):
        for root, dirs, files in os.walk(os.getcwd()):
            for filename in files:
                if fnmatch.fnmatch(os.path.join(root, filename), '*.txt*'):


    def parse_file(self, file):


class parse_log():
    def __init__(self):
        pass


if __name__ == '__main__':
    parser = parser_handle()
    parser.create_gui_and_start_parsing()