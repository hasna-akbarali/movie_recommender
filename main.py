import streamlit as st
import pandas as pd
import pickle
import requests

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=17775602ce89ef3eb9b372a895065fa7&language=en-US#"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxNzc3NTYwMmNlODllZjNlYjliMzcyYTg5NTA2NWZhNyIsInN1YiI6IjY0YWE0ZTM2YjY4NmI5MDEyZjg2ZTMxNCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.t3KdkhaOA15FvzfdvhnSwVJK2iTaHV9bmnv4K6PIrpo"
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    return 'https://image.tmdb.org/t/p/original/' + data['poster_path']

def recommend(movie):

    mov_index = movies[movies['title'] == movie].index[0]
    distances = similarity[mov_index]
    movies_list = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:6]

    recommend_movies = []
    recommend_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        # Fetch Poster with help of movie_id
        recommend_movies_posters.append(fetch_poster(movie_id))
        recommend_movies.append(movies.iloc[i[0]].title)
    return (recommend_movies,recommend_movies_posters)


st.title('Movie Recommender System')

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movies = pd.DataFrame(movies_dict)

selected_movie_name = st.selectbox('What movie would you like to watch?', movies['title'].values)

if st.button('Recommend'):
    header,image = recommend(selected_movie_name)
    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
            st.text(header[0])
            st.image(image[0])

    with col2:
            st.text(header[1])
            st.image(image[1])

    with col3:
            st.text(header[2])
            st.image(image[2])

    with col4:
            st.text(header[3])
            st.image(image[3])

    with col5:
            st.text(header[4])
            st.image(image[4])

