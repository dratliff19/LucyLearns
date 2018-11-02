##Dylan Ratliff 2018

import nltk
import ssl
import datetime
import random
from nltk.tokenize import RegexpTokenizer
nltk.download('stopwords')
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
nltk.download('punkt')
import csv
import collections
from nltk import ngrams


#common words from testing
commonNode1Words = []
commonNode3Words = []
commonNode2Words = []
#end

#common grams from testing
FreqNode1Grams = []
FreqNode3Grams = []
FreqNode2Grams = []

#common words from training
mostCommonNode1Words = []
mostCommonNode3Words = []
mostCommonNode2Words = []
#end

#common grams from training
mostFreqNode1Grams = []
mostFreqNode3Grams = []
mostFreqNode2Grams = []
#end

#overall number of Node1 word scores
totalNode1Score = 0
totalNode3Score = 0
totalNode2Score = 0
#end

#overall number of Node1 gram scores
totalNode1GramScore = 0
totalNode2GramScore = 0
totalNode3GramScore = 0
#end

#number of most common
numberCheckWords = 1500
numberCheckNgram = 3000
#end

#confidence level. Baiscally a vec.
posVec = 1.2
#end

#number of words in a phrase
numberOfWordsPhase = 3
#end

stopwords = nltk.corpus.stopwords.words('english')
notAllowed = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                  'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                  't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C',
                  'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                  'N','O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
              'X', 'Y', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                'bo', 'pic', 'www', 'twitter', 'com', 'are', 'just',
            'do', 'http', 'you', 'on', 'at','to', 'my', 'of', 'was',
              'is', 'for', 'as', 'in', 'have', 'that', 'with', 'and',
             'the', 'this','html','https','http','bit','ly']

def findNgrams(textToNgram):

    global numberOfWordsPhase
    global stopwords
    global notAllowed
    tokenizer = RegexpTokenizer(r'\w+')
    wordsFromText = tokenizer.tokenize(textToNgram)     #breaks sence into works, removes puncuation
    trueText = []
    for word in wordsFromText:
        if word.lower() not in notAllowed:
            if word.lower() not in stopwords:   #finds the true text of the
                trueText.append(word.lower())

    bigrams = ngrams(trueText, numberOfWordsPhase)   #splits into bigrams, specifically two
    return bigrams
#end

def findHashTags(textToHashTags):
    hashTagss = []
    for hashtag in textToHashTags.split():
        if hashtag.startswith('#'):
            hashTagss.append(hashtag)
    return hashTagss


##--finds most common words with-in text--##

def findMostCommonWords(wordsToAna, name):
    global stopwords
    global notAllowed

    totalWords = 0
    allowed = []
    for m2 in wordsToAna:
        if m2.lower() not in notAllowed:
            if m2.lower() not in stopwords:
                allowed.append(m2)
                totalWords += 1

    print("Total ",name," words: ", str(totalWords))

    mostCommonWords = nltk.FreqDist(w.lower() for w in allowed if w not in stopwords)
    return mostCommonWords
#end

def divide_byZero(n, d):
    return n / d if d else 0

