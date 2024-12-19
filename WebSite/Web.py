#Importtting files
from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import json
from datetime import datetime

app = Flask(__name__)
movies_df = pd.read_csv('IMDB-Movie-Data.csv')

app.secret_key = 'your_secret_key'

with open('Ques.json') as file:
    data = json.load(file)

#Home route
@app.route("/")
def index():
    return render_template('index.html')

#Info route
@app.route("/info", methods=['GET', 'POST'])
def info():
    if request.method == 'POST':
        name = request.form.get('name')
        if not name:
            return render_template('info.html', error="Please provide your name.")

        session['name'] = name
        return redirect(url_for('questions'))
    
    return render_template('info.html')

#Question route
@app.route("/questions", methods=['GET', 'POST'])
def questions():
    if 'name' not in session:
        return redirect(url_for('info'))

    question_index = session.get('question_index', 0)
    questions = list(data.items())

    if question_index >= len(questions):
        return redirect(url_for('results'))

    question_text, options = questions[question_index]

    if request.method == 'POST':
        selected_answer = request.form.get(question_text)
        print(f"Selected answer for {question_text}: {selected_answer}")  #Debugging line

        # Store the answer in session
        session[question_text] = selected_answer

        question_index += 1
        session['question_index'] = question_index

        # If there are more questions, update the session and redirect to the next question
        if question_index < len(questions):
            return redirect(url_for('questions'))
        else:
            return redirect(url_for('almost_route'))

    return render_template('questions.html', question=question_text, options=options)

@app.route("/almost", endpoint="almost_route")
def almost():
    return render_template('almost.html')  #AI helped me include an endpoint such as loading screen

#Result route
@app.route("/results")
def results():
    selected_answers = {question: session.get(question) for question in data.keys()}
    filtered_movies = movies_df.copy()

    current_year = datetime.now().year
    min_year = 2000

    #AI helped develop define my variables
    filtered_movies['Year'] = pd.to_numeric(filtered_movies['Year'], errors='coerce')
    filtered_movies = filtered_movies.dropna(subset=['Year'])

    for filter, selected_value in selected_answers.items():
        if not selected_value or selected_value == "None":
            continue
        
        print(f"Processing filter: {filter} with selected value: {selected_value}") #Debugging line

        # Genre filter
        if filter == "What genre where you interested in?":
            filtered_movies = filtered_movies[filtered_movies['Genre'].str.contains(selected_value, case=False, na=False)]

        # Emotion filter (Assuming stored in Genre for simplicity, adjust if needed)
        elif filter == "Where you feeling for a certain emotion?":
            filtered_movies = filtered_movies[filtered_movies['Genre'].str.contains(selected_value, case=False, na=False)]

            # Family filter
        elif filter == "Would you prefer family-friendly?" and selected_value.lower() == "yes":
            filtered_movies = filtered_movies[filtered_movies['Genre'].str.contains("family", case=False, na=False)]

            # Rating filter
        elif filter == "What kind of rating would you prefer?":
            if selected_value == "1 - 5":
                filtered_movies = filtered_movies[(filtered_movies['Rating'] >= 1) & (filtered_movies['Rating'] <= 5)]
            elif selected_value == "6 - 10":
                filtered_movies = filtered_movies[(filtered_movies['Rating'] >= 6) & (filtered_movies['Rating'] <= 10)]

        #Year filter
        elif filter == "How old would you prefer the movie?":
            if selected_value == "1 - 5 years":
                filtered_movies = filtered_movies[(filtered_movies['Year'] >= (current_year - 5))]
            elif selected_value == "5 - 10 years":
                filtered_movies = filtered_movies[(filtered_movies['Year'] >= (current_year - 10)) & (filtered_movies['Year'] < (current_year - 5))]
            elif selected_value == "10 - 20 years":
                filtered_movies = filtered_movies[(filtered_movies['Year'] >= (current_year - 20)) & (filtered_movies['Year'] < (current_year - 10))]
        
        #Runtime filter
        elif filter == "What run time where you thinking (minutes)?":
            if selected_value == "Less than 90":
                filtered_movies = filtered_movies[filtered_movies['Runtime (Minutes)'] < 90]
            elif selected_value == "90 - 120":
                filtered_movies = filtered_movies[(filtered_movies['Runtime (Minutes)'] >= 90) & (filtered_movies['Runtime (Minutes)'] <= 120)]
            elif selected_value == "120 or more":
                filtered_movies = filtered_movies[filtered_movies['Runtime (Minutes)'] > 120]

    filtered_movies = filtered_movies.dropna(subset=['Year'])

    #If no options selected it'll show the first movies in the database
    if filtered_movies.empty:
        top_movies = []
    else:
        top_movies = filtered_movies.head(10).to_dict(orient='records')

    session['question_index'] = 0

    return render_template('results.html', movies=top_movies)

#Running application
if __name__ == "__main__":
    app.run(debug=True)