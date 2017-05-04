from flask import Flask, render_template
from flask import request, json
import Pandas as pd
import numpy
from data_science import get_recommendations, get_top_50, test_func

app = Flask(__name__)

@app.route('/',methods=['POST'])
def recommend():
 
    # read the posted values from the UI
    _userid = request.form['UserID']
    print(_userid)
 
    # validate the received values
    if _userid:
    	return render_template('index.html', recommendations=get_recommendations(_userid))
        #return json.dumps({'html':'<span>All fields good !!</span>'})
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})

@app.route("/")
def main():
	return render_template('index.html')

if __name__ == "__main__":
	app.run()