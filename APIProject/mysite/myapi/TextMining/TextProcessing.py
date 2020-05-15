import heapq
import string
from operator import itemgetter

import nltk
import spacy
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
# from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from afinn import Afinn
from rake_nltk import Rake

#from .ParagraphExtraction import structure_text


# from .TextFiltering import get_tags_from

advertise_words = ['google', 'buy', 'amazon', 'subscribe', 'instagram', 'follow us', 'follow me', 'gmail', 'mail',
                   'facebook', 'platforms', 'click']


def replace_letter(list, letter, text):
    for l in list:
        text = text.replace(l, letter)
    for l in list:
        text = text.replace(l.upper(), letter)
    return text

def replace_non_eng_letters(text):
    a_letter = {'à', 'á', 'â', 'ã', 'ä', 'å', 'ă', 'Ă¤'}
    e_letter = {'è', 'é', 'ê', 'ë'}
    i_letter = {'ì', 'í', 'î', 'ï'}
    o_letter = {'ò', 'ó', 'ô', 'õ', 'ö'}
    u_letter = {'ù', 'ú', 'û', 'ü', 'ĂĽ'}
    s_letter = {'ş', 'š', 'ß', 'Ăź'}
    # ’
    punctuation = {'â€™', '’'}
    text = replace_letter(s_letter, 's', text)
    text = replace_letter(punctuation, '\'', text)
    text = replace_letter(u_letter, 'u', text)
    text = replace_letter(a_letter, 'a', text)
    text = replace_letter(e_letter, 'e', text)
    text = replace_letter(i_letter, 'i', text)
    text = replace_letter(o_letter, 'o', text)

    return text

def remove_stop_words(text):
    stop_words = set(stopwords.words('english'))

    text = text.split(' ')
    new_text = ''
    for word in text:
        if not word.lower() in stop_words:
            new_text += ' ' + word
    return new_text


def remove_punctuation(word):
    punctuations = '''‘!()-[]{};:'’"\,<>./?@#$%^&*_~€™'''

    no_punct = ""
    if '\'s' in word:
        word = word.replace('\'s', '')

    for char in word:
        if char not in punctuations:
            no_punct = no_punct + char

    return no_punct


def get_preprocessed_text(text):
    # Put a space after punctuation
    text = nltk.re.sub(r'(?<=[.,!?:])(?=[^\s])', r' ', text)

    # All Caps words -> small caps
    temp = ""
    for word in text.split(' '):
        if word.isupper():
            word = word.lower()
        temp = temp + word + " "
    text = temp

    # Put space between words
    text = nltk.re.sub(r'(\w)([A-Z])', r"\1 \2", text)

    # Convert to lowercase
    text = text.lower()

    # Remove Numbers
    text = nltk.re.sub('(\d)+', '', text)

    # Remove advertising text
    splitted_text = nltk.re.split('[?.,]', text)
    advertisings = []
    for prop in splitted_text:
        for word in advertise_words:
            if word in prop:
                advertisings.append(prop)
    for ad in advertisings:
        if ad in splitted_text:
            splitted_text.remove(ad)
    text = ".".join(splitted_text)
    print(text)

    # Tokenize words
    text = tokenize_words(text)

    # Lamentize the words
    lamented_text = lemantized_form(text)
    text = " ".join(lamented_text)
    return text


def remove_useless_words(tokens):
    stop_words = stopwords.words("english")
    stop_words.extend(["’", "‘"])
    tokens = [w for w in tokens.split(" ") if w not in stop_words]
    return tokens

def sentiment_analysis(tokens):
    af = Afinn()
    sentiment_scores = dict()
    for token in tokens:
        sentiment_scores[token] = af.score(token)
    return sentiment_scores


def frequency(tokens):
    response = nltk.FreqDist(tokens)
    return response


# tag words as adj or nouns etc
def speach_tagging(tokens):
    myDict = dict()
    for token in tokens:
        myDict.update(nltk.pos_tag([token]))
    return myDict


def tokenize_words(text):
    print(text)
    tokens = word_tokenize(text)
    return tokens


def stemmered_form(tokens):
    porter = PorterStemmer()
    stems = []
    for t in tokens:
        stems.append(porter.stem(t))
    return stems


def lemantized_form(tokens):
    words = ["was", "does", "has"]
    wordnet_lemmatizer = WordNetLemmatizer()
    lementized_tokens = []

    if type(tokens) is list:
        for w in tokens:
            if w not in words:
                lementized_tokens.append(wordnet_lemmatizer.lemmatize(w))
    else:
        lementized_tokens.append(wordnet_lemmatizer.lemmatize(tokens))

    return lementized_tokens








