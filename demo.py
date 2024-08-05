from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'

DATABASE = 'responses.db'

def get_db():
    conn = sqlite3.connect(DATABASE, timeout=10)
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS responses (id INTEGER PRIMARY KEY AUTOINCREMENT, question_id INTEGER NOT NULL, selected_option TEXT NOT NULL)')
    conn.commit()
    conn.close()

def get_questions():
    conn = sqlite3.connect('questions.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM questions ORDER BY id')
    questions = cur.fetchall()
    conn.close()
    return questions

def get_correct_answers():
    conn = sqlite3.connect('questions.db')
    cur = conn.cursor()
    cur.execute('SELECT id, correct_answer FROM questions')
    correct_answers = {row[0] - 1: row[1] for row in cur.fetchall()}  # Adjust to start indexing from 0
    print("Correct Answers:", correct_answers)  # Debug print
    conn.close()
    return correct_answers

def save_response(question_id, selected_option):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO responses (question_id, selected_option) VALUES (?, ?)', (question_id, selected_option))
    conn.commit()
    conn.close()

init_db()

questions = get_questions()
correct_answers = get_correct_answers()

@app.route('/')
def index():
    session['index'] = 0
    session['answers'] = {}
    return redirect(url_for('question'))

@app.route('/question', methods=['GET', 'POST'])
def question():
    index = session.get('index', 1)
    answers = session.get('answers', {})

    if request.method == 'POST':
        selected_option = request.form.get('option')
        print(f"Selected Option: {selected_option} for Question ID: {index}")  # Debug print
        answers[str(index)] = selected_option
        session['answers'] = answers

        if 'next' in request.form:
            index += 1
        elif 'prev' in request.form:
            index -= 1
        elif 'submit' in request.form:
            for qid, ans in answers.items():
                save_response(int(qid), ans)
            return redirect(url_for('submit'))

        session['index'] = index

    if 0 <= index < len(questions):
        question_data = {
            'question': questions[index][1],
            'option1': questions[index][2],
            'option2': questions[index][3],
            'option3': questions[index][4],
            'option4': questions[index][5]
        }
        selected_option = answers.get(str(index))
        return render_template('index.html', question=question_data, index=index, total=len(questions), selected_option=selected_option)
    else:
        return "Question not found", 404

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    answers = session.get('answers', {})
    print(f"User Answers: {answers}")  # Debug print
    score = 0
    for idx, ans in answers.items():
        correct_answer = correct_answers.get(int(idx))
        print(f"Question ID: {idx}, User Answer: {ans}, Correct Answer: {correct_answer}")  # Debug print
        if ans == correct_answer:
            score += 1
    print(f"Score: {score}")  # Debug print
    return render_template('submit.html', score=score, total=len(questions))

if __name__ == '__main__':
    app.run(debug=True)
