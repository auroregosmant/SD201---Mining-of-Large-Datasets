## -*- coding: utf-8 -*-
#
## -*- coding: utf-8 -*-
import numpy as np
inputFile = "C:/Users/agos6/Desktop/Aurore/SD/texte.txt"
minNum = 1


class node():
    "Define tree by root, nodes, leaves, and links, which are splitting criteria"
    nodes_numbers = 0
    
    def __init__(self): #tree defined by its root
        self.value = None
        self.attribute= None
        self.data = None
        self.classe = None
        self.parent = []
        
        self.haschildren = 0
        self.children = []
        
        self.left=None
        self.right = None

        self.level = None

    
def D(inputFile): #reads the inputFile and builds the dataSet
   f = open(inputFile,'r')
   D = []
   for lines in f : 
       D.append(lines.split())
   A = D[0]
   del A[-1]#la colonne classe n'est pas un attribut donc on le retire de la liste des attributs
   del D[0]
   
   A = [A]
   print(D)
      
   BuildDecisionTree(D,A,minNum = 5, defaultValue = 0)
    
    
def BuildDecisionTree(D, A, minNum, defaultValue) :
    
   root = node()
   root.level = 1
   Build(D,A,minNum, root, defaultValue)
   rootNode = [root]
   
   tree = addChildrenToRoot(rootNode, root) #the root contains all the nodes of the tree
   
   printTree(tree)
   #print("GEN_ERROR",gen_error(tree.data, tree, alpha = 0.5))
   
   #tree = PostPrune(tree, alpha = 0.5, minNum = 5, d = 0)
   #print("this is the pruned tree")
   #printTree(tree)
   #print("GEN_ERROR",gen_error(tree.data, tree, alpha = 0.5))

def printTree(tree):
    for children in tree.children:
        if (children is not None):
                if (children.level==1):
                    print("Root")
                elif (children.haschildren==0):
                    print("Leaf")
                else:
                    print("Intermediate")
                    
                print("Level",children.level)
                if(children.value is not None):
                    print("Features" , children.attribute, children.value)
                print("Gain" , Gain(children.data))
                print("Classe", children.classe)
                #print("data", children.data)
        
    
def addChildrenToRoot(rootNode, root): #add all the nodes of the tree to the root
    liste = []
    if len(rootNode) == 0:
        return 
    else : 
        for nodee in rootNode : 
            if (nodee is not None):
                
                root.children.append(nodee)
            
                liste.append(nodee.left)
                liste.append(nodee.right)
    
        addChildrenToRoot(liste, root)
    return root
        
def Build(D,A, minNum, node0, defaultValue):  
    
   node0.data = D

   level = node0.level
   
   if(len(D)!=0):
       
       attribute, attributeIndex, value, gain = perfGain(D,A,level)
       
       numRecords = len(D)-1
       classIndex = len(D[0])-1
       
       #First case : all records have same class
       classe=D[0][classIndex]
       classIndex = len(D[0])-1
       somme = 0
       for i in range(0,len(D)):
           if (D[i][classIndex]==classe):
               somme+=1
               node0.classe = D[0][classIndex]
               
               
       if (somme == numRecords): 
           node0.classe = classe
           return

           
       #Second case : number of records in D < minNum
       elif(numRecords < minNum):
          node0.classe= defaultValue
          return
       
       #Third case : Set of attributes is a empty set
       elif (A[level-1]==[-1 for k in range(len(A))]) : 
           node0.classe = majorityClass(node0)
           return 
       
       #Fourth case : 
       
       else :
           
           attribute, attributeIndex, value, gain = perfGain(D,A,level)
           
           if attribute !=-1:
               
               leftRight = getLeftRight(D,attributeIndex,value)#list0 list of left hand-side
               
               
               node0.attribute = attribute
               node0.classe = majorityClass(node0)

               
               
               if value is not None : 
                   node0.value = {k for k in range(0,int(value)+1)}
                   
               
               if attributeIndex is not None :
                   B = [k for k in A[level-1]]
                   B[attributeIndex]=-1
                   A.append(B)

                   
               for k in range(0,2):
                    if len(leftRight[k])>0:
                        node_k = node() 
                        for parent in node0.parent : #updates the list of parents
                            node_k.parent.append(parent)
                        node_k.parent.append(node0)
                        node_k.data = leftRight[k]
                        node_k.level = level+1
                        if (k==0):
                            node0.left = node_k
                            node0.haschildren = 1
                        elif (k==1):
                            node0.right = node_k
                            node0.haschildren=1
                        Build(leftRight[k], A, minNum, node_k, defaultValue)
                        
def majorityClass(node): #find the class that is in majority in the data of a node
    dataSet = node.data

    classIndex = len(dataSet[0])-1
    num0 = countOccurenceClass(dataSet,0,classIndex)
    num1 = countOccurenceClass(dataSet, 1, classIndex)
    if (num0>=num1):
        return 0
    else : 
        return 1
                    
def countOccurenceClass(listsplit, valueClass, classIndex): #count the occurence of a class in a split
    somme = 0
    for i in range(0,len(listsplit)):
        if (int(listsplit[i][classIndex]) == valueClass):
            somme = somme +1
    return somme    

def Gain(nodeData): #calculates the gain of a node given its data
    entropy = 0
    listProb = prob(nodeData)
    for proba in listProb : 
        if(proba!=0):
            entropy = entropy - proba*np.log(proba)
    return entropy


def GainSplit(listSplit,attributeIndex,D): #calcul le Gain d'un split
    entropy=[]
    
    numSplit = 0
    for split in listSplit:
        numSplit+= len(split)
        
        entropy.append(Gain(split))


    entropyParent = Gain(D)

        
    entropTOT = 0
    for k in range(0,len(listSplit)) : 
        n = len(listSplit[k])
        entropTOT += (n/numSplit)*entropy[k]

    

    gain = entropyParent - entropTOT

    
    return gain

    
def prob(split):
    n = len(split)
    listProb = []
    if (n==0):
        listProb.append(0)
    else : 
        for value in range(0,2):
            som =countOccurence(split,value)
            listProb.append(som/n)#arrondir la probabilité au millième
    return listProb

        
    
def countOccurence(listsplit, value):
    somme = 0
    classIndex = len(listsplit[0])-1
    for i in range(0,len(listsplit)):
        if (int(listsplit[i][classIndex]) == value):
            somme = somme +1
    return somme

def getLeftRight(D, attribute, VAL): #works out the data of the left and right children
    left =[] 
    right=[]
    if (attribute is None):
        return left,right
    else :
        for record in D:
            if (record[attribute] <= VAL): 
                left.append(record)
            else : 
                right.append(record)
    return left,right
    
        

def perfGain(D, A, level): #trouve le plus petit gain en parcourant tous les splits possibles
    gain, value, attrib, attribIndex = 0, None, None, None
    attributeIndex = []
    for attribute in range(0,len(A[level-1])):
        if(A[level-1][attribute]!=-1):
            attributeIndex.append(attribute)
            
            
    for attribute in attributeIndex : 
        values = []
        for k in range(0,len(D)):
            if D[k][attribute] not in values : 
                values.append(D[k][attribute])
    
        for VAL in values :
            left,right = getLeftRight(D,attribute, VAL)
            
            #print("left: {}".format(left))
            #print("right: {}".format(right))
            
            gainTMP = GainSplit([left,right],attribute,D)
            if( gain< gainTMP):
                gain = gainTMP
                value = VAL;
                attrib = A[level-1][attribute]
                attribIndex = attribute

    return(attrib,attribIndex, value, gain)
    

    




    
    

    
    
        
 