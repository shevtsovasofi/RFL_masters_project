import re
import spacy
import ruts
from evaluate import load
import pymorphy3

class TextValidator:
    def __init__(self, spacy_model="ru_core_news_sm"):
        self.nlp = spacy.load(spacy_model)
        self.morph = pymorphy3.MorphAnalyzer()
        self.bertscore_metric = load("bertscore")

        self.abstract_suffixes = ["ость", "ение", "ание", "изм", "ция", "ство", "ность", "ие"]
  

    def calculate_base_metrics(self, text: str) -> dict:
        if not text.strip():
            return {}
        
        bs = ruts.BasicStats(text)
        stats = bs.get_stats()
        
        words = re.findall(r'[а-яА-ЯёЁ]+', text.lower())
        total_words = len(words)

        abs_count = sum(1 for word in words if any(word.endswith(suffix) for suffix in self.abstract_suffixes))
        abstract_percent = (abs_count / total_words) * 100 if total_words > 0 else 0

        return {
        "n_words": total_words,
            "n_unique_words": stats.get("n_unique_words", 0),
            "avg_word_length": (sum(len(w) for w in words) / total_words) if total_words > 0 else 0,
            "abstract_percent": abstract_percent
        }

    def analyze_morphology_and_syntax(self, text: str) -> dict:
        
        doc = self.nlp(text)
        words = [t for t in doc if not t.is_punct and not t.is_space]
        total_words = len(words)
        
        if total_words == 0:
            return {
                "gent_frequency_per_1000": 0.0,
                "indirect_cases_share": 0.0,
                "participial_turns": 0,
                "adverbial_participial_turns": 0
            }

        # Считаем родительный падеж (Gent)
        gent_count = sum(1 for t in words if "Case=Gen" in str(t.morph))
        
        # Поиск именных частей речи для подсчета косвенных падежей
        nouns_and_pronouns = [t for t in words if t.pos_ in ["NOUN", "PRON", "PROPN"]]
        indirect_count = sum(1 for t in nouns_and_pronouns if "Case=Nom" not in str(t.morph))
        
        # Поиск причастий (VerbForm=Part) и деепричастий (VerbForm=Conv)
        verbal_adjectives = sum(1 for t in words if "VerbForm=Part" in str(t.morph))
        transverbals = sum(1 for t in words if "VerbForm=Conv" in str(t.morph))
        
        return {
            "gent_frequency_per_1000": (gent_count / total_words) * 1000,
            "indirect_cases_share": (indirect_count / len(nouns_and_pronouns) * 100) if nouns_and_pronouns else 0,
            "participial_turns": verbal_adjectives,
            "adverbial_participial_turns": transverbals
        }   
    def calculate_readability_metrics(self, text: str) -> dict:
        if not text.strip():
            return {}
            
        rd = ruts.ReadabilityStats(text)
        readability_stats = rd.get_stats()
        
        return {
            "flesch_kincaid": readability_stats.get("flesch_kincaid_grade", 0),
            "smog": readability_stats.get("smog", 0),
            "flesch_reading_ease": readability_stats.get("flesch_reading_ease", 0)  
        }
    def calculate_diversity_metrics(self, text: str) -> dict:
        """Расчет лексического разнообразия текста (TTR, MATTR, MTLD) из библиотеки ruts"""
        if not text.strip():
            return {}
            
        # Используем ruts.DiversityStats для вычисления разнообразия словаря
        ds = ruts.DiversityStats(text)
        diversity_stats = ds.get_stats()
        
        return {
            "ttr": diversity_stats.get("ttr", 0),
            "mattr": diversity_stats.get("mattr", 0),
            "mtld": diversity_stats.get("mtld", 0)
        }
    
    def calculate_bertscore(self, original_text: str, simplified_text: str) -> float:
        results = self.bertscore_metric.compute(
            predictions=[simplified_text], 
            references=[original_text], 
            lang="ru"
        )
        return results["precision"][0]
    