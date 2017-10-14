# -*- coding:utf-8 -*-
from xml.etree import ElementTree


class xml_parser():

    def read_node(self, device, xml_path):
        nodes = []
        root = ElementTree.parse(xml_path)
        lst_nodes = root.getiterator(device)
        for node in lst_nodes:
            for child in node.getchildren():
                nodes.append(child.text)
        return nodes
