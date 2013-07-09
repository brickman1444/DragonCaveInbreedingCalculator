'''
V0.1 Created on Jun 23, 2013
V0.2 Created on Jul 6, 2013
V0.3 Created on Jul 7, 2013

@author: Zac Gross
'''
from urllib.request import urlopen
import urllib.error
from bs4 import BeautifulSoup
from binarytree import BinaryTree
from math import pow
import time

#returns (motherID,fatherID) for bred dragons
#returns ('','') for caveborn dragons
def getParents(childID):
    url = 'http://dragcave.net/view/' + childID
    page = urlopen(url).read()
    soup = BeautifulSoup(page)
    #prettySoup = soup.prettify()
    
    #this will screw up everything if the phrases 'Mother: ' and 'Father: ' appear in places outside the information box 
    motherSearch = soup.find(text='Mother: ')
    fatherSearch = soup.find(text='Father: ')
    
    #returns empty tuple if caveborn
    if motherSearch is None and fatherSearch is None:
        return ('','')
    
    motherLinkTag = motherSearch.string.next_sibling
    motherLink = motherLinkTag.get('href')
    motherID = motherLink[6:]# is 6 because the string starts with '/view/'
    
    fatherLinkTag = fatherSearch.string.next_sibling
    fatherLink = fatherLinkTag.get('href')
    fatherID = fatherLink[6:]# is 6 because the string starts with '/view/'
    
    return(motherID,fatherID)
    
#Fills the tree below node with its parents
#Mother goes in the left node
#Father goes in the right side
#Children are left as empty trees
def fillTree(node):
    childID = str(node)
    parentTuple = getParents(childID)
    
    if (parentTuple == ('','')):
        return node
    else:
        node.setLeft(fillTree(BinaryTree(parentTuple[0])))#Mother
        node.setRight(fillTree(BinaryTree(parentTuple[1])))#Father
        return node

deceasedDragonCounter = 0 
deceasedDragonPlaceholderString = '@@@@@'   
deceasedDragonPlaceholderStringLen = len(deceasedDragonPlaceholderString)

def nextDragonTuple():
    global deceasedDragonCounter
    retTuple = (deceasedDragonPlaceholderString + str(deceasedDragonCounter),1)
    deceasedDragonCounter += 1
    return retTuple

def idToLineageList(idCode):
    url = 'http://dragcave.net/lineage/' + idCode
    page = urlopen(url).read()
    soup = BeautifulSoup(page)
    #prettySoup = soup.table.prettify()
    lineageList = list()
    listOfTr = soup.table.find_all('tr')
    for trTag in listOfTr:
        rowList = list()
        for tdTag in trTag.find_all('td'):
            if tdTag.a is not None:
                dragonTuple = (tdTag.a.img['alt'],int(tdTag['rowspan']))
            else:
                dragonTuple = nextDragonTuple()
            rowList.append(dragonTuple)
        lineageList.append(rowList)
    
    return lineageList
        
def lineageListToTree(lineageList):
    count = 0;
    for row in lineageList:
        for cell in row:
            count += 1
    
    #escape case for recursion
    if(count == 1):
        return BinaryTree(lineageList[0][0])
      
    root = BinaryTree(lineageList[0][0])
    lineageList[0] = lineageList[0][1:]
      
    #root = BinaryTree(('z2qI',5))
    current = root
    stack = [BinaryTree(("Sentinel Node",-1)), root]
     
    for row in lineageList:
        for cell in row:
            previous = current
            current = BinaryTree(cell)
            if(previous.getRight() == BinaryTree.THE_EMPTY_TREE):
                #print(str(current.getRoot()) + str(previous.getRoot()))
                if(current.getRoot()[1] < previous.getRoot()[1]):
                    stack.append(previous)
                previous.setRight(current)
            else:
                previous.setLeft(current)
                
        #recursive way to continue beyond one lineage page
        if (current.getRoot()[0][:deceasedDragonPlaceholderStringLen] != deceasedDragonPlaceholderString):
            tempLineageList = idToLineageList(current.getRoot()[0])
            tempNode = lineageListToTree(tempLineageList)
        
            if (previous.getRight() == current):
                previous.setRight(tempNode)
            elif(previous.getLeft() == current):
                previous.setLeft(tempNode)
        
        current = stack.pop()
    return root

