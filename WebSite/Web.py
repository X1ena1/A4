#Importtting files
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import json

#Importing Json
with open('Ques.json') as file:
    data = json.load(file)

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

#Question route
@app.route("/questions", methods=['GET', 'POST'])
def questions():
    if request.method == 'POST':
        
        selected_answers = request.form.to_dict()

        return redirect(url_for('results', **selected_answers))
    
    return render_template('questions.html', questions=data)

#Result route
@app.route("/results")
def results():
    answers = request.args.get('answers')
    
    if not answers:
        return "No answers provided. Please go back and fill out the form."

    # (Optional) Filter movies based on the selected genre or other answers
    selected_genre = answers.get("What genre are you interested in?")
   
    if selected_genre:
        filtered_movies = movies_df[movies_df['Genre'].str.contains(selected_genre, case=False, na=False)]
    else:
        filtered_movies = movies_df

    top_movies = filtered_movies.head(5)
    # Display the filtered movies
    return render_template('results.html', movies=top_movies)

#Running application
if __name__ == "__main__":
    app.run(debug=True)