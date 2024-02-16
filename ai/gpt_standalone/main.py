from flask import Flask, request, render_template
import g4f


app = Flask(__name__)


def get_response(inp_text: str) -> str:
    response = g4f.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'user', 'content': inp_text}]
    )
    return response


@app.route('/result', methods=['GET', 'POST'])
def show_result():
    gpt_answer = ""
    if request.method == 'POST':
        gpt_answer = get_response(request.form['text'])
    return render_template('result_answer.html', gpt_answer=gpt_answer)


@app.route('/chat', methods=['POST'])
def simple_chat():
    user_mes = request.get_json().get("user_chat", "")
    gpt_answer = get_response(user_mes)
    return {
        "gpt_answer": gpt_answer
    }


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)