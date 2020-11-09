import requests
import pandas as pd
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
load_dotenv()

RAPIDAPI_KEY = os.getenv('RA_API_KEY')
API_DEEZ_KEY = os.getenv('API_DEEZ_KEY')

def get_artist_titles(artist):
    '''
    Esta función recibe como parámetro el artista y realiza una llamada a la API para obtener una lista de las canciones
    que existen en Deezer de dicho artista.
    '''
    url = "https://deezerdevs-deezer.p.rapidapi.com/search"
    querystring = {"q":f"{artist}"}
    headers = {
        'x-rapidapi-key': RAPIDAPI_KEY,
        'x-rapidapi-host': "deezerdevs-deezer.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    json = response.json()
    songs_list = json["data"]
    titles = [ song['title'] for song in songs_list ]
    return titles

def titles_in_dataset(artist, titles, start_year, end_year):
    '''
    Esta función recibe como parámetros el artista, la lista de canciones obtenida en la función anterior y
    como parámetros opcionales, un rango de fechas. Comprueba que la lista de canciones obtenidas de la API se encuentren
    en el dataset, y te imprime o el total de canciones o las existentes del rango de tiempo señalado y te imprime en la terminal
    la lista con la duración de cada canción al lado. Además, pide como input un 'yes' o un 'no' de modo que, si se le indica que sí,
    te devuelve un histograma que muestra el comportamiento de la lista de canciones en conjunto respecto a las propiedades de las canciones.
    '''
    data = pd.read_csv('./output/clean_data.csv')
    data["duration_minutes"] = data["duration_ms"] / 60000
    data_titles = data[data['name'].isin(titles)]

    if start_year and end_year:
        data_titles = data_titles[(data_titles['year'] >= int(start_year)) & (data_titles['year'] >= int(end_year))]
    
    should_show_histplot = input("\nWould you like to see the histplot of the track list properties? (danceability, energy...)(y/N)")
    if should_show_histplot[0] == 'y' or should_show_histplot[0] == 'Y':
        data_titles.hist(figsize=(20, 20))
        plt.show()

    print(f"\n\n-----\t{artist}'s titles\t-----\n\n")
    for index, row in data_titles.iterrows():
        print("\tTitle: " + row["name"] + " " + " Duration" + " " + str(row["duration_minutes"]))
    
    print("\n")

def top_charts(category):
    '''
    Esta función recibe como parámetro una categoría, o 'tracks' o 'albums' y realiza una llamada a la API de Deezer
    de modo que, en función del parámetro que se le pase, devuelve una lista del top chart de dicha categoría.
    '''
    url = f"https://api.deezer.com/chart/0/{category}"
    headers = {'x-rapidapi-key': API_DEEZ_KEY,
           'x-rapidapi-host': "https://developers.deezer.com"
    }
    response = requests.request("GET", url, headers=headers)
    json = response.json()
    top_category = []
    top_list = json["data"]
    print(f"\n\n-----\tTop Charts by {category}\t-----\n\n")
    for name in top_list:
        title = name["title"]
        if category == "tracks":
            top_category.append(title)
            print(f"\tTrack title: {title}")
        elif category == "albums":
            top_category.append(name["artist"])
            artist_name = name["artist"]["name"]
            print(f"\tAlbum name: {title} by {artist_name}")
    print("\n")

    return top_category
   