# ats_match_logic.py

import re
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import wordnet


ps = PorterStemmer()
tokenizer = RegexpTokenizer(r'\w+')

def clean_and_stem(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    tokens = tokenizer.tokenize(text)
    return [ps.stem(token) for token in tokens]

def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().lower())
    return synonyms

def keyword_match_score(jd_keywords, resume_text):
    resume_tokens = clean_and_stem(resume_text)
    jd_tokens = clean_and_stem(" ".join(jd_keywords))

    matched = []
    unmatched = []

    for token in jd_tokens:
        if token in resume_tokens:
            matched.append(token)
        else:
            synonyms = get_synonyms(token)
            if any(syn in resume_tokens for syn in synonyms):
                matched.append(token + "*")  # partial match via synonym
            else:
                unmatched.append(token)

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
    tokens = tokenizer.tokenize(text)
    return [ps.stem(token) for token in tokens]

def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().lower())
    return synonyms

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

        if re.search(r'\bsummary\b', line):
            current_section = "summary"
        elif re.search(r'\b(experience|internship)\b', line):
            current_section = "experience"
        elif re.search(r'\bprojects?\b', line):
            current_section = "projects"
        elif re.search(r'\bskills?\b', line):
            current_section = "skills"
        elif re.search(r'\beducation\b', line):
            current_section = "education"

        if current_section:
            sections[current_section] += line + " "

    return sections

def weighted_keyword_score(jd_keywords, resume_text):
    resume_sections = split_resume_sections(resume_text)
    jd_tokens = clean_and_stem(" ".join(jd_keywords))

    matched_total = 0
    total_weighted_keywords = 0
    match_details = {}

    for section, text in resume_sections.items():
        section_tokens = clean_and_stem(text)
        weight = SECTION_WEIGHTS.get(section, 1.0)

        matched = []
        unmatched = []

        for token in jd_tokens:
            if token in section_tokens:
                matched.append(token)
            else:
                synonyms = get_synonyms(token)
                if set(synonyms) & set(section_tokens):
                    matched.append(token + "*")  # synonym match
                else:
                    unmatched.append(token)

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
