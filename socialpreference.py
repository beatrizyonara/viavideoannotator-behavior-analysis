import tkinter as tk
import tkinter.messagebox
import customtkinter

# Definindo a aparência e o tema padrão do pacote customtkinter
customtkinter.set_appearance_mode("System")  # Modos: "System" (padrão), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Temas: "blue" (padrão), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("MultiStopwatch")
        self.geometry("600x400")

        self.timers = [tk.StringVar() for _ in range(4)]
        self.running = [False] * 4
        self.start_times = [None] * 4

        self.create_widgets()

    def create_widgets(self):
        for i in range(4):
            timer_label = tk.Label(self, textvariable=self.timers[i], font=("Arial", 16))
            timer_label.pack(padx=10, pady=5, anchor="w")

        self.start_button = tk.Button(self, text="Start/Stop", command=self.toggle_timer, font=("Arial", 14))
        self.start_button.pack(pady=5)

        self.reset_button = tk.Button(self, text="Reset", command=self.reset_timer, font=("Arial", 14))
        self.reset_button.pack(pady=5)

        self.save_as_button = tk.Button(self, text="Save As", command=self.save_time_as, font=("Arial", 14))
        self.save_as_button.pack(pady=5)

        self.bind("<KeyPress-1>", lambda event: self.handle_keypress(0))
        self.bind("<KeyPress-2>", lambda event: self.handle_keypress(1))
        self.bind("<KeyPress-3>", lambda event: self.handle_keypress(2))
        self.bind("<KeyPress-4>", lambda event: self.handle_keypress(3))

        self.bind("<space>", self.toggle_timer)

        self.update_display()

    def update_display(self):
        for i in range(4):
            if self.running[i]:
                self.timers[i].set("Timer {}: Running".format(i + 1))
            else:
                self.timers[i].set("Timer {}: Stopped".format(i + 1))
        self.after(100, self.update_display)

    def toggle_timer(self):
        for i in range(4):
            if self.running[i]:
                self.running[i] = False
                self.timers[i].set("Timer {}: Stopped".format(i + 1))
            else:
                self.running[i] = True
                self.start_times[i] = tk.datetime.now()
                self.timers[i].set("Timer {}: Running".format(i + 1))

    def reset_timer(self):
        for i in range(4):
            self.running[i] = False
            self.timers[i].set("Timer {}: Reset".format(i + 1))

    def save_time_as(self):
        # Implemente a função de salvamento conforme necessário
        pass

    def handle_keypress(self, timer_index):
        if not self.running[timer_index]:
            self.running[timer_index] = True
            self.start_times[timer_index] = tk.datetime.now()
            self.timers[timer_index].set("Timer {}: Running".format(timer_index + 1))
        else:
            self.running[timer_index] = False
            elapsed_time = tk.datetime.now() - self.start_times[timer_index]
            self.timers[timer_index].set("Timer {}: Elapsed Time: {}".format(timer_index + 1, elapsed_time))


if __name__ == "__main__":
    app = App()
    app.mainloop()
