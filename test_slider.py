import customtkinter as ctk
from tkinter import Tk

print("creating root")
root = ctk.CTk()
print("root created")

# try creating slider with numeric bounds
try:
    slider = ctk.CTkSlider(root, from_=0, to=10)
    print("slider created")
except Exception as e:
    print("slider error", e)

root.destroy()
print("done")
