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
