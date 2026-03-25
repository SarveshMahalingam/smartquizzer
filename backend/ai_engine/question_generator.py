import random

from config import Config

try:
    from transformers import pipeline
except Exception:  # pragma: no cover
    pipeline = None

try:
    from openai import OpenAI
except Exception:  # pragma: no cover
    OpenAI = None
class QuestionGenerator:
    def __init__(self):
        self.generator = self._load_hf_pipeline()
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY) if OpenAI and Config.OPENAI_API_KEY else None

    def _load_hf_pipeline(self):
        if Config.LIGHTWEIGHT_MODE:
            return None
        if not pipeline:
            return None
        try:
            return pipeline("text2text-generation", model="google/flan-t5-base")
        except Exception:
            return None

    def _infer_difficulty(self, text):
        words = len((text or "").split())
        if words < 35:
            return "Easy"
        if words < 70:
            return "Medium"
        return "Hard"

    def _distractors(self, keywords, answer):
        pool = [item.title() for item in keywords if item.lower() != answer.lower()]
        pool = list(dict.fromkeys(pool))
        selected = pool[:3]
        while len(selected) < 3:
            selected.append(f"Option {len(selected) + 1}")
        options = selected + [answer]
        random.shuffle(options)
        return options

    def _timer_for_difficulty(self, difficulty):
        if difficulty == "Easy":
            return 120
        if difficulty == "Medium":
            return 140
        return 160

    def _heuristic_questions(self, chunk):
        text = chunk["text"]
        difficulty = self._infer_difficulty(text)
        timer = self._timer_for_difficulty(difficulty)

        keywords = [k for k in (chunk.get("keywords") or []) if k and not any(ch.isdigit() for ch in k)]
        concepts = [c for c in (chunk.get("concepts") or []) if c and not any(ch.isdigit() for ch in c)]
        anchor = (concepts or keywords or ["the main topic"])[0].strip().title()
        keyword_answer = (keywords[0] if keywords else anchor).strip().title()

        # Build MCQ options
        mcq_options = self._distractors(keywords or concepts or [anchor], keyword_answer)
        mcq_options = list(dict.fromkeys(mcq_options))
        if keyword_answer not in mcq_options:
            mcq_options = (mcq_options + [keyword_answer])
        while len(mcq_options) < 4:
            mcq_options.append(f"Option {len(mcq_options)+1}")
        mcq_options = mcq_options[:4]
        random.shuffle(mcq_options)

        def format_q(question_text, answer):
            return {
                "difficulty": difficulty,
                "timer": timer,
                "type": "MCQ",
                "question": question_text.strip()[:220],
                "options": mcq_options,
                "answer": answer,
                "question_type": "MCQ",
                "explanation": f"The passage emphasizes {answer}.",
            }

        questions = []
        main_q = f"What best describes {anchor} based on the passage?"
        questions.append(format_q(main_q, keyword_answer))

        concept_q = f"Which option best relates to {anchor} in this context?"
        questions.append(format_q(concept_q, keyword_answer))

        # Limit to two MCQs per chunk to reduce noise
        return questions

    def _openai_questions(self, text):
        if not self.client:
            return None
        prompt = (
            "Generate four quiz questions from the text: one MCQ, one fill-in-the-blank, "
            "one true/false, and one short answer. Return a JSON array with question, options, "
            "answer, difficulty, question_type, explanation.\n\nText:\n"
            f"{text}"
        )
        try:
            response = self.client.responses.create(
                model=Config.OPENAI_MODEL,
                input=prompt,
                temperature=0.3,
            )
            return response.output_text
        except Exception:
            return None

    def generate(self, chunks):
        generated = []
        for chunk in chunks:
            if not chunk.get("keywords") and not chunk.get("concepts"):
                # still allow fallbacks; we will add generic questions later
                pass
            questions = self._heuristic_questions(chunk)
            for question in questions:
                question["chunk_index"] = chunk["chunk_index"]
                generated.append(question)

        # Fallback: if nothing generated, craft minimal questions from the first chunk
        if not generated and chunks:
            chunk = chunks[0]
            text = chunk["text"]
            anchor = (chunk.get("concepts") or chunk.get("keywords") or ["the topic"])[0].title()
            snippet = text[:140]
            generated.append(
                {
                    "difficulty": self._infer_difficulty(text),
                    "timer": self._timer_for_difficulty(self._infer_difficulty(text)),
                    "type": "MCQ",
                    "question": f"What is the main idea discussed in this passage: {snippet}?",
                    "options": [anchor, "Background context", "Supporting detail", "Irrelevant statement"],
                    "answer": anchor,
                    "question_type": "MCQ",
                    "explanation": f"The passage focuses on {anchor}.",
                    "chunk_index": chunk["chunk_index"],
                }
            )
            generated.append(
                {
                    "difficulty": self._infer_difficulty(text),
                    "timer": self._timer_for_difficulty(self._infer_difficulty(text)),
                    "type": "MCQ",
                    "question": f"Provide one key concept mentioned about {anchor}.",
                    "options": [anchor, "A secondary note", "An unrelated term", "A generic idea"],
                    "answer": anchor,
                    "question_type": "MCQ",
                    "explanation": f"Any core idea about {anchor} is acceptable.",
                    "chunk_index": chunk["chunk_index"],
                }
            )
        return generated
