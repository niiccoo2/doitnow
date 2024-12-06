import pandas as pd
from nltk.corpus import stopwords
import string
from nltk.stem import WordNetLemmatizer

lemma = WordNetLemmatizer()
filename='Fai Adesso Novembre (Responses) - Form Responses 1.csv'


pd.read_csv(filename, encoding='utf-8')
df = pd.read_csv(filename)

df.columns = ['post_id', 'post_title', 'subreddit']
df['post_title'] = df['post_title'].str.lower().str.replace(r'[^\w\s]+', '').str.split()


stop = stopwords.words('english')

df['post_title'] = df['post_title'].apply(lambda x: [item for item in x if item not in stop])

df['post_title']= df['post_title'].apply(lambda x : [lemma.lemmatize(y) for y in x])


df.to_csv('fixed.csv', encoding='utf-8')