from flask import Flask, render_template, request
from dotenv import load_dotenv
from gemini_service import review_code
import os

# Load environment variables
load_dotenv()

# Debug: Print the first 10 characters of the API key
key = os.getenv("GEMINI_API_KEY")

if key:
    print("===================================")
    print("Loaded API Key:", key[:10] + "...")
    print("===================================")
else:
    print("===================================")
    print("ERROR: GEMINI_API_KEY NOT FOUND!")
    print("===================================")

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/review", methods=["POST"])
def review():

    language = request.form.get("language")
    code = request.form.get("code")

    review = review_code(language, code)

    return render_template(
        "index.html",
        language=language,
        code=code,
        review=review
    )


if __name__ == "__main__":
    app.run(debug=True)