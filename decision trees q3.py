# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 16:31:59 2019

@author: agos6
"""

import numpy as np
inputFile = "C:/Users/agos6/Desktop/Aurore/SD/texte.txt"

class node():
    "Define tree by root, nodes, leaves, and links, which are splitting criteria"
    nodes_numbers = 0
    
    def __init__(self):
        self.value = None
        self.attribute= None
        self.data = None
        self.classe = None
        self.gain = None
        self.parent=[]
        
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
   


def getMaxLevel(T):
    return T.children[-1].level
   
def copyTree(rootTree):
    P = rootTree
    return P
    
 
 
def PostPrune(T,alpha, minNum, d):
    
    levelMaximum = getMaxLevel(T)
    
    for level in range(levelMaximum, 1, -1) :
        for node in T.children :
            if node is not None : 
                gen_T = gen_error(T.data, T, alpha)
                P = copyTree(T)
                if (node.level == level):
                    node.haschildren = 0
                    node.classe = determineClass(node, minNum, d)
                    new_P, listRemove, listIndex = deleteChildren(node, P)
                    gen_P = gen_error([],new_P,alpha)
                    if (gen_P<gen_T):
                        T = new_P
                    else : #we need to rebuild the tree as before to bring no changes
                        rebuildChildren(listRemove, listIndex, T)
    return T
                
def deleteChildren(node, tree): #delete the children of a node in the tree
    listToRemove=[]
    listIndex = []
    for nodee in tree.children :
        for parent in nodee.parent : 
            if (parent == node):
                listToRemove.append(nodee)
                listIndex.append(tree.children.index(nodee))
    for children in listToRemove : 
        tree.children.remove(children)
    return tree, listToRemove, listIndex

def rebuildChildren(listToRemove, listIndex, tree):
    for k in range(len(listToRemove)):
        tree.children.insert(listIndex[k], listToRemove[k])
    return tree


def determineClass(node, minNum,d):   
    D = node.data      
    if(len(D)!=0):
       
       numRecords = len(D)-1
       classIndex = len(D[0])-1
       
       #First case : all records have same class
       classe=D[0][classIndex]
       classIndex = len(D[0])-1
       somme = 0
       for i in range(0,len(D)):
           if (D[i][classIndex]==classe):
               somme+=1
               node.classe = D[0][classIndex]
       if (somme == numRecords): 
           return classe
           
       #Second case : number of records in D < minNum
       elif(numRecords < minNum):
          return d
       
       #Third case : classe determined by majority
       else : 
           classe = majorityClass(node)
           return classe
           
            
def majorityClass(node):
    dataSet = node.data

    classIndex = len(dataSet[0])-1
    num0 = countOccurenceClass(dataSet,0,classIndex)
    num1 = countOccurenceClass(dataSet, 1, classIndex)
    if (num0>=num1):
        return 0
    else : 
        return 1


def gen_error(dataTest, inputTree, alpha):
    numLeaves, error = leavesCount(inputTree, alpha) #counts the number of leaves of a tree
    dataTrain= inputTree.data
    N = len(dataTrain) #works out the number of records
    generalisationError = (error + numLeaves*alpha)/N
    return generalisationError
   
def leavesCount(inputTree, alpha):
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
