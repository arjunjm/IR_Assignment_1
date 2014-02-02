import sys
import re
import pickle
import os
import time

invertedList = {}
docNameToIDMap = {}

def tokenize(file):
    tokenSet = set() 
    for line in file:
        line = line.lower()
        tokens = re.findall('\w+', line)
        for token in tokens:
            tokenSet.add(token)            
    return tokenSet

def buildIndex(tokenSet, docID):
    global invertedList
    for token in tokenSet:
        if token in invertedList:
            invertedList[token].add(docID)
        else:
            invertedList[token] = set([docID])

def buildDocIndex():
    
    global docNameToIDMap
    fileList = []

    for root, dirs, files in os.walk(os.getcwd()+"//nsf award abstracts"):
        for singleFile in files:
            if str(singleFile).endswith("txt"):
                fileList.append(singleFile)

    docID = 1                
    for singleFile in fileList:
        docNameToIDMap[singleFile] = docID
        docID = docID + 1
        
    pickle.dump(docNameToIDMap, open("DocumentList.p", "wb"))   
    
def dumpInvertedListToFile(invertedList):
    pickle.dump(invertedList, open("InvertedList.p", "wb" ))
    
def processUserQuery():
    print "Please wait while the index is being loaded...."
    invertedIndex = pickle.load(open("InvertedList.p", "rb"))
    docMap        = pickle.load(open("DocumentList.p", "rb"))
    userQuery = ""
    
    while True:
        print " "
        userQuery = raw_input("Please input your query : ")
        userQuery = userQuery.lower()
        
        if str(userQuery) == "exit":
            break
        
        queryTokenList  = userQuery.split()
        postingList = []
        setIntersection = set()
            
        for token in queryTokenList:
            if invertedIndex.get(token) != None:
                postingList.append(invertedIndex[token])

        if len(postingList) == 0:
            print "Sorry, No Matches found :("
            continue
                    
        setIntersection = set.intersection(*postingList)
        
        if len(setIntersection) == 0:
            print "Sorry, No Matches found :("
            continue
            
        print str(len(setIntersection)) + " occurrences found."
        
        invertedDocMap = {v:k for k,v in docMap.items()}
        matchedDocumentsList = []
        
        for docID in setIntersection:
            matchedDocumentsList.append(invertedDocMap[docID])
        
        print matchedDocumentsList
    
def main():
    processUserQuery()
    global docNameToIDMap
    global invertedList
    buildDocIndex()

    for root, dirs, files in os.walk(os.getcwd()+"//nsf award abstracts"):
        for singleFile in files:
            if str(singleFile).endswith("txt"):
                textFile = open(root+"//"+str(singleFile), 'r')
                tokenSet = tokenize(textFile)
                buildIndex(tokenSet, docNameToIDMap.get(str(singleFile)))
                textFile.close()
                             
    dumpInvertedListToFile(invertedList)
    
    processUserQuery()
    
if __name__ == '__main__':
    main()      
          