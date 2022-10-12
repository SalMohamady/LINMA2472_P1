from pathlib import Path
import re
import ftfy
import spacy
import networkx as nx
import matplotlib.pyplot as plt



allnames=['Pison', 'Hiddekel', 'Adam', 'Eve', 'Cain', 'Enoch', 'Irad', 'Mehujael', 'Methusael', 'Lamech', 'Zillah', 'Seth', 'Enos', 'Methuselah', 'Noah', 'Canaan', 'Shem', 'Cush', 'Mizraim', 'Heth', 'Gether', 'Salah', 'Eber', 'Peleg', 'Jerah', 'Uzal', 'Diklah', 'Obal', 'Terah', 'Abram', 'Haran', 'Lot', 'Sarai', 'Shinab', 'Zoar', 'Dan', 'Sarah', 'Benammi', 'Nahor', 'Buz', 'Kemuel', 'Chesed', 'Jidlaph', 'Rebekah', 'Laban', 'Zimran', 'Medan', 'Jokshan', 'Sheba', 'Epher', 'Abidah', 'Isaac', 'Ishmael', 'Rachel', 'Bilhah', 'Levi', 'Jacob', 'Asher', 'Reuben', 'Zebulun', 'Dinah', 'Joseph', 'Deborah', 'Benjamin', 'Naphtali', 'Korah', 'Omar', 'Zepho', 'Zerah', 'Jaalam', 'Lotan', 'Shobal', 'Dishan', 'Samlah', 'Baalhanan', 'Mehetabel', 'Hirah', 'Onan', 'Pharez', 'Jachin', 'Shaul', 'Arodi', 'Malchiel', 'Belah', 'Jordan', 'Ephron', 'Machir', 'Abraham', 'Aaron', 'Jethro', 'Zipporah', 'Shimi', 'Elzaphan', 'Eleazar', 'Miriam', 'Hur', 'Joshua', 'Eliezer']
lg_allnames = len(allnames)
names={}

def extract_names(path):
    NER = spacy.load("en_core_web_sm")
    doc = Path(path, encoding='cp1252').read_text(encoding='cp1252').split('\n\n')
                    
    for i in range(len(doc)):
        names[i]=[]
        doc[i]= re.sub(' +', ' ', ftfy.fix_text(doc[i]))
        doc[i]= re.sub('\n', ' ', doc[i])
        doc[i]= re.sub('\'', ' ', doc[i])

        #print(re.findall("(?<!^)(?<!\. )[A-Z][a-z]+", doc[i]))
        text1= NER(doc[i])
        for word in text1.ents:
            if(word.label_ == "PERSON"):
                if(word.text not in names[i]):
                    if(word.text in allnames):
                        names[i].append(word.text)

def get_index(list_name):
    if list_name == []:
        return []

    list_index=[]
    for i in list_name:
        for j in range(lg_allnames):
            if(i==allnames[j]):
                list_index.append(j)

    return list_index

def create_matrix():

    matrix_occ = [[0 for _ in range(lg_allnames)] for _ in range(lg_allnames)]

    for i in range(len(names)):
        list_index = get_index(names[i])

        lg_index = len(list_index)

        for j in range(lg_index):
            for k in range(lg_index):
                matrix_occ[list_index[j]][list_index[k]]+=1

    return matrix_occ

def create_graph(matrix_occ):
    G = nx.Graph()
    G.add_nodes_from([i for i in range(lg_allnames)], size = [matrix_occ[i][i] for i in range(lg_allnames)])

    for j in range(lg_allnames):
        for k in range (j,lg_allnames,1):
            if(j!=k):
                if(matrix_occ[j][k]!=0):
                    G.add_edge(j,k,weight=matrix_occ[j][k])

    g_draw = G
    pos = nx.spring_layout(g_draw)
    nx.draw(g_draw, pos, node_color='black', node_size=10, width=0.5)
    plt.show()


def main():
    extract_names('bible12_n.txt')
    matrix = create_matrix()
    create_graph(matrix)



main()