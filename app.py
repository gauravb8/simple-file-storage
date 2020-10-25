from datetime import datetime
from boto3 import client
from flask import Flask, request
from werkzeug.utils import secure_filename
import boto3
import time

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'txt', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4'}
s3 = boto3.resource('s3')

def build_new_filename(client_filename):
	client_filename = secure_filename(client_filename)
	name, extension = client_filename.rsplit('.', 1) if '.' in client_filename else (None, None)
	print(name, extension)
	if extension and extension in ALLOWED_EXTENSIONS:
		return '{}_{}.{}'.format(name, datetime.strftime(datetime.now(), "%d%m%Y%H%M%S"), extension)


@app.route('/list', methods=['GET'])
def get_files_list():
	bucket = s3.Bucket('simple-file-storage-app-bucket')
	return ', '.join(item.key for item in bucket.objects.all())

@app.route('/upload', methods=['POST'])
def upload_file_to_s3():
	start = time.time()
	bucket = s3.Bucket('simple-file-storage-app-bucket')
	image_obj = request.files['image']
	print('Old name:', image_obj.filename)
	# [print(bucket.name) for bucket in s3.buckets.all()]
	new_name = build_new_filename(image_obj.filename)
	print(new_name)
	if new_name:
		print('Starting upload to s3')
		s3.upload_fileobj(image_obj, new_name)
		print('Finished upload')
		print('Turn around time: {} seconds'.format(time.time()-start))
		return 'Hello, World!'
	return 'Failed. File format not supported!'
