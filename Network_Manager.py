import tkinter as tk
from tkinter import ttk
import psutil
import time
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import subprocess
from ttkbootstrap import Style
import json


class NetworkMonitor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('700x600')
        self.root.title("Network Monitor")
        # style
        style = Style(theme='superhero')
        f = open('theme.json', 'r')
        theme = json.load(f)
        st = ttk.Style()
        st.theme_create('MyStyle', settings=theme)
        st.theme_use("MyStyle")

        network_stats = psutil.net_io_counters()
        self.last_dl = network_stats.bytes_recv
        self.last_ul = network_stats.bytes_sent

        self.tabs = ttk.Notebook(self.root)
        self.tab1 = ttk.Frame(self.tabs)
        self.tab2 = ttk.Frame(self.tabs)
        self.tab3 = ttk.Frame(self.tabs)
        self.tabs.add(self.tab1, text="Info")
        self.tabs.add(self.tab2, text="Netstat")
        self.tabs.add(self.tab3, text="Ping")
        self.tabs.pack(expand=True, fill="both")

        # Info Tab
        self.info_text = tk.Text(self.tab1, font="20")
        self.info_text.pack()

        # define netStat attributes
        self.plot_dl = 0
        self.plot_ul = 0
        self.tab2_canvas = 0
        self.z = [0 for _ in range(30)]
        self.y = [0 for _ in range(30)]
        self.plot_init()

        # Ping tab
        self.ping_address = 0
        self.ping_res_text = 0
        self.ping_tab_init()

    def run(self):
        self.update_tabs()
        self.root.mainloop()

    def plot_init(self):
        netstat_text = tk.Label(self.tab2, text="Instantaneous Network Status", font="bold")
        netstat_text.pack()
        fig = Figure(figsize=(5, 5), dpi=80)
        plot = fig.add_subplot(111)
        plot.set_title('Download and Upload Rate')
        plot.set_xlabel("Last 30 secs")
        plot.set_ylabel("Rate in KB")
        self.plot_dl, = plot.plot(self.y, label="DL Rate")
        self.plot_ul, = plot.plot(self.z, label="UL Rate")
        plot.legend()
        self.tab2_canvas = FigureCanvasTkAgg(fig, master=self.tab2)
        self.tab2_canvas.draw()
        self.tab2_canvas.get_tk_widget().pack()
        toolbar = NavigationToolbar2Tk(self.tab2_canvas, self.tab2)
        toolbar.update()
        self.tab2_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def ping_tab_init(self):
        ping_text = tk.Label(self.tab3, text="Enter the network address to ping an internet route to.")
        ping_text.grid(column=0, row=0, padx=10, pady=5)
        self.ping_address = ttk.Entry(self.tab3, width=30)
        self.ping_address.grid(column=0, row=1, ipadx=2, ipady=2, padx=5, pady=15)
        ping_button = ttk.Button(self.tab3, text="Ping", command=self.ping, style='secondary.TButton')
        ping_button.grid(column=1, row=1, ipadx=7, ipady=7, padx=5, pady=0)
        self.ping_res_text = tk.Label(self.tab3, text=50*' ')
        self.ping_res_text.grid(column=0, row=2)

    def update_tabs(self):
        network_stats = psutil.net_io_counters()
        b_sent = network_stats.bytes_sent
        b_rec = network_stats.bytes_recv

        self.update_info_tab(b_sent, b_rec, network_stats.packets_sent, network_stats.packets_recv)
        self.update_netstat_tab(b_sent, b_rec)
        self.root.after(1000, self.update_tabs)  # Update every 1 second

    def update_info_tab(self, bytes_sent, bytes_recv, packets_sent, packets_recv):
        # Date and time and network stats
        datestamp = time.strftime("%Y-%m-%d")
        timestamp = time.strftime("%H:%M:%S")
        details_text = f"\nDate: {datestamp} - Time : {timestamp}\nNetwork Details:\n\n"
        details_text += f"Bytes Sent:\n{convert_b_to_readable(bytes_sent)}\n"
        details_text += f"Bytes Received:\n{convert_b_to_readable(bytes_recv)}\n\n"
        details_text += f"Packets Sent:\n{packets_sent}\nPackets Received:\n{packets_recv}\n\n"
        details_text += (f"Instant Bytes Received:\n{convert_b_to_readable(self.y[-1])}\n"
                         f"Instant Bytes Sent:\n{convert_b_to_readable(self.z[-1])}\n")

        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, details_text)
        self.info_text.tag_config("start", font='bold')
        self.info_text.tag_add("start", "2.0", "3.16")

    def update_netstat_tab(self, ul, dl):
        # calculate instantaneous upload and download rate
        del self.z[0]
        self.z.append(int((ul - self.last_ul) / 1000))
        self.last_ul = ul
        del self.y[0]
        self.y.append(int((dl - self.last_dl)/1000))
        self.last_dl = dl
        x = [i+1 for i in range(30)]

        self.plot_dl.set_data(x, self.y)
        self.plot_ul.set_data(x, self.z)
        self.tab2_canvas.figure.axes[0].set_ylim(0, max(40, max(self.z), max(self.y)))
        self.tab2_canvas.draw()

    def ping(self):
        command = ['ping', str(self.ping_address.get())]
        result = subprocess.run(command, stdout=subprocess.PIPE)
        result = str(result.stdout, encoding='utf-8')
        self.ping_res_text.config(text=result)


def convert_b_to_readable(bytes_value):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            break
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} {unit}"


if __name__ == "__main__":
    app = NetworkMonitor()
    app.run()
