import pandas as pd 
import string 
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('vader_lexicon')
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.sentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud
import plotly.express as px 
import matplotlib.pyplot as plt

# Load
def load_data():
    data = pd.read_csv("./data/reviews-dataset.csv")
    return data

# get preprocessed data
def get_preprocessed_data():
    data = load_data()
    return preprocess_data(data)

# Remove stopwords
def remove_stopwords(tokens):
    en_stopwords = stopwords.words("English")
    en_stopwords.extend(['im','its','youre','thing','cant','dont','doesnt'])
    return [t for t in tokens if t not in en_stopwords]

# Extract adjectives
def extract_adj(tokens):
    adjectives = []
    for x in tokens:
        if x[1] in ['JJ','JJR','JJS']:
            adjectives.append(x[0])

    return adjectives

# Category wise Reviews
def category_reviews():
    data = load_data()
    return data.product_category.value_counts().to_dict()

# Get total reviews
def get_total_reviews():
    data = load_data()
    return data.shape[0]

# Preprocessing steps
def preprocess_data(data):
    #Convert the reviews into Lower Case
    data.product_review = data.product_review.str.lower()

    #Removing puctuations
    data.product_review = data.product_review.str.translate(str.maketrans('','',string.punctuation))

    #Tokenize words
    data['product_review_tokenized'] = data.product_review.apply(nltk.word_tokenize)

    #Remove stopwords
    data['cleaned_tokens'] = data.product_review_tokenized.apply(remove_stopwords)

    #Stingify cleaned tokens
    data['product_review_cleaned'] = data.cleaned_tokens.apply(lambda x: ' '.join(x))

    #POS Tagging
    data['POS_tokens'] = data.product_review_tokenized.apply(nltk.pos_tag)

    #Extract adjectives
    data['adjectives'] = data.POS_tokens.apply(extract_adj)

    return data

# Get word cloud
def get_wordcloud(categories):
    data = get_preprocessed_data()
    pass


#get sentiments
def polarity_score(review):
    # Initilizing the Sentiment Analyzer
    sent = SentimentIntensityAnalyzer()
   
    # Extracting the sentiment polarity scores of a review
    scores = sent.polarity_scores(review)
    
    # Getting the compound score
    compound = scores['compound']
    
    if compound > 0.05:
        return "positive"
    elif compound < -0.5:
        return "negative"
    else:
        return "neutral"
    
def get_sent_analysis():
    data = get_preprocessed_data()

    # Label sentiments
    data['sentiment'] = data.product_review_cleaned.apply(polarity_score)

    # Get results
    df = data.groupby(["product_category","sentiment"]).size().reset_index(name="counts")
    return df.to_dict()
