# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 10:04:21 2019

@author: agos6
"""

class node():
    "Define tree by root, nodes, leaves, and links, which are splitting criteria"
    nodes_numbers = 0
    
    def __init__(self):
        self.value = None
        self.attribute= None
        self.data = None
        self.classe = None
        self.gain = None
        
        self.haschildren = 0
        
        self.left=None
        self.right = None

        self.level = None
        
def D(inputFile):
   f = open(inputFile,'r')
   D = []
   for lines in f : 
       D.append(lines.split())
   A = D[0]
   del A[-1]#la colonne classe n'est pas un attribut donc on le retire de la liste des attributs
   del D[0]
   
   A = [A]
   print(D)
   return D
     
   
def gen_error(dataTest, inputTree, alpha):
    numLeaves, error = leavesCount(inputTree, alpha)#(inputTree, [0], []) #counts the number of leaves of a tree
    dataTrain= inputTree.data
    N = len(dataTrain)
    generalisationError = (error + numLeaves*alpha)/N
    return generalisationError
   
def leavesCount(inputTree, alpha):#counts the number of leaves and the error in a tree
    count = 0
    error = 0
    for nodee in inputTree.children:
        if nodee.haschildren==0 : 
            count+=1
            classe = nodee.classe
            data = nodee.data
            error+=countOccurenceClass(data, 1-int(classe), len(data[0])-1)
    return count, error



def countOccurenceClass(listsplit, valueClass, classIndex):
    somme = 0
    for i in range(0,len(listsplit)):
        if (int(listsplit[i][classIndex]) == valueClass):
            somme = somme +1
    return somme   
    