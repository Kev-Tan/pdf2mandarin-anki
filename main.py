import argparse
from tools.extract_words import extract_words
from tools.generate_sample_sentences import retrieve_sample_sentences_tatoeba
from tools.misc import is_chinese_sentence
import asyncio
from pypdf import PdfReader
from tools.misc import extract_chinese_text
import re
import pymupdf
import json


def main():
    
    parser = argparse.ArgumentParser(description="Process arguments")
    parser.add_argument('--pdf_path', type=str)
    parser.add_argument('--page_start', type=int)
    parser.add_argument('--page_end', type=int)
    args = parser.parse_args()
    
    extracted_words = extract_words(args)
    original_text = extract_chinese_text(args.pdf_path)
    
    word_sentence_pair = []
    
    for word in extracted_words:
        print(word)
        sentence_to_be_appended = []
        for index, sentence in enumerate(original_text):
            if word in sentence:
                sentence_to_be_appended.append(sentence)
        word_sentence_pair.append({
            "word": word,
            "sentence": sentence_to_be_appended
        })
    
    print(word_sentence_pair)
    with open("word_sentence_pairs.json", "w", encoding="utf-8") as file:
        json.dump(word_sentence_pair, file, ensure_ascii=False, indent=2)
    

if __name__ == "__main__":
    main()