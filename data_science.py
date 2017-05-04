import pandas as pd
import numpy
from pandas import DataFrame
from datetime import datetime
import pickle
import math

def test_func():
    return "test succedeed!"

def import_data():
    data = pd.DataFrame()
    data = pd.read_csv(open("./movies.csv", 'r'), delimiter=';')
    return data

def create_users_and_movies_files(data):
    users = {}
    movies = {}
    movies_rate = {}
    max_year = data.Novelty.max()
    data.Novelty = data.Novelty.apply(lambda x: max_year - x + 1)
    data.ReviewImpact = data.ReviewImpact.apply(lambda x: x / 50)

    counter = 0
    total = len(data)

    for tup in data.itertuples():
        if tup.UserID not in users:
            users[tup.UserID] = []
        if tup.MovieID not in movies:
            movies[tup.MovieID] = []
            movies_rate[tup.MovieID] = (0,0)

        users[tup.UserID].append(tup.MovieID)
        movies[tup.MovieID].append(tup.UserID)
        movies_rate[tup.MovieID] = ( movies_rate[tup.MovieID][0] + 1, movies_rate[tup.MovieID][1] + ((tup.Score * tup.Helpfulness) / (tup.Novelty * 2)) + tup.ReviewImpact )

        if counter % (math.floor(total/100)) == 0:
            print(str(round((counter+1)*100/total)) + "%")
        counter = counter + 1

    rates = {}
    for mrate in movies_rate:
        rates[mrate] = movies_rate[mrate][1] / movies_rate[mrate][0]

    with open('movies_users.txt', 'wb') as handle:
        pickle.dump(movies, handle)

    with open('movies_rate.txt', 'wb') as handle:
        pickle.dump(rates, handle)

    sort_func = get_movie_rating(rates)
    for u in users:
        users[u] = sorted(users[u], key=sort_func, reverse=True)

    with open('users.txt', 'wb') as handle:
        pickle.dump(users, handle)

def get_recommendations(userID):
    with open('users.txt', 'rb') as handle:
        users = pickle.loads(handle.read())

    with open('movies_users.txt', 'rb') as handle:
        movies = pickle.loads(handle.read())

    with open('movies_rate.txt', 'rb') as handle:
        movies_rate = pickle.loads(handle.read())

    recommended_movies = []
    reviewed_movies = users[userID]

    for m in reviewed_movies[1:6]: # Bests 5
        reviewed_by = movies[m]
        for u in reviewed_by:
            others_reviews = users[u]
            for rm in others_reviews[1:6]: # Bests 5
                if rm not in reviewed_movies and rm not in recommended_movies:
                    recommended_movies.append(rm)

    sort_func = get_movie_rating(movies_rate)
    recommended_movies = sorted(recommended_movies, key=sort_func, reverse=True)
    return recommended_movies[1:11]

def get_movie_rating(movies_rate):
    def get_movie_rating_(movie):
        return movies_rate[movie]
    return get_movie_rating_

def get_top_50():
    with open('movies_rate.txt', 'rb') as handle:
        movies_rate = pickle.loads(handle.read())

    sort_func = get_movie_rating(movies_rate)
    moviesID = [m for m in movies_rate]
    moviesID = sorted(moviesID, key=sort_func, reverse=True)
    return moviesID[1:51]

def create_simplified_file():
    header = ["MovieID;", "UserID;", "Helpfulness;", "Score;", "Novelty;", "ReviewImpact\n"]
    fw = open('movies.csv', 'w')
    fr = open('movies.txt', 'r')
    total = 7911684

    fw.writelines(header)
    for i in range(total):
        try: 
            # productID
            raw_line = fr.readline()
            prodID = raw_line.split(": ")[1].replace("\n", "")
            # print(raw_line + ' - ' + prodID)

            # userID
            raw_line = fr.readline()
            userID = raw_line.split(": ")[1].replace("\n", "")
            # print(raw_line + ' - ' + userID)

            # profileName (SKIPPED)
            next(fr)

            # helpfulness
            raw_line = fr.readline()
            values = list(map(lambda x: int(x), raw_line.split(": ")[1].replace("\n", "").split("/")))
            helpfulness = (values[0] + values[1]) / ((values[1]/2) - (values[0]/2) + 1) # x+y / ( (y/2) - (x/2) + 1 )
            # print(raw_line + ' - ' + str( helpfulness ))

            # score
            raw_line = fr.readline()
            score = raw_line.split(": ")[1].replace("\n", "")
            # print(raw_line + ' - ' + str( score ))

            # time
            raw_line = fr.readline()
            year = datetime.fromtimestamp(int(raw_line.split(": ")[1].replace("\n", ""))).strftime('%Y')
            # print(raw_line + ' - ' + year )

            # summary (SKIPPED)
            next(fr)

            # text (SKIPPED because of problems with encoding)
            raw_line = fr.readline()
            text = raw_line.split(": ", 1)[1].replace("\n", "")
            reviewImpact = len(text) # lexical diversity would be more interesting
            # print(raw_line + ' - ' + str( reviewImpact ))

            # write in new file
            next(fr)
            fw.write(prodID + ";")
            fw.write(userID + ";")
            fw.write(str(helpfulness) + ";")
            fw.write(str(score) + ";")
            fw.write(str(year) + ";")
            fw.write(str(reviewImpact))
            fw.write("\n")
        except:
            pass
            # print("Bad codec")
        if i % (math.floor(total/100)) == 0:
            print(str(round((i+1)*100/total)) + "%")

    fw.close()
    fr.close()

def main():
    create_simplified_file()
    print("created")
    data = import_data ()
    print("imported")
    create_users_and_movies_files(data)
    print(get_recommendations('A141HP4LYPWMSR'))
    print(get_top_50())
    print("Done!")


if __name__ == "__main__":
	main()