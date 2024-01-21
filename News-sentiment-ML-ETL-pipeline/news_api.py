import requests
import json
import pandas as pd
import numpy as np
from textblob import TextBlob
from sqlalchemy import create_engine

def news_fetch(topic):
  url = "https://newsapi.org/v2/everything?q={topic1}&from=2024-01-01&sortBy=popularity&apiKey=389ed82f1909424185318432a6a03c66".format(topic1 = topic)
  response = requests.get(url)
  response.ok # for status code less than 400 it returns true
  response_json = response.json()
  response_data = response_json['articles']
  with open("articles.json", "w") as outfile:
    json.dump(response_data, outfile)
  extracted_df = pd.read_json('articles.json')
  extracted_df.drop(['source', 'author', 'urlToImage'], axis=1)
  tittle_extracted = extracted_df['title']
  content_extracted = extracted_df['content']
  # print(len(tittle_extracted)) -- all the new tittle were less than 200 as len of this and tittle_for_analysis are same
  data_for_analysis = []
  for i in tittle_extracted:
      data_for_analysis.append(i)
  j = 0
  for i in content_extracted:
      curr_len = len(data_for_analysis[j])
      rem_len = 200 - curr_len

      data_for_analysis[j] = data_for_analysis[j] + " - " + i[:rem_len - 3]
      j += 1
  newDf = pd.DataFrame(data_for_analysis, columns = ['Content'])
  newDf = newDf.drop(newDf[newDf['Content'] == '[Removed] - [Removed]'].index) # preprocessing the data
  newDf['Date'] = extracted_df['publishedAt']
  newDf['Date'] = newDf['Date'].apply(lambda x : x[:10])
  newDf['url'] = extracted_df['url']
  sentiment_analysis(newDf)
  newDf = newDf.drop(['Subjectivity', 'Polarity'], axis=1)
  # host="mysql"
  # user="root"
  # password="root"
  # database="sentiment_analysis"
  # port=3306
  def get_connection():
    return create_engine(
      # url="mysql+mysqlconnector://root:@localhost/sentiment_analysis"
      url="mysql+mysqlconnector://root:root@mysql/sentiment_analysis"
    )

  engine = get_connection()
  # engine = create_engine("mysql+mysqlconnector://root:root@localhost:3306/sentiment_analysis")
  newDf.drop_duplicates()
  newDf.to_sql('sentiments', con=engine, if_exists='replace', index=False)
  newDf[newDf['Date'] == '2024-01-07']

def sentiment_analysis(tweet):
 def getSubjectivity(text):
   return TextBlob(text).sentiment.subjectivity
  
 #Create a function to get the polarity
 def getPolarity(text):
   return TextBlob(text).sentiment.polarity
  
 #Create two new columns 'Subjectivity' & 'Polarity'
 tweet['Subjectivity'] = tweet['Content'].apply(getSubjectivity)
 tweet ['Polarity'] = tweet['Content'].apply(getPolarity)
 def getAnalysis(score):
  if score < 0:
    return 'Negative'
  elif score == 0:
    return 'Neutral'
  else:
    return 'Positive'
 tweet ['Analysis'] = tweet['Polarity'].apply(getAnalysis )
 return tweet
