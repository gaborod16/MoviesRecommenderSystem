import pandas as pd
import numpy
from pandas import DataFrame



def import_data():
    data = pd.DataFrame()
    data = pd.read_csv(open("./movies.txt", 'rb'),delimiter=',')
    return data

def transform_data(data):
    review_length = []

    for idx in range(1,len(data)):
        review_length.append( len(data.VAL[idx]) )
    data['LENGTH'] = review_length
    return data

def main():
    data = import_data()


if __name__ == "__main__":
	main()