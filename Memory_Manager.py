import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog

class MemoryManager:
    def __init__(self, total_memory):
        self.total_memory = total_memory
        self.memory_blocks = []

    def allocate_memory(self, block_size):
        if sum(self.memory_blocks) + block_size > self.total_memory:
            messagebox.showerror("Error", "Insufficient memory space.")
            return False
        else:
            self.memory_blocks.append(block_size)
            return True

    def deallocate_memory(self, index):
        if 0 <= index < len(self.memory_blocks):
            del self.memory_blocks[index]
            return True
        else:
            messagebox.showerror("Error", "Invalid memory block index.")
            return False

    def get_memory_state(self):
        return f"Total Memory: {self.total_memory} KB\nAllocated Blocks: {self.memory_blocks}"

class MemoryManagementApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Memory Management Simulator")
        self.master.geometry("300x200")

        self.memory_manager = MemoryManager(total_memory=1024)  # Total memory in KB

        self.label = tk.Label(self.master, text=self.memory_manager.get_memory_state())
        self.label.pack(pady=10)

        self.allocate_button = tk.Button(self.master, text="Allocate Memory", command=self.allocate_memory)
        self.allocate_button.pack(pady=5)

        self.deallocate_button = tk.Button(self.master, text="Deallocate Memory", command=self.deallocate_memory)
        self.deallocate_button.pack(pady=5)

    def allocate_memory(self):
        block_size = simpledialog.askinteger("Allocate Memory", "Enter block size (KB):", parent=self.master)
        if block_size is not None:
            if self.memory_manager.allocate_memory(block_size):
                self.update_memory_state()

    def deallocate_memory(self):
        index = simpledialog.askinteger("Deallocate Memory", "Enter block index to deallocate:", parent=self.master)
        if index is not None:
            if self.memory_manager.deallocate_memory(index - 1):
                self.update_memory_state()

    def update_memory_state(self):
        self.label.config(text=self.memory_manager.get_memory_state())

if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryManagementApp(root)
    root.mainloop()
