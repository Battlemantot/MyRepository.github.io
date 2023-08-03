import customtkinter
import time
import datetime
import threading

customtkinter.set_default_color_theme("dark-blue")
customtkinter.set_appearance_mode("dark")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Simple Timer")
        #self.geometry("320x320")

        self.entry_Hours = customtkinter.CTkEntry(self, placeholder_text="Hours")
        self.entry_Hours.grid(row=0, column=0, padx=20, pady=20)
        self.entry_Minutes = customtkinter.CTkEntry(self, placeholder_text="Minutes")
        self.entry_Minutes.grid(row=0, column=1, padx=20, pady=20)
        self.entry_Seconds = customtkinter.CTkEntry(self, placeholder_text="Seconds")
        self.entry_Seconds.grid(row=0, column=2, padx=20, pady=20)

        self.label_Time = customtkinter.CTkLabel(self, text="Time remaining:", fg_color="transparent")
        self.label_Time.grid(row=1, column=0, padx=20, pady=20)

        # Need to fix threading so program doesn't freeze
        self.button = customtkinter.CTkButton(self, text="Start Timer", command=lambda : threading.Thread(target= self.countdown(int(self.entry_Hours.get()), int(self.entry_Minutes.get()), int(self.entry_Seconds.get()))).start())
        self.button.grid(row=2, column=0, padx=20, pady=20)
        
    def countdown(self, h, m, s):
        total_seconds = h * 3600 + m * 60 + s

        while total_seconds > 0:
            timer = datetime.timedelta(seconds = total_seconds)
            print(timer, end="\r")
            time.sleep(1)
            total_seconds -= 1
        print("Timer end!")

app = App()
app.mainloop()