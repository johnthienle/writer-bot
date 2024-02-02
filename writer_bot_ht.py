'''
    File: writer_bot_ht.py
    Author: John Le
    Purpose: Using the markov chain algorithm, produce a randomly generated
    text of a specific length from a given source text
    CSC 120, 001, Fall Semester
'''

import sys
import random

SEED = 8
random.seed(SEED)
NONWORD = '@'

class HashTable:
    '''A class for a HashTable, initializes a hash table of a specified size.
    Parameters: size is an int
    Return Value: Prints a list of hash values.'''
    def __init__(self, size):
        # initializes a hash table
        self._size = size
        self._pairs = [None] * size
    
    def _hash(self, key):
        # computes the hash value of a specific key
        p = 0
        for c in key:
            p = 31 * p + ord(c)
        return p % self._size
    
    def put(self, key, value):
        # puts a key and value as a key/value pair into the
        # hash table object
        i = self._hash(key)
        if self._pairs[i] != None:
            while True:
                i -= 1
                if i < 0:
                    i = len(self._pairs) - 1
                if self._pairs[i] == None:
                    break
        self._pairs[i] = [key, value]

    def get(self, key):
        # checks the hash table object to return the value of a
        # specific key, if the key does not exist, returns None
        i = self._hash(key)
        if self._pairs[i][0] == key:
            return self._pairs[i][1]
        if self._pairs[i] != None:
            while True:
                i -= 1
                if i < 0:
                    i = len(self._pairs) - 1
                if self._pairs[i][0] == key:
                    return self._pairs[i][1]
                elif self._pairs[i] == None:
                    return None

    def __contains__(self, key):
        # checks the hash table object to see if key is present
        # in the table, returns True if it is, False if not
        i = self._hash(key)
        if self._pairs[i] == None:
            return False
        if self._pairs[i][0] == key:
            return True
        if self._pairs[i] != key:
            while True:
                i -= 1
                if i < 0:
                    i = len(self._pairs) - 1
                if self._pairs[i] == None:
                    return False
                elif self._pairs[i][0] == key:
                    return True

    def __str__(self):
        # returns a string representation of a hash table
        return (str(self._pairs))

def processFile(file, prefixsize):
    '''Processes a specified file and puts every word in the file into a
    list to be later used.
    Paramters: file is a file, prefixsize is an int
    Pre-Condition: file is a file, prefixsize is an int
    Post-Condition: Returns a list made of words that are in given file'''
    wordlist = []
    f = open(file, "r")
    for line in f:
        line = line.strip("\n")
        line = line.lstrip(" ")
        line = line.rstrip(" ")
        wordlist += line.split(" ")
    while "" in wordlist:
        wordlist.remove("")
    for i in range(prefixsize):
        wordlist.insert(0, NONWORD)
    return wordlist

def definekey(prefixsize, wordlist, start, end):
    '''Makes a string that is prefixsize amount of words.
    Paramters: prefixsize is an int, wordlist is a list, start is an int,
    end is an int
    Pre-Condition: prefixsize is an int, wordlist is a list, start is an int,
    end is an int
    Post-Condition: Returns a string that is made up of a prefixsize amount of
    words to be used as a key in a hash table.'''
    key = ""
    spaces = prefixsize - 1
    while start < end:
        key += wordlist[start]
        if spaces != 0:
            key += " "
        start += 1
        spaces -= 1
    return key

def createtable(prefixsize, tablesize, wordlist):
    '''Prompts the user for inputs on what file to open, table size,
    prefix size, and how many words should be randomly generated.
    Paramters: table is a hashtable, wordlist is a list, length is an int,
    prefixsize is an int
    Pre-Condition: prefixsize is an int, wordlist is a list, tablesize is an int
    Post-Condition: Returns a hash table of words and the specific words that occur
    after the specific word.'''
    t = HashTable(tablesize)
    temp = []
    for i in range(len(wordlist) - prefixsize):
        key = definekey(prefixsize, wordlist, i, i + prefixsize)
        if key not in t:
            t.put(key, [wordlist[i + prefixsize]])
        else:
            temp = t.get(key)
            temp += [wordlist[i + prefixsize]]
            t.put(key, temp)
    return t

def restofprefix(prefix):
    result = ""
    for word in prefix:
        result = result + word + " "
    return result

def printtext(table, wordlist, length, prefixsize):
    '''Prompts the user for inputs on what file to open, table size,
    prefix size, and how many words should be randomly generated.
    Paramters: table is a hashtable, wordlist is a list, length is an int,
    prefixsize is an int
    Pre-Condition: table is a hashtable, wordlist is a list, length is an int,
    prefixsize is an int
    Post-Condition: Prints a randomly generated text of a specific length
    from a given file'''
    message = ""
    suffix = []
    prefix = ""
    wordcount = 0
    randomw = ""
    for i in range(length - 1):
        if len(message.split()) == 10:
            print(message)
            message = ""
        if i == 0:
            message += definekey(prefixsize, wordlist, i + prefixsize, i + prefixsize * 2) + " "
            prefix = definekey(prefixsize, wordlist, i + prefixsize, i + prefixsize * 2)
            suffix = table.get(definekey(prefixsize, wordlist, i + prefixsize, i + prefixsize * 2))
            wordcount += prefixsize
        else:
            suffix = table.get(prefix)
            if i == length:
                if len(suffix) == 1:
                    message += suffix[0]
                    wordcount += 1
                elif len(suffix) > 1:
                    randomw = suffix[random.randint(0, len(suffix) - 1)]
                    prefix = restofprefix(prefix.split()[1:]) + randomw
                    message += randomw
                    wordcount += 1
            if len(suffix) == 1:
                message += (suffix[0] + " ")
                prefix = restofprefix(prefix.split()[1:]) + suffix[0]
                wordcount += 1
            elif len(suffix) > 1:
                randomw = suffix[random.randint(0, len(suffix) - 1)]
                prefix = restofprefix(prefix.split()[1:]) + randomw
                message += (randomw + " ")
                wordcount += 1
    print(message)

def main():
    '''Prompts the user for inputs on what file to open, table size,
    prefix size, and how many words should be randomly generated.
    Paramters: N/A
    Pre-Condition: N/A
    Post-Condition: Prints a randomly generated text of a specific length
    from a given file'''
    file = input()
    tablesize = int(input())
    prefixsize = int(input())
    length = int(input())
    if prefixsize < 1:
        print("ERROR: specified prefix size is less than one")
        sys.exit(0)
    if length < 1:
        print("ERROR: specified size of the generated text is less than one")
        sys.exit(0)
    wordlist = processFile(file, prefixsize)
    table = createtable(prefixsize, tablesize, wordlist)
    printtext(table, wordlist, length, prefixsize)

main()