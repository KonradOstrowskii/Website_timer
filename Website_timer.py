import tkinter as tk
from tkinter import filedialog
import webbrowser
import time
import pandas as pd

class WebsiteTimer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Website Timer")
        self.root.geometry("400x250")
        
        self.file_path = ""
        self.is_running = False
        self.start_time = 0
        
        self.select_button = tk.Button(self.root, text="Select CSV File", command=self.select_file)
        self.select_button.pack(pady=10)
        
        self.create_button = tk.Button(self.root, text="Create CSV File", command=self.create_file)
        self.create_button.pack(pady=5)
        
        self.start_button = tk.Button(self.root, text="Start Timer", command=self.start_timer)
        self.start_button.pack(pady=5)
        
        self.stop_button = tk.Button(self.root, text="Stop Timer", command=self.stop_timer, state=tk.DISABLED)
        self.stop_button.pack(pady=5)
        
        self.website_list = ["linkedin.com", "9gag.com", "chat.openai.com"]
        self.website_label = tk.Label(self.root, text="Select a website:")
        self.website_label.pack()
        self.website_var = tk.StringVar(self.root)
        self.website_dropdown = tk.OptionMenu(self.root, self.website_var, *self.website_list, "Enter custom website")
        self.website_dropdown.pack()
        
    def run(self):
        self.root.mainloop()
        
    def select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if self.file_path:
            print("Selected file:", self.file_path)
        
    def create_file(self):
        if self.file_path:
            print("CSV file already exists:", self.file_path)
            return
        
        self.file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if self.file_path:
            print("CSV file created:", self.file_path)
        
    def start_timer(self):
        if not self.file_path:
            print("Please select or create a CSV file first.")
            return
        
        if self.is_running:
            print("Timer is already running.")
            return
        
        print("Timer started.")
        self.is_running = True
        self.start_button.configure(state=tk.DISABLED)
        self.stop_button.configure(state=tk.NORMAL)
        
        self.timer_loop()
    
    def stop_timer(self):
        if not self.is_running:
            print("Timer is not running.")
            return
        
        print("Timer stopped.")
        self.is_running = False
        self.start_button.configure(state=tk.NORMAL)
        self.stop_button.configure(state=tk.DISABLED)
        
    def timer_loop(self):
        website = self.website_var.get()
        if website == "Enter custom website":
            website = input("Enter a website URL or 'q' to quit: ")
            if website == "q":
                return
            
        if not website:
            print("Invalid website URL. Please try again.")
            self.root.after(1000, self.timer_loop)
            return
        
        if not website.startswith("http://") and not website.startswith("https://"):
            website = "http://" + website
        
        try:
            webbrowser.open_new(website)
            self.start_time = time.time()
            input("Press Enter when you are done.")
            end_time = time.time()
        except webbrowser.Error:
            print("Error accessing the website. Please check the URL.")
            self.root.after(1000, self.timer_loop)
            return
        
        time_spent = end_time - self.start_time
        formatted_time_spent = self.format_time_spent(time_spent)
        print("Time spent:", formatted_time_spent)
        
        data = {
            "Website": [website],
            "Time Visited": [time.ctime()],
            "Time Spent": [formatted_time_spent]
        }
        df = pd.DataFrame(data)
        
        if not self.file_exists():
            df.to_csv(self.file_path, index=False)
        else:
            existing_data = pd.read_csv(self.file_path)
            combined_data = pd.concat([existing_data, df], ignore_index=True)
            combined_data.to_csv(self.file_path, index=False)
        
        if self.is_running:
            self.root.after(1000, self.timer_loop)
    
    def format_time_spent(self, time_spent):
        hours = int(time_spent / 3600)
        minutes = int((time_spent % 3600) / 60)
        seconds = int(time_spent % 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def file_exists(self):
        try:
            pd.read_csv(self.file_path)
            return True
        except (FileNotFoundError, pd.errors.EmptyDataError):
            return False

if __name__ == "__main__":
    app = WebsiteTimer()
    app.run()
