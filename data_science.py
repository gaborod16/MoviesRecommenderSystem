import pandas as pd
import numpy
from pandas import DataFrame
from datetime import datetime
import os



def import_data():
    data = pd.DataFrame()
    data = pd.read_csv(open("./movies.csv", 'r'), delimiter=';')
    return data

def transform_data(data):
    review_length = []

    for idx in range(1,len(data)):
        review_length.append( len(data.VAL[idx]) )
    data['LENGTH'] = review_length
    return data

def create_simplified_file():
    header = ["MovieID;", "UserID;", "Helpfulness;", "Score;", "Novelty;", "ReviewImpact\n"]
    fw = open('movies.csv', 'w')
    fr = open('movies.txt', 'r')

    fw.writelines(header)
    for i in range(7911684):
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
            fw.write(str(reviewImpact) + ";")
            fw.write("\n")
        except:
            pass
            # print("Bad codec")

    fw.close()
    fr.close()

def main():


if __name__ == "__main__":
	main()