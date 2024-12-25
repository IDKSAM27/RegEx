import re

def check_missing_semicolons(code):
    pattern = r"[^\s;{}]\s*$"
    errors = []
    for i, line in enumerate(code.splitlines(), 1):
        if re.search(pattern, line):
            errors.append(f"Line {i}: Missing semicolon.")
    return errors

def analyse_code(code):
    errors = []
    errors.extend(check_missing_semicolons(code))
    return errors

if __name__ == "__main__":
    print("Enter your code (type END on a new line to finish):")
    code_lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        code_lines.append(line)

    code = "\n".join(code_lines)
    errors = analyse_code(code)
    if errors:
        print("Issues found:")
        for errors in errors:
            print(errors)
        
    else: 
        print("No issues found!")