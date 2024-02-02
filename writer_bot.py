'''
    File: writer_bot.py
    Author: John Le
    Purpose: Given a text file, generates a random text based on
    different prefixes and suffixes using the markov chain algorithm.
    CSC 120, 001, Spring Semester
'''

import random
SEED = 8
random.seed(SEED)
NONWORD = " "

def processFile(file):
    '''Processes a text file and splits the entire file into a list of each individual
    word for further processing needs later.
    Parameters: file if a text file
    Pre-Condition: file is a text file
    Post-Condition: Returns a list of words'''
    openFile = open(file)
    result = []
    for lines in openFile:
        line = lines.split()
        for word in line:
            result.append(word)
    return result

def nonwordstart(text, n):
    '''Creates the beginning of the dictionary with NONWORD's in order to later
    produce a dictionary that has all prefixes and suffixes of a given text file
    to produce a random text.
    Parameters: text is a list of words, n is an integer
    Pre-Condition: text is a list of words, n is an integer
    Post-Condition: Returns a dictionary with the appropriate keys
    and values (NONWORDS) that are needed to further produce a dictionary with
    the appropriate keys and values to produce a random text generation
    based off the suffixes and prefixes of words'''
    result = {}
    count = 0
    x = n
    for i in range(n):
        index = 0
        temp = []
        for j in range(x):
            temp.append(NONWORD)
        if len(temp) < n:
            y = len(temp)
            while y < n:
                temp.append(text[index])
                index += 1
                y += 1
        x -= 1
        key = tuple(temp)
        result[key] = [text[count]]
        count += 1
    for i in range(len(text) - (n + 1)):
        prefix = [text[i]]
        counter = 0
        j = i
        while counter < (n - 1):
            prefix.append(text[j + 1])
            counter += 1
            j += 1
        key = tuple(prefix)
        if key not in result:
            result[key] = [text[j + 1]]
        else:
            result[key].append(text[j + 1])
    return result

def move(wordIndex, newValue):
    '''Shifts the suffix over one word in order to further help with
    random text production
    Parameters: wordIndex is a list, newValue is a string
    Pre-Condition: wordIndex is a list, newValue is a string
    Post-Condition: Returns a list that is a key to be used later in order
    to find an appropriate suffix for text generation'''
    wordIndex = wordIndex[1:]
    wordIndex.append(newValue)
    return wordIndex

def printText(listOfWords, wordCount):
    '''Prints out 10 words per loop in order to correctly produce a result
    that is a length of wordCount, given by a list of words listOfWords
    Parameters: listOfWords is a list, wordCount is an integer
    Pre-Condition: listOfWords is a list, wordCount is an integer
    Post-Condition: Prints lines of words as specified by wordCount'''
    counter = 0
    i = 0
    while i < wordCount:
        if counter < 9:
            if i == wordCount - 1:
                print(listOfWords[i])
            else:
                print(listOfWords[i],end=' ')
        if counter == 9:
            print(listOfWords[i])
            counter = 0
        else:
            counter += 1
        i += 1


def generateText(dict, n, wordCount):
    '''Generates a list of words that are randomly generated from a
    given dictionary of words and text file in order to be printed out
    Parameters: dict is a dictionary, n is an integer, wordCount is an integer
    Pre-Condition: dict is a dictionary, n is an integer, wordCount is an integer
    Post-Condtion: Returns a list of words that were randomly selected from
    resulting suffixes and prefixes generated from a given text file'''
    result = []
    index = [NONWORD] * n
    counter = n
    while counter < (wordCount + n):
        pair = tuple(index)
        if pair in dict.keys():
            wordDict = dict[pair]
            if len(wordDict) > 1:
                randomChoice = wordDict[random.randint(0, (len(wordDict) - 1))]
                result.append(randomChoice)
                index = move(index, randomChoice)
            else:
                result.append(wordDict[0])
                index = move(index, wordDict[0])
        else:
            break
        counter += 1
    printText(result, wordCount)

def main():
    """Runs all the functions in the file in order to produce a randomly
    generated text of a length of wordCount, using Markov chain analysis.
    Additionally takes in three inputs in order to be used by the functions,
    the file name, the prefix size, and how many words to be printed.
    Parameters: N/A
    Pre-Condition: N/A
    Post-Condition: Prints a text of random selected words from a given text file"""
    file = input()
    n = int(input())
    wordCount = int(input())
    processedFile = processFile(file)
    dict = nonwordstart(processedFile, n)
    generateText(dict, n, wordCount)

main()