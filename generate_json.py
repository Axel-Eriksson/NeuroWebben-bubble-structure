import random 
import json
import requests 
from bs4 import BeautifulSoup 


NAME = "name"
COLOR = "color"
LINK = "link"
CHILDREN = "children"
SIZE = "size"
HEADING_SIZE = 14
SUB_HEADING_SIZE = 10
SUB_SUB_HEADING_SIZE = 7
ALL_SUB_HEADINGS = {
    "Hjärnsmart lärande": "#e91d17",
    "Berikande miljöer": "#ea5b19",
    "Människa & teknik": "#ea5b19",
    "Social interaktion": "#e9ed1a",
    "Personlig utveckling": "#95d514", 
    "Kropp & livsstil": "#10d281",
    "Tankar": "#149dce",
    "Känslor": "#149dce",
    "Stress": "#615ae6",
    "Minne": "#615ae6",
    "Hjärnans kemi": "#b219f5"}

def auto_generate_children(name, color):
    children_list = []
    childs = int(random.uniform(2,5))
    for it in range(childs):
        children_list.append({NAME: name + str(it), SIZE: int(random.uniform(2,4)), COLOR: color})
    return children_list

def fill_tree_json(): 
    # the target we want to open     
    url='http://neurowebben.se'
      
    #open with GET method 
    resp=requests.get(url) 
    #http_respone 200 means OK status 

    if resp.status_code==200: 
        tree_json = {
            NAME: "neurowebben",
            COLOR: "#2f528f",
            SIZE: HEADING_SIZE,
            CHILDREN: []}
        # we need a parser,Python built-in HTML parser is enough . 
        soup=BeautifulSoup(resp.text,'html.parser')  
        # l is the list which contains all the text i.e news  
        l=soup.find("ul",{"class":"elementor-nav-menu"}) 
        #print(l)
        #now we want to print only the text part of the anchor. 
        #find all the elements of a, i.e anchor 
        node_name = None
        children = []
        color = None
        link = None
        def add_completed_node():
            tree_json[CHILDREN].append({NAME: node_name,
                    COLOR: color,
                    LINK: link,
                    SIZE: SUB_HEADING_SIZE,
                    CHILDREN: children if children else auto_generate_children(node_name, color)})

        def add_child(item):
            children.append({NAME: item.text,
                    COLOR: color,
                    LINK: item.get("href"),
                    SIZE: SUB_SUB_HEADING_SIZE,
                    CHILDREN: auto_generate_children(item.text, color)})

        for item in l.findAll("a"): 
            if item.text == "NeuroWebben": # start
                continue
            elif item.text == "Om NeuroWebben": # stop
                    add_completed_node()
                    break
            elif item.text in ALL_SUB_HEADINGS:
                if node_name:
                    add_completed_node()
                node_name = item.text
                children = []
                color = ALL_SUB_HEADINGS[item.text]
                link = item.get("href")    
            else:
                add_child(item)
        return tree_json
    else: 
        print("Error") 
        return
          
tree_json = fill_tree_json()

with open("data_file.json", "w") as write_file:
    json.dump(tree_json, write_file)
print(tree_json)
