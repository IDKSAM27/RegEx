import re
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

def check_missing_semicolons(code):
    # The below pattern checks for missing semicolons, if neglects the error if any of the special case appears.
    pattern = r"^(?!\s*#)(?!.*\b(main|if|else|while|for|switch|case)\b).*[^\s;{}]\s*$"
    errors = []
    for i, line in enumerate(code.splitlines(), 1):

        if re.search(pattern, line): 
            errors.append(f"Line {i}: Missing semicolon.")
    return errors

def analyse_code(code):
    # This def is purely for returning errors 
    errors = []
    errors.extend(check_missing_semicolons(code))
    return errors

def analyse_code_gui():
    code = code_input.get("1.0", tk.END).strip()
    if not code:
        messagebox.showwarning("Warning", "Please enter some code to analyse.")
        return

    errors = analyse_code(code)
    if errors:
        result_output.config(state=tk.NORMAL)
        result_output.delete("1.0", tk.END)
        result_output.insert(tk.END, "Issues found:\n" + "\n".join(errors))
        result_output.config(state=tk.DISABLED)
    else:
        result_output.config(state=tk.NORMAL)
        result_output.delete("1.0", tk.END)
        result_output.insert(tk.END, "No issues found!")
        result_output.config(state=tk.DISABLED)

# Create the main window
root = tk.Tk()
root.title("Code Analyzer")

# Create widgets
input_label = tk.Label(root, text="Enter your code below:")
code_input = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=15)
analyze_button = tk.Button(root, text="Analyze Code", command=analyse_code_gui)
result_label = tk.Label(root, text="Results:")
result_output = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=10, state=tk.DISABLED)

# Layout widgets
input_label.pack(pady=5)
code_input.pack(padx=10, pady=5)
analyze_button.pack(pady=5)
result_label.pack(pady=5)
result_output.pack(padx=10, pady=5)

# Run the application
root.mainloop()
# Make an initial window for asking the programming language the user want to enter (eg., Python or C)