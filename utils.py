import sqlite3
from collections import Counter


class DbConnect:
    def __init__(self, path):
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()

    def __del__(self):
        self.cur.close()
        self.con.close()


def execute_quere(quere):
    with sqlite3.connect('netflix.db') as con:
        cur = con.cursor()
        cur.execute(quere)
        result = cur.fetchall()
    return result


def movie_by_title(title):
    db_connect = DbConnect('netflix.db')
    db_connect.cur.execute(
        f"""SELECT title, country, release_year, listed_in, description 
        from netflix
        where title like '%{title}%'
        order by release_year desc
        limit 1""")
    result = db_connect.cur.fetchone()
    return {
        "title": result[0],
        "country": result[1],
        "release_year": result[2],
        "genre": result[3],
        "description": result[4]
    }


def movies_by_years(year1, year2):
    db_connect = DbConnect('netflix.db')
    query = f"select title, release_year from netflix where release_year between {year1} and {year2} limit 100;"
    db_connect.cur.execute(query)
    result = db_connect.cur.fetchall()
    result_list = []
    for movie in result:
        result_list.append({"title": movie[0],
                            "release_year": movie[1]})
    return result_list


def movies_by_rating(rating):
    # db_connect = DbConnect('netflix.db')
    rating_parameters = {
        "children": "'G'",
        "family": "'G', 'PG', 'PG-13'",
        "adult": "'R', 'NC-17'"
    }
    if rating not in rating_parameters:
        return "Переданной группы не существует"
    query = f"select title, rating, description from netflix where rating in ({rating_parameters[rating]})"
    result = execute_quere(query)
    # db_connect.cur.execute(query)
    # result = db_connect.cur.fetchall()
    result_list = []

    for movie in result:
        result_list.append({
            "title": movie[0],
            "rating": movie[1],
            "description": movie[2]})
    return result_list


def movies_by_genre(genre):
    result = execute_quere(f"""select title, description 
    from netflix where listed_in like '%{genre}%' 
    order by release_year desc limit 10;""")
    result_list = []
    for movie in result:
        result_list.append({
            "title": movie[0],
            "description": movie[1]
        })
    return result


def cast_parameters(actor1, actor2):
    quere = f"select `cast` from netflix where `cast` like '%{actor1}%' and `cast` like '%{actor2}%';"
    result = execute_quere(quere)
    actors_list = []
    for cast in result:
        actors_list.extend(cast[0].split(', '))
    counter = Counter(actors_list)
    print(counter)
    result_list = []
    for actor, count in counter.items():
        if actor not in [actor1, actor2] and count >= 2:
            result_list.append(actor)
    return result_list

print(cast_parameters('Jack Black', 'Dustin Hoffman'))

def search_movie_by_param(movie_type, release_year, genre):
    quere = f"""select title, description
    from netflix
    where type = {movie_type}
    and release_year = {release_year}
    and listed_in like '%{genre}%'"""
    result = execute_quere(quere)
    result_list = []
    for movie in result:
        result_list.append({'title': movie[0], 'description': movie[1]})
    return result_list

