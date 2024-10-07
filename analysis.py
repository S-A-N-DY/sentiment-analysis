import pandas as pd
from textblob import TextBlob
import re
 
# Using double backslashes to escape special characters in the file path
data_clean = pd.read_excel(r'C:\Users\moyu2001\Desktop\PROJECT\Hackfest Data.xlsx', sheet_name='Data')

import pandas as pd
import numpy as np

# Assuming df is your DataFrame
# Replace integer values with NaN
data_clean = data_clean.replace(np.nan, 'integer')

# Display the updated DataFrame
print(data_clean)


# Function to check if the text is non-textual (standalone hyperlinks, emojis, etc.)
def is_non_textual(text):
    # Check if the entire string is made up of non-alphanumeric characters (emojis, symbols)
    # and/or if it is a hyperlink, or a float/int represented as a string
    return bool(re.fullmatch(r'(http\S+|[^\w\s,.\-!?\'"]+|\d+\.?\d*)', text))
 
# Function to clean and check the text data
def clean_and_check_text(text):
    if pd.isnull(text):  # Preserve empty values
        return None
    text = str(text).strip()
    if is_non_textual(text):  # Skip standalone non-textual content
        return None
    return text  # Return text as is for valid content
 

 

for col in ['qcheck', 'x01_2', 'x01_3']:
    sentiment_col_name = col + '_sentiment'
    data_clean[sentiment_col_name] = data_clean[col].apply(lambda x: TextBlob(str(x)).sentiment.polarity if x is not None else None)









    # Sentiment analysis on the translated text

    # Determine if a response is missing based on the cleaned and translated data
    data_clean['is_missing'] = data_clean[['qcheck', 'x01_2', 'x01_3']].isnull().all(axis=1)


def calculate_sentiment(text):
    if isinstance(text, int):  # Check if the value is a float
        text = str(text)  # Convert float to string
    return TextBlob(text).sentiment.polarity

data_clean['qcheck_sentiment'] = data_clean['qcheck'].apply(calculate_sentiment)

 
data_clean['qcheck_sentiment'] = data_clean['qcheck'].apply(calculate_sentiment)
data_clean['x01_2_sentiment'] = data_clean['x01_2'].apply(calculate_sentiment)
data_clean['x01_3_sentiment'] = data_clean['x01_3'].apply(calculate_sentiment)


# Repeat for 'x01_2_english' and 'x01_3_english' as needed
 
# Step 5: Anomaly detection
def is_outlier(row):
    word_count_thresh = 10
    sentiment_thresh = 0.8
    is_suspicious_text = ("guaranteed results" in str(row['qcheck']) or
                          "money back no questions asked" in str(row['x01_2']))
    try:
        qcheck_words = str(row['qcheck']).split()
    except AttributeError:
        qcheck_words = []
    return (
        len(qcheck_words) < word_count_thresh or
        len(qcheck_words) > 50 or
        abs(row['qcheck_sentiment']) > sentiment_thresh or
        is_suspicious_text
    )
 
data_clean['is_outlier'] = data_clean.apply(is_outlier, axis=1)
 
# Step 6: Trust-rating system
def assign_trust_rating(row):
    trust_rating = 10
    if row['is_outlier']:
        trust_rating -= 5
    if row['is_missing']:
        trust_rating -= 5
    # Additional logic for adjusting trust rating could go here
    return trust_rating
 
# Determine if a response is missing based on the cleaned and translated data
data_clean['is_missing'] = data_clean[['qcheck', 'x01_2', 'x01_3']].isnull().all(axis=1)
data_clean['trust_rating'] = data_clean.apply(assign_trust_rating, axis=1)
 
# Step 7: Filter and display genuine responses
genuine_responses = data_clean[~data_clean['is_outlier'] & ~data_clean['is_missing']]
print(genuine_responses[['idnr', 'qcheck', 'qcheck_sentiment', 'trust_rating']])    
