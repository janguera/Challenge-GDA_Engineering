from textblob import TextBlob

def get_polarity(text):
    return TextBlob(text).sentiment.polarity

def classify_polarity(polarity_score):
    if polarity_score > 0:
        return 'Positive'
    elif polarity_score < 0:
        return 'Negative'
    else:
        return 'Neutral'
    
