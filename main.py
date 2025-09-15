import subprocess
import time
import threading
import tkinter as tk
from tkinter import font
from tkinter import ttk
from tkinter import filedialog, messagebox

from audio import FFMPEG

def check_for_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        label_ffmpeg.config(text="FFmpeg installed and working!")
    except:
        label_ffmpeg.config(text="It appears FFmpeg is not installed. This makes us sad :(")

    label_ffmpeg.after(3000, lambda: label_ffmpeg.config(text=""))

def create_converted_filename(file: str, format: str):
    output_filename = file.split('.')
    output_filename = output_filename[0]
    output_filename = output_filename.lower()
    output_filename = output_filename + '.' + format
    return output_filename

def open_file():
    file = filedialog.askopenfilename(
        title="Select an audio file",
        # filetypes=[("Audio files", "*.mp3 *.wav *.flac *.ogg *.aac"), ("All files", "*.*")]
    )
    if file:
        selected_file.set(file)

def convert_audio(input_file, format):
    ffmpeg = FFMPEG()
    ffmpeg.input_file = input_file
    ffmpeg.output_file = create_converted_filename(file=input_file, format=format)
    ffmpeg.convert()
    status_label.config(text="")
    messagebox.showinfo("info", f"file create: {ffmpeg.output_file}")

def run_conversion():
    file = selected_file.get()
    fmt = output_format.get()
    if not file:
        messagebox.showwarning("Warning", "Please select an input file")
        return
    if not fmt:
        messagebox.showwarning("Warning", "Please select an output format")
        return
    status_label.config(text="Converting file...")

    threading.Thread(target=convert_audio, args=(file, fmt), daemon=True).start()

root = tk.Tk()
root.title("Audio Converter")
root.geometry("700x300")

button_font = font.Font(family="Arial", size=16 , weight="bold")

button_style = ttk.Style()
button_style.configure("My.TButton",
                relief="flat",
                background="lightgray",
                font=button_font)
button_style.map("My.TButton",
          background=[("active", "white"), ("disabled", "gray")],
          foreground=[("active", "white")])

selected_file = tk.StringVar()
output_format = tk.StringVar()

ttk.Button(root, text="Check for FFmpeg", command=check_for_ffmpeg, style="My.TButton").pack(anchor="nw", padx=15)
label_ffmpeg = tk.Label(root, text="")
label_ffmpeg.pack(anchor="nw", padx=15)

ttk.Button(root, text="Choose File", command=open_file, style="My.TButton").pack(pady=5)
tk.Label(root, textvariable=selected_file, wraplength=300).pack(pady=5)

tk.Label(root, text="Output format:").pack(pady=5)
tk.OptionMenu(root, output_format, "mp3", "wav", "flac", "ogg", "aac").pack(pady=5)

ttk.Button(root, text="Convert", command=run_conversion, style="My.TButton").pack(pady=10)

status_label = tk.Label(root, text="")
status_label.pack(pady=5)

root.mainloop()