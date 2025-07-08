import tkinter as tk
from tkinter import messagebox
import subprocess
import threading
from utils.search_logs import open_search_window  # 🔍 For search logs

class DashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Intelligent Face Tracker Dashboard")
        self.root.geometry("720x650")
        self.root.configure(bg="#f0f4f8")

        # 🏷️ Title Header
        title_frame = tk.Frame(root, bg="#2c3e50")
        title_frame.pack(fill=tk.X)

        title_label = tk.Label(
            title_frame,
            text="🤖 Intelligent Face Tracker",
            font=("Helvetica", 26, "bold"),
            fg="white",
            bg="#2c3e50",
            pady=30
        )
        title_label.pack()

        # 🔘 Button Container
        button_frame = tk.Frame(root, bg="#f0f4f8")
        button_frame.pack(pady=30)

        # 🟡 Status Label
        self.label = tk.Label(
            root,
            text="🟡 Status: Idle",
            font=("Arial", 18, "bold"),
            bg="#f0f4f8",
            fg="#7f8c8d"
        )
        self.label.pack(pady=10)

        # ▶ Start Video File Tracking
        self.start_video_button = tk.Button(
            button_frame,
            text="▶ Start Tracking (Videos)",
            command=lambda: self.start_tracking("test_multiple_videos.py"),
            width=30,
            height=2,
            bg="#1abc9c",
            fg="white",
            activebackground="#16a085",
            activeforeground="white",
            font=("Arial", 16, "bold"),
            relief=tk.RAISED,
            bd=5
        )
        self.start_video_button.grid(row=0, column=0, pady=10)

        # 🎥 Start Live Webcam Tracking
        self.start_webcam_button = tk.Button(
            button_frame,
            text="🎥 Start Live Webcam Tracking",
            command=lambda: self.start_tracking("test_webcam_live.py"),
            width=30,
            height=2,
            bg="#9b59b6",
            fg="white",
            activebackground="#8e44ad",
            activeforeground="white",
            font=("Arial", 16, "bold"),
            relief=tk.RAISED,
            bd=5
        )
        self.start_webcam_button.grid(row=1, column=0, pady=10)

        # ⛔ Stop Tracking Button
        self.stop_button = tk.Button(
            button_frame,
            text="⛔ Stop Tracking",
            command=self.stop_tracking,
            width=30,
            height=2,
            bg="#e74c3c",
            fg="white",
            activebackground="#c0392b",
            activeforeground="white",
            font=("Arial", 16, "bold"),
            relief=tk.RAISED,
            bd=5,
            state=tk.DISABLED
        )
        self.stop_button.grid(row=2, column=0, pady=10)

        # 📁 Export Logs Button
        self.export_button = tk.Button(
            button_frame,
            text="📁 Export Logs as CSV",
            command=self.export_logs,
            width=30,
            height=2,
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            font=("Arial", 16, "bold"),
            relief=tk.RAISED,
            bd=5
        )
        self.export_button.grid(row=3, column=0, pady=10)

        # 🔍 Search Visitor Logs
        self.search_button = tk.Button(
            button_frame,
            text="🔍 Search Visitor Logs",
            command=open_search_window,
            width=30,
            height=2,
            bg="#8e44ad",
            fg="white",
            activebackground="#732d91",
            activeforeground="white",
            font=("Arial", 16, "bold"),
            relief=tk.RAISED,
            bd=5
        )
        self.search_button.grid(row=4, column=0, pady=10)

        # 👣 Footer
        footer = tk.Label(
            root,
            text="© 2025 | Team IntelligentVision | Hackathon Edition 🚀",
            font=("Arial", 11, "italic"),
            bg="#f0f4f8",
            fg="#7f8c8d"
        )
        footer.pack(side=tk.BOTTOM, pady=12)

        self.process = None

    def start_tracking(self, script_name):
        if self.process:
            return

        self.label.config(text="🟢 Status: Running", fg="#27ae60")
        self.start_video_button.config(state=tk.DISABLED)
        self.start_webcam_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        def run_script():
            self.process = subprocess.Popen(["python", script_name])
            self.process.wait()
            self.label.config(text="🟡 Status: Idle", fg="#7f8c8d")
            self.start_video_button.config(state=tk.NORMAL)
            self.start_webcam_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.process = None

        thread = threading.Thread(target=run_script)
        thread.daemon = True
        thread.start()

    def stop_tracking(self):
        if self.process:
            self.process.terminate()
            self.label.config(text="🔴 Status: Stopped", fg="#e74c3c")
            self.start_video_button.config(state=tk.NORMAL)
            self.start_webcam_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.process = None

    def export_logs(self):
        try:
            from utils.export_csv import export_csv
            export_csv()
            messagebox.showinfo("✅ Exported", "CSV logs exported successfully!")
        except Exception as e:
            messagebox.showerror("❌ Error", f"Export failed:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DashboardApp(root)
    root.mainloop()
