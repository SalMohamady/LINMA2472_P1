from pathlib import Path
import re
import ftfy
import spacy
import networkx as nx
import community.community_louvain as community_louvain
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from clana.optimize import simulated_annealing
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np




allnames_withliers=['Pison', 'Hiddekel', 'Adam', 'Eve', 'Cain', 'Enoch', 'Irad', 'Methusael', 'Lamech', 'Zillah', 'Seth', 'Enos', 'Methuselah', 'Noah', 'Canaan', 'Shem', 'Cush', 'Mizraim', 'Heth', 'Gether', 'Salah', 'Eber', 'Peleg', 'Jerah', 'Uzal', 'Diklah', 'Obal', 'Terah', 'Abram', 'Haran', 'Lot', 'Sarai', 'Shinab', 'Zoar', 'Dan', 'Sarah', 'Benammi', 'Nahor', 'Buz', 'Kemuel', 'Chesed', 'Jidlaph', 'Rebekah', 'Laban', 'Zimran', 'Medan', 'Jokshan', 'Sheba', 'Epher', 'Abidah', 'Isaac', 'Ishmael', 'Rachel', 'Bilhah', 'Levi', 'Jacob', 'Asher', 'Reuben', 'Zebulun', 'Dinah', 'Joseph', 'Deborah', 'Benjamin', 'Naphtali', 'Korah', 'Omar', 'Zepho', 'Zerah', 'Jaalam', 'Lotan', 'Shobal', 'Dishan', 'Samlah', 'Baalhanan', 'Mehetabel', 'Hirah', 'Onan', 'Pharez', 'Jachin', 'Shaul', 'Arodi', 'Malchiel', 'Belah', 'Jordan', 'Ephron', 'Machir', 'Abraham', 'Aaron', 'Jethro', 'Zipporah', 'Shimi', 'Elzaphan', 'Eleazar', 'Miriam', 'Hur', 'Joshua', 'Eliezer']
allnames=['Pison', 'Hiddekel', 'Adam', 'Eve', 'Cain', 'Enoch', 'Irad', 'Lamech', 'Zillah', 'Seth', 'Enos', 'Methuselah', 'Noah', 'Canaan', 'Shem', 'Cush', 'Heth', 'Gether', 'Salah', 'Peleg', 'Jerah', 'Uzal', 'Diklah', 'Obal', 'Terah', 'Abram', 'Sarai', 'Shinab', 'Zoar', 'Dan', 'Sarah', 'Benammi', 'Nahor', 'Buz', 'Kemuel', 'Chesed', 'Jidlaph', 'Rebekah', 'Laban', 'Zimran', 'Medan', 'Sheba', 'Epher', 'Abidah', 'Isaac', 'Rachel', 'Bilhah', 'Levi', 'Asher', 'Reuben', 'Zebulun', 'Dinah', 'Joseph', 'Benjamin', 'Naphtali', 'Korah', 'Omar', 'Zepho', 'Zerah', 'Jaalam', 'Lotan', 'Shobal', 'Dishan', 'Samlah', 'Baalhanan', 'Mehetabel', 'Hirah', 'Onan', 'Pharez', 'Jachin', 'Shaul', 'Arodi', 'Malchiel', 'Belah', 'Jordan', 'Machir', 'Aaron', 'Jethro', 'Zipporah', 'Shimi', 'Elzaphan', 'Miriam', 'Hur', 'Joshua', 'Eliezer']
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

def create_diag_matrix():
    matrix_occ = np.zeros((lg_allnames,lg_allnames))
    for i in range(len(names)):
        list_index = get_index(names[i])

        lg_index = len(list_index)
        matrix_occ[i][i]=lg_index
    return matrix_occ

def create_matrix():

    matrix_occ = np.zeros((lg_allnames,lg_allnames))
    matrix_Diag = np.zeros((lg_allnames,lg_allnames))

    for i in range(len(names)):
        list_index = get_index(names[i])

        lg_index = len(list_index)

        for j in range(lg_index):
            for k in range(lg_index):
                if (j!=k):
                    matrix_occ[list_index[j]][list_index[k]]=1
                    matrix_Diag[list_index[j]][list_index[j]]+=1
                    matrix_Diag[list_index[k]][list_index[k]]+=1
    matrix_Diag=matrix_Diag/2
    return matrix_occ, matrix_Diag

def plot_matrix(acc,diag):
    #maximum = max (max(matrix))
    #coef = (255//maximum)
    #matrix = matrix * coef
    #plt.figure(figsize=(10,10))
    #plt.subplot(111)
    matrix = diag - acc+1

    for i in range (len(matrix)):
        for j in range (len(matrix)):
            if (i!=j):
                if (matrix[i][j]==0 ):
                    matrix[i][j] =1
                elif (matrix[i][j]==1 ):
                    matrix[i][j] =0

    matrix = np.log(matrix)
    plt.matshow(matrix)
    plt.colorbar()
    plt.show()


def create_graph(matrix_occ):
    G = nx.Graph()

    weight = []
    for i in range(lg_allnames):
        weight.append(matrix_occ[i][i])

    G.add_nodes_from([i for i in range(lg_allnames)], size = weight)

    for j in range(lg_allnames):
        for k in range (j,lg_allnames,1):
            if(j!=k):
                if(matrix_occ[j][k]!=0):
                    G.add_edge(j,k)

    g_draw = G
    print(nx.degree_assortativity_coefficient(G))
    pos = nx.spring_layout(g_draw)
    nx.draw(g_draw, pos, node_color='black', node_size=10, width=0.5)



def louvain(matrix):
    G = nx.Graph()
    G.add_nodes_from([i for i in range(lg_allnames)])

    for j in range(lg_allnames):
        for k in range (j,lg_allnames,1):
            if(j!=k):
                if(matrix[j][k]!=0):
                    G.add_edge(j,k)

    partition = community_louvain.best_partition(G)


    pos = nx.spring_layout(G)
    # color the nodes according to their partition
    cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
    nx.draw_networkx_nodes(G, pos, partition.keys(), node_size=10,cmap=cmap, node_color=list(partition.values()))
    nx.draw_networkx_edges(G, pos, alpha=0.5)
    plt.show()

def histo (matrix):

    maximum = int(matrix.max())
    '''print(int(maximum))
    list = np.zeros(int(maximum)+1)
    for i in range (len(matrix)):
        list[int(matrix[i][i])]+=1
        print(matrix[i][i])
    plt.hist(list)
    plt.show()'''

    diagoV = [matrix[i][i] for i in range (len (matrix))]
    plt.hist(diagoV,bins = list(range(0,int(maximum)+1)))


    plt.show()


def main():
    extract_names('bible12_n.txt')
    OCC , D = create_matrix()
    #plot_matrix(OCC, D)
    #create_graph(OCC+D)
    louvain(OCC)
    #histo(D)




main()
