from datetime import datetime
from boto3 import client
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
import boto3
import time

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'txt', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mp3'}
s3 = boto3.resource('s3', region_name='ap-south-1')
client = boto3.client('s3', region_name='ap-south-1')
BUCKET_NAME = 'simple-file-storage-app-bucket'

def build_new_filename(client_filename):
	client_filename = secure_filename(client_filename)
	name, extension = client_filename.rsplit('.', 1) if '.' in client_filename else (None, None)
	print(name, extension)
	if extension and extension in ALLOWED_EXTENSIONS:
		return client_filename
		# return '{}_{}.{}'.format(name, datetime.strftime(datetime.now(), "%d%m%Y%H%M%S"), extension)

@app.route('/')
def serve_home_page():
	return render_template("index.html")

@app.route('/list', methods=['GET'])
def get_files_list():
	bucket = s3.Bucket(BUCKET_NAME)
	keys = [item.key for item in bucket.objects.all()]
	return jsonify(result={
		'filenames':keys
		})

@app.route('/download/<filename>')
def view_file(filename):
	return jsonify(result={
		'url': 	client.generate_presigned_url(
					'get_object',
					{'Bucket': BUCKET_NAME, 'Key': filename},
					ExpiresIn=600,
                    HttpMethod='GET'
				)
	})

@app.route('/upload', methods=['POST'])
def upload_file_to_s3():
	app.logger.debug(request)
	app.logger.debug(request.files)
	start = time.time()
	bucket = s3.Bucket('simple-file-storage-app-bucket')
	# image_obj = request.files['image']
	files = request.files.getlist("images")
	for file_obj in files:
		app.logger.debug('Old name: {}'.format(file_obj.filename))
		# [app.logger.debug(bucket.name) for bucket in s3.buckets.all()]
		new_name = build_new_filename(file_obj.filename)
		app.logger.debug(new_name)
		if new_name:
			app.logger.debug("Uploading file {} to S3...".format(file_obj.filename))
			bucket.upload_fileobj(file_obj, new_name)
			app.logger.debug('Finished upload')
	app.logger.debug('Total time taken: {} seconds'.format(time.time()-start))
	
	return jsonify(result="Success! {} files uploaded successfully".format(len(files)))
