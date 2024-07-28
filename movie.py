import pickle
import difflib
import pandas as pd
from flask import Flask,render_template,request
import requests

with open("feature.pkl",'rb')as file:
  feature=pickle.load(file)
  
with open("similarity.pkl",'rb')as file:
  similarity=pickle.load(file)
  
df=pd.read_csv("movies.csv")
list_of_all_titles=df['title'].tolist()
  
app=Flask(__name__)

API_KEY = '33f08421b12d0c05d8db4e64558efed4'
BASE_URL = 'https://api.themoviedb.org/3'
IMG_BASE_URL = 'https://image.tmdb.org/t/p/w500'

def get_movie_poster(movie_title):
    search_url = f"{BASE_URL}/search/movie"
    params = {
        'api_key': API_KEY,
        'query': movie_title
    }
    response = requests.get(search_url, params=params)
    data = response.json()
    if data['results']:
        poster_path = data['results'][0]['poster_path']
        return f"{IMG_BASE_URL}{poster_path}"
    return None

@app.route('/')
def welcome():
  return render_template("index.html")

@app.route('/recommend',methods=['POST'])
def recommend():
  movie_name=request.form['movie']
  find_closest_match=difflib.get_close_matches(movie_name,list_of_all_titles)

  closest_match=find_closest_match[0]


  index_of_the_movie=df[df.title==closest_match]['index'].values[0]


  similarity_score=list(enumerate(similarity[index_of_the_movie]))
  sorted_similarity_movies=sorted(similarity_score, key = lambda x:x[1],reverse=True)

  suggested=[]
  i=1
  for movie in sorted_similarity_movies:
    index=movie[0]
    title_of_movie=df[df.index==index]['title'].values[0]
    if(i<5):
        suggested.append(title_of_movie)
        i+=1
  poster_urls=[]
  for title in suggested:
    poster_url=get_movie_poster(title)
    poster_urls.append(poster_url)
        
  return render_template('index.html',poster_urls=poster_urls)

if __name__=='__main__':
  app.run(debug=True)