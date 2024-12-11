#Importtting files
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import json

#reading the CSV file
movies_df = pd.read_csv('IMDB-Movie-Data.csv')

app = Flask(__name__)

# Load the questions from the JSON file
with open('Ques.json') as file:
    data = json.load(file)

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

        print("Selected answers:", selected_answers)  # Debugging line

        if selected_answers:
            query_string = '&'.join([f"{key}={value}" for key, value in selected_answers.items()])
            return redirect(f"{url_for('results')}?{query_string}")
    
        else:
            return "No answers provided. Please fill out the form."

    return render_template('questions.html', questions=data)

#Result route
@app.route("/results")
def results():

    # (Optional) Filter movies based on the selected genre or other answers
    selected_genre = request.args.get("What genre are you interested in?")

    print("Selected genre:", selected_genre)

    if not selected_genre:
        return "No answers provided."

    filtered_movies = filtered_movies[filtered_movies['Genre'].str.contains(selected_genre, case=False, na=False)]

    filtered_movies = movies_df
    top_movies = filtered_movies.head(5)

    return render_template('results.html', movies=top_movies)

#Running application
if __name__ == "__main__":
    app.run(debug=True)