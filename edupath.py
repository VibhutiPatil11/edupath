import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
import hashlib

st.set_page_config(page_title="EduPath", layout="centered")
st.markdown(
    """
    <style>
        .stApp {background-color: #F3E5F5;}
        .stButton>button { background-color: #D1C4E9; color: white; }
        .stApp, .stApp h1, .stApp h2, .stApp h3, .stApp p, .stApp label,.stwrite  {color: #3D2A4D; }
        .stSidebar {background-color: #B39DDB;}
        .stRadio, .stSlider {color: #FFFFFF;}
        .stSelectbox > div > div {background-color: #B39DDB;  border: 1px solid #E6E6FA;}
        .stSelectbox > div > div > div{background-color: #B39DDB;  border: 1px solid #E6E6FA;}
    </style>
    """,
    unsafe_allow_html=True
)
questions_10th = {
    "Numerical-Ability": {
        "questions": [
            {"question": "What is 25% of 160?", "options": ["40", "35", "45", "50"], "answer": 1},
            {"question": "Solve for x:3x+9=27", "options": ["6", "12", "7", "8"], "answer": 1},
            {"question": "A sum of money doubles itself in 8 years at simple interest.How many years will it take to triple itself?", "options": ["12 years", "16 years", "20 years", "24 years"], "answer": 2},
            {"question": "Find the square root of 144", "options": ["12", "18", "22", "24"], "answer": 1},
            {"question": "What is the value of 15% of 300?", "options": ["45", "50", "65", "70"], "answer": 1},
            {"question": "A car travels 240 km in 4 hours. What is its average speed?","options": ["50 km/hr", "55 km/hr", "60 km/hr", "65 km/hr"], "answer": 3},
            {"question": "If a = 6 and b = 4, find the value of a2+b2a^2 + b^2a2+b2", "options": ["32", "36", "52", "68"], "answer": 3},
            {"question": "If 5x = 45, what is the value of x?", "options": ["9", "5", "6", "8"], "answer": 1},
            {"question": "Find the HCF of 18 and 24", "options": ["6", "3", "4", "5"], "answer": 1},
            {"question": "If 3 pens cost ₹90, how much will 7 pens cost?", "options": ["210", "200", "220", "250"], "answer": 1}   
        ]
    },
    "Verbal-Ability": {
        "questions": [
            {"question": "Choose the correct synonym for the word 'Industrious'", "options": ["lazy", "hardworking", "careless", "passive"], "answer": 2},
            {"question": "Find antonym of 'Optimistic'", "options": ["cheerful", "positive", "pesimistic", "hopeful"], "answer": 3},
            {"question": "Complete the sentence: 'He is not only intelligent ___hardworking.'", "options": ["and", "also", "but also", "nor"], "answer": 3},
            {"question": "Which word is incorrectly spelled? ", "options": ["accomodate", "receive", "priviledge", "exaggerate"], "answer": 2},
            {"question": "Choose the word that is closest in meaning to Average", "options": ["ordinary", "outstanding", "medicore", "terrible"], "answer": 1},
            {"question": "Fill in the blank: 'The manager requested that everyone ___ the meeting on time '", "options": ["attend", "attends", "attending", "will attend"], "answer": 1},
            {"question": "Find the word closest in meaning to 'Ambiguous'", "options": ["clear", "vague", "certain", "obvious"], "answer": 2},
            {"question": "Choose the correct synonym for 'Impeccable'", "options": ["flawless", "defective", "rough", "imperfect"], "answer": 1},
            {"question": "Complete the sentence: 'Despite the heavy rain, they ___ to th event.'", "options": ["goes", "gone", "went", "going"], "answer": 3},
            {"question": "Select the correct antonym for 'Benevolent'", "options": ["kind", "malevolent", "generous", "charitable"], "answer": 2},
        ]
    },
    "Logical-Reasoning": {
        "questions": [
            {"question": "Complete the series: 2, 4, 8, 16, __?", "options": ["20", "30", "32", "40"], "answer": 3},
            {"question": "If 1 = 5, 2 = 10, 3 = 15, then 5 = __?", "options": ["10", "25", "20", "30"], "answer": 2},
            {"question": "Which number comes next in the series: 5, 10, 17, 26, __?", "options": ["33", "35", "37", "40"], "answer": 3},
            {"question": "If TABLE is coded as UCDNG, how is CHAIR coded?", "options": ["DKBJT", "EJBKT", "EJATK", "FKCLU"], "answer": 3},
            {"question": "Pointing to a man, a woman said, 'His mother is the only daughter of my mother.'How is the woman related to the man?", "options": ["aunt", "mother", "grandmother", "sister"], "answer": 2},
            {"question": "In a certain code, BEAR is written as 6789 and RISK is written as 9475. How is BRISK written?","options": ["67895", "68945", "67495", "69475"],"answer": 4 },
            {"question": "If A is coded as Z, B as Y, and so on, what is the code for DANCE?","options": ["WZMXV", "XZMVW", "XWZMV", "WXMZV"],"answer": 2 },
            {"question": "In a family, there are six members: A, B, C, D, E, and F. B is the son of A but A is not the father of B. D is the brother of A. C is the wife of A. E is the daughter of C. F is the brother of B. Who is the father of B?","options": ["C", "A", "D", "F"],"answer": 3},
            {"question": "In certain words CATS is written as 1234 and DOGS is written as 5678,How is SCAT written?","options":["4123","5678","1235","7845"],"answer":1},
            {"question": "If TEACHER is written as VGCEJGT, how will STUDENT be written?","options": ["UVWFGRV", "UWVFGVR", "VWUFGVR", "UVWGFRV"],"answer": 2},
        ]
    },
    "General-Knowledge": {
        "questions": [
           {"question": "What is the capital of France?","options": ["Paris", "Berlin", "Madrid", "Rome"],"answer": 1},
           {"question": "Which planet is known as the Red Planet?","options": ["Earth", "Mars", "Jupiter", "Saturn"],"answer": 2},
           {"question": "Who wrote the famous play 'Romeo and Juliet'?","options": ["Charles Dickens", "J.K. Rowling", "William Shakespeare", "Mark Twain"],"answer": 3 },
           {"question": "What is the largest ocean on Earth?","options": ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"],"answer": 4},
           {"question": "In which year did India gain independence?","options": ["1945", "1947", "1950", "1960"],"answer": 2},
           {"question": "Who was the first person to walk on the moon?","options": ["Neil Armstrong", "Buzz Aldrin", "Yuri Gagarin", "John Glenn"],"answer": 1},
           {"question": "Which country is known as the Land of the Rising Sun?","options": ["China", "Japan", "Thailand", "South Korea"],"answer": 2},
           {"question": "What is the chemical symbol for water?","options": ["O2", "H2O", "CO2", "HO2"],"answer": 3 },
           {"question": "Who is known as the Father of the Nation in India?","options": ["Jawaharlal Nehru", "Mahatma Gandhi", "Sardar Patel", "Subhas Chandra Bose"],"answer": 2},
           {"question": "Which is the smallest continent by land area?","options": ["Europe", "Australia", "Antarctica", "South America"],"answer": 2}        
        ]
    },
    "Spatial-Ability": {
    "questions": [
        {"question": "Which shape will the unfolded form of a cube with 6 square faces resemble?", "options": ["Circle", "Square", "Cross", "Triangle"], "answer": 2},
        {"question": "If you rotate a rectangle by 90 degrees clockwise, what shape will you get?", "options": ["Circle", "Rectangle", "Square", "Triangle"], "answer": 1},
        {"question": "Which two shapes combine to form a rectangle?", "options": ["Two triangles", "Two squares", "A triangle and a square", "Two circles"], "answer": 1},
        {"question": "How many faces does a triangular prism have?", "options": ["4", "5", "6", "7"], "answer": 1},
        {"question": "A net for a pyramid is made of which shapes?", "options": ["Rectangles and circles", "Squares and triangles", "Triangles", "Squares"], "answer": 2},
        {"question": "Which shape has only one surface?", "options": ["Cube", "Sphere", "Cylinder", "Cone"], "answer": 1},
        {"question": "What is the name of a 3D shape with a circular base and a single vertex?", "options": ["Sphere", "Cube", "Pyramid", "Cone"], "answer": 3},
        {"question": "If a square is cut diagonally, what shapes are formed?", "options": ["Two rectangles", "Two triangles", "Two circles", "Two squares"], "answer": 1},
        {"question": "What is the minimum number of colors required to fill a map without two adjacent regions having the same color?", "options": ["2", "3", "4", "5"], "answer": 2},
        {"question": "Which shape does not have any edges?", "options": ["Cube", "Cylinder", "Sphere", "Pyramid"], "answer": 2}
    ]
}
}

questions_12th = {
    "Personality-Traits":{
        "questions": [
            {"question": "How do you prefer to approach problems?", "options": ["Analyze the situation carefully before deciding", "Jump to conclusions quickly", "Avoid the problem", "Wait for someone else to solve it   "], "answer":1},
            {"question": "How do you handle criticism?", "options": ["Get defensive", " Ignore it",  "Learn from it and try to improve", "Feel discouraged"], "answer": 3},
            {"question":  "Which environment do you feel most comfortable in? ", "options": [" An organized and structured setting", "An unpredictable and fast-paced setting", "A relaxed and casual setting", "A chaotic and loud setting"], "answer": 1},
            {"question": "How do you respond to new challenges?", "options": ["Excited and ready to take it on", "Hesitant but willing to try", "Avoid if possible", "Worry about failing"], "answer":  1},
            {"question": "When faced with a decision, you are more likely to: ", "options": ["Gather all the information before deciding", "Go with your gut feeling", "Avoid making the decision", "Let others decide for you"], "answer": 1},
            {"question": "How do you prefer to work on projects? ", "options": ["Plan every step in advance", "Jump in and figure it out as you go", "Rely on others for guidance", "Avoid detailed planning"], "answer": 1},
            {"question": "Which describes your social interactions best?    ", "options": ["Friendly and outgoing with new people", "Reserved and quiet    ", "Prefer to be alone", " Anxious in social settings"], "answer": 1},
            {"question": "When under pressure, you tend to:", "options": ["Feel stressed but manage", "Panic and struggle", "Avoid responsibility", " Stay calm and focused"], "answer": 4},
            {"question": "What motivates you most to achieve your goals?    ", "options": ["1External rewards like money or recognition", "Personal satisfaction and growth", "Fear of failure", "Pressure from others"], "answer": 2},
            {"question": "What describes your leadership style?    ", "options": ["Dictating and controlling    ",  "  Collaborative and democratic    ", " Guiding and encouraging", "Passive and hands-off"], "answer": 3}
            ]
        },
    "Abstract-Reasoning":{
        "questions":[
            {"question": " What comes next in the series? 1, 2, 4, 8, 16, __?", "options": ["32", "24", "20", "28"], "answer": 1},
            {"question": "Select the figure that does not belong: (Imagine a series of shapes: Square, Hexagon, Pentagon, Triangle)", "options": ["square", "Hexagon", "Pentagon", " Triangle"], "answer": 3},
            {"question": "Which number comes next? 2, 6, 12, 20, 30, __?", "options": ["35", "42", "50", "38"], "answer": 2},
            {"question": "Choose the odd one out: (Imagine a series: 3, 5, 7, 9)", "options": ["3", "9", "5", "7"], "answer": 2},
            {"question": " Complete the series: B, D, F, H, __?", "options": ["I", "J", "K", "L"], "answer": 3},
            {"question": "Find the next number: 5, 10, 20, 40, __?", "options": ["80", "100", "60", "50"], "answer":1},
            {"question": "Select the odd one out: 1, 4, 9, 16, 25, 40", "options": ["4", "9", "25", "40"], "answer": 4},
            {"question": " What is next in the pattern? AA, AB, AC, AD, __?", "options": ["AE", "AF", "BC", "BB"], "answer": 1},
            {"question": " Choose the missing shape: (Imagine a pattern: Triangle → Circle → Square → __?)", "options": ["Pentagon", "Rectangle", " Hexagon", "Oval"], "answer": 2},
            {"question": "Which letter comes next? P, R, T, V, __? ", "options": ["W", "Y", "Z", "X"], "answer": 4}
            ]
        },
    "Mechanical Aptitude":{
        "questions":[
            {"question": " Which of the following tools is used to measure the diameter of a cylindrical object?", "options": ["Ruler", "Vernier Caliper ", "Protractor ", "T-square"], "answer": 2},
            {"question": "If a gear with 20 teeth is driving a gear with 40 teeth, how will the second gear rotate compared to the first?", "options": ["At the same speed", "Half the speed ", " Double the speed", "Four times the speed"], "answer": 2},
            {"question": "A lever is used to lift a heavy load. Which of the following positions will make it easier to lift the load?", "options": ["Applying force near the fulcrum", "Placing the load closer to the force", "Applying force farther from the fulcrum", "Placing the load farther from the fulcrum"], "answer": 3},
            {"question": " A screw is an example of which simple machine? ", "options": ["Inclined plane", "Lever", "Pulley", "Wheel and axle "], "answer": 1},
            {"question": "If the pulley system has 3 pulleys and you pull the rope 3 meters, how far does the object rise?", "options": [" 1.5 meters", "1 meter", " 3 meters", "6 meters"], "answer": 2},
            {"question": "Which of the following materials would make the best insulator?", "options": ["COPPER", "ALUMINIUM", "RUBBER", "STEEL"], "answer": 3},
            {"question": "If two objects of different weights are dropped from the same height in a vacuum, which will hit the ground first?", "options": ["The heavier object", "The lighter object", "Both at the same time", "It depends on the size of the objects"], "answer": 3},
            {"question": " A 1-meter ramp is used to lift a 10 kg box to a height of 0.5 meters. Which of the following is true about the effort required? ", "options": ["It is reduced because of the inclined plane", "It is increased because of the inclined plane", "It stays the same as lifting the box directly", " No effort is required"], "answer": 1},
            {"question": "Which of these is the correct unit of torque?", "options": [" Newton", "JOULE", "PASCAL", "NEWTON METER"], "answer": 4},
            {"question": " Which principle explains the upward force on an object submerged in a fluid?", "options": ["Bernoulli’s principle", "Pascal’s law", "Archimedes’ principle", "Boyle’s law"], "answer": 4}      
            ]
       },
    "Verbal-Ability":{
        "questions":[ 
            {"question": "Find the synonym of the word 'Benevolent'", "options": ["Kind", "Greedy", "Cruel", "Angry"], "answer":1},
            {"question": "Choose the correctly spelt word:", "options": ["Restaurant", "Restuarant", "Restourant", "Restraunt"], "answer":1},
            {"question": "Identify the meaning of the idiom 'A blessing in disguise'", "options": ["A good thing that seemed bad at first", "A harmful situation", "A surprise gift", "A misunderstanding"], "answer":1},
            {"question": "Complete the sentence: 'He __ to the store every morning.'", "options": ["goes", "go", "going", "gone"], "answer":1},
            {"question": "Choose the antonym of the word 'Acute'", "options": ["Dull", "Sharp", "Intense", "Severe"], "answer":1},
            {"question": "Choose the word that best fits in the blank: 'The sun __ at 6:00 am.'", "options": ["raised", "rises", "raising", "rise"], "answer":2},
            {"question": "Select the correct form of the verb: 'They __ the movie before I arrived.'", "options": ["had watched", "will watch", "are watching", "watch"], "answer":1},
            {"question": "Find the antonym of the word 'Expand':", "options": ["Contract", "Widen", "Extend", "Increase"], "answer":1},
            {"question": "Which of the following is a synonym of the word 'Obstinate'?", "options": ["Stubborn", "Obidient", "Flexible", "Understanding"], "answer":1},
            {"question": "Choose the correct meaning of the idiom 'Cut corners':", "options": ["To avoid shortcuts", "To take the long way", "To perform poorly to save time or money", "To do something in the easiest way"], "answer":4}
            ]
        },
    "Quantitative Ability":{
        "questions":[
            {"question": "What is the value of (25 × 25) + (25 × 75)?", "options": ["2000", "2500", "3500", "3000"], "answer":2},
            {"question": "Simplify: (125 ÷ 5) + (48 × 2) = ?", "options": ["151", "146", "149", "144"], "answer":2},
            {"question": "A car travels 60 km in 1 hour. How far will it travel in 5 hours?","options": ["250 km", "350 km", "280 km", "300 km"], "answer":4},
            {"question": "If a number is increased by 20%, it becomes 240. What is the original number?","options": ["200", "210", "180", "230"], "answer":1},
            {"question": "Find the square root of 256.","options": ["20", "14", "16", "12"], "answer":3},
            {"question": "A train travels 180 km in 3 hours. What is the average speed of the train?","options": ["60 km/h", "50 km/h", "45 km/h", "75 km/h"], "answer":1},
            {"question": "If 3x + 5 = 20, what is the value of x?","options": ["7", "5", "6", "4"], "answer":2},
            {"question": "What is the value of 2/3 of 99?","options": ["64", "68", "66", "72"], "answer":3},
            {"question": "What is 20% of 450?","options": ["90", "85", "75", "80"], "answer":1},
            {"question": "Find the next number in the series: 2, 5, 10, 17, 26,?","options": ["36", "40", "38", "37"], "answer":4}
            ]
        }
    }

mental_health_questions = [
    "How often do you feel tired or fatigued during the day?",
    "How often do you experience headaches?",
    "How often do you feel physically drained after completing daily activities?",
    "How often do you struggle with maintaining your energy levels throughout the day?",
    "How often do you find it difficult to concentrate due to physical discomfort?",
    "How often do you feel tense or experience muscle pain?",
    "How often do you experience difficulty sleeping or insomnia?",
    "How often do you feel refreshed after a night's sleep?",
    "How often do you find yourself relying on caffeine or energy drinks to stay awake?",
    "How often do you engage in physical activity or exercise?",
    "How often do you feel headaches due to stress or tension?",
    "How often do you experience stomachaches or digestive issues?",
    "How often do you feel short of breath or have difficulty breathing?",
    "How often do you find it hard to stay awake during classes or meetings?",
    "How often do you experience dizziness or lightheadedness?",
    "How often do you have trouble maintaining a regular eating schedule?",
    "How often do you feel your heart racing or experience palpitations?",
    "How often do you feel restless or unable to sit still?",
    "How often do you skip meals due to a busy schedule?",
    "How often do you feel a lack of motivation to engage in physical activities?",
    "How often do you experience joint pain or stiffness?",
    "How often do you feel mentally fatigued or exhausted after a day of work or study?",
    "How often do you experience mood swings related to your physical health?",
    "How often do you neglect self-care or relaxation practices?",
    "How often do you feel that your physical health impacts your emotional well-being?"
]

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS feedback (
    user_id INTEGER NOT NULL,
    feedback TEXT,
    rating INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")
conn.commit()
def init_db():
    conn = sqlite3.connect("feedback.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            rating INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()
init_db()
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        security_pin TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()
init_db()
def add_feedback(feedback_text, rating):
    conn = sqlite3.connect("feedback.db")
    c = conn.cursor()
    c.execute("INSERT INTO feedback (text, rating) VALUES (?, ?)", (feedback_text, rating))
    conn.commit()
    conn.close()

def get_all_feedback():
    conn = sqlite3.connect("feedback.db")
    c = conn.cursor()
    c.execute("SELECT text, rating FROM feedback")
    feedbacks = c.fetchall()
    conn.close()
    return feedbacks

def login_user(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, hashed_password))
    user = cursor.fetchone()
    conn.close()
    return user

def register_user(username, password, security_pin):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    if c.fetchone():
        conn.close()
        return False  
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    c.execute("INSERT INTO users (username, password, security_pin) VALUES (?, ?, ?)",
              (username, hashed_password, security_pin))
    conn.commit()
    conn.close()
    return True

def reset_password(username, security_pin, new_password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND security_pin = ?", (username, security_pin))
    user = c.fetchone()  

    if user:
        hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
        c.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_password, username))
        conn.commit()  
        conn.close()
        return True  
    else:
        conn.close()
        return False
    
def save_feedback(user_id, feedback, rating):
    cursor.execute("INSERT INTO feedback (user_id, feedback, rating) VALUES (?, ?, ?)", (user_id, feedback, rating))
    conn.commit()

if "logged_in_user" not in st.session_state:
    st.session_state["logged_in_user"] = None

if "selected_tab" not in st.session_state:
    st.session_state["selected_tab"] = "About Us"

if "feedbacks" not in st.session_state:
            st.session_state["feedbacks"] = []
    
def select_grade():
    grade_choice = st.selectbox("Select your grade level:", ["10th Grade", "12th Grade"])
    return grade_choice

def ask_all_questions(questions):
    if 'responses' not in st.session_state:
        st.session_state.responses = {}

    for category, data in questions.items():
        st.subheader(f"{category} Questions")
        st.session_state.responses[category] = []
        for i, q in enumerate(data['questions'], 1):
            response = st.radio(
                f"{category} Q{i}: {q['question']}", 
                options=q['options'],
                key=f"{category}_Q{i}",
                # index=None
            )
            if response is not None: 
                st.session_state.responses[category].append(q['options'].index(response) + 1)
            else:
                st.session_state.responses[category].append(None)

def analyze_career_guidance_responses(questions):
    category_scores = {}
    for category, data in questions.items():
        score = sum(
            1 for i, q in enumerate(data['questions'])
            if st.session_state.responses[category][i] == q['answer']
        )
        category_scores[category] = score
    return category_scores

def plot_results(category_scores):
    labels = category_scores.keys()
    scores = category_scores.values()
    fig, ax = plt.subplots()
    ax.pie(
        scores, 
        labels=labels, 
        autopct='%1.1f%%', 
        startangle=140, 
        colors=plt.cm.Pastel1.colors
    )
    ax.set_title("Score Distribution by Category")
    st.pyplot(fig)

def suggest_careers(category_scores):
    career_options ={
    'Numerical-Ability': [
        {
            'Career': 'Data Analyst',
            'Degree': "Bachelor's in Computer Science / IT; Master's in Data Science",
            'Duration': "4-6 years",
            'Entrance': "JEE, GRE (for higher studies)",
            'Scope': "High demand in various industries, especially in tech and finance."
        },
        {
            'Career': 'Accountant',
            'Degree': "Bachelor's in Accounting, Finance, or related field",
            'Duration': "3-4 years",
            'Entrance': "None (some institutes may require entrance exams)",
            'Scope': "Steady demand across industries, especially in finance and government."
        },
        {
            'Career': 'Actuary',
            'Degree': "Bachelor's in Actuarial Science or related field",
            'Duration': "4-5 years",
            'Entrance': "Actuarial Common Entrance Test (ACET)",
            'Scope': "Growing demand in insurance and risk management sectors."
        },
        {
            'Career': 'Investment Banker',
            'Degree': "Bachelor's in Finance, Economics, or related field",
            'Duration': "4-6 years",
            'Entrance': "GMAT, GRE (for higher studies)",
            'Scope': "High earning potential in the financial sector."
        },
        {
            'Career': 'Statistician',
            'Degree': "Bachelor's in Statistics or Mathematics",
            'Duration': "3-5 years",
            'Entrance': "None or institute-specific exams",
            'Scope': "In-demand in research, healthcare, and data-driven industries."
        },
        {
            'Career': 'Market Research Analyst',
            'Degree': "Bachelor's in Business, Marketing, or Statistics",
            'Duration': "3-4 years",
            'Entrance': "None",
            'Scope': "Growing demand in marketing and business intelligence."
        },
        {
            'Career': 'Operations Research Analyst',
            'Degree': "Bachelor's in Operations Research or related field",
            'Duration': "4-5 years",
            'Entrance': "JEE (for engineering background)",
            'Scope': "Opportunities in logistics, transportation, and business optimization."
        },
        {
            'Career': 'Economist',
            'Degree': "Bachelor's/Master's in Economics",
            'Duration': "5-6 years",
            'Entrance': "Institute-specific exams or GRE (for higher studies)",
            'Scope': "Career options in public policy, financial institutions, and research."
        },
        {
            'Career': 'Risk Manager',
            'Degree': "Bachelor's in Finance, Economics, or Actuarial Science",
            'Duration': "3-5 years",
            'Entrance': "Institute-specific exams",
            'Scope': "High demand in banks and insurance companies."
        },
        {
            'Career': 'Financial Analyst',
            'Degree': "Bachelor's in Finance, Accounting, or Economics",
            'Duration': "3-4 years",
            'Entrance': "None (CFA preferred for growth)",
            'Scope': "Opportunities in corporate finance and investment firms."
        }
    ],
    'Verbal-Ability': [
        {
            'Career': 'Journalist',
            'Degree': "Bachelor's in Journalism or Mass Communication",
            'Duration': "3-4 years",
            'Entrance': "University-specific entrance exams (e.g., DUET, IPU CET)",
            'Scope': "Opportunities in print, TV, and digital media."
        },
        {
            'Career': 'Content Writer',
            'Degree': "Bachelor's in English, Communication, or related field",
            'Duration': "3-4 years",
            'Entrance': "None (depends on the institute)",
            'Scope': "Freelance and full-time opportunities in diverse industries."
        },
        {
            'Career': 'Copywriter',
            'Degree': "Bachelor's in Advertising, English, or related field",
            'Duration': "3-4 years",
            'Entrance': "None",
            'Scope': "Opportunities in advertising agencies and marketing firms."
        },
        {
            'Career': 'Public Relations Specialist',
            'Degree': "Bachelor's in Communication, PR, or Journalism",
            'Duration': "3-4 years",
            'Entrance': "None",
            'Scope': "Growing demand in corporate and government sectors."
        },
        {
            'Career': 'Editor',
            'Degree': "Bachelor's in English, Journalism, or related field",
            'Duration': "3-4 years",
            'Entrance': "None",
            'Scope': "Opportunities in publishing, media, and online platforms."
        },
        {
            'Career': 'Technical Writer',
            'Degree': "Bachelor's in Technical Writing, IT, or related field",
            'Duration': "3-4 years",
            'Entrance': "None",
            'Scope': "High demand in IT and engineering sectors."
        },
        {
            'Career': 'Translator',
            'Degree': "Bachelor's in Linguistics, Foreign Languages, or related field",
            'Duration': "3-4 years",
            'Entrance': "None",
            'Scope': "Opportunities in international business and diplomacy."
        },
        {
            'Career': 'Communications Manager',
            'Degree': "Bachelor's in Public Relations or Mass Communication",
            'Duration': "3-4 years",
            'Entrance': "None",
            'Scope': "Careers in corporate communication and branding."
        },
        {
            'Career': 'Language Teacher',
            'Degree': "Bachelor's in Education or Linguistics",
            'Duration': "3-4 years",
            'Entrance': "B.Ed entrance exams (India)",
            'Scope': "Opportunities in schools, colleges, and online platforms."
        },
        {
            'Career': 'Speech-Language Pathologist',
            'Degree': "Bachelor's in Speech-Language Pathology",
            'Duration': "4-5 years",
            'Entrance': "Institute-specific exams",
            'Scope': "High demand in healthcare and therapy sectors."
        }
    ],
    'Logical-Reasoning': [
       {
        'Career': 'Software Developer',
        'Degree': "Bachelor's in Computer Science / IT",
        'Duration': "4-6 years",
        'Entrance': "JEE, SAT (for abroad studies)",
        'Scope': "One of the most sought-after professions in the tech industry."
       },
       {
        'Career': 'Cybersecurity Analyst',
        'Degree': "Bachelor's in IT, Cybersecurity, or related field",
        'Duration': "4-6 years",
        'Entrance': "JEE or institute-specific exams",
        'Scope': "High demand in IT security and risk management."
       },
       {
        'Career': 'Artificial Intelligence Engineer',
        'Degree': "Bachelor's in Computer Science; Master's in AI (preferred)",
        'Duration': "4-6 years",
        'Entrance': "JEE, GATE (for higher studies)",
        'Scope': "Opportunities in machine learning, robotics, and automation."
       },
       {
        'Career': 'Business Analyst',
        'Degree': "Bachelor's in Business Administration or IT; MBA preferred",
        'Duration': "4-6 years",
        'Entrance': "CAT, GMAT, GRE (for higher studies)",
        'Scope': "High demand in tech and business consulting industries."
       },
       {
        'Career': 'Forensic Scientist',
        'Degree': "Bachelor's in Forensic Science or related field",
        'Duration': "3-4 years",
        'Entrance': "Institute-specific exams",
        'Scope': "Career options in law enforcement and criminal investigations."
       },
       {
        'Career': 'Cryptographer',
        'Degree': "Bachelor's in Mathematics, IT, or Cybersecurity",
        'Duration': "4-6 years",
        'Entrance': "JEE or institute-specific exams",
        'Scope': "High demand in government agencies and tech companies."
       },
       {
        'Career': 'Logistics Manager',
        'Degree': "Bachelor's in Business Administration or Logistics Management",
        'Duration': "3-4 years",
        'Entrance': "None (institute-specific exams for some courses)",
        'Scope': "Opportunities in supply chain and operations management."
       },
       {
        'Career': 'Operations Manager',
        'Degree': "Bachelor's in Business Administration or Operations Management",
        'Duration': "3-4 years",
        'Entrance': "None (MBA for career advancement)",
        'Scope': "High demand in manufacturing, retail, and service industries."
       },
       {
        'Career': 'Robotics Engineer',
        'Degree': "Bachelor's in Robotics Engineering or related field",
        'Duration': "4-5 years",
        'Entrance': "JEE, GATE (for higher studies)",
        'Scope': "Opportunities in automation, AI, and industrial robotics."
       },
       {
        'Career': 'IT Consultant',
        'Degree': "Bachelor's in IT or Computer Science; MBA preferred",
        'Duration': "4-6 years",
        'Entrance': "JEE, GMAT (for higher studies)",
        'Scope': "High demand in consulting firms and tech companies."
       }
   ],
    'General-Knowledge': [
       {
        'Career': 'Civil Services Officer (IAS, IPS)',
        'Degree': "Bachelor's in any field",
        'Duration': "3-4 years (plus UPSC preparation)",
        'Entrance': "UPSC Civil Services Exam",
        'Scope': "Prestigious and stable career in government administration."
       },
       {
        'Career': 'Diplomat',
        'Degree': "Bachelor's in International Relations or Political Science",
        'Duration': "3-4 years",
        'Entrance': "IFS exam (through UPSC)",
        'Scope': "Opportunities in international relations and foreign affairs."
       },
       {
        'Career': 'Political Scientist',
        'Degree': "Bachelor's/Master's in Political Science",
        'Duration': "5-6 years",
        'Entrance': "Institute-specific exams",
        'Scope': "Opportunities in policy-making, research, and academia."
       },
       {
        'Career': 'Policy Analyst',
        'Degree': "Bachelor's in Public Administration, Political Science, or related field",
        'Duration': "4-5 years",
        'Entrance': "None",
        'Scope': "High demand in government and non-profit organizations."
       },
       {
        'Career': 'Historian',
        'Degree': "Bachelor's/Master's in History",
        'Duration': "3-6 years",
        'Entrance': "Institute-specific exams",
        'Scope': "Opportunities in research, museums, and academia."
       },
       {
        'Career': 'Archaeologist',
        'Degree': "Bachelor's in Archaeology, History, or related field",
        'Duration': "3-6 years",
        'Entrance': "Institute-specific exams",
        'Scope': "Opportunities in heritage preservation and academic research."
       },
       {   
        'Career': 'Social Worker',
        'Degree': "Bachelor's in Social Work (BSW)",
        'Duration': "3-4 years",
        'Entrance': "None (institute-specific exams for some courses)",
        'Scope': "Opportunities in NGOs, healthcare, and public welfare."
       },
       {
        'Career': 'Museum Curator',
        'Degree': "Bachelor's in History, Art History, or related field",
        'Duration': "3-4 years",
        'Entrance': "None (Master's preferred for advancement)",
        'Scope': "Opportunities in museums, art galleries, and heritage sites."
       },
       {
        'Career': 'Travel Writer',
        'Degree': "Bachelor's in Journalism or Mass Communication",
        'Duration': "3-4 years",
        'Entrance': "Institute-specific exams",
        'Scope': "Freelance and full-time opportunities in media and tourism."
       },
       {
        'Career': 'International Relations Specialist',
        'Degree': "Bachelor's in International Relations or Political Science",
        'Duration': "3-4 years",
        'Entrance': "None (Master's preferred for advancement)",
        'Scope': "Careers in diplomacy, global NGOs, and think tanks."
       }
   ],
    'Spatial-Ability': [
    {
        'Career': 'Architect',
        'Degree': "Bachelor's in Architecture",
        'Duration': "5 years",
        'Entrance': "NATA, JEE (Architecture Paper)",
        'Scope': "High demand in construction, urban planning, and design industries."
    },
    {
        'Career': 'Urban Planner',
        'Degree': "Bachelor's in Urban Planning or Architecture",
        'Duration': "5 years",
        'Entrance': "Institute-specific exams",
        'Scope': "Opportunities in city development, infrastructure, and environmental planning."
    },
    {
        'Career': 'Interior Designer',
        'Degree': "Bachelor's in Interior Design or Architecture",
        'Duration': "3-4 years",
        'Entrance': "NATA, institute-specific exams",
        'Scope': "Demand in residential, commercial, and corporate interior design."
    },
    {
        'Career': 'Civil Engineer',
        'Degree': "Bachelor's in Civil Engineering",
        'Duration': "4 years",
        'Entrance': "JEE, GATE (for higher studies)",
        'Scope': "Opportunities in infrastructure, construction, and urban development."
    },
    {
        'Career': '3D Animator',
        'Degree': "Bachelor's in Animation, Multimedia, or related field",
        'Duration': "3-4 years",
        'Entrance': "Institute-specific exams",
        'Scope': "Opportunities in film, gaming, and advertising industries."
    },
    {
        'Career': 'Game Designer',
        'Degree': "Bachelor's in Game Design, Computer Science, or related field",
        'Duration': "3-4 years",
        'Entrance': "Institute-specific exams or entrance exams like NID",
        'Scope': "Opportunities in video game development, programming, and creative design."
    },
    {
        'Career': 'Graphic Designer',
        'Degree': "Bachelor's in Graphic Design, Visual Arts, or related field",
        'Duration': "3-4 years",
        'Entrance': "Institute-specific exams",
        'Scope': "Opportunities in digital media, advertising, branding, and visual communication."
    },
    {
        'Career': 'Industrial Designer',
        'Degree': "Bachelor's in Industrial Design or Product Design",
        'Duration': "4 years",
        'Entrance': "NID, NIFT, or institute-specific exams",
        'Scope': "Opportunities in manufacturing, consumer products, and automotive industries."
    },
    {
        'Career': 'CAD Technician',
        'Degree': "Bachelor's in Mechanical Engineering, Civil Engineering, or related field",
        'Duration': "3-4 years",
        'Entrance': "Institute-specific exams",
        'Scope': "Opportunities in engineering design, architecture, and product development."
    },
    {
        'Career': 'Cartographer',
        'Degree': "Bachelor's in Geography, Geomatics, or related field",
        'Duration': "3-4 years",
        'Entrance': "Institute-specific exams",
        'Scope': "Opportunities in mapping, geospatial analysis, and geographic information systems (GIS)."
    }
    ],
    'Personality-Traits': [
    {
        'Career': 'HR Manager',
        'Degree': "Bachelor's in Human Resources, Psychology, or Business Administration",
        'Duration': "3-4 years",
        'Entrance': "None",
        'Scope': "High demand in companies for talent acquisition, employee relations, and organizational development."
    },
    {
        'Career': 'Counseling Psychologist',
        'Degree': "Bachelor's in Psychology; Master's in Counseling Psychology",
        'Duration': "5-6 years",
        'Entrance': "None",
        'Scope': "Demand in schools, hospitals, and private practices for mental health counseling."
    },
    {
        'Career': 'Teacher',
        'Degree': "Bachelor's in Education (B.Ed)",
        'Duration': "4 years",
        'Entrance': "None (some institutes may have entrance exams)",
        'Scope': "High demand in schools, colleges, and online education platforms."
    },
    {
        'Career': 'Marketing Manager',
        'Degree': "Bachelor's in Marketing, Business Administration, or Communications",
        'Duration': "3-4 years",
        'Entrance': "CAT, XAT (for MBA)",
        'Scope': "Opportunities in consumer goods, media, and digital marketing."
    },
    {
        'Career': 'Event Planner',
        'Degree': "Bachelor's in Event Management, Hospitality, or related field",
        'Duration': "3-4 years",
        'Entrance': "None",
        'Scope': "Demand in corporate, personal, and public event planning."
    },
    {
        'Career': 'Public Relations Officer',
        'Degree': "Bachelor's in Public Relations, Journalism, or Communications",
        'Duration': "3-4 years",
        'Entrance': "None",
        'Scope': "Opportunities in corporate communications, media houses, and government sectors."
    },
    {
        'Career': 'Social Worker',
        'Degree': "Bachelor's in Social Work",
        'Duration': "3-4 years",
        'Entrance': "None",
        'Scope': "High demand in NGOs, hospitals, and community development projects."
    },
    {
        'Career': 'Customer Relationship Manager',
        'Degree': "Bachelor's in Business Administration or Marketing",
        'Duration': "3-4 years",
        'Entrance': "None",
        'Scope': "Demand in service industries, retail, and e-commerce sectors."
    },
    {
        'Career': 'Sales Manager',
        'Degree': "Bachelor's in Sales, Marketing, or Business Administration",
        'Duration': "3-4 years",
        'Entrance': "None",
        'Scope': "Opportunities in retail, FMCG, and tech industries."
    },
    {
        'Career': 'Life Coach',
        'Degree': "Certifications in Coaching or Psychology",
        'Duration': "Variable (depends on certification)",
        'Entrance': "None",
        'Scope': "Increasing demand for personal and professional development guidance."
    }
    ],
    'Abstract-Reasoning': [
    {
        'Career': 'Software Engineer',
        'Degree': "Bachelor's in Computer Science or IT",
        'Duration': "4 years",
        'Entrance': "JEE, GATE (for higher studies)",
        'Scope': "High demand in tech companies, with opportunities in software development and systems analysis."
    },
    {
        'Career': 'Data Scientist',
        'Degree': "Bachelor's in Computer Science, Statistics, or Data Science",
        'Duration': "4-5 years",
        'Entrance': "JEE, GRE (for higher studies)",
        'Scope': "Opportunities in data-driven industries like finance, healthcare, and tech."
    },
    {
        'Career': 'AI Researcher',
        'Degree': "Bachelor's in AI, Machine Learning, or Computer Science",
        'Duration': "4-5 years",
        'Entrance': "GATE, GRE",
        'Scope': "Growing demand in AI, deep learning, and automation technologies."
    },
    {
        'Career': 'Financial Analyst',
        'Degree': "Bachelor's in Finance, Economics, or Business Administration",
        'Duration': "3-4 years",
        'Entrance': "None",
        'Scope': "High demand in banking, finance, and investment firms."
    },
    {
        'Career': 'Blockchain Developer',
        'Degree': "Bachelor's in Computer Science, IT, or related field",
        'Duration': "4 years",
        'Entrance': "None",
        'Scope': "Rapidly growing demand in cryptocurrency and blockchain-based solutions."
    },
    {
        'Career': 'Quantitative Analyst',
        'Degree': "Bachelor's in Mathematics, Statistics, or Finance",
        'Duration': "4 years",
        'Entrance': "None",
        'Scope': "Opportunities in finance, banking, and stock market analysis."
    },
    {
        'Career': 'Robotics Engineer',
        'Degree': "Bachelor's in Robotics, Mechanical, or Electrical Engineering",
        'Duration': "4 years",
        'Entrance': "JEE, GATE (for higher studies)",
        'Scope': "Demand in automation, manufacturing, and robotics industries."
    },
    {
        'Career': 'Game Developer',
        'Degree': "Bachelor's in Game Development, Computer Science",
        'Duration': "4 years",
        'Entrance': "None",
        'Scope': "Opportunities in gaming companies and startups."
    },
    {
        'Career': 'Systems Analyst',
        'Degree': "Bachelor's in Information Systems or Computer Science",
        'Duration': "4 years",
        'Entrance': "JEE, GRE",
        'Scope': "Opportunities in technology companies working on business processes and IT solutions."
    },
    {
        'Career': 'Logistics Manager',
        'Degree': "Bachelor's in Logistics, Supply Chain Management, or Business",
        'Duration': "3-4 years",
        'Entrance': "None",
        'Scope': "Demand in transportation, warehousing, and supply chain industries."
    }
    ],
    'Mechanical-Aptitude': [
    {
        'Career': 'Mechanical Engineer',
        'Degree': "Bachelor's in Mechanical Engineering",
        'Duration': "4 years",
        'Entrance': "JEE, GATE (for higher studies)",
        'Scope': "High demand in manufacturing, automotive, and aerospace industries."
    },
    {
        'Career': 'Automobile Engineer',
        'Degree': "Bachelor's in Automobile Engineering",
        'Duration': "4 years",
        'Entrance': "JEE, GATE (for higher studies)",
        'Scope': "Opportunities in automobile design, manufacturing, and testing."
    },
    {
        'Career': 'Aerospace Engineer',
        'Degree': "Bachelor's in Aerospace Engineering",
        'Duration': "4 years",
        'Entrance': "JEE, GATE (for higher studies)",
        'Scope': "Opportunities in the defense, aviation, and space exploration industries."
    },
    {
        'Career': 'Marine Engineer',
        'Degree': "Bachelor's in Marine Engineering",
        'Duration': "4 years",
        'Entrance': "JEE, IMU CET",
        'Scope': "Opportunities in the maritime, shipping, and naval industries."
    },
    {
        'Career': 'Nuclear Engineer',
        'Degree': "Bachelor's in Nuclear Engineering",
        'Duration': "4 years",
        'Entrance': "JEE, GATE (for higher studies)",
        'Scope': "Opportunities in power generation, defense, and medical applications."
    },
    {
        'Career': 'Petroleum Engineer',
        'Degree': "Bachelor's in Petroleum Engineering",
        'Duration': "4 years",
        'Entrance': "JEE, GATE (for higher studies)",
        'Scope': "High demand in the oil and gas industry."
    },
    {
        'Career': 'Production Manager',
        'Degree': "Bachelor's in Production Engineering or Manufacturing Technology",
        'Duration': "4 years",
        'Entrance': "None",
        'Scope': "Opportunities in manufacturing plants, production lines, and quality control."
    },
    {
        'Career': 'HVAC Engineer',
        'Degree': "Bachelor's in Mechanical Engineering or related field",
        'Duration': "4 years",
        'Entrance': "None",
        'Scope': "Demand in construction, energy, and cooling/heating systems industries."
    },
    {
        'Career': 'Mechatronics Engineer',
        'Degree': "Bachelor's in Mechatronics Engineering",
        'Duration': "4 years",
        'Entrance': "JEE, GATE (for higher studies)",
        'Scope': "Growing demand in automation, robotics, and manufacturing sectors."
    },
    {
        'Career': 'Tool Designer',
        'Degree': "Bachelor's in Mechanical Engineering or Industrial Design",
        'Duration': "4 years",
        'Entrance': "None",
        'Scope': "Demand in industries requiring precision tools and machinery."
    }
    ],
    'Quantitative-Ability': [
    {
        'Career': 'Statistician',
        'Degree': "Bachelor's in Statistics or Mathematics",
        'Duration': "3-4 years",
        'Entrance': "None",
        'Scope': "Demand in research, government, and healthcare sectors."
    },
    {
        'Career': 'Actuary',
        'Degree': "Bachelor's in Actuarial Science, Mathematics, or Statistics",
        'Duration': "4 years",
        'Entrance': "None",
        'Scope': "High demand in insurance, finance, and risk management."
    },
    {
        'Career': 'Economist',
        'Degree': "Bachelor's in Economics or related field",
        'Duration': "3-4 years",
        'Entrance': "None",
        'Scope': "Opportunities in government, think tanks, and financial institutions."
    },
    {
        'Career': 'Investment Banker',
        'Degree': "Bachelor's in Finance, Economics, or Business Administration",
        'Duration': "3-4 years",
        'Entrance': "CAT, GRE, GMAT (for higher studies)",
        'Scope': "High demand in finance, banking, and corporate sectors."
    },
    {
        'Career': 'Market Research Analyst',
        'Degree': "Bachelor's in Marketing, Economics, or Business",
        'Duration': "3-4 years",
        'Entrance': "None",
        'Scope': "Opportunities in businesses focusing on consumer research and analytics."
    },
    {
        'Career': 'Data Engineer',
        'Degree': "Bachelor's in Computer Science, IT, or related field",
        'Duration': "4 years",
        'Entrance': "JEE, GATE (for higher studies)",
        'Scope': "Demand in tech companies, managing and processing large datasets."
    },
    {
        'Career': 'Operations Research Analyst',
        'Degree': "Bachelor's in Operations Research, Mathematics, or Engineering",
        'Duration': "4 years",
        'Entrance': "None",
        'Scope': "Opportunities in logistics, manufacturing, and corporate decision-making."
    },
    {
        'Career': 'Financial Planner',
        'Degree': "Bachelor's in Finance, Business Administration",
        'Duration': "3-4 years",
        'Entrance': "None",
        'Scope': "Demand in banking, insurance, and personal financial planning."
    },
    {
        'Career': 'Credit Analyst',
        'Degree': "Bachelor's in Finance, Economics, or Business Administration",
        'Duration': "3-4 years",
        'Entrance': "None",
        'Scope': "Opportunities in banks, lending institutions, and financial advisory firms."
    },
    {
        'Career': 'Supply Chain Manager',
        'Degree': "Bachelor's in Supply Chain Management, Logistics, or Business",
        'Duration': "3-4 years",
        'Entrance': "None",
        'Scope': "Demand in retail, manufacturing, and logistics industries."
    }
    ]
}
    suggested_careers = set()
    for category, score in category_scores.items():
      if score >= 5:
        if category in career_options:
            st.write(f"### Suggested Careers for Category: {category}")
            for career in career_options[category]:
                suggested_careers.add(career['Career'])
                with st.expander(f"**{career['Career']}** (More......)"):
                    st.markdown(f"""
                    - **📚 Degree Required:** {career['Degree']}
                    - **⏳ Duration of Study:** {career['Duration']}
                    - **📝 Entrance Exams:** {career['Entrance']}
                    - **🚀 Future Scope:** {career['Scope']}
                    """)
        else:
            st.write(f"Warning: No career options available for category '{category}'")
    
    if not suggested_careers:
       st.write("No career options suggested based on your scores.")  
    
def ask_mental_health_questions():
    st.subheader("Mental Health Tracker")
    st.write("Please rate the following statements on a scale of 1 to 5:")
    st.write("1: Strongly Disagree, 2: Disagree, 3: Neutral, 4: Agree, 5: Strongly Agree")
    if 'responses' not in st.session_state:
        st.session_state.responses = []
    for i, question in enumerate(mental_health_questions, 1):
        response = st.radio(f"Q{i}: {question}", options=[1, 2, 3, 4, 5], index=2) 
        st.session_state.responses.append(response)

def analyze_mental_health(responses): 
    st.write("\nAnalyzing your mental health responses...")
    rating_counts = [responses.count(i) for i in range(1, 6)]
    rating_labels = ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]
    avg_score = sum(responses) / len(responses)
    pastel_colors = ["#FAD6D6", "#F9E2AE", "#BEE3DB", "#AFCBFF", "#D9AFFC"]
    plt.figure(figsize=(6, 6))
    plt.pie(rating_counts,
            labels=rating_labels,
            autopct='%1.1f%%',
            startangle=90,
                colors=pastel_colors)
    plt.title("Mental Health Tracker Response Distribution")
    plt.axis('equal')  
    st.pyplot(plt)
    st.write("Analysis Summary")
    stress_levels = {"Low Stress": 0, "Moderate Stress": 0, "High Stress": 0}
    for response in responses:
     if 1 <= response <= 2:
        stress_levels["Low Stress"] += 1
     elif 3 <= response <= 3:
        stress_levels["Moderate Stress"] += 1
     elif 4 <= response <= 5:
        stress_levels["High Stress"] += 1
    total_responses = len(responses)
    stress_percentages = {level: (count / total_responses) * 100 for level, count in stress_levels.items()}
    pastel_colors = ["#BEE3DB", "#F9E2AE", "#FAD6D6"] 
    plt.figure(figsize=(6, 6))
    plt.bar(stress_percentages.keys(), stress_percentages.values(), color=pastel_colors)
    plt.title("Stress Level Distribution")
    plt.ylabel("Percentage (%)")
    plt.xlabel("Stress Levels")
    plt.ylim(0, 100)
    for i, (level, percentage) in enumerate(stress_percentages.items()):
        plt.text(i, percentage + 1, f"{percentage:.1f}%", ha='center')
    st.pyplot(plt)

    if avg_score <= 2.5:
        st.write("Your stress level is **Low**. Keep maintaining a healthy balance!")
        st.success("Your mental health appears stable. Great job maintaining a balanced lifestyle!")
        st.write("**WHO-Based Recommendations:**")
        st.markdown("- Maintain healthy sleep patterns and regular exercise.")
        st.markdown("- Engage in activities that bring you joy and relaxation.")
        st.markdown("- Stay connected with supportive family and friends.")
        st.markdown("- Continue practicing gratitude or mindfulness.")
    elif 2.6 <= avg_score <= 3.5:
        st.write("Your stress level is **Moderate**. Try relaxation techniques like yoga or meditation.")
        st.warning("You may be experiencing moderate stress or anxiety.")
        st.write("**WHO-Based Suggestions for Reducing Stress:**")
        st.markdown("- Practice mindfulness or guided meditation for 10–15 minutes daily.")
        st.markdown("- Incorporate physical activities like walking, yoga, or sports.")
        st.markdown("- Build problem-solving and interpersonal skills to manage stress.")
        st.markdown("- Limit time on social media and get adequate sleep.")
    elif 3.6 <= avg_score <= 5.0:
        st.write("Your stress level is **High**. Consider seeking support or counseling for better stress management.")
        st.error("Your responses indicate high levels of stress or anxiety.")
        st.write("**WHO-Based Immediate Actions:**")
        st.markdown("- Talk to a trusted adult, counselor, or mental health professional.")
        st.markdown("- Engage in breathing exercises to calm your mind.")
        st.markdown("- Avoid unhealthy coping mechanisms, such as skipping meals.")
        st.markdown("- Contact local mental health services or helplines if needed.")

    st.write(" Key Insights from WHO:")
    st.info(
        "Adolescence is a critical period for developing emotional and social habits. Healthy sleep, regular "
        "exercise, and supportive environments in families and schools are essential for well-being."
    )
    st.write("Recommended Resources for Stress Management and Mental Health:")
    st.markdown("- [Mayo Clinic - Stress Management](https://www.mayoclinic.org/healthy-lifestyle/stress-management/basics/stress-basics/hlv-20049495)")
    st.markdown("- [HelpGuide - Stress Management](https://www.helpguide.org/articles/stress/stress-management.htm)")
    st.markdown("- [Anxiety and Depression Association of America (ADAA)](https://adaa.org/)")
    st.markdown("- [Calm - Breathing and Anxiety Reduction](https://www.calm.com/)")
    st.markdown("- [Headspace - Anxiety Management](https://www.headspace.com/anxiety)")
    st.markdown("- [Yoga with Adriene (YouTube)](https://www.youtube.com/user/yogawithadriene)")
    st.markdown("- [Art of Living - Meditation](https://www.artofliving.org/in-en)")
    st.markdown("- [Mindful - Meditation for Students](https://www.mindful.org/)")
    st.write("Note:")
    st.info(
        "These recommendations are based on WHO insights and other trusted resources. They are not a substitute for professional mental health advice. "
        "If you are experiencing severe stress or anxiety, consider consulting a licensed therapist or counselor."
    )