##--decides if a sentence is Node1, Node3, Node2 --##
def judge(reviewWords):
    #globals
    global posVec

    global ifOne
    global ifTwo
    global ifThree

    global totalNode1Score
    global totalNode3Score
    global totalNode2Score

    global mostFreqNode1Grams
    global mostFreqNode3Grams
    global mostFreqNode2Grams


    global countNode1
    global countNode3
    global countNode2
    #end


    #breaks words into sentences
    sentences = nltk.sent_tokenize(reviewWords)
    #end

    #variables
    Node1 = 0
    Node3 = 0
    Node2 = 0

    countNode1 = 0
    countNode3 = 0
    countNode2 = 0

    totalNode1Words = 0
    totalNode3Words = 0
    totalNode2Words = 0
    #end



    ngramsFromSentence = findNgrams(reviewWords)
    for word in ngramsFromSentence:
        if word in mostFreqNode1Grams:
            for word11, count22 in mostFreqNode1Grams.most_common(numberCheckNgram):
                if word == word11:
                    countNode1 += count22 / totalNode1GramScore
                    FreqNode1Grams.append(word11)
        if word in mostFreqNode3Grams:
            for word22, count33 in mostFreqNode3Grams.most_common(numberCheckNgram):
                if word == word22:
                    countNode3 += count33 / totalNode3GramScore
                    FreqNode3Grams.append(word22)

        if word in mostFreqNode2Grams:
            for word33, count44 in mostFreqNode2Grams.most_common(numberCheckNgram):
                if word == word33:
                    countNode2 += count44 / totalNode2GramScore
                    FreqNode2Grams.append(word33)


    #for each sentence of the text
    for sentence in sentences:


        review = nltk.word_tokenize(sentence)   #breaks sentence into words
        review = [word.lower() for word in review]  #lower case all words for consistancy



        #for each word in the sentence
        for word in review:
            if word in mostCommonNode1Words:
                for word1, count in mostCommonNode1Words.most_common(numberCheckWords):   #looks at N most common Node1 words
                    if word == word1:
                        countNode1 += count / totalNode1Score   #if it finds the word, add it's weight to overall confidence
                        totalNode1Words += 1
                        commonNode1Words.append(word)     #adds word to common
            if word in mostCommonNode2Words:
                for word2, count in mostCommonNode2Words.most_common(numberCheckWords):   #looks at N most common Node2 words
                    if word2 == word:
                        countNode2 += count / totalNode2Score   #if it finds the word, add it's weight to overall confidence
                        totalNode2Words += 1
                        commonNode2Words.append(word)     #adds word to common

            if word in mostCommonNode3Words:
                for word1, count in mostCommonNode3Words.most_common(numberCheckWords):   #looks at N most common Node3 words
                    if word == word1:
                        countNode3 += count / totalNode3Score   #if it finds the word, add it's weight to overall confidence
                        totalNode3Words += 1
                        commonNode3Words.append(word)     #adds word to common

    ####future plans for more nodes#####
    ##overAverages = []
    ##overAverages.append((countNode1,"Node1"))
    ##overAverages.append((countNode3,"Node3"))
    ##overAverages.append((countNode2,"Node2"))


    #overAverages.sort(reverse=True)
    #print(str(overAverages))
    #for x, y in overAverages:
        #print(str(y))
        #return y

    #the core for determining if the word is node1, node2, node3
    if divide_byZero(countNode1, countNode3) >= posVec:     #if Node1 divided by Node3 is greater or equal to confidence
        if divide_byZero(countNode2, countNode1) >= posVec:#if Node2 divided by Node1 is greater or equal to confidence
            if divide_byZero(countNode2, countNode3) >= posVec:
                print("Confidence: ",str(countNode2/(countNode3 + countNode1 + countNode2)))
                return "Node2"
            else:
                print("Confidence: ",str(countNode3/(countNode3 + countNode1 + countNode2)))
                return "Node3"
        else:
            print("Confidence: ", str(countNode1 / (countNode3 + countNode1 + countNode2)))
            return "Node1"    #else Node1
    else:                                               #else Node1 is less
        if divide_byZero(countNode2, countNode3) >= posVec:     #if Node2 divided by Node3 is greater or equal to confidence
            if divide_byZero(countNode2, countNode1) >= posVec:
                print("Confidence: ", str(countNode2 / (countNode3 + countNode1 + countNode2)))
                return "Node2"
            else:
                print("Confidence: ", str(countNode1 / (countNode3 + countNode1 + countNode2)))
                return "Node1"

        else:
            print("Confidence: ", str(countNode3 / (countNode3 + countNode1 + countNode2)))
            return "Node3" #else Node3

