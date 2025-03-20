from flask import Flask, render_template, request
import finder
import subprocess

def ensure_dependencies():
    try:
        import flask
        import boto3
        import botocore
        import dotenv
    except ImportError:
        print("Missing dependencies detected. Installing...")
        subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)

# Install dependencies before importing
ensure_dependencies()

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    file_name = None
    if request.method == "POST":
        file_name = request.form["file_name"]
        print(f"Searching for file: {file_name}")
        url = finder.search_and_download_file(file_name)
        if url:
            return render_template("index2.html", file_name=file_name, url=url)
    return render_template("index.html", file_name=file_name)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
