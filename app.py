from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from resume_parser import extract_text_from_pdf, extract_docx_text
from job_desc_extract import extract_jd_keywords
from ats_match_logic import keyword_match_score

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/links')
def links():
    return render_template('links.html')

@app.route('/portfolio')
def portfolio():
    return "<h1>Portfolio page coming soon</h1>"

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        jd_text = request.form.get('jd')
        resume_file = request.files.get('resume')

        if not jd_text or not resume_file:
            return jsonify({"error": "Missing inputs"}), 400

        if resume_file.filename.endswith('.pdf'):
            resume_text = extract_text_from_pdf(resume_file)
        elif resume_file.filename.endswith('.docx'):
            resume_text = extract_docx_text(resume_file)
        else:
            return jsonify({"error": "Unsupported file format"}), 400

        jd_keywords = extract_jd_keywords(jd_text)
        result = keyword_match_score(jd_keywords, resume_text)

        return jsonify(result)

    except Exception as e:
        print("🔥 BACKEND ERROR:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
