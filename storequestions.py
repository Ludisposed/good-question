# -*- coding: utf-8 -*-
from xml.etree.ElementTree import iterparse
import xml.etree.ElementTree as ET
import os

def walkData(root_node, level, result_list):
    temp_list = str(level) + "--" + root_node.tag
    result_list.add(temp_list)

    children_node = root_node.getchildren()
    if len(children_node) == 0:
        return
    for child in children_node:
        walkData(child, level+1, result_list)

    return

def getXMLData(filename):
    level = 1
    result_list = set()
    root = ET.parse(filename).getroot()
    walkData(root, level, result_list)

    return sorted(list(result_list))

def parse(filename):
    name = os.path.basename(filename).split(".")[0]
    doc = iterparse(filename, events=('start','end'))
    next(doc)
    for event, elem in doc:
        if event == "end":
            with open(f"/tmp/{name}/{elem.tag}", "a+") as f:
                if elem.text:
                    f.write("text\n")
                    f.write(elem.text)
                if elem.attrib:
                    f.write("\nattrib\n")
                    for k in elem.attrib:
                        f.write(f"{k}: {elem.attrib[k]}\n")
                f.write("\n")
            
if __name__ == "__main__":
    for file in os.listdir('/codereview'):
        name = file.split(".")[0]
        if not os.path.exists(f"/tmp/{name}"):
            os.system(f"mkdir /tmp/{name}")
        filename=os.path.join('/codereview', file)       
        parse(filename)
