import tkinter as tk
from tkinter import ttk, filedialog
import random

from .modals import SettingsModal
"""
+---------------------------------------------+
|                               [⚙ Settings] |
+---------------------------------------------+
| File:       [ Choose File ] (.dxd / .mera)  |
| From COM:   [ COM3 ▼ ]                      |
| To COM:     [ COM4 ▼ ]                      |
| Delay (ms): [   5    ]                      |
|                                             |
| [ ▶ Start ] [ ⏸ Pause ] [ ⏹ Stop ]        |
| [================= 100% ==================] |
+---------------------------------------------+
| Status: Loaded file example.mera            |
+---------------------------------------------+
"""
METHODS = ["Serial", "Modbus TCP"]
FROM_COM_PORTS = ["COM1", "COM2", "COM3"]
TO_COM_PORTS = ["COM4", "COM5", "COM6"]
class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("COM Port File Emulator")
        self.geometry("600x400")
        
        self.selected_file = None  # file path
        
        self.method = tk.StringVar(value="Serial")
        self.from_com = tk.StringVar(value=FROM_COM_PORTS[0])
        self.to_com = tk.StringVar(value=TO_COM_PORTS[0])
        self.ip = tk.StringVar(value='192.168.0.1')
        self.port = tk.StringVar(value='4200')
        self.delay = tk.StringVar(value='5')
        self.status_var = tk.StringVar(value="Ready")
        
        self.start_state = False
        self.pause_state = False
        self.stop_state = False
        
        self.build_ui()
        
    def build_ui(self):
        # Navbar
        self._build_navbar()
        
        # Main content
        self._build_form()
        self._build_controls()
        self._build_progressbar()
        self._build_statusbar()
        
        
    def open_settings_modal(self):
        SettingsModal(self)
        
    def _build_navbar(self):
        navbar = ttk.Frame(self)
        navbar.pack(fill="x", side="top")
        
        settings_btn = ttk.Button(navbar, text="Settings", command=self.open_settings_modal)
        settings_btn.pack(side="right", padx=10, pady=5)
        
    def _build_content(self):
        content = ttk.Frame(self)
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        label = ttk.Label(content, text="main_window works", font=("Segoe UI", 12))
        label.pack(pady=10)
        
    def _build_form(self):
        self.form_frame = ttk.Frame(self, padding=10)
        self.form_frame.pack(fill="x")

        LABEL_WIDTH = 12
        ENTRY_WIDTH = 30

        # Method selection
        ttk.Label(self.form_frame, text="Method:", width=LABEL_WIDTH, anchor="e").grid(row=0, column=0, padx=5, pady=5)
        method_cb = ttk.Combobox(self.form_frame, textvariable=self.method, values=METHODS, width=ENTRY_WIDTH, state="readonly")
        method_cb.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        method_cb.bind("<<ComboboxSelected>>", lambda e: self._update_form_fields())

        # File selection
        ttk.Label(self.form_frame, text="File:", width=LABEL_WIDTH, anchor="e").grid(row=1, column=0, padx=5, pady=5)
        file_frame = ttk.Frame(self.form_frame)
        file_frame.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Show selected file path (Label)
        BUTTON_WIDTH = 10
        self.file_label = ttk.Label(file_frame, text="No file selected", width=ENTRY_WIDTH - BUTTON_WIDTH, anchor="w")
        self.file_label.pack(side="left", padx=(0, 5))

        ttk.Button(file_frame, text="Choose File", command=self._choose_file, width=BUTTON_WIDTH).pack(side="left")

        # From COM
        self.from_com_label = ttk.Label(self.form_frame, text="From COM:", width=LABEL_WIDTH, anchor="e")
        self.from_com_cb = ttk.Combobox(self.form_frame, textvariable=self.from_com, values=FROM_COM_PORTS, width=ENTRY_WIDTH)
        self.from_com_label.grid(row=2, column=0, padx=5, pady=5)
        self.from_com_cb.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # To COM
        self.to_com_label = ttk.Label(self.form_frame, text="To COM:", width=LABEL_WIDTH, anchor="e")
        self.to_com_cb = ttk.Combobox(self.form_frame, textvariable=self.to_com, values=TO_COM_PORTS, width=ENTRY_WIDTH)
        self.to_com_label.grid(row=3, column=0, padx=5, pady=5)
        self.to_com_cb.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # IP (for Modbus TCP)
        ip_vcmd = (self.register(self._validate_ip_input), "%P")
        self.ip_label = ttk.Label(self.form_frame, text="IP Address:", width=LABEL_WIDTH, anchor="e")
        self.ip_entry = ttk.Entry(self.form_frame, textvariable=self.ip, width=ENTRY_WIDTH, validate="key", validatecommand=ip_vcmd)
        self.ip_label.grid(row=2, column=0, padx=5, pady=5)
        self.ip_label.grid_remove()
        self.ip_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.ip_entry.grid_remove()

        # Port
        port_vcmd = (self.register(self._validate_digit_input), "%P")
        self.port_label = ttk.Label(self.form_frame, text="Port:", width=LABEL_WIDTH, anchor="e")
        self.port_entry = ttk.Entry(self.form_frame, textvariable=self.port, width=ENTRY_WIDTH, validate="key", validatecommand=port_vcmd)
        self.port_label.grid(row=3, column=0, padx=5, pady=5)
        self.port_label.grid_remove()
        self.port_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.port_entry.grid_remove()

        # Delay
        vcmd = (self.register(self._validate_float), "%P")
        
        ttk.Label(self.form_frame, text="Delay (ms):", width=LABEL_WIDTH, anchor="e").grid(row=4, column=0, padx=5, pady=5)
        self.delay_entry = ttk.Entry(self.form_frame, width=ENTRY_WIDTH, textvariable=self.delay, validate="key", validatecommand=vcmd)
        self.delay_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        # , textvariable=tk.StringVar(value="Hello, world!")
        
    def _build_controls(self):
        self.controls_frame = ttk.Frame(self)
        self.controls_frame.pack(pady=10, padx=10, fill="x")

        # Start button
        self.start_control = ttk.Button(self.controls_frame, text="▶ Start", command=lambda: self._on_control_click('start'))
        self.start_control.grid(row=0, column=0, padx=5)

        # Pause button (initially disabled)
        self.pause_control = ttk.Button(self.controls_frame, text="⏸ Pause", command=lambda: self._on_control_click('pause'), state="disabled")
        self.pause_control.grid(row=0, column=1, padx=5)

        # Stop button
        self.stop_control = ttk.Button(self.controls_frame, text="⏹ Stop", command=lambda: self._on_control_click('stop'), state="disabled")
        self.stop_control.grid(row=0, column=2, padx=5)
        
    def _build_progressbar(self):
        self.progress_frame = ttk.Frame(self)
        self.progress_frame.pack(fill="x", padx=10, pady=(10, 0))

        self.progress_var = tk.DoubleVar(value=0)

        self.progressbar = ttk.Progressbar(
            self.progress_frame,
            variable=self.progress_var,
            maximum=100,
            mode="determinate"
        )
        self.progressbar.pack(fill="x")
        
    def _build_statusbar(self):
        status_bar_frame = ttk.Frame(self)
        status_bar_frame.pack(fill="x", padx=10, pady=(10, 0))
        
        self.statusbar = ttk.Label(status_bar_frame, textvariable=self.status_var, relief="sunken", anchor="w")
        self.statusbar.pack(side="bottom", fill="x")
        
    def _choose_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Data Files", "*.dxd *.mera")])
        if file_path:
            print(f"Selected file: {file_path}")
            self.selected_file = file_path
            self._update_form_fields()
            
    def _update_form_fields(self, event=None):
        if self.selected_file:
            filename = self.selected_file.split("/")[-1]
            self.file_label.config(text=filename)
            
        method = self.method.get()
        if method == METHODS[0]:
            self.from_com_label.grid()
            self.from_com_cb.grid()
            self.to_com_label.grid()
            self.to_com_cb.grid()

            self.ip_label.grid_remove()
            self.ip_entry.grid_remove()
            self.port_label.grid_remove()
            self.port_entry.grid_remove()
        elif method == METHODS[1]:
            self.from_com_label.grid_remove()
            self.from_com_cb.grid_remove()
            self.to_com_label.grid_remove()
            self.to_com_cb.grid_remove()

            self.ip_label.grid()
            self.ip_entry.grid()
            self.port_label.grid()
            self.port_entry.grid()
            
    def _update_progress(self, percent):
        self.progress_var.set(percent)
        self.update_idletasks() 
        
    def _on_control_click(self, action_type):
        # Reset all flags
        self.start_state = False
        self.pause_state = False
        self.stop_state = False

        # Set the selected action flag
        if action_type == 'start':
            self.start_state = True
            self._start()
        elif action_type == 'pause':
            self.pause_state = True
            self._pause()
        elif action_type == 'stop':
            self.stop_state = True
            self._stop()

        # Update control buttons
        self._update_controls_state()
        
    def _update_controls_state(self):
        # Disable/enable buttons based on current state
        if self.start_state:
            self.start_control.config(state="disabled")
            self.pause_control.config(state="normal")
            self.stop_control.config(state="normal")
        elif self.pause_state:
            self.start_control.config(state="normal")
            self.pause_control.config(state="disabled")
            self.stop_control.config(state="normal")
        elif self.stop_state:
            self.start_control.config(state="normal")
            self.pause_control.config(state="disabled")
            self.stop_control.config(state="disabled")
        else:
            self.start_control.config(state="normal")
            self.pause_control.config(state="disabled")
            self.stop_control.config(state="disabled")
            
    def _start(self):
        self._update_status('Start')
        def loop():
            if not self.start_state or self.pause_state or self.stop_state:
                return
            current = self.progress_var.get()
            increment = random.uniform(0.01, 1.0)
            new_value = current + increment
            if new_value > 100:
                self._on_control_click('stop')
                self._update_status('Completed')
                new_value = 0
                
            self.progress_var.set(new_value)
            try:
                delay = float(self.delay.get())
            except ValueError:
                delay = 5.0

            self.after(int(delay), loop)
            
        loop()
            
    
    def _pause(self):
        self._update_status('Paused')
    
    def _stop(self):
        self._update_status('Stopped')
        self.progress_var.set(0)
            
    def _update_status(self, message):
        self.status_var.set(message)
        self.statusbar.update_idletasks()
    
    def _validate_float(self, new_value: str) -> bool:
        if new_value == "":
            return True
        try:
            float(new_value)
            return True
        except ValueError:
            return False
        
    def _validate_ip_input(self, value: str) -> bool:
        # Allow empty input (for editing)
        if value == "":
            return True

        parts = value.split(".")
        if len(parts) > 4:
            return False

        for part in parts:
            if not part.isdigit():
                return False
            num = int(part)
            if not (0 <= num <= 255):
                return False

        return True
    
    def _validate_digit_input(self, value: str) -> bool:
        if value == "":
            return True
        return value.isdigit()
        
        
      
    
