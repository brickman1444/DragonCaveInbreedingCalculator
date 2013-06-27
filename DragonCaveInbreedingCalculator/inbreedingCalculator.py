'''
Created on Jun 23, 2013

@author: Zac
'''
from urllib.request import urlopen
from bs4 import BeautifulSoup
from binarytree import BinaryTree
from math import pow

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
    
def pathToRootChild(node):
    nodeList = [node.getRoot()]
    while (node.getParent() != BinaryTree.THE_EMPTY_TREE):
        nodeList.append(node.getParent().getRoot())
        node = node.getParent()
    return nodeList
    
def coefficientOfInbreeding(idCode):
        tree = BinaryTree(idCode)
        print("filling tree")
        tree = fillTree(tree)
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

#Dragon test codes
#Not inbred:
#TNiK
#SWUm
#Inbred:
#CLIF
#dresI 0.25
#Super Inbred:
#mcb0 0.25000572204589844
 
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
        print("Coefficient of Inbreeding: " + str(coefficientOfInbreeding(ID)))
    elif (x == '2'):
        ID1 = input("What is the first dragon's ID code?\n")
        ID2 = input("What is the second dragon's ID code?\n")
        print("Coefficient of Relationship: " + str(coefficientOfRelationship(ID1,ID2)))
    else:
        print("Unknown Command")
