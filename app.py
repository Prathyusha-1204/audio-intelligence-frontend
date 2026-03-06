from flask import Flask, render_template, request
import boto3

app = Flask(__name__)

s3 = boto3.client('s3')

BUCKET_NAME = "audio-input-bucket-sai-us"

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    file = request.files["audio"]

    s3.upload_fileobj(
        file,
        BUCKET_NAME,
        file.filename
    )

    return "File uploaded successfully!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)