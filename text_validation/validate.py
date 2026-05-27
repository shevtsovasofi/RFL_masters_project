import sys
import os
import pandas as pd

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.metrics import TextValidator
from src.plots import save_metrics_plot

def main():
    validator = TextValidator()
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    
    orig_path = os.path.join(project_root, "data", "original.txt")
    simp_path = os.path.join(project_root, "data", "simplified.txt")
    
    if not os.path.exists(orig_path) or not os.path.exists(simp_path):
        print(f"Error: One or both text files not found\n1) {orig_path}\n2) {simp_path}")
        return

    # Чтение текстов
    with open(orig_path, "r", encoding="utf-8") as f:
        orig_text = f.read()
    with open(simp_path, "r", encoding="utf-8") as f:
        simp_text = f.read()

    print("📊 Расчет всех лингвистических параметров...")
    
    orig_base = validator.calculate_base_metrics(orig_text)
    simp_base = validator.calculate_base_metrics(simp_text)
    
    orig_morph = validator.analyze_morphology_and_syntax(orig_text)
    simp_morph = validator.analyze_morphology_and_syntax(simp_text)
    
    orig_read = validator.calculate_readability_metrics(orig_text)
    simp_read = validator.calculate_readability_metrics(simp_text)
    
    orig_div = validator.calculate_diversity_metrics(orig_text)
    simp_div = validator.calculate_diversity_metrics(simp_text) 
    
    orig_total = {**orig_base, **orig_morph, **orig_read, **orig_div}
    simp_total = {**simp_base, **simp_morph, **simp_read, **simp_div}

    print("🧠 Расчет BERTScore семантического соответствия...")
    bert_precision = validator.calculate_bertscore(orig_text, simp_text)

    all_metric_labels = {
        "n_words": "Number of Words",
        "avg_word_length": "Average Word Length",
        "abstract_percent": "Abstract Lexicon Percentage",
        "gent_frequency_per_1000": "Genitive Case Frequency (per 1000 words)",
        "indirect_cases_share": "Share of Indirect Cases (%)",
        "participial_turns": "Participial Turns (count)",
        "adverbial_participial_turns": "Adverbial Participial Turns (count)",
        "flesch_kincaid": "Flesch-Kincaid Grade Level",
        "flesch_reading_ease": "Flesch Reading Ease Score",
        "smog": "SMOG Index",
        "ttr": "Type-Token Ratio (TTR)",
        "mattr": "Moving-Average TTR (MATTR)",
        "mtld": "Measure of Textual Lexical Diversity (MTLD)"
    }
    
    table_data = []
    for key, label in all_metric_labels.items():
        table_data.append({
            "Parameter": label,
            "Original Lecture": orig_total.get(key, 0),
            "Simplified Text": simp_total.get(key, 0)
        })
        
    results_df = pd.DataFrame(table_data)
    
    print("\n" + "="*65)
    print("Results:")
    print(results_df.to_string(index=False))
    print(f"\nBERTScore (Precision): {bert_precision:.4f}")
    print("="*65)

    save_metrics_plot(orig_total, simp_total, output_dir="images")

if __name__ == "__main__":
    main()