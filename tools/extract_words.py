import argparse
import pymupdf
from pdf_highlight_extractor.reader import extract_highlights
import jieba
import re
import requests
import edge_tts
from pathlib import Path

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


    
    