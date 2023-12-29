from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from PIL import Image, ImageDraw
import face_recognition
import os


app = Flask(__name__)
upload_folder = os.path.join('static', 'upload')
app.config['UPLOAD'] = upload_folder


@app.route('/result', methods=['GET'])
def show_result():
    person_filename = secure_filename('person.png')
    group_filename = secure_filename('find_in_group.JPG')

    person_image = face_recognition.load_image_file(os.path.join(app.config['UPLOAD'], person_filename))
    group_persons = face_recognition.load_image_file(os.path.join(app.config['UPLOAD'], group_filename))

    person_encodings = face_recognition.face_encodings(person_image)
    face_loc_list = face_recognition.face_locations(group_persons, model='hog')
    all_face_found_encodings = face_recognition.face_encodings(group_persons, face_loc_list)

    pil_image = Image.fromarray(group_persons)
    draw_obj = ImageDraw.Draw(pil_image)

    for idx, person_found in enumerate(all_face_found_encodings):
        result = face_recognition.compare_faces(person_encodings, person_found)

        if result[0]:
            top, right, bottom, left = face_loc_list[idx]
            draw_obj.rectangle([left, top, right, bottom], outline='red', width=5)
            pil_image.save(os.path.join(app.config['UPLOAD'], group_filename))

    return render_template('person_image.html', img=os.path.join(app.config['UPLOAD'], group_filename))


@app.route('/person', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['img']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD'], filename))
        img = os.path.join(app.config['UPLOAD'], filename)
        return render_template('person_image.html', img=img)
    return render_template('person_image.html')


@app.route('/search_files')
def search_files():
    return render_template("search_images.html")


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        files = request.files.getlist('file')
        for file in files:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD'], filename))
        return {
            'files': os.listdir('static/upload')
        }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
