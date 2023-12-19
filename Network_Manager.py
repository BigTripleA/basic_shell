import tkinter as tk
from tkinter import ttk
import psutil
import time

class NetworkMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Monitor")

        self.tabs = ttk.Notebook(root)
        self.tab1 = ttk.Frame(self.tabs)
        self.tabs.add(self.tab1, text="Details")
        self.tabs.pack(expand=1, fill="both")

        # Details Tab
        self.details_label = tk.Label(self.tab1, text="Network Details:")
        self.details_label.pack()

        self.details_text = tk.Text(self.tab1, height=10, width=50)
        self.details_text.pack()

        self.update_details()

    def convert_bytes_to_readable(self, bytes_value):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                break
            bytes_value /= 1024.0
        return f"{bytes_value:.2f} {unit}"

    def update_details(self):
        network_stats = psutil.net_io_counters()
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        
        details_text = f"{timestamp}\n"
        details_text += f"Bytes Sent: {self.convert_bytes_to_readable(network_stats.bytes_sent)}\n"
        details_text += f"Bytes Received: {self.convert_bytes_to_readable(network_stats.bytes_recv)}\n"
        details_text += f"Packets Sent: {network_stats.packets_sent}\n"
        details_text += f"Packets Received: {network_stats.packets_recv}\n"
        
        self.details_text.delete(1.0, tk.END)
        self.details_text.insert(tk.END, details_text)
        self.root.after(1000, self.update_details)  # Update every 1 second

if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkMonitor(root)
    root.mainloop()
