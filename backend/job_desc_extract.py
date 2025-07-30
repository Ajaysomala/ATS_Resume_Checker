import re

def extract_jd_keywords(text):
    # Basic cleanup
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # remove punctuation

    # Common stopwords to ignore
    stopwords = set([
        "the", "and", "to", "a", "in", "for", "with", "of", "on", "is", "at", 
        "as", "by", "an", "be", "from", "or", "that", "this", "are", "we", "you"
    ])

    words = text.split()
    keywords = [word for word in words if word not in stopwords and len(word) > 2]

    return list(set(keywords))  # unique keywords


file3_path = r"D:\100%Workouts\ATS_Resume_Folder\documents\jd_text.txt"

with open(file3_path, 'r', encoding='utf-8') as f:
    jd_text = f.read()

jd_keywords = extract_jd_keywords(jd_text)

# print("Extracted JD Keywords:", jd_keywords)
# print("Total Keywords:", len(jd_keywords))