import tkinter as tk
from tkinter import scrolledtext, messagebox
from tkinter import filedialog
from analysis import analyse_code_redirector
from tkinter import Button, Label
from tkinter.ttk import Radiobutton

# Main GUI for analyzing code
def open_main_window(language_selector, selected_language):
    if not selected_language.get():
        messagebox.showwarning("Warning", "Please select a language.")
        return

    language_selector.destroy()

    # Create the main window
    root = tk.Tk()
    root.title(f"Code Analyzer - {selected_language.get()}")

    # Create widgets
    save_button = tk.Button(root, text="Save Results", command=lambda: save_results(result_output))
    example_btn = tk.Button(root, text="Show example code", command=lambda: set_language_example(code_input, selected_language))
    input_label = tk.Label(root, text=f"Enter your {selected_language.get()} code below:")
    code_input = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=15)
    analyze_button = tk.Button(root, text="Analyze Code", command=lambda: analyse_code_gui(code_input, result_output, selected_language))
    result_label = tk.Label(root, text="Results:")
    result_output = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=10, state=tk.DISABLED)

    # Layout widgets
    save_button.pack(pady=5)
    example_btn.pack(pady=5)
    input_label.pack(pady=5)
    code_input.pack(padx=10, pady=5)
    analyze_button.pack(pady=5)
    result_label.pack(pady=5)
    result_output.pack(padx=10, pady=5)

    root.mainloop()

# GUI for language selection
def open_language_selector(language_selector, selected_language):
    language_label = tk.Label(language_selector, text="Select the programming language:")
    language_label.pack(pady=10)

    languages = ["C++", "Python", "JS"]
    for lang in languages:
        rb = tk.Radiobutton(language_selector, text=lang, value=lang, variable=selected_language, indicatoron=0)
        rb.pack(anchor="w", padx=20, fill="x")

    continue_button = tk.Button(language_selector, text="Continue", command=lambda: open_main_window(language_selector, selected_language))
    continue_button.pack(pady=10)

# Display example code
def set_language_example(code_input, selected_language):
    example_code = ""
    if selected_language.get() == "C++":
        example_code = "// Example C++ Code\n#include <iostream>\nint main() {\n    std::cout << \"Hello, World!\";\n    return 0;\n}"
    elif selected_language.get() == "Python":
        example_code = "# Example Python Code\nprint(\"Hello, World!\")"
    elif selected_language.get() == "JS":
        example_code = "// Example JS Code\nconsole.log(\"Hello, World!\");"
    code_input.delete("1.0", tk.END)
    code_input.insert(tk.END, example_code)

# Analyze the code in the GUI
def analyse_code_gui(code_input, result_output, selected_language):
    code = code_input.get("1.0", tk.END).strip()
    if not code:
        messagebox.showwarning("Warning", "Please enter some code to analyze.")
        return

    errors = analyse_code_redirector(code, selected_language.get())
    if errors:
        result_output.config(state=tk.NORMAL)
        result_output.delete("1.0", tk.END)
        result_output.insert(tk.END, "Issues found:\n" + "\n".join(errors))
        result_output.config(state=tk.DISABLED)

        highlight_errors(code_input, errors)
    else:
        result_output.config(state=tk.NORMAL)
        result_output.delete("1.0", tk.END)
        result_output.insert(tk.END, "No issues found!")
        result_output.config(state=tk.DISABLED)
        code_input.tag_remove("error", "1.0", tk.END)

# Highlight errors in the code input
def highlight_errors(code_input, errors):
    code_input.tag_remove("error", "1.0", tk.END)
    for error in errors:
        try:
            line_number = int(error.split(":")[0].split(" ")[1])  # Extract line number
            start_index = f"{line_number}.0"
            end_index = f"{line_number}.end"
            code_input.tag_add("error", start_index, end_index)
        except (ValueError, IndexError):
            # Skip if no valid line number is found
            continue
    code_input.tag_config("error", background="yellow", foreground="red")

# Save analysis results to a file
def save_results(result_output):
    results = result_output.get("1.0", tk.END).strip()
    if not results:
        messagebox.showinfo("Info", "No results to save.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(results)
        messagebox.showinfo("Info", "Results saved successfully.")
