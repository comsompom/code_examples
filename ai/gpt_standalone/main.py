# pylint: disable=E0401
"""Simple Flask application for using the gpt ai for free"""
from flask import Flask, request, render_template
import g4f


app = Flask(__name__)


def get_response(inp_text: str) -> str:
    """Internal method for getting response"""
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4,
        messages=[{'role': 'user', 'content': inp_text}]
    )
    return response


@app.route('/result', methods=['GET', 'POST'])
def show_result():
    """The Flask route to get the result. Use the GET and POST"""
    gpt_answer = ""
    if request.method == 'POST':
        gpt_answer = get_response(request.form['text'])
    return render_template('result_answer.html', gpt_answer=gpt_answer)


@app.route('/chat', methods=['POST'])
def simple_chat():
    """Flask route to get the answer from the user question. Using the POST"""
    user_mes = request.get_json().get("user_chat", "")
    gpt_answer = get_response(user_mes)
    return {
        "gpt_answer": gpt_answer
    }


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
