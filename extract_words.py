import argparse
import pymupdf
from pdf_highlight_extractor.reader import extract_highlights
import jieba
import re
import requests
from urllib.parse import quote
import edge_tts
import asyncio
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

async def generate_audio(text, destination_path, rate="-15%"):
    Path(destination_path).parent.mkdir(parents=True, exist_ok=True)
    communicate = edge_tts.Communicate(text, "zh-TW-YunJheNeural", rate = rate)
    await communicate.save(destination_path)
    
async def get_sample_sentences(word):
    url = f"https://api.tatoeba.org/v1/sentences?lang=cmn&q={quote(word)}&sort=relevance&limit=25"
    response = requests.get(url)
    
    if response.status_code == 200:
        res = response.json()
        
        try:
            for i, sentence in enumerate(res["data"]):
                print(i)
                text = sentence["text"]
                if word in text:
                    sentence_id = res["data"][0]["id"]
                    destination_path = f"D:/Personal/Mandarin/python_extract/trial_audio/{sentence_id}.mp3"
                    print(f"Text: {text}")
                    await generate_audio(text, destination_path)
                    
        except Exception as e:
            print(f"Something went wrong: {e}")
            
    else:
        print(f"Error: {response.status_code}")
    
    

def main():
    parser = argparse.ArgumentParser(description="Process arguments")
    parser.add_argument('--pdf_path', type=str)    
    args = parser.parse_args()
    
    extracted_words = extract_words(args)
    
    for word in extracted_words:
        print(word)
        asyncio.run(get_sample_sentences(word))
        
    print("Number of extracted words: ", len(extracted_words))
    print(extracted_words)

    
    return

if __name__ == "__main__":
    main()