from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models.user import User
from flask_app.models.landlord import Landlord
from flask_app.models.review import Review
from flask_bcrypt import Bcrypt
from datetime import datetime
from werkzeug.utils import secure_filename
import os


UPLOAD_FOLDER = 'flask_app/static/uploads/' # Folder where image is stored
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 640 * 640
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/review')
def review():
    return render_template('review.html')

@app.route('/review', methods=['POST'])
def upload_image():
	if 'file' not in request.files:
		flash('No file part')
		return redirect('review.html')
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect('review.html')
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		#print('upload_image filename: ' + filename)
		flash('Image successfully uploaded and displayed below')
		return render_template('review.html', filename=filename)
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect('review.html')

@app.route('/review/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)








@app.route('/create/review/<int:landlord_id>', methods = ['POST'])
def create_review_for_landlord(landlord_id):



    if 'file' not in request.files:
        flash('No file part')

    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')






    active_user = User.get_user_by_id({'id': session['user']})
    try:
        review_data = {
            'landlord_id': landlord_id,
            'user_id': session['user'],
            'rating': request.form['rating'],
            'text': request.form['review'],
            'file_location': file.filename
        }
    except KeyError:
        review_data = {
            'landlord_id': landlord_id,
            'user_id': session['user'],
            'rating': 0,
            'text': request.form['review'],
            'file_location': file.filename
        }
    review_added = Review.save(review_data)
    return redirect('/landlord/' + str(landlord_id))
