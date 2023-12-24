import psutil
import numpy as np
import matplotlib.pyplot as plt

def update_memory():
    memory_stats = psutil.virtual_memory()
    available_gb = memory_stats.available / (1024 ** 3)
    used_gb = memory_stats.used / (1024 ** 3)

    labels = ['Available', 'Used']
    sizes = [available_gb, used_gb]
    colors = ['blue', 'pink']
    explode = (0.1, 0.0)

    fig, ax = plt.subplots()

    wedges, texts, autotexts = ax.pie(sizes,
                                      autopct=lambda pct: "{:.1f}%\n({:.2f})".format(pct, pct / 100 * np.sum(sizes)),
                                      explode=explode,
                                      labels=labels,
                                      colors=colors,
                                      startangle=90,
                                      wedgeprops=dict(width=0.4, edgecolor='w'))

    for text, autotext, label in zip(texts, autotexts, labels):
        text.set_text(label)
        autotext.set_text(f"{autotext.get_text()} GB")

    ax.set_title("Memory Usage")

    plt.show() 

if __name__ == "__main__":
    update_memory()