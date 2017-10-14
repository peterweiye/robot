# -*- coding:utf-8 -*-


class work_order():
    def __init__(self, device, description, classification):
        self.device = device
        self.description = description
        self.classification = classification

    def show_work_order(self):
        print ("device name:{0}".format(self.device))
        print ("order description:{0}".format(self.description))
        print ("order classification:{0}".format(self.classification))