import os
import tkinter as tk
from tkinter import filedialog, messagebox

from audio import FFMPEG

def create_converted_filename(file: str, format: str):
    print("creating converted filename")
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
    convert_audio(input_file=file, format=fmt)

root = tk.Tk()
root.title("Audio Converter")
root.geometry("900x300")

selected_file = tk.StringVar()
output_format = tk.StringVar()

tk.Button(root, text="Choose File", command=open_file).pack(pady=5)
tk.Label(root, textvariable=selected_file, wraplength=300).pack(pady=5)

tk.Label(root, text="Output format:").pack(pady=5)
tk.OptionMenu(root, output_format, "mp3", "wav", "flac", "ogg", "aac").pack(pady=5)

tk.Button(root, text="Convert", command=run_conversion).pack(pady=10)

root.mainloop()