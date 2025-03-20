# S3_finder
A Flask-based web application that allows users to search for files stored in AWS S3 and generate pre-signed download links
Flask S3 File Finder 🔍

🚀 Features
✅ Search for files in an S3 bucket
✅ Generate pre-signed URLs for secure file downloads
✅ Built using Flask & Boto3 for AWS S3 integration
✅ Secure authentication using environment variables
✅ Lightweight & fast – Easy to deploy with Docker 

🌐 How It Works
1️⃣ User enters a filename into the search form
2️⃣ App checks AWS S3 for the file
3️⃣ If file exists:

A download link (pre-signed URL) is displayed
4️⃣ If file does not exist:
A message prompts the user to search again