def add_footer():
    st.markdown("""
        <hr style="border:1px solid #ccc;">
        <div style="text-align: center;">
            <h6>Email: <a href="mailto:support@edupath.com" style="color: blue;">support@edupath.com</a></h6>
            <h6>Phone: <a href="tel:+911010101010" style="color: blue;">+91 1010101010</a></h6>
            <h6>Follow Us</h6>
            <p>
                <a href="https://instagram.com/edupath" target="_blank" style="color: blue;">Instagram: @edupath</a><br>
                <a href="https://facebook.com/pedupath" target="_blank" style="color: blue;">Facebook: facebook.com/pedupath</a><br>
                <a href="https://twitter.com/edupath" target="_blank" style="color: blue;">Twitter: @edupath</a>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
if st.session_state["logged_in_user"] is None:
    st.sidebar.title("Welcome to EduPath")
    option = st.sidebar.radio("Choose an action", ["Login", "Register","Forgot Password"])

    if option == "Login":
        st.title("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user = login_user(username, password)
            if user:
                st.session_state["logged_in_user"] = user[0]
                st.success("Logged in successfully!")
            else:
                st.error("Invalid username or password.")

    elif option == "Register":
        st.title("Register")
        username = st.text_input("Choose a Username")
        password = st.text_input("Choose a Password", type="password")
        security_pin = st.text_input("Choose a Birthplace")
        if st.button("Register"):
            if register_user(username, password, security_pin):
                st.success("Registration successful! Please log in.")
            else:
                st.error("Username already exists.")
    elif option == "Forgot Password":
        st.title("Forgot Password")
        username = st.text_input("Enter your Username")
        security_pin = st.text_input("Enter your Birthplace")
        new_password = st.text_input("Enter your new Password", type="password")
        
        if st.button("Reset Password"):
            if reset_password(username, security_pin, new_password):
                st.success("Password reset successfully! You can now log in.")
            else:
                st.error("Invalid username or birthplace.")

else:
    st.sidebar.title("Navigation")
    st.sidebar.write(f"Logged in as User ID: {st.session_state['logged_in_user']}")
    st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"logged_in_user": None, "selected_tab": "About Us"}))
    st.sidebar.radio("Select a tab", ["About Us", "Career Guidance", "Mental Health Tracker", "Feedback"], key="selected_tab")

    if st.session_state["selected_tab"] == "About Us":
        st.title("🎓 Personalized Career Guidance & Mental Health Tracker")
        questions = {
        "🤖 Ask Your Bot":"Select question",
        "How to start the test?": "To start the test, go to the Career Guidance Test tab .",
        "What is the purpose of this app?": "The app provides personalized career guidance and tracks mental health for students.",
        "How is my data used?": "Your data is securely used only to generate your results.",
        "Can I retake the test?": "Yes, you can retake the test anytime by revisiting the test tab.",
        "What kind of careers does this app suggest?": "The app suggests careers based on your aptitude and interests, covering fields in Science, Commerce, and Arts.",
        "How does the mental health tracker work?": "The tracker uses simple questions to assess your mental well-being and provides helpful insights.",
        "Is my mental health data private?": "Absolutely. Your mental health data is confidential and used only for your benefit.",
        "What should I do if I feel overwhelmed?": "Take a break, practice deep breathing, and refer to the resources provided in the app for support.",
        "Does this app provide mental health resources?": "Yes, the app includes tips and resources for stress management and mental well-being.",
        "Can I track my mental health progress over time?": "Yes, your responses are saved, allowing you to view your progress in the Mental Health Tracker section."
         }
        st.write("Welcome to EduPath! "
             "We’re on a mission to empower students with the guidance and support they need during the critical stages of their academic journey."
             "As a platform dedicated to 10th and 12th-grade students in India, we offer tailored career guidance and mental health resources to help you make informed choices for a fulfilling future."
             "Our unique approach combines expert-driven career insights with a focus on mental well-being, ensuring you feel supported both academically and personally."
             "Whether you’re looking to explore potential career paths, navigate exam stress, or simply need someone to talk to, we’re here for you every step of the way."
             "Our resources, tools, and assessments are designed to provide you with personalized recommendations based on your interests, strengths, and goals."
             "At EduPath, we believe that every student deserves the chance to shine in their own way. Let’s work together to build a brighter future—starting today.")
        st.subheader("🌍✨Our Mission")
        st.write("Our mission is to provide 10th and 12th-grade students in India with personalized career guidance and mental health support, empowering them to make informed decisions about their future while nurturing their well-being. "
                 "Through our platform, we strive to create a supportive space where students can explore their interests, strengths, and goals, fostering confidence and clarity during this important stage of life.")
        st.subheader("👁️Our Vision")
        st.write("Our vision is to become a trusted companion for students across India, guiding them towards fulfilling careers and balanced mental health. We envision a future where every student has the resources and support they need to navigate academic pressures," 
             "explore career opportunities, and build a meaningful path forward—enabling them to thrive personally and professionally.")
        selected_question = st.selectbox("Ask me a question:", list(questions.keys()))

        if selected_question:
           st.info(questions[selected_question])

    elif st.session_state["selected_tab"] ==  "Career Guidance":
        st.header("Aptitude Test - Career Guidance")
        st.subheader("Discover Your Potential")
        st.write("Take the aptitude test to receive personalized career guidance.")
        grade_level = st.selectbox("Select your grade", ["10th Grade", "12th Grade"])
        questions = questions_10th if grade_level == "10th Grade" else questions_12th
        
        if 'test_started' not in st.session_state:
            st.session_state['test_started'] = False
        if 'questions_displayed' not in st.session_state:
            st.session_state['questions_displayed'] = False

        if st.button("Start Aptitude Test"):
            st.session_state['test_started'] = True
            st.session_state['questions_displayed'] = True
        
        if st.session_state['questions_displayed']:
            ask_all_questions(questions)

        if st.button("Submit Aptitude Test") and st.session_state['test_started']:
            category_scores = analyze_career_guidance_responses(questions)
            total_score = sum(category_scores.values())
            percentage_score = (total_score / 50 ) * 100
            
            # Show final scores
            st.write("### Your Final Scores by Category:")
            scores_df = pd.DataFrame(list(category_scores.items()), columns=['Category', 'Score'])
            st.table(scores_df)
            st.write(f"**Total Score:** {total_score} marks / 50 marks")
            st.write(f"**Percentage:** {percentage_score:.2f}%")
            st.success("🌟 Keep going! Every score is a step towards your future. 🌱")
            plot_results(category_scores)
            suggest_careers(category_scores)
            st.write("Recommended Resources for Suggested Careers:")
            st.markdown("- [General Career Exploration](https://www.careerexplorer.com/)")
            st.markdown("- [LinkedIn Careers](https://www.linkedin.com/jobs/)")
            st.markdown("- [Indeed Careers](https://www.indeed.com/career-advice)")
            st.markdown("- [Glassdoor Careers](https://www.glassdoor.com/Job/)")
            st.markdown("- [Naukri Careers](https://www.naukri.com/career-advice)")
            st.markdown("- [Coursera Career Courses](https://www.coursera.org/browse/business/career-development)")
            st.markdown("- [EdX Career Courses](https://www.edx.org/learn/career-development)")
            st.write("Note:")
            st.info(
                "These career recommendations are based on insights from industry experts and trusted career resources. "
                "They aim to help guide you in exploring potential career paths based on your aptitude and interests. "
                "However, they are not a substitute for professional career counseling. If you're unsure about your career choices or need personalized guidance, consider consulting a certified career counselor or mentor."
            )


    elif st.session_state["selected_tab"] ==  "Mental Health Tracker":
        st.header("Mental Health Tracker")
        st.subheader("Assess Your Wellbeing")
        st.write("Please rate the following statements on a scale of 1 to 5:")
        st.write("1: Strongly Disagree, 2: Disagree, 3: Neutral, 4: Agree, 5: Strongly Agree")

        responses = []
        for i, question in enumerate(mental_health_questions, 1):
            response = st.slider(
                f"Q{i}: {question}",
                min_value=1,
                max_value=5,
                value=3,  
                step=1,
                format="%d"  
            )
            responses.append(response)

        if st.button("Submit Mental Health Assessment", key="mh_assessment_button"):
            st.success("Assessment submitted! Analyzing your results...")
            analyze_mental_health(responses)  

    if st.session_state["selected_tab"] == "Feedback":  
        if "selected_tab" not in st.session_state or st.session_state["selected_tab"] == "Feedback":
            st.title("💬 Feedback Section")
            st.subheader("We'd love to hear from you!")
            feedback_text = st.text_area("Write your feedback here:", placeholder="Share your thoughts...")
            rating = st.slider("Rate your experience (1 = Poor, 5 = Excellent):", 1, 5, 3)
            if st.button("Submit Feedback"):
                if feedback_text.strip():  
                    st.session_state["feedbacks"].append({"text": feedback_text, "rating": rating})
                    st.success("Thank you for your feedback!")
                else:
                    st.error("Please enter some feedback before submitting.")
            st.write("---")
            st.subheader("Previous Feedback")
            if st.session_state["feedbacks"]:
                for i, feedback in enumerate(st.session_state["feedbacks"]):
                    st.write(f"**Feedback {i+1}:**")
                    st.write(f"🌟 **Rating:** {feedback['rating']}/5")
                    st.info(f"💬 {feedback['text']}")
            else:
                st.write("No feedback submitted yet.")
                
add_footer()