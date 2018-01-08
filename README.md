# Movie Review Autocomplete Program

This is an Autocomplete program in Python, done for the Coatue Hack4Alpha Challenge. The program takes movie reviews as training data, and outputs the most likely words given some string fragment, i.e. if fed the string fragment *"loc"*, the program might output *"al"*, *"ation"* and *"ality"*.

## Approach

I employed a Naive Bayesian classifier. Given a partial string fragment, the calculated probability for any completed string is proportional to the overall frequency of the completed string in the training data, as well as the frequency of the string for the particular reviewer, movie and rating, as per Bayes' Rule. The classifier treats punctuation as normal characters too.

Implementation-wise, I used a trie-based approach. Specifically, I loaded the training data into two tries -- one trie parsed each movie review by word (i.e. space-separated) and the other parsed a movie review by string length (i.e. the first 6 characters, then the next 6 characters, and so long). This was because the by-word approach worked better if the test data contains a movie or user that the training data has not seen before (presumably since all reviews must share common English words), whereas the by-string-length approach worked better for known movies or users (since it can better predict specific character sequences, e.g. *"harry potter"*). Given the size of the training data, it made sense to employ both approaches since the test data set is unknown.


## Usage

Note that the reviews and metadata should be on the same directory as the Python scripts. 

The runner can be executed with `python runner.py`, this will allow users to manually input any string fragment into the terminal.

The grader file (provided by Coatue) can be run using `python grader.py python -u runner.py`, this will test the classifier against a small test data and return the number of invocations needed by the Autocomplete program.

Note that I have modified the original grader file to change the decoding codec from `utf8` to `latin-1` since `utf8` decoding is not compatible with some of the data.



 
