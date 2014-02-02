import re
import sys
import os
import math
import heapq
from operator import itemgetter

documentVectorMap = {}
documentFrequencyMap= {}
fileCount = 0
   
def updateDocumentVectorMap():
    global documentVectorMap
    global documentFrequencyMap
    global fileCount
    for document in documentVectorMap:
        sumOfSquares = 0
        documentTokenFrequencyMap = documentVectorMap[document]
        for token in documentTokenFrequencyMap:
            tokenFrequency = 1 + math.log10(documentTokenFrequencyMap[token])
            tokenIDFValue  = math.log10(fileCount/documentFrequencyMap[token])
            documentTokenFrequencyMap[token] = tokenFrequency * tokenIDFValue
            sumOfSquares += math.pow(documentTokenFrequencyMap[token], 2)
        
        for token in documentTokenFrequencyMap:
            documentTokenFrequencyMap[token] = documentTokenFrequencyMap[token]/math.sqrt(sumOfSquares)
            
        documentVectorMap[document] = documentTokenFrequencyMap
             
def computeDocumentFrequency(inputFile):
    global documentVectorMap
    global documentFrequencyMap
    tokenFrequencyMap = {}
    tokenSet = set()
    for line in inputFile:
        line = line.lower()
        tokens = re.findall('\w+', line)
        for token in tokens:
            tokenFrequencyMap[token] = tokenFrequencyMap.get(token, 0) + 1
            tokenSet.add(token)
    
    fileName = os.path.basename(inputFile.name)
    documentVectorMap[fileName] = tokenFrequencyMap
    
    for token in tokenSet:
        documentFrequencyMap[token] = documentFrequencyMap.get(token, 0) + 1
            
def computeDocumentFrequencyForAllTerms():
    global fileCount
    if len(sys.argv) > 1:
        datasetDirectory = sys.argv[1]
    else:
        datasetDirectory = "nsf award abstracts"
    #for root, dirs, files in os.walk(os.getcwd()+"//nsf award abstracts"):
    for root, dirs, files in os.walk(os.getcwd()+"//"+datasetDirectory):
        for singleFile in files:
            if str(singleFile).endswith("txt"):
                textFile = open(root+"//"+str(singleFile), 'r')
                fileCount = fileCount + 1
                computeDocumentFrequency(textFile)
                textFile.close()

def processUserQuery():
    #print "Please wait while the document vector index is being loaded...."
    #documentVectorMap        = pickle.load(open("DocumentVectorMap.p", "rb"))
    global documentVectorMap
    userQuery = ""
    
    while True:
        documentRankHeap = []
        userQuery = raw_input("Input your query : ")
        #start = time.clock()
        userQuery = userQuery.lower()
        
        if str(userQuery) == "exit":
            print "Exiting program...Have a nice day!"
            break
        
        userQueryTokenFrequencyMap = {}
        userQueryTokenList = re.findall('\w+', userQuery)
        for token in userQueryTokenList:
            if token in userQueryTokenFrequencyMap:
                userQueryTokenFrequencyMap[token] += 1
            else:
                userQueryTokenFrequencyMap[token] = 1
                
        userQueryTokenFrequencyMap = buildQueryUnitVector(userQueryTokenFrequencyMap)
        
        for document in documentVectorMap:
            documentScore = 0
            documentVector = documentVectorMap[document]
            for token in userQueryTokenFrequencyMap:
                if token in documentVector:
                    documentScore += userQueryTokenFrequencyMap[token] * documentVector[token]
            if documentScore != 0:
                if len(documentRankHeap) < 50:
                    heapq.heappush(documentRankHeap, (documentScore, document))
                elif documentScore > documentRankHeap[0][0]:
                    heapq.heappushpop(documentRankHeap, (documentScore, document))
        
        topRankedDocumentList = heapq.nlargest(50, documentRankHeap, key = itemgetter(0))

        if len(topRankedDocumentList) == 0:
            print "Sorry, no matches found :("
            continue

        print "Displaying top "+str(len(topRankedDocumentList)) +" results"
        topRankedDocumentList = [(y, x) for (x, y) in topRankedDocumentList]
        for documentRankItem in topRankedDocumentList:
            print documentRankItem
        
    
def buildQueryUnitVector(userQueryTokenFrequencyMap):
    sumOfSquares = 0
    for token in userQueryTokenFrequencyMap:
            sumOfSquares += math.pow(userQueryTokenFrequencyMap[token], 2)
    
    for token in userQueryTokenFrequencyMap:
            userQueryTokenFrequencyMap[token] = userQueryTokenFrequencyMap[token]/math.sqrt(sumOfSquares)
            
    return userQueryTokenFrequencyMap

def main():
    global documentVectorMap
    global fileCount
    print "Generating index...Please wait!!"
    computeDocumentFrequencyForAllTerms()

    print "Number of tokens = "+str(len(documentFrequencyMap))

    #f = open("tokenList.txt", "wb")
    #for token in documentFrequencyMap.keys():
    #    f.write(token+'\n')

    #f.close()
    updateDocumentVectorMap()
    print "Index generation complete. You may enter your queries now!"
    processUserQuery()
    
if __name__ == '__main__':
    main()
                    
                    
