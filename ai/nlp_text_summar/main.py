from flask import Flask, request, render_template
from summarizer import extract_text_from_url, summerize_text


app = Flask(__name__)
url = "https://en.wikipedia.org/wiki/Natural_language_processing"


@app.route('/result', methods=['GET', 'POST'])
def show_result():
    inp_text = ""
    input_text = extract_text_from_url(url)
    if request.method == 'POST':
        inp_text = request.form['text']
    if inp_text:
        input_text = extract_text_from_url(inp_text)
    summary = summerize_text(input_text)
    return render_template('result_summeraze.html', summary=summary)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
