# -*- coding: utf-8 -*-
from xml.etree import ElementTree

import jieba

from bean.xml_parser import xml_parser
import pandas as pd

lst = []
lst.append(2)
print lst

seg_list = jieba.cut("没问题的", cut_all=False)
print " ".join(seg_list)

lst = ['asas', 'as', 'asasasas']
num_lst = [1,2,3,4]
print (lst)

seg_list = jieba.cut("打印机故障", cut_all=False)
seg_list = " ".join(seg_list)
if u'打印机' in seg_list:
    seg_list = seg_list.replace(u'打印机', '')
print seg_list

parser = xml_parser()
root = ElementTree.parse('problem_xml/problem_node.xml')
lst_nodes = root.getiterator('printer')
for node in lst_nodes:
    for child in node.getchildren():
        print child.tag, ":", child.text

nodes = parser.read_node(device='printer', xml_path='problem_xml/problem_node.xml')
print (nodes[0])

device = 'printer'
deviceMat = pd.read_csv('interaction_result/'+device+'.csv')

print (deviceMat.columns)
if (deviceMat[deviceMat[deviceMat.columns[0]].isin(['yes'])]['label'] == 'software').bool():
    print ("as")
print (deviceMat[deviceMat['node1'].isin(['yes'])]['label'] == 'software')


device_name = '打印机 printer'
lst = device_name.split(' ')
device_en = lst[1]
device_zh = lst[0]
print (device_en, device_zh)











