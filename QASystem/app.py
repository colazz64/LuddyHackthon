from flask import Flask, request, jsonify, render_template
from transformers import pipeline
import pdfplumber
import os
import re

# Initialize Flask app
app = Flask(__name__)

# Load models for summarization and Q&A
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
qa_pipeline = pipeline("question-answering")

# Function to extract text from PDF
def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Route for the homepage
@app.route('/')
def home():
    return render_template('index.html')

# Route for document summarization
@app.route('/summarize', methods=['POST'])
def summarize():
    file = request.files['document']
    file_path = os.path.join("uploads", file.filename)
    file.save(file_path)
    
    # Extract text from the uploaded PDF
    text = extract_text_from_pdf(file_path)
    
    # Generate summary (truncate input for model limits)
    summary = summarizer(text[:1000], max_length=130, min_length=30, do_sample=False)[0]['summary_text']
    
    return jsonify({"summary": summary})

# Route for Q&A
@app.route('/qa', methods=['POST'])
def question_answering():
    data = request.json
    question = data['question']
    context = data['context']

    # Search for all tasks explicitly (e.g., "Task 1", "Task 2")
    if "task" in question.lower():
        tasks = re.findall(r"(Task \d+: .*?)(?:\n|$)", context)
        if tasks:
            # Format tasks as a bulleted list for better readability
            formatted_tasks = "\n".join(f"- {task}" for task in tasks)
            return jsonify({"answer": formatted_tasks})

    # Default Q&A pipeline
    answer = qa_pipeline(question=question, context=context)
    return jsonify({"answer": answer['answer']})

if __name__ == '__main__':
    # Create uploads folder if it doesn't exist
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    
    # Run the app on port 5500
    app.run(debug=True, port=5500)
