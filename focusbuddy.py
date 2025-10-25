import tkinter as tk
from tkinter import ttk, messagebox
import threading, time, random
from PIL import Image, ImageTk, ImageDraw

ROASTS = [
    "✨ Focus mode exited. Did you actually do something or just stare aesthetically?",
    "🦋 You did it! The productivity fairy approves (barely).",
    "💿 Another focus session complete. Windows XP is proud of you.",
    "🌈 Congrats! You survived your own attention span.",
    "🕹️ Timer’s up. Go touch some grass, retro queen."
]

# create a vertical gradient image
def make_gradient(width, height, c1, c2):
    base = Image.new("RGB", (width, height), c1)
    top = Image.new("RGB", (width, height), c2)
    mask = Image.new("L", (width, height))
    draw = ImageDraw.Draw(mask)
    for y in range(height):
        draw.line((0, y, width, y), fill=int(255 * (y / height)))
    return ImageTk.PhotoImage(Image.composite(top, base, mask))

class FocusBuddyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FocusBuddy 💿")
        self.root.geometry("460x340")
        self.root.overrideredirect(1)
        self.root.resizable(False, False)

        # gradient background
        self.canvas = tk.Canvas(root, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.bg = make_gradient(460, 340, "#ffdee9", "#b5fffc")
        self.canvas.create_image(0, 0, image=self.bg, anchor="nw")

        # faux rounded shape
        self.canvas.create_oval(-60, -60, 520, 400, fill="#fff6ff", outline="")

        # close button
        tk.Button(root, text="✕", bg="#fff6ff", borderwidth=0, command=root.destroy,
                  font=("Verdana", 9)).place(x=430, y=10)

        # title
        self.title_label = tk.Label(root, text="    💾 FocusBuddy ", font=("Comic Sans MS", 18, "bold"),
                                    bg="#fff6ff", fg="#b19cd9")
        self.title_label.place(x=90, y=20)

        # input
        tk.Label(root, text="Focus Time (minutes):", font=("Century Gothic", 10),
                 bg="#fff6ff", fg="#5f4b8b").place(x=150, y=70)
        self.entry = tk.Entry(root, justify='center', font=("Courier", 12))
        self.entry.place(x=160, y=95, width=140)

        # progress bar
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("Y2K.Horizontal.TProgressbar",
                             troughcolor="#e6e0ff", bordercolor="#e6e0ff",
                             background="#ffb6c1", lightcolor="#ffb6c1", darkcolor="#d8bfd8")
        self.progress = ttk.Progressbar(root, length=360, mode='determinate',
                                        style="Y2K.Horizontal.TProgressbar")
        self.progress.place(x=50, y=150)

        # buttons
        btns = [
            ("▶ Start", self.start_focus),
            ("⏸ Pause", self.pause_focus),
            ("⏹ Stop", self.stop_focus),
            ("🔄 Reset", self.reset_focus)
        ]
        self.buttons = []
        for i, (txt, cmd) in enumerate(btns):
            b = tk.Button(root, text=txt, command=cmd, font=("Verdana", 10),
                          bg="#b19cd9", fg="white", activebackground="#d8bfd8",
                          relief="flat", width=8)
            b.place(x=60 + i*95, y=200)
            self.buttons.append(b)

        # status
        self.status = tk.Label(root, text="Ready to focus ✨",
                               bg="#fff6ff", font=("Arial", 10, "italic"), fg="#5f4b8b")
        self.status.place(x=160, y=260)

        # state
        self.running = False
        self.paused = False
        self.total_seconds = 0
        self.elapsed = 0

        # animations
        self.animate_title()
        self.pulse_progress()

    # --- animation loops ---
    def animate_title(self):
        colors = ["#b19cd9", "#ff8da1", "#7ec8e3", "#ffb6c1"]
        self.title_label.config(fg=random.choice(colors))
        self.root.after(700, self.animate_title)

    def pulse_progress(self):
        if not self.running:
            val = self.progress["value"]
            self.progress["value"] = (val + 0.5) % 100
        self.root.after(100, self.pulse_progress)

    # --- control functions ---
    def start_focus(self):
        if self.running:
            return
        try:
            mins = float(self.entry.get())
            self.total_seconds = int(mins * 60)
            self.elapsed = 0
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number!")
            return
        self.running, self.paused = True, False
        self.entry.config(state="disabled")
        self.status.config(text="🌸 Focusing... stay fab!")
        threading.Thread(target=self.run_timer, daemon=True).start()

    def pause_focus(self):
        if not self.running:
            return
        self.paused = not self.paused
        self.status.config(text="💤 Paused." if self.paused else "🌼 Resumed!")

    def stop_focus(self):
        if not self.running:
            return
        self.running = False
        self.progress["value"] = 0
        self.status.config(text="❌ Session stopped.")

    def reset_focus(self):
        self.running = False
        self.paused = False
        self.elapsed = 0
        self.entry.config(state="normal")
        self.progress["value"] = 0
        self.status.config(text="🔄 Reset! Ready again 💿")

    def run_timer(self):
        while self.elapsed < self.total_seconds and self.running:
            if self.paused:
                time.sleep(0.5)
                continue
            time.sleep(1)
            self.elapsed += 1
            self.progress["value"] = (self.elapsed / self.total_seconds) * 100
        if self.running:
            self.session_done()

    def session_done(self):
        self.running = False
        self.entry.config(state="normal")
        roast = random.choice(ROASTS)
        self.status.config(text="🌟 Done! You did it 💜")
        messagebox.showinfo("FocusBuddy Y2K+ Says:", roast)

if __name__ == "__main__":
    root = tk.Tk()
    app = FocusBuddyApp(root)
    root.mainloop()

