import spacy
from spacy.training.example import Example
from intent_training_data import TRAINING_DATA

def train_nlp_model():
    # Create a blank English NLP model
    nlp = spacy.blank("en")

    # Add a text categorizer to the pipeline if not present
    if "textcat" not in nlp.pipe_names:
        textcat = nlp.add_pipe("textcat", last=True)
    else:
        textcat = nlp.get_pipe("textcat")

    # Add labels to the text categorizer
    for intent in {intent_data[1]['intent'] for intent_data in TRAINING_DATA}:
        textcat.add_label(intent)

    # Train the model
    nlp.begin_training()
    for epoch in range(10):  # You can increase the number of epochs for better accuracy
        losses = {}
        for text, annotations in TRAINING_DATA:
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, {"cats": {annotations["intent"]: 1.0}})
            nlp.update([example], losses=losses)
        print(f"Losses at epoch {epoch}: {losses}")

    # Save the trained model
    nlp.to_disk("intent_model")
    print("Model trained and saved to 'intent_model' directory.")

if __name__ == "__main__":
    train_nlp_model()
