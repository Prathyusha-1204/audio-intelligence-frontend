import os
from flask import Flask, render_template, request, jsonify
import boto3
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

load_dotenv()

app = Flask(__name__)

# Configure AWS clients securely
# If AWS keys are provided (e.g., in a local .env file), use them.
# Otherwise, boto3 will automatically pick up the IAM Role credentials when running on EC2.
s3_client_kwargs = {}
if os.environ.get('AWS_ACCESS_KEY_ID') and os.environ.get('AWS_SECRET_ACCESS_KEY'):
    s3_client_kwargs['aws_access_key_id'] = os.environ.get('AWS_ACCESS_KEY_ID')
    s3_client_kwargs['aws_secret_access_key'] = os.environ.get('AWS_SECRET_ACCESS_KEY')

if os.environ.get('AWS_REGION'):
    s3_client_kwargs['region_name'] = os.environ.get('AWS_REGION')

s3 = boto3.client('s3', **s3_client_kwargs)

BUCKET_NAME = os.environ.get('S3_INPUT_BUCKET_NAME', 'audio-input-bucket-sai-us')

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if 'audio' not in request.files:
        return jsonify({"error": "No file part"}), 400
        
    file = request.files["audio"]
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    if file:
        filename = secure_filename(file.filename)
        try:
            s3.upload_fileobj(
                file,
                BUCKET_NAME,
                filename
            )
            return jsonify({"message": f"File '{filename}' safely vaulted in S3."}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)