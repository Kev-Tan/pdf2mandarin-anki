import argparse
import pymupdf
from pdf_highlight_extractor.reader import extract_highlights
import jieba
import re
import requests
import edge_tts
from pathlib import Path
from .misc import is_chinese



def extract_words(args):
    highlights = extract_highlights(args.pdf_path)
    extracted_words = []
    
    for h in highlights: 
        word = h['text']
        word = word.strip("\n.")
        if len(word) < 10 and is_chinese(word):
            extracted_words.append(h['text'])
    return extracted_words


    
    