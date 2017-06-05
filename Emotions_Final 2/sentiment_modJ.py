from nltk.classify import ClassifierI
import pickle
from nltk.tokenize import word_tokenize
from collections import Counter


#  #For Training
#  Step 1: Convert the training data in the format of list of tuples (list of words, category), Shuffle for unbiased.
#  Step 2: Collect all words from training data, refine them using POS tagging.
#  Step 3: Set feature words as the most frequent words. (PICKLE these words)
#  Step 4: Pass the training data via function find_features to get a list of tuples (dictionary of features, category)
#  Step 5: Use the training data to train all the classifiers (PICKLE the trained classifier)

#  #Classifying module
#  Step 1: Create your own Classifier Class inherit ClassifierI, parameters = all predefined classifiers
#  Step 2: Create a function in class to classify by the method of voting.
#  Step 3: Create a function in class to return the the confidence in your classification.
#  Step 4: load feature words pickle
#  Step 5: load the trained classifiers pickle.
#  Step 6: Make an object of our class of votingClassifier
#  Step 7: Define find_features to convert the input_text_words to a dictionary of features.
#  Step 8: Define the Sentiment func to take input, call the classify function with features and return sentiment.


class voteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)  # list of pos and neg
        data = Counter(votes)
        # if data.most_common(2)[0][1] != data.most_common(2)[1][1]:
        return data.most_common(1)[0][0]  # For Unique Emotion
        # else:
        #     return data.most_common(2)[0][0]+"/"+data.most_common(2)[1][0]

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        data = Counter(votes)
        choice_votes = votes.count(data.most_common(1)[0][0])
        conf = choice_votes / len(votes)
        return conf


fw_file = open("pickles/fwJ.pickle", "rb")
feature_words = pickle.load(fw_file)  # ALL IN lowercase Words Against which we trained our algo
fw_file.close()

file = open("pickles/nbc4J.pickle", "rb")
NBclassifier = pickle.load(file)
file.close()
file = open("pickles/nbc4J1.pickle", "rb")
NBclassifier1 = pickle.load(file)
file.close()
file = open("pickles/nbc4J2.pickle", "rb")
NBclassifier2 = pickle.load(file)
file.close()
file = open("pickles/nbc4J3.pickle", "rb")
NBclassifier3 = pickle.load(file)
file.close()
file = open("pickles/nbc4J4.pickle", "rb")
NBclassifier4 = pickle.load(file)
file.close()

file = open("pickles/mnbc4J.pickle", "rb")
MNBc = pickle.load(file)
file.close()
file = open("pickles/mnbc4J1.pickle", "rb")
MNBc1 = pickle.load(file)
file.close()
file = open("pickles/mnbc4J2.pickle", "rb")
MNBc2 = pickle.load(file)
file.close()
file = open("pickles/mnbc4J3.pickle", "rb")
MNBc3 = pickle.load(file)
file.close()
file = open("pickles/mnbc4J4.pickle", "rb")
MNBc4 = pickle.load(file)
file.close()

file = open("pickles/bnbc4J.pickle", "rb")
BNBc = pickle.load(file)
file.close()
file = open("pickles/bnbc4J1.pickle", "rb")
BNBc1 = pickle.load(file)
file.close()
file = open("pickles/bnbc4J2.pickle", "rb")
BNBc2 = pickle.load(file)
file.close()
file = open("pickles/bnbc4J3.pickle", "rb")
BNBc3 = pickle.load(file)
file.close()
file = open("pickles/bnbc4J4.pickle", "rb")
BNBc4 = pickle.load(file)
file.close()

file = open("pickles/lrc4J.pickle", "rb")
LogisticRegressionC = pickle.load(file)
file.close()
file = open("pickles/lrc4J1.pickle", "rb")
LogisticRegressionC1 = pickle.load(file)
file.close()
file = open("pickles/lrc4J2.pickle", "rb")
LogisticRegressionC2 = pickle.load(file)
file.close()
file = open("pickles/lrc4J3.pickle", "rb")
LogisticRegressionC3 = pickle.load(file)
file.close()
file = open("pickles/lrc4J4.pickle", "rb")
LogisticRegressionC4 = pickle.load(file)
file.close()

file = open("pickles/lsvc4J.pickle", "rb")
LinearSVCc = pickle.load(file)
file.close()
file = open("pickles/lsvc4J1.pickle", "rb")
LinearSVCc1 = pickle.load(file)
file.close()
file = open("pickles/lsvc4J2.pickle", "rb")
LinearSVCc2 = pickle.load(file)
file.close()
file = open("pickles/lsvc4J3.pickle", "rb")
LinearSVCc3 = pickle.load(file)
file.close()
file = open("pickles/lsvc4J4.pickle", "rb")
LinearSVCc4 = pickle.load(file)
file.close()

OurClassifier = voteClassifier(LinearSVCc, LinearSVCc1, LogisticRegressionC, LogisticRegressionC1, BNBc, BNBc1, MNBc,
                               MNBc1, NBclassifier, NBclassifier1, LinearSVCc2, LogisticRegressionC2, MNBc2, BNBc2,
                               NBclassifier2, LinearSVCc3, LogisticRegressionC3, MNBc3, BNBc3, NBclassifier3,
                               LinearSVCc4, LogisticRegressionC4, MNBc4, BNBc4, NBclassifier4)


def find_features(review_words):
    review_words = set(review_words)
    features = {}  # Dictionary of words with value = TRUE/FALSE
    # TRUE if we a match between the input_text and ourFeatureWords
    for f in feature_words:
        features[f] = (f in review_words)
    return features


def sentiment(input_text):
    input_text = [w.lower() for w in word_tokenize(input_text)]
    feats = find_features(input_text)  # would return matching feature words input_words vs. words used for training

    return OurClassifier.classify(feats), OurClassifier.confidence(
        feats)  # sending a dictionary and getting a category returned from the classify function ({features},category)
