import re
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

# Function to check missing semicolons for C++
def check_missing_semicolons(code):
    # The below pattern checks for missing semicolons, if neglects the error if any of the special case appears.
    pattern = r"^(?!\s*#)(?!.*\b(main|if|else|while|for|switch|case)\b).*[^\s;{}]\s*$"
    errors = []
    for i, line in enumerate(code.splitlines(), 1):
        if re.search(pattern, line):
            errors.append(f"Line {i}: Missing semicolon.")
    return errors

# Function to check syntax for Python
def check_python_syntax(code):
    errors = []
    try:
        compile(code, "<string>", "exec")
    except SyntaxError as e:
        errors.append(f"Line {e.lineno}: {e.msg}")
    return errors

# Function to analyze code based on language
def analyse_code(code, language):
    errors = []
    if language == "C++":
        errors.extend(check_missing_semicolons(code))
    elif language == "Python":
        errors.extend(check_python_syntax(code))
    return errors

# Function to analyze code in the GUI
def analyse_code_gui():
    code = code_input.get("1.0", tk.END).strip()
    if not code:
        messagebox.showwarning("Warning", "Please enter some code to analyze.")
        return

    errors = analyse_code(code, selected_language.get())
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

# Function to open the main window
def open_main_window():
    if not selected_language.get():
        messagebox.showwarning("Warning", "Please select a language.")
        return

    language_selector.destroy()

    # Create the main window
    root = tk.Tk()
    root.title(f"Code Analyzer - {selected_language.get()}")

    # Create widgets
    example_btn = tk.Button(root, text="Show example code", command=set_language_example)
    input_label = tk.Label(root, text=f"Enter your {selected_language.get()} code below:")
    global code_input
    code_input = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=15)
    analyze_button = tk.Button(root, text="Analyze Code", command=analyse_code_gui)
    result_label = tk.Label(root, text="Results:")
    global result_output
    result_output = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=10, state=tk.DISABLED)

    # Layout widgets
    input_label.pack(pady=5)
    code_input.pack(padx=10, pady=5)
    analyze_button.pack(pady=5)
    result_label.pack(pady=5)
    result_output.pack(padx=10, pady=5)
    example_btn.pack(pady=5)

    # Run the main loop
    root.mainloop()

def set_language_example():
    if selected_language.get() == "C++":
        example_code = "// Example C++ Code\n#include <iostream>\nint main() {\n    std::cout << \"Hello, World!\";\n    return 0;\n}"
    elif selected_language.get() == "Python":
        example_code = "# Example Python Code\nprint(\"Hello, World!\")"
    code_input.delete("1.0", tk.END)
    code_input.insert(tk.END, example_code)

# Create the language selector window
language_selector = tk.Tk()
language_selector.title("Select Language")

selected_language = tk.StringVar()

language_label = tk.Label(language_selector, text="Select the programming language:")
language_label.pack(pady=10)

languages = ["C++", "Python"]
for lang in languages:
    rb = tk.Radiobutton(language_selector, text=lang, value=lang, variable=selected_language, indicatoron=0)
    rb.pack(anchor="w", padx=20, fill="x")

continue_button = tk.Button(language_selector, text="Continue", command=open_main_window)
continue_button.pack(pady=10)

# Run the language selector loop
language_selector.mainloop()