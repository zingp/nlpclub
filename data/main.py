
from utils import read_excel, write_text
from utils import obj_to_json

# 保存原文
# 保存文本违规json
# 音频违规json
# 数据加载


def build_audio_dic(text_list):
    if len(text_list) != 5:
        return {}
    dic = {
        "idx": text_list[0],
        "date": text_list[1],
        "cate1": text_list[2],
        "cate2": text_list[3],
        "reason": text_list[4]
        }
    return dic


def pretreat_excel():
    excel = "~/Desktop/录播标注数据/2020年unsafe节目复核改-319.xlsx"
    data, cols = read_excel(excel)
    print(cols)
    print(data[:2])
    text_risk_list = []
    voice_risk_list = []
    for li in data:
        isText = li[3]
        dic = build_audio_dic(li)
        if isText.strip() == "文本违规":
            text_risk_list.append(dic)
        else:
            voice_risk_list.append(dic)
    
    text_risk_data = obj_to_json(text_risk_list)
    voice_risk_data = obj_to_json(voice_risk_list)
    write_text(text_risk_data, "text_risk_data.json")
    write_text(voice_risk_data, "voice_risk_data.json")
    print("Done!")


if __name__ == "__main__":
    pretreat_excel()
