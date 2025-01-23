import tkinter as tk
from gui import open_language_selector
import ttkbootstrap as ttk

if __name__ == "__main__":
    # Initialize the language selector window
    language_selector = ttk.Window(themename="solar")
    language_selector.title("Select Language")

    selected_language = tk.StringVar()

    open_language_selector(language_selector, selected_language)
    language_selector.mainloop()

# Use the same RE technique in python too.
# Commenting after any {} in cpp will cause missing semicolon error
# Highlighting problem is js analysis (nothing works bcs, highlighting def taked line "number" and js errors does not give line numbers in their error)