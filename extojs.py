#!/usr/bin/python
# -*- coding:utf-8 -*-
import pandas as pd
import json
import datetime

def json_inputs(open_path):
    """
    返回json字符串列表
    :param path: 需要转换excel文件的路径
    :return: 返回json列表
    """
    df = pd.read_excel(open_path)
    # print(df)
    cols = [colName for colName in df.columns]
    json_list = []
    for row in df.itertuples():
        json_dict = {}
        for index in range(len(cols)):
            json_dict[cols[index]] = getattr(row,cols[index])
        json_list.append(json_dict)

    return json_list

def save_json(open_path,save_path):
    json_list = json_inputs(open_path)
    with open(save_path,"w",encoding="utf-8") as fw:
        #解决中文编码问题
        json.dump(json_list,fw,ensure_ascii=False)

ISOTIMEFORMAT = '%Y%m%d%H%M%S'
time= datetime.datetime.now().strftime(ISOTIMEFORMAT)
if __name__ == '__main__':
    open_path = r'D:\system\desktop\test\雀魂.xlsx'
    save_path = r'D:\system\desktop\test\data\source\雀魂{date}.json'.format(date=time)
    save_json(open_path,save_path)