import sys
import re
import os

invertedList = {}
docNameToIDMap = {}

# This function returns a set containing individual tokens in the
# file passed to the function.

def tokenize(file):
    tokenSet = set() 
    for line in file:
        line = line.lower()
        tokens = re.findall('\w+', line)
        for token in tokens:
            tokenSet.add(token)            
    return tokenSet

# This function gets called continuously for each document and builds
# the inverted list (dict) containing the token to the documentID set

def buildIndex(tokenSet, docID):
    global invertedList
    for token in tokenSet:
        if token in invertedList:
            invertedList[token].add(docID)
        else:
            invertedList[token] = set([docID])

# This function gets called at the beginning and builds a map from
# document name to document ID.

def buildDocIndex():
    
    global docNameToIDMap
    fileList = []

    if len(sys.argv) > 1:
        datasetDirectory = sys.argv[1]
    else:
        datasetDirectory = "nsf award abstracts"

    for root, dirs, files in os.walk(os.getcwd()+"//"+datasetDirectory):
        for singleFile in files:
            if str(singleFile).endswith("txt"):
                fileList.append(singleFile)

    docID = 1                
    for singleFile in fileList:
        docNameToIDMap[singleFile] = docID
        docID = docID + 1
        
# This function processes the user query.

def processUserQuery():
    global invertedList
    global docNameToIDMap
    userQuery = ""
    
    while True:
        print " "
        userQuery = raw_input("Input your query : ")
        userQuery = userQuery.lower()
        
        if str(userQuery) == "exit":
            print "Exiting program...Have a nice day!"
            break
        
        queryTokenList  = re.findall('\w+', userQuery)
        postingList = []
        setIntersection = set()
            
        for token in queryTokenList:
            if invertedList.get(token) != None:
                postingList.append(invertedList[token])

        if len(postingList) == 0:
            print "Sorry, No Matches found :("
            continue
                    
        setIntersection = set.intersection(*postingList)
        
        if len(setIntersection) == 0:
            print "Sorry, No Matches found :("
            continue
            
        print str(len(setIntersection)) + " occurrences found."
        
        invertedDocMap = {v:k for k,v in docNameToIDMap.items()}
        matchedDocumentsList = []
        
        for docID in setIntersection:
            matchedDocumentsList.append(invertedDocMap[docID])
        
        for document in matchedDocumentsList:
            print document
    
def main():
    global docNameToIDMap
    global invertedList
    print "Please wait while the index is generated.."
    buildDocIndex()
    
    if len(sys.argv) > 1:
        datasetDirectory = sys.argv[1]
    else:
        datasetDirectory = "nsf award abstracts"

    # Each file in the directory is traversed and the inverted list is built.
    for root, dirs, files in os.walk(os.getcwd()+"//"+datasetDirectory):
        for singleFile in files:
            if str(singleFile).endswith("txt"):
                textFile = open(root+"//"+str(singleFile), 'r')
                tokenSet = tokenize(textFile)
                buildIndex(tokenSet, docNameToIDMap.get(str(singleFile)))
                textFile.close()
                             
    print "Index built! You may enter your queries now!"
    processUserQuery()
    
if __name__ == '__main__':
    main()      
          