##-- Analyzes the correctness of the learning and thinking algorithm --##
def analyzeFile(rowsToScan, documentToOpen):
    #globals
    global commonNode1Words
    global commonNode3Words
    global commonNode2Words

    global FreqNode1Grams
    global FreqNode2Grams
    global FreqNode3Grams

    #end

    #variables for function
    overallNode1 = 0
    overallNode3 = 0
    overallNode2 = 0

    actualNode1 = 0
    actualNode3 = 0
    actualNode2 = 0
    #end

    #start time for function
    startTime = datetime.datetime.now() 
    #end

    #open document for analyzing, create headers
    with open(documentToOpen, "r", encoding='utf-8') as csvfile:
        data = csv.reader(csvfile)

        headers = next(data)    #finds the headers

        #test Naives bayes on data set. (TESTING)
        #end

        headerCount = 0     #counts headers
        for h in headers:
            print("["+ str(headerCount) + "]" + h)
            headerCount += 1
    #end

        #print document stats
        print("Numer of columns: " + str(headerCount))
        print("Number of rows to scan: " + str(rowsToScan))
        #end

        #runs rows through the judge function
        splitNum = round(rowsToScan / 3)
        countRow = 0
        countNode1 = 0
        countNode2 = 0
        countNode3 = 0
        overall = []
        for row in data:
            if int(row[0]) == 1:
                if countNode1 < splitNum and len(row[1]) > 100:
                    overall.append([judge(row[1]), row[0]])
                    countRow += 1
                    countNode1 += 1
            if int(row[0]) == 2:
                if countNode2 < splitNum and len(row[1]) > 100:
                    overall.append([judge(row[1]), row[0]])
                    countRow += 1
                    countNode2 += 1
            if int(row[0]) == 3:
                if countNode3 < splitNum and len(row[1]) > 100:
                    overall.append([judge(row[1]), row[0]])
                    countRow += 1
                    countNode3 += 1
            #print(str(countRow),"/",str(rowsToScan))
            if countRow == (splitNum * 3):
                print("made it")
                break
        #end

        #counts all corrrect and incorrect, and overAll
        numCorrect = 0
        numIncorrect = 0

        for num in overall:
            if num[0] == 'Node1':
                overallNode1 += 1
            if num[0] == 'Node2':
                overallNode2 += 1
            if num[0] == 'Node3':
                overallNode3 += 1

        incorrectNode1 = 0
        incorrectNode1AsNode3 = 0
        incorrectNode1AsNode2 = 0
        incorrectNode3 = 0
        incorrectNode3AsNode1 = 0
        incorrectNode3AsNode2 = 0
        incorrectNode2 = 0
        incorrectNode2AsNode1 = 0
        incorrectNode2AsNode3 = 0

        for r in overall:
            if int(r[1]) == 1:
                    actualNode1 += 1
                    if r[0] == "Node1":
                        numCorrect += 1
                    if r[0] == "Node3":
                        numIncorrect += 1
                        incorrectNode1 += 1
                        incorrectNode1AsNode3 += 1
                    if r[0] == "Node2":
                        numIncorrect += 1
                        incorrectNode1 += 1
                        incorrectNode1AsNode2 += 1

            if int(r[1]) == 3:
                    actualNode3 += 1
                    if r[0] == "Node3":
                        numCorrect += 1
                    if r[0] == "Node1":
                        numIncorrect += 1
                        incorrectNode3 += 1
                        incorrectNode3AsNode1 += 1
                    if r[0] == "Node2":
                        numIncorrect += 1
                        incorrectNode3 += 1
                        incorrectNode3AsNode2 += 1

            elif int(r[1]) == 2:
                    actualNode2 += 1
                    if r[0] == "Node2":
                        numCorrect += 1
                    if r[0] == "Node1":
                        numIncorrect += 1
                        incorrectNode2 += 1
                        incorrectNode2AsNode1 += 1
                    if r[0] == "Node3":
                        numIncorrect += 1
                        incorrectNode2 += 1
                        incorrectNode2AsNode3 += 1
        # end

        #most Common word counts
        mostCommonNode1Words = collections.Counter(commonNode1Words)
        mostCommonNode3Words = collections.Counter(commonNode3Words)
        mostCommonNode2Words = collections.Counter(commonNode2Words)
        #end

        mostCommonNode1Grams = collections.Counter(FreqNode1Grams)
        mostCommonNode2Grams = collections.Counter(FreqNode2Grams)
        mostCommonNode3Grams = collections.Counter(FreqNode3Grams)


        #  prints most common words  #
        print("\nMost common node1 words:")
        for word, count in mostCommonNode1Words.most_common(15):
            print(word, ": ", count)
        print("Most common node1 Phrases")
        for Node1Gram, count in mostCommonNode1Grams.most_common(15):
            print(Node1Gram, ":", count)


        print("\nMost common node2 words:")
        for word, count in mostCommonNode2Words.most_common(15):
            print(word, ": ", count)
        print("Most common node2 Phrases")
        for Node2Gram, count in mostCommonNode2Grams.most_common(15):
            print(Node2Gram, ":", count)
        #end

        print("\nMost common node3 words:")
        for word, count in mostCommonNode3Words.most_common(15):
            print(word, ": ", count)
        print("Most common node3 Phrases")
        for Node3Gram, count in mostCommonNode3Grams.most_common(15):
            print(Node3Gram, ":", count)


        #  prints stats  #
        print("\n")
        print("Percent of incorrect node1: ", str(incorrectNode1/numIncorrect * 100),"%")
        print("Percent of incorrect node2: ", str(incorrectNode2/numIncorrect * 100),"%")
        print("Percent of incorrect node3: ", str(incorrectNode3/numIncorrect * 100),"%")
        print("\n")

        print("<+> Prediction Statistics <+>")
        accuracy = (numCorrect / (numCorrect + numIncorrect)) * 100
        print("Correct: " + str(numCorrect))
        print("incorrect: " + str(numIncorrect))
        print("Overall Accuracy: " + str(accuracy) + "%")

        percentOverall = (((actualNode1 - incorrectNode1) / actualNode1 * 100) + ((actualNode2 - incorrectNode2) / actualNode2 * 100) + ((actualNode3 - incorrectNode3) / actualNode3 * 100)) / 3
        print("Average Accuracy of all Nodes: ", str(percentOverall), "%")

        #print("Node1 Accuracy: " + str(((actualNode1 - incorrectNode1) / actualNode1) * 100),"%")
        #print((actualNode1 - incorrectNode1),"/",actualNode1)
        #print(str(incorrectNode1AsNode3))
        #print(str(incorrectNode1AsNode2))
        #print("Node2 Accuracy: " + str(((actualNode2 - incorrectNode2) / actualNode2) * 100),"%")
        #print((actualNode2 - incorrectNode2),"/",actualNode2)
        #print(str(incorrectNode2AsNode1))
        #print(str(incorrectNode2AsNode3))
        #print("Node3 Accuracy: " + str(((actualNode3 - incorrectNode3) / actualNode3) * 100),"%")
        #print((actualNode3 - incorrectNode3),"/",actualNode3)
        #print(str(incorrectNode3AsNode1))
        #print(str(incorrectNode3AsNode2))

        print("node1:")
        print("Number of node1 correct: ",str(actualNode1 - incorrectNode1),"/",str(actualNode1))
        print("     node1 as node3: ",str(incorrectNode1AsNode3))
        print("     node1 as node2: ",str(incorrectNode1AsNode2))
        print("node2 stats")
        print("Number of node2 correct: ",str(actualNode2 - incorrectNode2),"/",str(actualNode2))
        print("     node2 as node1:",str(incorrectNode2AsNode1))
        print("     node2 as node3: ",str(incorrectNode2AsNode3))
        print("node3 stats")
        print("Number of node3 correct: ",str(actualNode3 - incorrectNode3),"/",str(actualNode3))
        print("     node3 as node1: ",str(incorrectNode3AsNode1))
        print("     node3 as node2: ",str(incorrectNode3AsNode2))


        #end

        #End time and print
        endTime = datetime.datetime.now()
        print("Time taken: ", endTime-startTime)
        #end



