#Importtting files
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

#reading the CSV file
movies_df = pd.read_csv('IMDB-Movie-Data.csv')

app = Flask(__name__)

#Home route
@app.route("/")
def index():
    return render_template('index.html')

#Info route
@app.route("/info")
def info():
    return render_template('info.html')

#Result route
@app.route("/results")
def results():

    #Reads top movies
    movies = movies_df.head()

    print(movies.head())

    return render_template('results.html', movies=movies)

#Running application
if __name__ == "__main__":
    app.run(debug=True)