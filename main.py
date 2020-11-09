import src.API_calls as t
import argparse

def input_year(year):
    if year:
        year = int(year)
        correct_year = list(range(1921,2021,1))
        if year in correct_year:
            return year
        else:
            error = 'Por favor, introduce un año entre 1921 y 2020'
            raise argparse.ArgumentTypeError(error)

def input_category(category):
    if category:
        category = category.lower()
        correct_category = ["tracks", "albums"]
        if category in correct_category:
            return category
        else:
            error = 'Por favor, elige e introduce una categoría entre las dos siguientes: "tracks" o "albums"'
            raise argparse.ArgumentTypeError(error)

def parse():
    parser = argparse.ArgumentParser(description='Introduces el nombre de un artista o una categoría y te saca una lista de canciones o el top chart de la categoría elegida.')
    parser.add_argument('-a', dest='artist', default="", help='el artista del que quieras obtener la información')
    parser.add_argument('-s', dest='start_year', default="", help='el año a partir del que se quieren filtrar las canciones del artista', type=input_year)
    parser.add_argument('-e', dest='end_year', default="", help='el año hasta el cual se quieren filtrar las canciones del artista', type=input_year)
    parser.add_argument('-c', dest='category', default="", help='la categoría de la que quieres obtener el top charts', type=input_category)
    args = parser.parse_args()
    return args
    
def main():
    args = parse()
    artist = args.artist
    start_year = args.start_year
    end_year = args.end_year
    category = args.category
    if artist:
        t.titles_in_dataset(artist, t.get_artist_titles(artist), start_year, end_year)

    if category:
        t.top_charts(category)
                        
if __name__ == "__main__":
        main()
