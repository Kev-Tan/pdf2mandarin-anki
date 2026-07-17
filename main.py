import argparse
from tools.extract_words import extract_words
from tools.generate_sample_sentences import retrieve_sample_sentences
import asyncio

def main():
    parser = argparse.ArgumentParser(description="Process arguments")
    parser.add_argument('--pdf_path', type=str)    
    args = parser.parse_args()
    
    extracted_words = extract_words(args)
    
    for word in extracted_words:
        print(word)
        asyncio.run(retrieve_sample_sentences(word))
        
    print("Number of extracted words: ", len(extracted_words))
    print(extracted_words)

    
    return

if __name__ == "__main__":
    main()