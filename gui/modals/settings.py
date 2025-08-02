import tkinter as tk
from tkinter import ttk

class SettingsModal(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("Settings")
        self.geometry("400x300")
        self.resizable(False, False)
        
        # Make window modal
        self.transient(parent)  # set window above parent
        self.grab_set()         # block parent window
        
        self.build_ui()
        
        # Wait for the window to be closed (if needed)
        self.wait_window()
        
      
    def build_ui(self):
        label = ttk.Label(self, text="Settings window (currently empty)", font=("Segoe UI", 12))
        label.pack(pady=20, padx=20)

        close_btn = ttk.Button(self, text="Close", command=self.destroy)
        close_btn.pack(pady=10)   
    
    def run(self):
        print('SettingsModal run!')