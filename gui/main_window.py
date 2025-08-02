import tkinter as tk
from tkinter import ttk


from .modals import SettingsModal


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("COM Port File Emulator")
        self.geometry("600x400")
        
        self.build_ui()
        
    def build_ui(self):
        # Navbar
        navbar = ttk.Frame(self)
        navbar.pack(fill="x", side="top")
        
        settings_btn = ttk.Button(navbar, text="Settings", command=self.open_settings_modal)
        settings_btn.pack(side="right", padx=10, pady=5)
        
        # Main content
        content = ttk.Frame(self)
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        label = ttk.Label(content, text="main_window works", font=("Segoe UI", 12))
        label.pack(pady=10)
        
        
    def open_settings_modal(self):
        SettingsModal(self)