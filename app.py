from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
import random
import string
import time

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


def generate_sequence(length, element_type):
    if element_type == 'alphabet':
        return [random.choice(string.ascii_uppercase) for _ in range(length)]  
    elif element_type == 'symbols':
        symbols = '!@#$%^&*()_-+=<>?/\\'
        return [random.choice(symbols) for _ in range(length)]  
    elif element_type == 'words':
        return ['apple', 'banana', 'orange', 'grape', 'kiwi'][:length]


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/memory_game/<element_type>/<difficulty>')
def memory_game(element_type, difficulty):
    if difficulty == 'easy':
        sequence_length = 3
    elif difficulty == 'medium':
        sequence_length = 5
    elif difficulty == 'hard':
        sequence_length = 7
    else:
        return redirect(url_for('home'))

    sequence = generate_sequence(sequence_length, element_type)


    session['sequence'] = sequence
    session['current_index'] = 0
    session['start_time'] = time.time()
    session['user_score'] = 0 
    return render_template('memory_game.html', sequence=sequence, element_type=element_type, difficulty=difficulty)


@app.route('/check_sequence', methods=['POST'])
def check_sequence():
    user_input = [digit for digit in request.form.getlist('user_input[]')]
    sequence = session.get('sequence', [])
    difficulty = request.args.get('difficulty', 'unknown')
    element_type = request.args.get('element_type', 'unknown')
    start_time = session.get('start_time', 0)
    user_score = session.get('user_score', 0)

   
    if user_input == sequence:
        end_time = time.time()
        elapsed_time = round(end_time - start_time, 2)
        
       
        user_score += int(1000 / elapsed_time)

        if user_score >= 3000:
            memory_level = 'Low risk of memory disease'
        elif 1500 <= user_score < 3000:
            memory_level = 'Moderate risk of memory disease'
        else:
            memory_level = 'High risk of memory disease'
        
        result = f"Congratulations! You are free from Alzheimer’s disease.!! Time taken: {elapsed_time} seconds. Your score: {user_score}"
    else:
        result = "Sorry, the sequence was not correct. Try again."

 
    session['user_score'] = user_score

    return render_template('result.html', result=result, difficulty=difficulty, element_type=element_type, memory_level=memory_level)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.run(debug=True)
