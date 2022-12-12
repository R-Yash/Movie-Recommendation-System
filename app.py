import streamlit as st
import pickle
import pandas as pd
import requests


def fetchPoster(id):
    response = requests.get(
        "https://api.themoviedb.org/3/movie/{}?api_key=bb9591de0e67241ed7d4b7db9aa0c641".format(id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie, number):
    movieIndex = moviesDf[moviesDf['title'] == movie].index[0]
    distances = sim[movieIndex]
    moviesList = sorted(list(enumerate(distances)),
                        reverse=True, key=lambda x: x[1])[1:number+1]
    recommendMovies = []
    moviePosters = []
    for i in moviesList:
        recommendMovies.append(moviesDf.iloc[i[0]].title)
        moviePosters.append(fetchPoster(moviesDf.iloc[i[0]].id))
    return recommendMovies, moviePosters


moviesDf = pickle.load(open("movies.pkl", "rb"))
moviesList = moviesDf['title'].values

sim = pickle.load(open("similarityMatrix.pkl", "rb"))

st.title("Movie Recommendation System")
option = st.selectbox("What movie do you like?", moviesList)


if st.button("Recommend"):
    st.write("Here are some movies just like " + option)
    recommendations, moviePosters = recommend(option, 5)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommendations[0])
        st.image(moviePosters[0])
    with col2:
        st.text(recommendations[1])
        st.image(moviePosters[1])

    with col3:
        st.text(recommendations[2])
        st.image(moviePosters[2])
    with col4:
        st.text(recommendations[3])
        st.image(moviePosters[3])
    with col5:
        st.text(recommendations[4])
        st.image(moviePosters[4])
