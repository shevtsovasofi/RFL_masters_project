import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def save_metrics_plot(orig_metrics: dict, simp_metrics: dict, output_dir="images"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    data = []
    metrics_to_plot = {
        'avg_word_length': 'Avg. Word Length',
        'abstract_percent': 'Abstract Percentage',
        'flesch_kincaid': 'Flesch-Kincaid Grade Level',
    }
    
    for key, label in metrics_to_plot.items():
        data.append({"Parameter": label, "Value": orig_metrics[key], "Text Type": "Original"})
        data.append({"Parameter": label, "Value": simp_metrics[key], "Text Type": "AI Assistant"})
        
    df = pd.DataFrame(data)
    
    plt.figure(figsize=(8, 5))
    sns.set_theme(style="whitegrid")
    
    ax = sns.barplot(x="Parameter", y="Value", hue="Text Type", data=df, palette="Pastel1")
    
    # Добавляем подписи значений над столбцами
    for p in ax.patches:
        if p.get_height() > 0:
            ax.annotate(f'{p.get_height():.1f}',
                        (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='bottom', xytext=(0, 5), textcoords='offset points')
            
    plt.title("Linguistic Metrics Comparison", fontsize=12, pad=15)
    plt.tight_layout()
    
    plot_path = os.path.join(output_dir, "comparison_chart.png")
    plt.savefig(plot_path, dpi=300)
    plt.close()
    print(f"Comparison plot saved to {plot_path}")