#end



#the training algorithm.
#more to come...
def train(rowstoscan, documentToOpen):
    #global variables
    global mostCommonNode1Words
    global mostCommonNode3Words
    global mostCommonNode2Words

    global mostFreqNode1Grams
    global mostFreqNode3Grams
    global mostFreqNode2Grams


    global totalNode1Score
    global totalNode3Score
    global totalNode2Score

    global totalNode1GramScore
    global totalNode2GramScore
    global totalNode3GramScore
    #end

    #sets function start time
    startTime = datetime.datetime.now()
    #end

    #open documents, prepare headers
    with open(documentToOpen, "r", encoding='utf-8') as csvfile:
        data = csv.reader(csvfile)


        headers = next(data)
        headerCount = 0
        for h in headers:
            print("[" + str(headerCount) + "]" + h)
            headerCount += 1
    #end

        #print row stats
        print("Numer of columns: " + str(headerCount))
        print("Number of rows to scan: " + str(rowstoscan))
        #end

        #variables
        numOfNode1 = 0
        numOfNode3 = 0
        numOfNode2 = 0

        Node1ReviewWords = []
        Node3ReviewWords = []
        Node2ReviewWords = []

        countRow = 0
        tokenizer = RegexpTokenizer(r'\w+')

        Node1NgramsTotal = []
        Node3NgramsTotal = []
        Node2NgramsTotal = []

        Node1HashTags = []
        Node2HashTags = []
        Node3HashTags = []

        #end


    #inputs training data into memory banks
        for row in data:
            countRow += 1
            if countRow == int(rowstoscan):
                break
            if int(row[0]) == 1:       #first clasification
                if numOfNode1 < 1500 and len(row[1]) > 100:
                    numOfNode1 += 1
                    wordsFromRow = tokenizer.tokenize(row[1])
                    Node1NgramsTotal += findNgrams(row[1])
                    Node1HashTags += findHashTags(row[1])
                    for ww in wordsFromRow:
                        Node1ReviewWords.append(ww)
            if int(row[0]) == 2:    #second classification
                if numOfNode2 < 1500 and len(row[1]) > 100:
                    numOfNode2 += 1
                    wordsFromRow2 = tokenizer.tokenize(row[1])
                    Node2NgramsTotal += findNgrams(row[1])
                    Node2HashTags += findHashTags(row[1])

                    for ww in wordsFromRow2:
                        Node2ReviewWords.append(ww)
            if int(row[0]) == 3:    #third classification
                if numOfNode3 < 1400 and len(row[1]) > 100:
                    numOfNode3 += 1
                    wordsFromRow3 = tokenizer.tokenize(row[1])
                    Node3NgramsTotal += findNgrams(row[1])
                    Node3HashTags += findHashTags(row[1])

                    for ww in wordsFromRow3:
                        Node3ReviewWords.append(ww)
        #end


        #print stats for number of reviews
        print("Number of Node1: ", numOfNode1)
        print("Numer of Node3: ", numOfNode3)
        print("Number of Node2: ", numOfNode2)
        #end


    #finds most common words
    mostCommonNode1Words = findMostCommonWords(Node1ReviewWords, "node1")
    mostCommonNode3Words = findMostCommonWords(Node3ReviewWords, "node3")
    mostCommonNode2Words = findMostCommonWords(Node2ReviewWords, "node2")
    ##end

    #finds most common grams
    mostFreqNode1Grams = nltk.FreqDist(w for w in Node1NgramsTotal)
    mostFreqNode3Grams = nltk.FreqDist(w for w in Node3NgramsTotal)
    mostFreqNode2Grams = nltk.FreqDist(w for w in Node2NgramsTotal)
    ##end

    #finds most common hashtags
    mostFeqNode1HashTags = nltk.FreqDist(w for w in Node1HashTags)
    mostFeqNode2HashTags = nltk.FreqDist(w for w in Node2HashTags)
    mostFeqNode3HashTags = nltk.FreqDist(w for w in Node3HashTags)



    ##Print stats about Node1
    print("\nMost common node1 words")
    for word, count in mostCommonNode1Words.most_common(numberCheckWords):
        totalNode1Score = totalNode1Score + count
    for word, count in mostCommonNode1Words.most_common(20):
        print(word, ": ", count)
    print("Total Score: ", int(totalNode1Score))

    print("\nMost common node1 Phases")

    for word, count in mostFreqNode1Grams.most_common(numberCheckNgram):
        totalNode1GramScore = totalNode1GramScore + count
    for Node1Gram, count in mostFreqNode1Grams.most_common(20):
        print(Node1Gram, ":", count)
    print("Total Score: ", int(totalNode1GramScore))

    print("\nMost common node1 HashTags")
    for hashTag, count in mostFeqNode1HashTags.most_common(20):
        print(hashTag, ":",count)
    ##end


    ##Print stats about Node2
    print("\nMost common node2 words")

    for word, count in mostCommonNode2Words.most_common(numberCheckWords):
        totalNode2Score = totalNode2Score + count
    for word, count in mostCommonNode2Words.most_common(20):
        print(word, ": ", count)

    print("\nMost common node2 Phases")

    for word, count in mostFreqNode2Grams.most_common(numberCheckNgram):
        totalNode2GramScore = totalNode2GramScore + count
    for Node2Gram, count in mostFreqNode2Grams.most_common(20):
        print(Node2Gram, ":", count)
    print("Total Score: ", int(totalNode2GramScore))

    print("\nMost common node2 HashTags")
    for hashTag, count in mostFeqNode2HashTags.most_common(20):
        print(hashTag, ":", count)
    ##end

    ##Print stats about Node3
    print("\nMost common node3 words")

    for word, count in mostCommonNode3Words.most_common(numberCheckWords):
        totalNode3Score = totalNode3Score + count
    for word, count in mostCommonNode3Words.most_common(20):
        print(word, ": ", count)
    print("Total Score: ", int(totalNode3Score))

    print("\nMost common node3 Phases")

    for word, count in mostFreqNode3Grams.most_common(numberCheckNgram):
        totalNode3GramScore = totalNode3GramScore + count
    for Node3Gram, count in mostFreqNode3Grams.most_common(20):
        print(Node3Gram, ":", count)
    print("Total Score: ", int(totalNode3GramScore))

    print("\nMost common node3 HashTags")
    for hashTag, count in mostFeqNode3HashTags.most_common(20):
        print(hashTag, ":", count)
    ##end

    ##print totals
    print("Total Score: ", str(totalNode2Score))

    #set count to proper weight
    for word, count in mostCommonNode1Words.most_common(numberCheckWords):
        count = count / totalNode1Score
    for word, count in mostCommonNode3Words.most_common(numberCheckWords):
        count = count / totalNode3Score
    for word, count in mostCommonNode2Words.most_common(numberCheckWords):
        count = count / totalNode2Score

    for word, count in mostFreqNode2Grams.most_common(numberCheckNgram):
        count = count / totalNode2GramScore
    for word, count in mostFreqNode3Grams.most_common(numberCheckNgram):
        count = count / totalNode3GramScore
    for word, count in mostFreqNode1Grams.most_common(numberCheckNgram):
        count = count / totalNode1GramScore
    #end

    #end time
    endTime = datetime.datetime.now()
    print("Time taken: ", endTime - startTime)
    ##end

