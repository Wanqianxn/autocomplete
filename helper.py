import string
from collections import deque, Counter

# Set of all users and movies.
allUserMovies = set()

# Exception class for invalid trie path.
class NoPath(Exception):
    pass

'''
Node in trie represents a single character (a.k.a. a string fragment up until
that character). Data attributes record the number of occurences of this
fragment for a given rating, user and movie.
'''
class Node:

    def __init__(self):
        self.count = [0 for i in range(5)]
        self.usermovie = Counter()
        self.next = dict()

'''
Trie structure for loading movie reviews, comes with a "pointer".
Data attributes: total number of strings, and all users and movies ever recorded.
Methods: Move pointer around, add a string, find top 3 completed strings based
on partial string fragment, using Bayesian inferencing.
'''
class Trie:

    def __init__(self):
        self.total = 0
        self.first = dict()
        self.pointer = self.first

    # Resets pointer to start of trie.
    def resetPointer(self):
        self.pointer = self.first

    # Adds a word to the trie. Updates the word frequency as well as the
    # review's user and movie frequency.
    def addWord(self, word, rating, user, movie):
        self.resetPointer()
        allUserMovies.update([user, movie])
        charList, length = list(word), len(word)
        for i in range(length):
            if charList[i] not in self.pointer:
                self.pointer[charList[i]] = Node()
            if i != length - 1:
                self.pointer = self.pointer[charList[i]].next
            else:
                self.pointer = self.pointer[charList[i]]
        self.pointer.count[rating - 1] += 1
        self.pointer.usermovie[user] += 1
        self.pointer.usermovie[movie] += 1
        self.total += 1

    # Sets the pointer to a certain node.
    def setPointer(self, string):
        self.resetPointer()
        charList, length = list(string), len(string)
        for i in range(length):
            if charList[i] not in self.pointer:
                raise NoPath
            if i != length - 1:
                self.pointer = self.pointer[charList[i]].next
            else:
                self.pointer = self.pointer[charList[i]]


    # Helper function for self.completeWord. Computes the probability using
    # Bayes' Theorem. Note that if the trie doesn't contain the user or the movie,
    # then only the word frequency is taken into account.
    def insertList(self, lst, word, pointer, rating, user, movie, plen):
        countSum = sum(pointer.count)
        probWord = countSum / self.total
        probRatingWord = pointer.count[rating - 1] / countSum
        probUserWord = max((pointer.usermovie[user] / countSum), (user not in allUserMovies))
        probMovieWord = max((pointer.usermovie[movie] / countSum), (movie not in allUserMovies))
        bayesProduct = probWord * probRatingWord * probUserWord * probMovieWord

        lst.append((word[plen:], bayesProduct))
        return sorted(lst, key=lambda x: x[1], reverse=True)[:3]

    # Returns a list of the top 3 autoComplete suggestions based on a string
    # fragment. Every possible "completed string" is put into a (LIFO) stack
    # and then its probability is computed. A list of the top three words at
    # any point in time is maintained and eventually returned.
    def completeWord(self, string, rating, user, movie):
        try:
            self.setPointer(string)
        except:
            return (" ", ".", ",")
        wordqueue, topwords = deque(), []
        wordqueue.append((string, self.pointer))
        while wordqueue:
            partial, partpoint = wordqueue.pop()
            if sum(partpoint.count) > 0:
                topwords = self.insertList(topwords, partial, partpoint, rating, user, movie, len(string))
            for nextchar in partpoint.next:
                wordqueue.append((partial + nextchar, partpoint.next[nextchar]))
        for i in range(3 - len(topwords)):
            topwords.append((" ", 0))
        for i in range(3):
            if topwords[i][0] == "":
                topwords[i] = (".", 0)
        return topwords
