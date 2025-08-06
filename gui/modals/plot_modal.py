import tkinter as tk
import random
from tkinter import ttk, Canvas
from ports import FakePortListener

class PlotModal(tk.Toplevel):
    def __init__(self, parent, title="Plot", update_interval_ms=50):
        super().__init__(parent)
        self.title(title)
        self.geometry("600x400")
        self.update_interval_ms = update_interval_ms
        
        self.data = {}  # {key: list of values}
        self.canvas = Canvas(self, bg="white")
        self.canvas.pack(fill="both", expand=True)

        self.colors = {}
        self._render_loop_id = None
        self._start_render_loop()

    def update_data(self, new_data: dict):
        self.data = new_data
        for key in new_data.keys():
            if key not in self.colors:
                self.colors[key] = self._random_color()

    def _random_color(self):
        return "#%06x" % random.randint(0, 0xFFFFFF)

    def _start_render_loop(self):
        self._render_graph()
        self._render_loop_id = self.after(self.update_interval_ms, self._start_render_loop)

    def _render_graph(self):
        self.canvas.delete("all")
        if not self.data:
            return
        
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w == 1 or h == 1:
            return

        # get all data to fing a right scale
        all_points = []
        for values in self.data.values():
            all_points.extend(values)
        if not all_points:
            return
        
        max_val = max(all_points)
        min_val = min(all_points)
        range_val = max_val - min_val if max_val != min_val else 1

        # each channel with new line
        for key, values in self.data.items():
            if len(values) < 2:
                continue

            color = self.colors.get(key, "black")
            points = [
                (i * w / (len(values) - 1), h - ((v - min_val) / range_val) * h)
                for i, v in enumerate(values)
            ]
            for i in range(len(points) - 1):
                x1, y1 = points[i]
                x2, y2 = points[i+1]
                self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2)

            # Channel description, top left
            self.canvas.create_text(
                5, 20 + 20 * list(self.data.keys()).index(key),
                text=key, fill="black", anchor="w", font=("Arial", 10, "bold")
            )

    def close(self):
        if self._render_loop_id:
            self.after_cancel(self._render_loop_id)
        self.destroy()