def cleanUpTupleTree(node):
    if (node.getRight() != BinaryTree.THE_EMPTY_TREE):
        cleanUpTupleTree(node.getRight())
    node.setRoot(node.getRoot()[0])
    if (node.getLeft() != BinaryTree.THE_EMPTY_TREE):
        cleanUpTupleTree(node.getLeft())
    
def pathToRootChild(node):
    nodeList = [node.getRoot()]
    while (node.getParent() != BinaryTree.THE_EMPTY_TREE):
        nodeList.append(node.getParent().getRoot())
        node = node.getParent()
    return nodeList
    
def coefficientOfInbreeding(idCode):
    if( not idExists(idCode)):
        return (idCode + " does not exist")
    
    tree = BinaryTree(idCode)
    print("filling tree")
    tree = fillTree(tree)
    return COI(tree)

def coefficientOfInbreedingLineage(idCode):
    if( not idExists(idCode)):
        return (idCode + " does not exist")
    
    print("writing lineage list")
    lineageList = idToLineageList(idCode)
    print("filling tree from list")
    tree = lineageListToTree(lineageList)
    cleanUpTupleTree(tree)
    return COI(tree)
       
def COI(tree):
    #getLeft() gets mother
    #getRight() gets father
    #getParent() gets local child
    
    if(tree == BinaryTree.THE_EMPTY_TREE):
        return 0
    
    print("calculating paths")
        
    listOfMotherPaths = []
    for node in iter(tree.getLeft()):
        listOfMotherPaths.append(pathToRootChild(node))
            
    listOfFatherPaths = []
    for node in iter(tree.getRight()):
        listOfFatherPaths.append(pathToRootChild(node))
    
    listOfPathTuples = []
    for mPath in listOfMotherPaths:
        for fPath in listOfFatherPaths:
            if (mPath[0] == fPath[0] and mPath[1] != fPath[1]):
                listOfPathTuples.append((mPath,fPath))
    
    print("summing up coefficient")
    
    coefficient = 0
    for pathTuple in listOfPathTuples:
        commonAncestorNode = tree.find(pathTuple[0][0])
        coefficient += pow(.5, len(pathTuple[0]) + len(pathTuple[1]) - 3) * (1 + COI(commonAncestorNode))
        
    return coefficient

def coefficientOfRelationship(id1,id2):
    
        if( not idExists(id1)):
            return (id1 + " does not exist")
       
        if( not idExists(id2)):
            return (id2 + " does not exist")
    
        if (id1 == id2):
            return .5
    
        tree1 = BinaryTree(id1)
        print("filling tree1")
        tree1 = fillTree(tree1)
        
        tree2 = BinaryTree(id2)
        print("filling tree2")
        tree2 = fillTree(tree2)
        
        hypotheticalChild = BinaryTree("Hypothetical Child")
        hypotheticalChild.setLeft(tree1)
        hypotheticalChild.setRight(tree2)
        return 2 * COI(hypotheticalChild)

#returns True if a dragon exists and False if a dragon doesn't
def idExists(idCode):
    try:
        url = 'http://dragcave.net/view/' + idCode
        page = urlopen(url).read()
        BeautifulSoup(page)
        return True
    except urllib.error.HTTPError:
        return False

#Dragon test codes
#Not inbred:
#TNiK 0
#SWUm 0
#Inbred:
#CLIF 0.15625
#dresI 0.25
#Super Inbred:
#mcb0 0.25000572204589844
#Deceased Ancestors:
#BNZ5 0
#uNF7 0

horizontalBar = "------------------------------------"
     
while (True):
    x = input("""What would you like to do?
    0: Exit
    1: Check Coefficient of Inbreeding of a dragon
    2: Check Coefficient of Relationship between two dragons
    """)
    if (x == '0'):
        break;
    elif (x == '1'):
        ID = input("What is the dragon's ID code?\n")
        print("Coefficient of Inbreeding: " + str(coefficientOfInbreedingLineage(ID)))
 
    elif (x == '2'):
        ID1 = input("What is the first dragon's ID code?\n")
        ID2 = input("What is the second dragon's ID code?\n")
        print("Coefficient of Relationship: " + str(coefficientOfRelationship(ID1,ID2)))
    else:
        print("Unknown Command")
    print(horizontalBar)