import pandas as pd 
import numpy as np
import string


import nltk
#nltk.download('wordnet')

#nltk.download('stopwords')
from nltk.tokenize import word_tokenize

data = pd.read_csv('data.csv')

#data.head()
# Case conversion

reviews = data['Review_text'].astype(str)
data["text_lower"] = data["Review_text"].str.lower()
data.head()

#Punctuation removal

data.drop(["text_lower"], axis=1, inplace=True)

PUNCT_TO_REMOVE = string.punctuation
def remove_punctuation(Review_text):
    """custom function to remove the punctuation"""
    return Review_text.translate(str.maketrans('', '', PUNCT_TO_REMOVE))

data["text_wo_punct"] = data["Review_text"].apply(lambda text: remove_punctuation(text))
data.head()

# Removal of stop words

from nltk.corpus import stopwords
", ".join(stopwords.words('english'))

STOPWORDS = set(stopwords.words('english'))
def remove_stopwords(text):
    """custom function to remove the stopwords"""
    return " ".join([word for word in str(text).split() if word not in STOPWORDS])

data["text_wo_stop"] = data["text_wo_punct"].apply(lambda text: remove_stopwords(text))
data.head()



# Removal of frequent words

from collections import Counter
cnt = Counter()
for text in data["text_wo_stop"].values:
    for word in text.split():
        cnt[word] += 1
        
cnt.most_common(10)



# Stemming

from nltk.stem.porter import PorterStemmer

stemmer = PorterStemmer()
def stem_words(text):
    return " ".join([stemmer.stem(word) for word in text.split()])

data["text_stemmed"] = data["Review_text"].apply(lambda text: stem_words(text))
data.head()


# Lemmitization




from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
def lemmatize_words(text):
    return " ".join([lemmatizer.lemmatize(word) for word in text.split()])

data["text_lemmatized"] = data["Review_text"].apply(lambda text: lemmatize_words(text))
data.head()

lemmatizer.lemmatize("running")



from collections import Counter
cnt = Counter()
for text in data["text_wo_stop"].values:
    for word in text.split():
        cnt[word] += 1
        
print(cnt.most_common(10))

# Checking the polarity of the sentence

from textblob import TextBlob
data['sentiment'] = data['Review_text'][:212].apply(lambda x: TextBlob(x).sentiment)

print(data['sentiment'])