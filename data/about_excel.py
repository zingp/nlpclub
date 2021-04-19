
from utils import *



if __name__ == '__main__':
    txt = "/Users/liuyouyuan/Desktop/unsafe_text_main.txt"
    data = read_text(txt)
    new_data = [line.split("\t") for line in data]
    col = ["Live id", "Text", "违规类型"]
    write_excel(new_data, "/Users/liuyouyuan/Desktop/直播30s不安全标注20210419.xlsx", col)
        
