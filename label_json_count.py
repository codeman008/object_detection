# -*- coding:utf-8 -*-
#统计标注的目标框，一张图对应一个json

#time:2021/11/18


import os
import numpy as np
import pandas as pd
import json
import sys
import argparse


parser=argparse.ArgumentParser()
parser.add_argument('--input_path',type=str,help='json文件的路径',default='json/')
parser.add_argument('--csv',type=str,help='生成csv的名称',default='label_count_11-16.csv')
args=parser.parse_args()
path = args.input_path

list_label = []
for root,dirs,files in os.walk(path):
    for file in files:
        file_path = os.path.join(root,file)
        folder_name = os.path.basename(os.path.dirname(file_path))
        json_name = os.path.basename(file_path)
        if json_name.endswith(".json"):
            with open(file_path, 'rb') as load_f:
                load_dict = json.load(load_f)
                temp = load_dict['shapes']
                for i in range(len(temp)):
                    a = temp[i]['label']
                    list_label.append(a)
dict01 = {}
for item in list_label:
    dict01.update({item: list_label.count(item)})

def labelsum(labeldict):
    sum=0
    for j in labeldict:
        sum =sum+labeldict[j]
    return sum

# total_anno_group = pd.Series(list_label)
# label_count = total_anno_group.groupby(list_label).count()
# print(label_count)


writer=pd.DataFrame.from_dict(data=dict01,orient='index',columns=["number"])
writer=writer.reset_index().rename(columns={"index":"label_name"})
sumlabel=labelsum(dict01)
writer.loc[len(dict01),['label_name','number']] = ['目标框总数', sumlabel]
writer.to_csv(args.csv,index=False)


print("目标框总数：", sumlabel)
print('信息统计算完毕。')
