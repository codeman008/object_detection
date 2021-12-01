# -*- coding:utf-8 -*-
#统计标注的目标框，一张图对应一个xml


import os
import xml.etree.ElementTree as ET
import numpy as np
from openpyxl import workbook
import pandas as pd
import csv
import sys
import argparse

def parse_obj(xml_path, filename):
    tree = ET.parse(xml_path + filename)
    objects = []
    for obj in tree.findall('object'):
        obj_struct = {}
        obj_struct['name'] = obj.find('name').text
        objects.append(obj_struct)
    return objects

def labelsum(labeldict):
    sum=0
    for j in labeldict:
        sum =sum+labeldict[j]
    return sum

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_path', type=str, help='xml文件的路径',
                        default='xml/')
    parser.add_argument('--csv', type=str, help='生成csv的名称', default='label_count_xml.csv')
    args = parser.parse_args()
    xml_path = args.input_path
    filenamess = os.listdir(xml_path)
    # print(filenamess)
    filenames = []
    for name in filenamess:
        name = name.replace('.xml', '')
        filenames.append(name)
    recs = {}
    obs_shape = {}
    classnames = []
    num_objs = {}
    obj_avg = {}
    for i, name in enumerate(filenames):
        recs[name] = parse_obj(xml_path, name + '.xml')

    for name in filenames:
        for object in recs[name]:
            if object['name'] not in num_objs.keys():
                num_objs[object['name']] = 1
            else:
                num_objs[object['name']] += 1
            if object['name'] not in classnames:
                classnames.append(object['name'])
    writer=pd.DataFrame.from_dict(data=num_objs,orient='index',columns=["number"])
    writer=writer.reset_index().rename(columns={"index":"label_name"})
    writer.to_csv(args.csv,index=False)
    for name in classnames:
        print('{}:{}个'.format(name, num_objs[name]))
    print("目标框总数：", labelsum(num_objs))
    print('信息统计算完毕。')



