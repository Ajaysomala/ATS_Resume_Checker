# ats_match_logic.py

import re
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

ps = PorterStemmer()
tokenizer = RegexpTokenizer(r'\w+')

def clean_and_stem(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    tokens = tokenizer.tokenize(text)
    return [ps.stem(token) for token in tokens]

def keyword_match_score(jd_keywords, resume_text):
    resume_tokens = clean_and_stem(resume_text)
    jd_tokens = clean_and_stem(" ".join(jd_keywords))

    matched = list(set(jd_tokens) & set(resume_tokens))
    unmatched = list(set(jd_tokens) - set(resume_tokens))
    match_score = round((len(matched) / len(jd_tokens)) * 100, 2) if jd_tokens else 0.0

    return {
        "match_score": match_score,
        "matched_keywords": matched,
        "unmatched_keywords": unmatched
    }

# ats_weighted_score.py

ps = PorterStemmer()

SECTION_WEIGHTS = {
    "summary": 1.5,
    "experience": 2.0,
    "projects": 2.5,
    "skills": 2.5,
    "education": 1.0
}

def clean_and_stem(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    # ✅ Fixes punkt_tab error:
    tokens = word_tokenize(text, preserve_line=True)
    return [ps.stem(token) for token in tokens]

def split_resume_sections(resume_text):
    sections = {
        "summary": "",
        "experience": "",
        "projects": "",
        "skills": "",
        "education": ""
    }

    current_section = None
    for line in resume_text.split("\n"):
        line = line.strip().lower()
        if "summary" in line:
            current_section = "summary"
        elif any(word in line for word in ["experience", "internship"]):
            current_section = "experience"
        elif "project" in line:
            current_section = "projects"
        elif "skill" in line:
            current_section = "skills"
        elif "education" in line:
            current_section = "education"

        if current_section:
            sections[current_section] += line + " "

    return sections

def weighted_keyword_score(jd_keywords, resume_text):
    resume_sections = split_resume_sections(resume_text)
    jd_tokens = clean_and_stem(" ".join(jd_keywords))

    matched_total = 0
    unmatched_tokens = []
    match_details = {}

    total_weighted_keywords = 0

    for section, text in resume_sections.items():
        section_tokens = clean_and_stem(text)
        weight = SECTION_WEIGHTS.get(section, 1.0)

        matched = list(set(jd_tokens) & set(section_tokens))
        unmatched = list(set(jd_tokens) - set(section_tokens))

        match_details[section] = {
            "matched": matched,
            "unmatched": unmatched,
            "weight": weight
        }

        matched_total += len(matched) * weight
        total_weighted_keywords += len(jd_tokens) * weight

    score = round((matched_total / total_weighted_keywords) * 100, 2) if total_weighted_keywords else 0.0

    return {
        "match_score": score,
        "details": match_details,
        "total_keywords": len(jd_tokens)
    } 

