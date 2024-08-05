import sqlite3

DATABASE = 'quiz.db'

def drop_tables():
    try:
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        
        # Drop the questions and responses tables if they exist
        cur.execute('DROP TABLE IF EXISTS questions')
        cur.execute('DROP TABLE IF EXISTS responses')

        conn.commit()
        print("Existing tables dropped successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred while dropping tables: {e}")
    finally:
        conn.close()

def create_tables():
    try:
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()

        # Create the questions table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_text TEXT NOT NULL,
                option1 TEXT NOT NULL,
                option2 TEXT NOT NULL,
                option3 TEXT NOT NULL,
                option4 TEXT NOT NULL,
                correct_answer TEXT NOT NULL
            )
        ''')

        # Create the responses table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_id INTEGER NOT NULL,
                answer TEXT NOT NULL,
                FOREIGN KEY (question_id) REFERENCES questions (id)
            )
        ''')

        conn.commit()
        print("Tables created successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred while creating tables: {e}")
    finally:
        conn.close()

def populate_questions():
    sample_questions = [
        {
            'question_text': 'What is the capital of India?',
            'option1': 'Delhi',
            'option2': 'Mumbai',
            'option3': 'Chennai',
            'option4': 'Kolkata',
            'correct_answer': 'option1'
        },
        {
            'question_text': 'What is 2 + 5?',
            'option1': '3',
            'option2': '4',
            'option3': '7',
            'option4': '6',
            'correct_answer': 'option3'
        },
        {
            'question_text': 'What is capital of Maharashtra?',
            'option1': 'Pune',
            'option2': 'Nagpur',
            'option3': 'Latur',
            'option4': 'Mumbai',
            'correct_answer': 'option4'
        },
        {
            'question_text': 'What is national bird of India?',
            'option1': 'Pegion',
            'option2': 'Peacock',
            'option3': 'Chicken',
            'option4': 'Eagle',
            'correct_answer': 'option2'
        },

    ]

    try:
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()

        # Insert sample questions
        for question in sample_questions:
            cur.execute('''
                INSERT INTO questions (question_text, option1, option2, option3, option4, correct_answer)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (question['question_text'], question['option1'], question['option2'], question['option3'], question['option4'], question['correct_answer']))

        conn.commit()
        print("Sample questions inserted successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred while inserting questions: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    drop_tables()
    create_tables()
    populate_questions()
