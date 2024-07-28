import pickle
import difflib
import pandas as pd
from flask import Flask,render_template,request

with open("feature.pkl",'rb')as file:
  feature=pickle.load(file)
  
with open("similarity.pkl",'rb')as file:
  similarity=pickle.load(file)
  
df=pd.read_csv("movies.csv")
list_of_all_titles=df['title'].tolist()
  
app=Flask(__name__)

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
    if(i<4):
        suggested.append(title_of_movie)
        i+=1
  return render_template('index.html',arr=suggested)

if __name__=='__main__':
  app.run(debug=True)