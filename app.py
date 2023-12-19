from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []
question_index = 0

@app.route('/')
def go_home():
    global question_index
    global responses
    # question_index = 0 #reset the question index
    # responses = [] #reset responses list
    return render_template("home.html", title = satisfaction_survey.title, instructions = satisfaction_survey.instructions)

@app.route('/questions/<question_idx>')
def question(question_idx):
    global question_index
    question_count = len(satisfaction_survey.questions)

    if int(question_idx) != int(question_index):
        question_idx = question_index
        flash("Invalid question requested!")

    if int(question_idx) < 0 or int(question_idx) >= question_count:
        return redirect('/thankyou')
    else:
        return render_template("question.html", question = satisfaction_survey.questions[int(question_idx)].question, options = satisfaction_survey.questions[int(question_idx)].choices, index=int(question_idx))

@app.route('/thankyou')
def show_complete():
    return render_template("survey_complete.html")

@app.route('/answer', methods=["POST"])
def append_answer():
    global question_index
    answer =  request.form["select_option"]
    print(f"answer:{answer}")
    responses.append(answer)
    question_index += 1
    print(f"responses: {responses}")
    print(f"question index: {question_index}")
    return redirect(f'/questions/{int(question_index)}')
    