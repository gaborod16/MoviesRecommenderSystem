# MoviesRecommenderSystem
Recommender System for movies, based on reviews and adapted to each user.

## Setup:

1. For running this project you will need Python install the dependancies first:

	```
	pip install -r requirements.txt
	```

	After installing flask, open the command line (or Anaconda) and go to the folder where the project is stored.

2. To created the support files (download and uncompress the `movies.txt.gz` from the implementation notes link), execute the script for that purpose.

	```
	python data_science.py
	```

3. After its conclusion, run:

	```
	python app.py
	```

	The server will start.

	Open your browser and go to: http://localhost:5000/

	By this moment, the Movies Recommender System should be already running. 
	
	Type `A1RSDE90N6RSZF` as a demo `UserID`.

## Notes of the implementation:

The dataset used is the following: http://snap.stanford.edu/data/web-Movies.html

The big ammount of data was understimated and the creation of the support files takes a longer than expected.

However, once the support files are created, the recommendations are speeded up. This also means that in order to get the recommendations you need the support files.

The visuals of the web page weren't taken care of since they are not the main purpose of the work.

Enjoy!

@Gabriel Amarista Rodrigues.
