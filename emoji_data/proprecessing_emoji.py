import os
import re
import emoji
import numpy as np


def clean_text_zh(text):
    """中文数据清洗"""
    # 去除空格
    text = re.sub(' ', '', text)
    # 去掉全角空白符，\u3000 是全角的空白符
    text = re.sub('\u3000', '', text)
    # 去掉 \xa0 是不间断空白符 &nbsp;
    text = re.sub('\xa0', '', text)
    return text


def filter_emoji(text, restr=''):  
    """过滤emoji"""
    # 编译匹配表情的正则
    prog = emoji.get_emoji_regexp()
    return prog.sub(restr, text) 


def load_emoji(emoji_file):
    """加载表情和对应的中文"""
    dic = {}
    with open(emoji_file, "r") as f:
        for line in f:
            if len(line.strip("\n").strip()) == 0:
                continue
            line = line.strip("\n")
            line_li = line.split()
            key = line_li[0]
            value = line_li[-1]
            dic[key] = value
    return dic


def emoji2zh(text, emoji_dic):
    """表情替换为中文"""
    prog = emoji.get_emoji_regexp()
    li = re.findall(prog, text)
    for emo in li:
        text = text.replace(text, emoji_dic.get(emo, "表情")) 
    return text
