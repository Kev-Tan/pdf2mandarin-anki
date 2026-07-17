import argparse
import pymupdf
from pdf_highlight_extractor.reader import extract_highlights
import jieba
import re
import requests

def is_chinese(word):
    # Matches Chinese Unicode block U+4E00 to U+9FFF
    pattern = re.compile(r'^[\u4e00-\u9fff]+$')
    return bool(pattern.match(word))

def extract_words(args):
    highlights = extract_highlights(args.pdf_path)
    extracted_words = []
    
    for h in highlights: 
        word = h['text']
        word = word.strip("\n.")
        if len(word) < 10 and is_chinese(word):
            extracted_words.append(h['text'])
    return extracted_words        
    

def get_sample_sentences(word):
    response = requests.get(word)
    
    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print(f"Error: {response.status_code}")
    

def main():
    parser = argparse.ArgumentParser(description="Process arguments")
    parser.add_argument('--pdf_path', type=str)    
    args = parser.parse_args()
    
    extracted_words = extract_words(args)
        
    print("Number of extracted words: ", len(extracted_words))
    print(extracted_words)

    
    return

if __name__ == "__main__":
    main()