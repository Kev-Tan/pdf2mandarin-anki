import re
import pymupdf

def is_chinese(word):
    # Matches Chinese Unicode block U+4E00 to U+9FFF
    pattern = re.compile(r'^[\u4e00-\u9fff]+$')
    return bool(pattern.match(word))

def is_chinese_sentence(sentence):
    return re.search(r'[\u3400-\u4dbf\u4e00-\u9fff]', sentence) is not None

def extract_chinese_text(pdf_path):
    chinese_sentences = []
    sentences = []
    doc = pymupdf.open(pdf_path)

    for page in doc:
        page_text = page.get_text()
        page_text = page_text.replace('\n', '')

        page_sentences = re.split(r'(?<=[。！？.!?])', page_text)

        sentences.extend(
            sentence.strip()
            for sentence in page_sentences
            if sentence.strip()
        )

    for sentence in sentences:
        if is_chinese_sentence(sentence):
            chinese_sentences.append(sentence)
    
    return chinese_sentences
    