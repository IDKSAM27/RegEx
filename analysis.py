import re
import execjs

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

def analyse_javascript_code(code):
    errors = []
    try:
        execjs.eval(code)
    except Exception as e:
        # Extract line number if available
        error_message = str(e)
        print(f"Error Message: {error_message}") # print the error message to debug.

        line_match = re.search(r'line (\d+)', error_message, re.IGNORECASE)
        if line_match:
            line_number = int(line_match.group(1)) # Convert to integer (This is what I changed!)
            errors.append(f"Line {line_number}: {error_message}")
        else:
            # errors.append(error_message)
            errors.append(f"Error: {error_message}")
    return errors

# Redirect analysis to the appropriate function
def analyse_code_redirector(code, language):
    if language == "C++":
        return check_missing_semicolons_cpp(code)
    elif language == "Python":
        return analyse_python_code(code)
    elif language == "JS":
        return analyse_javascript_code(code)
    return []