import tkinter as tk
from tkinter import ttk, Canvas
from ports import FakePortListener

class PlotModal(tk.Toplevel):
    def __init__(self, parent, port_listener: FakePortListener):
        super().__init__(parent)

        self.title(f"Live Plot (Port {port_listener.port_id})")
        self.geometry("800x400")
        self.resizable(True, True)

        self.canvas = Canvas(self, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.data = []

        # Подписка на данные
        port_listener.subscribe(self.on_data_update)

        # Начать отрисовку графика
        self.render_graph()

        # Закрытие окна — остановить порт
        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def on_data_update(self, data):
        self.data = data

    def render_graph(self):
        self.canvas.delete("all")

        if self.data:
            width = self.canvas.winfo_width()
            height = self.canvas.winfo_height()
            if len(self.data) > 1:
                max_val = max(self.data)
                min_val = min(self.data)
                rng = max_val - min_val or 1

                scale_x = width / (len(self.data) - 1)
                scale_y = height / rng

                points = []
                for i, val in enumerate(self.data):
                    x = i * scale_x
                    y = height - (val - min_val) * scale_y
                    points.append((x, y))

                for i in range(len(points) - 1):
                    self.canvas.create_line(*points[i], *points[i + 1], fill="blue")

        # Повтор через 50 мс (~20 FPS)
        self.after(50, self.render_graph)
        
    # def close(self):
    #     self._is_closed = True
    #     if self.after_id:
    #         self.after_cancel(self.after_id)
    #         self.after_id = None
    #     self.destroy()
