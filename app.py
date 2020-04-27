from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'askingquestions'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

RESPONCES = []

@app.route('/')
def survey_home(survey_name=satisfaction_survey):
    title = survey_name.title
    instructions = survey_name.instructions
    return render_template('index.html', title=title, instructions=instructions)

@app.route('/questions/<q_num>')
def survey_questions(q_num, survey_name=satisfaction_survey):
    q_num = int(q_num)
    num_of_questions = len(survey_name.questions)
    if  num_of_questions <= q_num:
        return redirect('/thankyou')
    elif q_num != len(session['responces']):
        flash("Please do the survey in order.")
        q = len(session['responces'])
        return redirect(f'/questions/{q}')
    else:
        q = survey_name.questions[q_num]
        num = q_num + 1
        return render_template('questions.html', num = num, q = q)

@app.route('/answers', methods=["POST"])
def handle_answers():
    answer = request.form['answer']
    responces = session['responces']
    responces.append(answer)
    session['responces'] = responces
    q_num = len(session['responces'])
    print(session['responces'])
    return redirect(f'/questions/{q_num}')

@app.route('/thankyou')
def thankyou(survey_name=satisfaction_survey):
     title = survey_name.title
     return render_template('thankyou.html', title=title)

@app.route('/startsurvey', methods=['POST'])
def start_the_survey():
    session["responces"] = []
    return redirect('/questions/0')