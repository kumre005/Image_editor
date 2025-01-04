# pip install flask ovencv-python

from flask import Flask
from flask import render_template, request, flash
from werkzeug.utils import secure_filename
import os
import cv2

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'webp', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    # Process the image
def processImage(filename, operation):
    print(f'The operation is {operation} and the file is {filename}')
    img = cv2.imread(f'uploads/{filename}')
    match operation:
        case "cgrey":
            imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            new_filename = f'static/{filename}'
            cv2.imwrite(f'static/{filename}', imgProcessed)
            return new_filename
        case "cwebp":
            new_filename = f'static/{filename.split('.')[0]}.webp'
            cv2.imwrite(new_filename, img)

            return new_filename
        case "cjpg":
            new_filename = f'static/{filename.split('.')[0]}.jpg'
            cv2.imwrite(new_filename, img)

            return new_filename
        case "cpng":
            new_filename = f'static/{filename.split('.')[0]}.png'
            cv2.imwrite(new_filename, img)

            return new_filename
    pass
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/edit", methods = ['POST', 'GET'])
def edit():
    if request.method == 'POST':
        
        operation = request.form.get('operation')
          # check if the post request has the file part
        
        if 'file' not in request.files:
            flash('No file part')
            return "error"
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "redirect(request.url)"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new = processImage(filename, operation)
            flash(f"File {filename} proccessed successfully. <a href='/{new}' target='_blank'> Download here</a>") 

            return render_template("index.html")

    return render_template("index.html")

app.run(debug = True, port = 5000)

