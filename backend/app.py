import os
from flask import Flask, request, jsonify
from flask_cors import CORS

from pdf_utils import extract_text_from_pdf
from gemini_utils import (
    generate_structure,
    json_to_mermaid
)

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return {
        "message": "Backend Running"
    }


@app.route("/generate", methods=["POST"])
def generate_diagram():

    try:

        body = request.get_json()

        if not body:
            return jsonify({
                "error": "Invalid request body."
            }), 400

        text = body.get("text", "").strip()

        if not text:
            return jsonify({
                "error": "Input text cannot be empty."
            }), 400

        workflow = generate_structure(text)

        mermaid = json_to_mermaid(workflow)

        return jsonify({
            "workflow": workflow,
            "mermaid": mermaid
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


@app.route("/generate-pdf", methods=["POST"])
def generate_pdf_diagram():

    try:

        if "pdf" not in request.files:
            return jsonify({
                "error": "No PDF uploaded."
            }), 400

        file = request.files["pdf"]

        text = extract_text_from_pdf(file)

        if not text.strip():
            return jsonify({
                "error": "No readable text found in PDF."
            }), 400

        workflow = generate_structure(text)

        mermaid = json_to_mermaid(workflow)

        return jsonify({
            "workflow": workflow,
            "mermaid": mermaid
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )