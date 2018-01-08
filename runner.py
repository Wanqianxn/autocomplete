import sys, time
from sys import stdin, stderr, stdout
import helper
import pandas as pd

sep = chr(31)
reviewTrie1, reviewTrie2 = helper.Trie(), helper.Trie()

# Loads a review file into both tries, one by word (i.e. space-separated) and
# one by string size.
def loadReview(n, maxline):
    infile = open('reviews_{}.txt'.format(n), 'r', encoding='utf8')
    colnames = ['productID', 'userID', 'unixDate', 'rating']
    meta = pd.read_csv('metadata_{}.csv'.format(n), header=None, names=colnames)
    print('Loading review set {}...'.format(n), file=stderr)
    for i, line in enumerate(infile):
        rating, user, movie = meta.ix[i].rating, meta.ix[i].userID, meta.ix[i].productID
        wordlist1 = line.split()
        wordlist2 = [line[i:i+6].strip('\r\n') for i in range(0, len(line), 6)]
        for word in wordlist1:
            reviewTrie1.addWord(word.lower(), int(rating), user, movie)
        for word in wordlist2:
            if word != '':
                reviewTrie2.addWord(word.lower(), int(rating), user, movie)
        if i > 0 and i % (maxline / 10) == 0:
            print('{} of {} reviews loaded.'.format(i, maxline), file=stderr)
        if i == maxline:
            break
    infile.close()

# Call the completeWord method, using the by-string trie if the user and movie
# being evaluated have been loaded previously, otherwise, use the by-word trie.
def predictReview(productID, userID, unixDate, rating):
    review_typed = ''
    while True:
        next_chars = stdin.readline().rstrip('\r\n')
        if len(next_chars) == 0:
            return
        review_typed += next_chars

        current1 = review_typed.split()[-1]
        current2 = review_typed[-3:]
        if productID in helper.allUserMovies and userID in helper.allUserMovies:
            topwords = reviewTrie2.completeWord(current2, int(rating), userID, productID)
        else:
            topwords = reviewTrie1.completeWord(current1, int(rating), userID, productID)
        preds = tuple([x[0] for x in topwords])

        try:
            print('{}{}{}{}{}'.format(preds[0], sep, preds[1], sep, preds[2]))
            stdout.flush()
        except Exception:
            print(' {} {} '.format(sep, sep))
            stdout.flush()

try:
    t0 = time.time()
    for i in range(10):
        loadReview(i, 10000)
    loadtime = "{0:.2f}".format(time.time() - t0)
    print('Load Time: ' + str(loadtime) + 's', file=stderr)
    print('All files loaded.', file=stderr)
except Exception as e:
    print('Loading error.\n', file=stderr)
    print(e, file=stderr)
    sys.exit(1)

print("Starting analysis...", file=stderr)

while True:
    try:
        metadata = stdin.readline().rstrip('\r\n').split(',')
        productID, userID, unixDate, rating = metadata
        predictReview(productID, userID, unixDate, rating)
    except EOFError:
        sys.exit(0)
    except Exception as e:
        print('Analyzing error.\n', file=stderr)
        print(e, file=stderr)
        sys.exit(1)