#end


def changeVec():
    global posVec
    print("Currect Confidence - " + str(posVec))
    try:
        newVec = float(input("Confidence: "))
        posVec = newVec
        print("Success")
    except:
        print("Input must be a number!")
    main()


## --Changes number of words in a phase --##
def changePhaseNum():
    global numberOfWordsPhase
    try:
        changeTo = int(input("Number of words in phase or set: "))
        numberOfWordsPhase = changeTo
        print("Success")

    except:
        print("Only numbers allowed!")
        main()
    main()
#end




def changeWordGramNum():
    global numberCheckNgram
    global numberCheckWords
    print("Current number of N-Grams to check: ", str(numberCheckNgram))
    print("Current number of words to check: ", str(numberCheckWords))

    try:
        changeToNgram = int(input("--Number of nGrams to check: "))
        numberCheckNgram = changeToNgram
        changeToWords = int(input("--Number of words to check: "))
        numberCheckWords = changeToWords
        print("Success")
        main()
    except:
        print("Input must be a number!")
        main()

def addNotAllowed():
    global notAllowed
    print(notAllowed)
    try:
        newNotAllowed = input("Enter new words to not allow: ")
        for word in newNotAllowed.split():
            notAllowed.append(word)
        print(notAllowed)
        main()
    except:
        print("User cancelled input!")
        main()

def thinkHandle():
        try:
            rowsToScan = int(input("Number of rows to scan: "))
            #document = input("Enter the document name: ")
            analyzeFile(int(rowsToScan), 'tweetAnaTraining.csv')
            main()
            print("Success")
        except:
            print("Input must be a number!")
            main()

def learnHandle():
        try:
            rowsToScan = int(input("Number of rows to scan: "))
            train(rowsToScan, 'tweetAna.csv')
            main()
            print("Success")

        except:
            print("Input must be a number!")
            main()


def main():

    global posVec
    mainCmd = input("\nLUCY:>> : ")

    if mainCmd == "--think":
        thinkHandle()
    elif mainCmd == "--learn":
        learnHandle()
    elif mainCmd == "--chcon":
        changeVec()
    elif mainCmd == "--chphrase":
        changePhaseNum()
    elif mainCmd == "--chknow":
        changeWordGramNum()
    elif mainCmd == "--chdis":
        addNotAllowed()
    elif mainCmd == "--exit":
        print("LUCY shutting down.... goodbye.")
        exit()
    else:
        main()

train(18000, 'tweetAna.csv')

main()
