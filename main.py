# main.py
import os
import uuid
from datetime import timedelta

from flask import Flask, render_template, request, redirect, url_for
from google.cloud import storage

app = Flask(__name__)

# Configure Google Cloud Storage
BUCKET_NAME = os.environ.get("BUCKET_NAME")  # Replace with your bucket name
storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)

def get_signed_url(blob_name):
    """Generates a signed URL for a GCS object."""
    blob = bucket.blob(blob_name)
    url = blob.generate_signed_url(
        version="v4",
        # This URL is valid for 1 minutes
        expiration=timedelta(minutes=1),
        # Allow GET requests using this URL.
        method="GET",
    )
    return url

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)

        file = request.files["file"]

        if file.filename == "":
            return redirect(request.url)

        if file:
            blob_name = f"{uuid.uuid4()}-{file.filename}" # generate a unique filename
            blob = bucket.blob(blob_name)
            blob.upload_from_file(file)
            return redirect(url_for("index"))

    # Retrieve all blobs and generate signed URLs
    blobs = bucket.list_blobs()
    images = [{"name": blob.name, "url": get_signed_url(blob.name)} for blob in blobs]

    return render_template("index.html", images=images)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))