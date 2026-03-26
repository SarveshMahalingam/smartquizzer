import random
import spacy

nlp = spacy.load("en_core_web_sm")

def generate_mcq(sentence, global_keywords, difficulty="Medium"):
    doc = nlp(sentence)

    keywords = [token.text for token in doc if token.pos_ in ["NOUN", "PROPN", "ADJ"]]

    if not keywords:
        return None

    correct = random.choice(keywords)

    distractors = list(set(global_keywords) - {correct})

    if len(distractors) < 3:
        return None

    options = random.sample(distractors, 3)
    options.append(correct)
    random.shuffle(options)

    return {
        "question": sentence.replace(correct, "_____"),
        "options": options,
        "answer": correct,
        "difficulty": difficulty
    }