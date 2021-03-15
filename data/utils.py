import time
import json
import datetime
import xlrd
import xlsxwriter
"""
本模块定义通用数据处理相关的功能函数
"""


def read_text(file_path):
    """ 读文本文件返回内容列表，列表元素是原文的一行
    Args:
        file_path (str) 原文本文件
    Returns:
        data (list) 列表元素是文本行
    """
    with open(file_path, "r") as f:
        data = f.read().splitlines()
    return data


def write_text(str_list, out_file):
    """字符串列表按行写入文件
    Args:
        str_list (list(str)) 待写文本内容
        out_file (str)  输出文件
    """
    with open(out_file, "w") as f:
        for line in str_list:
            f.write(line + "\n")


def read_excel(file_path, sheet="Sheet1"):
    """读取excel
    Args:
        file_path (str) 待读文件，通常.xlsx结尾
        sheet     (str) excel sheet, 默认Sheet1
    Returns:
        data_li   (list（tuple）) Excel 每行内容
        sheet.row_values(0) list 列名
    """
    data_li= []
    workbook = xlrd.open_workbook(file_path)
    sheet = workbook.sheet_by_name(sheet)
    for i in range(1, sheet.nrows):
        row = sheet.row_values(i)
        data_li.append(row)
    return data_li, sheet.row_values(0)


def write_excel(data_list, file_path, column_names):
    workbook = xlsxwriter.Workbook(file_path)
    sheet1 = workbook.add_worksheet()
    #column_names = ["中心词", "节目id", "节目名称","节目摘要"]
    for i in range(len(column_names)):
        sheet1.write(0, i, column_names[i])
        # 将数据写入
    for i, row_li in enumerate(data_list):
        sheet1_row = i+1
        for j in range(len(row_li)):
            sheet1.write(sheet1_row, j, row_li[j])
    workbook.close()


def time2stamp(time_str):
    """字符串转时间戳"""
    d = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    t = d.timetuple()
    return int(time.mktime(t)) 


def reverse_json(str_list):
    """ 反序列化
    Args：
        str_list  list(str)
    Returns:
        data    list(obj)
        error   list(tuple)
    """
    data = []
    error = []
    for line in str_list:
        try:
            dic = json.loads(line)
            data.append(dic)
        except Exception as e:
            error.append([line, str(e)])
    return data, error
