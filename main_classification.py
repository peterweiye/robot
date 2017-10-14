# -*- coding:utf-8 -*-
import aiml
import os
import jieba

from bean.work_order import work_order
from bean.xml_parser import xml_parser
from train_corpus import training_vec
import pandas as pd
import sys
reload(sys)
sys.setdefaultencoding('utf8')
# 寒暄语句模板
kernel = aiml.Kernel()
# 设备列表模板
device_kernel = aiml.Kernel()
# 典型故障模板
typical_problems_kernel = aiml.Kernel()
# yes or no模板
answer_kernel = aiml.Kernel()
# 设备节点xml路径
device_problem_xml_path = 'problem_xml/problem_node.xml'
seg_list = jieba.cut("加载中", cut_all=False)
train_model = ''
if os.path.isfile("bot_brain.brn"):
    # kernel.bootstrap(brainFile = "bot_brain.brn")
    # 加载aiml库
    kernel.bootstrap(learnFiles=os.path.abspath("aiml/std-startup.xml"), commands="load aiml b")
    device_kernel.bootstrap(learnFiles=os.path.abspath("aiml/std-device.xml"),
                            commands="load aiml b")
    typical_problems_kernel.bootstrap(learnFiles=os.path.abspath("aiml/std-typicalproblem.xml"),
                            commands="load aiml b")
    answer_kernel.bootstrap(learnFiles=os.path.abspath("aiml/std-answer.xml"),
                            commands="load aiml b")
    kernel.saveBrain("bot_brain.brn")
    # 加载word2vec，训练词向量
    train_model = training_vec(input='./data/wrod2vec_train_data.txt', output='./data/seg_train_data.txt',
                               model='./model/software.model', vec_model='./model/software_bin.model',
                               sentence_model='./data/train_data.txt')
    train_model.sentence2vec()
else:
    kernel.bootstrap(learnFiles=os.path.abspath("aiml/std-startup.xml"),
                     commands = "load aiml b")
    kernel.saveBrain("bot_brain.brn")
    device_kernel.bootstrap(learnFiles=os.path.abspath("aiml/std-device.xml"),
                            commands="load aiml b")
    typical_problems_kernel.bootstrap(learnFiles=os.path.abspath("aiml/std-typicalproblem.xml"),
                                      commands="load aiml b")
    answer_kernel.bootstrap(learnFiles=os.path.abspath("aiml/std-answer.xml"),
                            commands="load aiml b")

def get_device_name_by_raw_input():
    message = raw_input("请问是什么设备出现了故障呢？：")
    device_name = device_kernel.respond(word_segmentation(message))
    if device_name == 'null':
        print ('我不太明白你在说什么！')
        return 'null'
    else:
        return device_name

def word_segmentation(sentence):
    seg_list = jieba.cut(sentence, cut_all=False)
    result = " ".join(seg_list)
    return result

def match_typical_problems(message, device_name):
    cut_message = word_segmentation(message)
    # 检测原句子是否含有device name,若有就删除
    if device_name in cut_message:
        if device_name in cut_message:
            cut_message.replace(device_name, '')
    # 打标签
    tag_message = device_name + ' ' + message
    print (tag_message)
    # 匹配典型问题
    label = typical_problems_kernel.respond(tag_message)
    if label == 'null':
        return False, None
    else:
        return True, label

def user_interaction(device):
    parser = xml_parser()
    # 获取交互节点的内容
    nodes = parser.read_node(device=device, xml_path=device_problem_xml_path)
    # 加载交互结果矩阵
    deviceMat = pd.read_csv('interaction_result/'+device+'.csv')
    columns = deviceMat.columns
    lst_answer = []
    for node in nodes:
        message = raw_input(node+':')
        lst_answer.append(answer_kernel.respond(word_segmentation(message)))
    index = 0
    for ans in lst_answer:
        deviceMat = deviceMat[deviceMat[columns[index]].isin([ans])]
        index += 1
    print (deviceMat['label'])
    if (deviceMat['label'] == 'software').bool():
        return 'software'
    else:
        return 'hardware'




# kernel now ready for use
while True:
    message = raw_input("Enter your message to the bot: ")
    if message == "quit":
        exit()
    elif message == "save":
        kernel.saveBrain("bot_brain.brn")
    else:
        # 先匹配寒暄语句，不进行断句
        origin_message = message
        command_respose = kernel.respond(origin_message)
        # 没有匹配到寒暄语句
        if command_respose == 'not match':
            bot_response = kernel.respond("not match")
            # 找出故障设备实体
            device_name = device_kernel.respond(word_segmentation(message))
            # 无法识别出故障设备的名称
            if device_name == 'null':
                # 通过交互获取故障设备的名称
                device_name = get_device_name_by_raw_input()
                # 如果还是匹配不了故障设备，放弃交互
                if device_name == 'null':
                    continue
            lst = device_name.split(' ')
            device_name_en = lst[1]
            device_name_zh = lst[0]
            # 匹配典型故障
            bool_result, label = match_typical_problems(word_segmentation(message),
                                                        device_name_zh)
            print (u"匹配典型问题: ", bool_result, label)
            if bool_result:
                order = work_order(device=device_name_zh, description=' ',
                                   classification=label)
                order.show_work_order()
            else:
                # 如果无法匹配到典型问题，再次进行交互
                label = user_interaction(device=device_name_en)
                order = work_order(device=device_name_zh, description=' ',
                               classification=label)
                order.show_work_order()
        # 寒暄语句匹配成功
        else:
            bot_response = kernel.respond(message)
        if bot_response != 'not match':
            print (bot_response)