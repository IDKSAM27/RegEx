import re
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog

# Function to check missing semicolons for C++
def check_missing_semicolons_cpp(code):

    # The below pattern checks for missing semicolons, if neglects the error if any of the special case appears.
    pattern = r"^(?!\s*#)(?!\s*//)(?!.*\b(main|if|else|while|for|switch|case)\b).*[^\s;{}]\s*$"
    """
    (?!\s*#) = Negative lookahead assertion. Ensures that the line does not start with optional whitespace (\s*) followed by a #

    (?!.*\b(main|if|else|while|for|switch|case)\b) =

    \b : A word boundary. Ensures the keywords are matched as whole words, not as part of longer words (e.g., mainframe wouldn't match main).

    (main|if|else|while|for|switch|case) : A group with an alternation (|). Matches any one of the listed keywords.

    .* : Matches zero or more characters of any kind (except newlines), as long as previous conditions are satisfied.

    [^\s;{}] : A character class that matches any single character not in the set:
    \s : Whitespace characters (spaces, tabs, etc.).
    ; : A semicolon.
    { and } : Curly braces.

    \s* : Matches zero or more whitespace characters at the end of the line.

    $ : Matches the end of the string.
    """    
    errors = []
    for i, line in enumerate(code.splitlines(), 1):
        if re.search(pattern, line):
            errors.append(f"Line {i}: Missing semicolon.")
    return errors

# Function to check syntax for Python
def analyse_python_code(code):
    errors = []
    try:
        compile(code, "<string>", "exec")
    except SyntaxError as e:
        errors.append(f"Line {e.lineno}: {e.msg}")
    return errors


# Function to analyze code based on language
def analyse_cpp_code(code, language):
    errors = []
    if language == "C++":
        errors.extend(check_missing_semicolons_cpp(code))
    elif language == "Python":
        errors.extend(analyse_python_code(code))
    return errors


# Function to analyze code in the GUI
def analyse_code_gui():
    code = code_input.get("1.0", tk.END).strip()
    if not code:
        messagebox.showwarning("Warning", "Please enter some code to analyze.")
        return

    errors = analyse_cpp_code(code, selected_language.get())
    if errors:
        result_output.config(state=tk.NORMAL)
        result_output.delete("1.0", tk.END)
        result_output.insert(tk.END, "Issues found:\n" + "\n".join(errors))
        result_output.config(state=tk.DISABLED)

        highlight_errors(code, errors)

    else:
        result_output.config(state=tk.NORMAL)
        result_output.delete("1.0", tk.END)
        result_output.insert(tk.END, "No issues found!")
        result_output.config(state=tk.DISABLED)

        code_input.tag_remove("error", "1.0", tk.END)


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
    save_button = tk.Button(root, text="Save Results", command=save_results)
    example_btn = tk.Button(root, text="Show example code", command=set_language_example)
    input_label = tk.Label(root, text=f"Enter your {selected_language.get()} code below:")
    global code_input
    code_input = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=15)
    analyze_button = tk.Button(root, text="Analyze Code", command=analyse_code_gui)
    result_label = tk.Label(root, text="Results:")
    global result_output
    result_output = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=10, state=tk.DISABLED)

    # Layout widgets
    save_button.pack(pady=5)
    example_btn.pack(pady=5)
    input_label.pack(pady=5)
    code_input.pack(padx=10, pady=5)
    analyze_button.pack(pady=5)
    result_label.pack(pady=5)
    result_output.pack(padx=10, pady=5)

    # Run the main loop
    root.mainloop()

def set_language_example():
    if selected_language.get() == "C++":
        example_code = "// Example C++ Code\n#include <iostream>\nint main() {\n    std::cout << \"Hello, World!\";\n    return 0;\n}"
    elif selected_language.get() == "Python":
        example_code = "# Example Python Code\nprint(\"Hello, World!\")"
    code_input.delete("1.0", tk.END)
    code_input.insert(tk.END, example_code)

def highlight_errors(code, errors):
    code_input.tag_remove("error", "1.0", tk.END)
    for error in errors:
        line_number = int(error.split(":")[0].split(" ")[1])
        start_index = f"{line_number}.0"
        end_index = f"{line_number}.end"
        code_input.tag_add("error", start_index, end_index)                                
    code_input.tag_config("error", background="yellow", foreground="red")

def save_results():
    results = result_output.get("1.0", tk.END).strip()
    if not results:
        messagebox.showinfo("Info", "No results to save.")
        return
    file_path = tk.filedialog.asksaveasfilename(defaultextension = ".txt", filetypes = [("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(results)
        messagebox.showinfo("Info", "Results saved successfully.")

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


language_selector.mainloop()

# Use the same RE technique in python too.
# Commenting after any {} in cpp will cause missing semicolon error
# Create a save button for saving the result!
