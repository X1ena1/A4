#Importtting files
from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import json

#reading the CSV file
movies_df = pd.read_csv('IMDB-Movie-Data.csv')

app = Flask(__name__)
app.secret_key = 'your_secret_key'

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
    question_index = session.get('question_index', 0)

    questions = list(data.items())

    if question_index >= len(questions):
        return redirect(url_for('results'))

    question_text, options = questions[question_index]

    if request.method == 'POST':

        selected_answer = request.form.get(question_text)
        print(f"Selected answer for {question_text}: {selected_answer}")

        # Store the answer in session
        session[question_text] = selected_answer

        # Move to the next question
        question_index += 1

        # If there are more questions, update the session and redirect to the next question
        if question_index < len(questions):
            session['question_index'] = question_index
            return redirect(url_for('questions'))
        else:
            # If no more questions, redirect to the results page
            return redirect(url_for('results'))

    return render_template('questions.html', question=question_text, options=options)

#Result route
@app.route("/results")
def results():
    selected_answers = {question: session.get(question) for question in data.keys()}

    print("Selected answers:", selected_answers) #debuggin line

    filtered_movies = movies_df.copy()

    #Genre Option
    selected_genre = selected_answers.get("What genre where you interested in?")
    if selected_genre:
        selected_genre = selected_genre.lower().strip()

        filtered_movies = movies_df[movies_df['Genre']
                                    .str.lower()
                                    .str.split(',')
                                    .apply(lambda genres: selected_genre in [genre.strip().lower() for genre in genres])]
    
    #Family Option
    family_option = selected_answers.get("Would you prefer family-friendly?")
    if family_option:
        if family_option.lower() == "yes":
        # Filter the movies that contain "family" in their genre
            filtered_movies = filtered_movies[filtered_movies['Genre']
                                          .str.contains("family", case=False, na=False)]
    
        elif family_option.lower() == "no":
            # If "No" is selected, we simply don't filter by family-friendly content
            print("Family-friendly filter: No. Skipping family filter.")

    top_movies = filtered_movies.head(10)

    session['question_index'] = 0

    return render_template('results.html', movies=top_movies)

#Running application
if __name__ == "__main__":
    app.run(debug=True)