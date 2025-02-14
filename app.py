import gradio as gr
import llmConnect
import csv
from dotenv import load_dotenv
import os 


def generate_questions(topic):
    llmConnect.addToDataset(topic)

def readDataset():
    with open('dataset.csv', 'r') as file:
        data = list(csv.reader(file))
        return data

def getFirstQuestion(topic):
    generate_questions(topic)
    data = readDataset()
    question = data[0][1]
    answers = data[0][2:6]
    return question, gr.update("answer",choices=answers)

def nextQuestion(question_no):
    data = readDataset()
    if question_no < len(data):
        question = data[question_no][1]
        answers = data[question_no][2:6]
        return question, gr.update("answer",choices=answers)
    return "Quiz completed!", gr.update("answer",choices=["Quiz completed"])

with gr.Blocks() as demo:
    # Initialize states
    user_answers = gr.State([])
    question_no = gr.State(0)
    
    with gr.Row():
        with gr.Column():
            topic = gr.Textbox(
                label="Topic",
                placeholder="Enter the topic you want to generate questions for"
            )
            submit = gr.Button(value="Generate Questions")
            
        with gr.Column():
            question = gr.Textbox(label="Question", elem_id="question")
            answer = gr.Dropdown(
                label="Answer",
                interactive=True,
                elem_id="answer",
                multiselect=False,
                allow_custom_value=False,
                filterable=False
            )
            
            def handle_next(ans, answers, q_no):
                # Store the answer
                answers.append(ans)
                # Increment question number
                next_q_no = q_no + 1
                # Get next question
                question, new_answers = nextQuestion(next_q_no)
                return question, new_answers, answers, next_q_no

            next = gr.Button(value="Next Question")
            next.click(
                handle_next,
                inputs=[answer, user_answers, question_no],
                outputs=[question, answer, user_answers, question_no]
            )

        submit.click(
            getFirstQuestion,
            inputs=[topic],
            outputs=[question, answer]
        )

        with gr.Column():
            score = gr.Textbox(
                label="Score",
                placeholder="Your score will be displayed here"
            )
            
            def calculate_score(answers):
                data = readDataset()
                correct_answers = []
                for i in range(len(data)):
                    correct_answers.append(data[i][1+int(data[i][6])])
                score = sum(1 for a, c in zip(answers, correct_answers) if a == c)
                return f"Your score: {score}/{len(answers)}"

            submit_score = gr.Button(value="Submit")
            submit_score.click(
                calculate_score,
                inputs=[user_answers],
                outputs=[score]
            )

demo.launch()