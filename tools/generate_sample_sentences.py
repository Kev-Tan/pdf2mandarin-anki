import requests
from .generate_audio import generate_audio
from urllib.parse import quote

async def retrieve_sample_sentences(word):
    url = f"https://api.tatoeba.org/v1/sentences?lang=cmn&q={quote(word)}&sort=relevance&limit=25"
    response = requests.get(url)
    
    if response.status_code == 200:
        res = response.json()
        
        try:
            for i, potential_sentence in enumerate(res["data"]):
                print(i)
                sentence_text = potential_sentence["text"]
                if word in sentence_text:
                    sentence_id = res["data"][0]["id"]
                    destination_path = f"D:/Personal/Mandarin/python_extract/trial_audio/{sentence_id}.mp3"
                    print(f"Text: {sentence_text}")
                    return sentence_text
                
            return False
                    
        except Exception as e:
            print(f"Something went wrong: {e}")
            
    else:
        print(f"Error: {response.status_code}")