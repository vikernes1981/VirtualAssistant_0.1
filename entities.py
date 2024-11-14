import spacy
from dotenv import load_dotenv
import os
from wit import Wit
from speech import current_language

load_dotenv()

WIT_API_KEY = os.getenv('WIT_API_KEY')
wit_client = Wit(WIT_API_KEY)

nlp_entity_en = spacy.load('en_core_web_sm')  # For English entity extraction (NER)
nlp_entity_gr = spacy.load('el_core_news_sm')  # For Greek entity extraction (NER)
nlp_intent = spacy.load("intent_model")  # Custom model for intent recognition

def extract_entities(text):
    if current_language == 'en':
        doc = nlp_entity_en(text)
    else:
        doc = nlp_entity_gr(text)
        
    entities = {}
    for ent in doc.ents:
        entities[ent.label_] = entities.get(ent.label_, []) + [ent.text]
    return entities

def predict_intent(text):
    response = wit_client.message(text)
    intent = response['intents'][0]['name'] if response['intents'] else None
    return intent