from flask import Flask , request, render_template
import pickle
import requests
import pandas as pd
from PIL import Image

# movies = pickle.load(open('model/movie_dict.pkl'),'rb')
movies_ = pickle.load(open('model/movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_)
similarity = pickle.load(open('model/similarity.pkl','rb'))

app = Flask(__name__)


@app.route("/")
def home():

    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=6a73943258b9b3c51e1556d0c08f8864&language=en-US'.format(
            movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    index= movies[movies['title']==movie].index[0]
    distances=sorted(list(enumerate(similarity[index])),reverse=True,key=lambda x:x[1])
    recommended_movies_name=[]
    recommended_movies_poster = []
    for i in distances[1:9]:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movies_poster.append(fetch_poster(movie_id))
        recommended_movies_name.append(movies.iloc[i[0]].title)

    return    recommended_movies_name , recommended_movies_poster




@app.route("/recommendation",methods=['GET','POST'])
def recommendation():
    movie_list=movies['title'].values
    status=False
    if request.method == 'POST':
        try:
            if request.form:
                movies_name=request.form['movies']
                # print movies name
                recommended_movies_name , recommended_movies_poster =recommend(movies_name)
                status=True

                return render_template("prediction.html",movies_name=recommended_movies_name,poster=recommended_movies_poster,movie_list=movie_list,status=status)



        except Exception as e:
            error={'error':e}
            return render_template("prediction.html",error=error,movie_list=movie_list,status=status)

    else:
        return render_template("prediction.html",movie_list=movie_list,status=status)








# for the home  page

# def fetch_poster_firstPage():
#     response = requests.get(
#         'https://api.themoviedb.org/3/movie/popular?api_key=6a73943258b9b3c51e1556d0c08f8864&language=en-US&page=1'.format())
#     data = response.json()
#     return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
#
#
# def new_released_movie():
#     #new_movies_name=[]
#     new_movies_poster = []
#     for i in range(2):
#           new_movies_poster.append(fetch_poster())
#     return   new_movies_poster

# @app.route("/newpage",methods=['GET','POST'])
# def newpage():
#     movie_list=movies['title'].values
#     status=False
#     if request.method == 'POST':
#         try:
#             if request.form:
#                 movies_name=request.form['movies']
#                 # print movies name
#                 recommended_movies_name , recommended_movies_poster =recommend(movies_name)
#                 status=True
#
#                 return render_template("newpage.html",movies_name=recommended_movies_name,poster=recommended_movies_poster,movie_list=movie_list,status=status)
#
#
#
#         except Exception as e:
#             error={'error':e}
#             return render_template("newpage.html",error=error,movie_list=movie_list,status=status)
#
#     else:
#         return render_template("newpage.html",movie_list=movie_list,status=status)
#


if __name__=='__main__':
    app.debug=True
    app.run()
