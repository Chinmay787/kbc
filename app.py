from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a real secret key for session security

DATABASE = 'quiz.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def get_questions():
    conn = get_db_connection()
    questions = conn.execute('SELECT * FROM questions').fetchall()
    conn.close()
    return questions

def save_response(question_id, answer):
    conn = get_db_connection()
    conn.execute('INSERT INTO responses (question_id, answer) VALUES (?, ?)', (question_id, answer))
    conn.commit()
    conn.close()

def get_correct_answers():
    # Mock function to return correct answers
    conn = get_db_connection()
    correct_answers = conn.execute('SELECT id, correct_answer FROM questions').fetchall()
    conn.close()
    return {row['id']: row['correct_answer'] for row in correct_answers}

@app.route('/')
def index():
    """Initialize the quiz session and redirect to the first question."""
    session.clear()
    session['index'] = 0
    session['answers'] = {}
    return redirect(url_for('question'))

@app.route('/question', methods=['GET', 'POST'])
def question():
    """Display the current question and handle form submissions."""
    questions = get_questions()
    index = session.get('index', 0)
    answers = session.get('answers', {})

    if request.method == 'POST':
        selected_option = request.form.get('option')
        if selected_option:
            question_id = str(questions[index]['id'])  # Ensure the key is a string
            answers[question_id] = selected_option
            session['answers'] = answers
            print(f"Selected Option: {selected_option} for Question ID: {question_id}")

        if 'next' in request.form:
            index += 1
        elif 'prev' in request.form:
            index -= 1
        elif 'submit' in request.form:
            # Print session data for debugging
            print("Session Answers Before Submission:", session['answers'])
            try:
                for qid, ans in answers.items():
                    qid = int(qid)  # Convert to integer
                    if ans:  # Ensure answer is not empty
                        print(f"Saving Response: Question ID={qid}, Answer={ans}")  # Debug print
                        save_response(qid, ans)
                    else:
                        print(f"No response selected for Question ID: {qid}")
            except ValueError as e:
                print(f"Error converting ID to integer: {e}")
            return redirect(url_for('submit'))

        # Validate index to ensure it is within range
        index = max(0, min(index, len(questions) - 1))
        session['index'] = index
        print(f"Index updated to: {index}")

    if 0 <= index < len(questions):
        question_data = {
            'question': questions[index]['question_text'],
            'option1': questions[index]['option1'],
            'option2': questions[index]['option2'],
            'option3': questions[index]['option3'],
            'option4': questions[index]['option4']
        }
        selected_option = answers.get(str(questions[index]['id']))  # Ensure the key is a string
        print(f"Displaying question ID: {questions[index]['id']}, Selected Option: {selected_option}")
        return render_template('Index.html', question=question_data, index=index, total=len(questions), selected_option=selected_option)
    else:
        print("Question not found or index out of range.")
        return "Question not found or index out of range.", 404

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    """Display the user's score after submitting the quiz."""
    answers = session.get('answers', {})
    print("Session Answers in Submit:", answers)  # Debugging session data

    correct_answers = get_correct_answers()
    score = 0
    print("User Answers Before Scoring:", answers)
    for qid, ans in answers.items():
        try:
            qid = int(qid)  # Convert to integer
            correct_answer = correct_answers.get(qid)
            print(f"Question ID: {qid}, User Answer: {ans}, Correct Answer: {correct_answer}")
            if ans == correct_answer:
                score += 1
        except ValueError as e:
            print(f"Error converting ID to integer: {e}")
    print(f"Final Score: {score}")
    return render_template('submit.html', score=score, total=len(get_questions()))

@app.route('/clear_session')
def clear_session():
    """Clear the session data."""
    session.clear()
    return "Session cleared"

if __name__ == '__main__':
    app.run(debug=True)
