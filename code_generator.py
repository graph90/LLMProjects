# ollama run llama3.1
# This script uses a llm to generate, save, and execute Python code based on a provided prompt.
# python3 code_generator.py "python quicksort" "quicksort.py"

import argparse, subprocess, re
from langchain_community.llms import Ollama
def extractPythonCode(full_text):
    pattern = r"```python\n(.*?)\n```"
    match = re.search(pattern, full_text, re.DOTALL)
    if match:
        return match.group(1)
    return ""
def saveCode(prompt, filename):
    llm = Ollama(model="llama3.1")
    full_response = llm.invoke(prompt)
    code = extractPythonCode(full_response)
    with open(filename, "w") as file:
        file.write(code)
    print(f"Code for '{prompt}' has been saved to {filename}")
    return code
def runCode(filename):
    try:
        result = subprocess.run(['python3', filename], capture_output=True, text=True, check=True)
        print(result.stdout)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        print(e.stderr)
        with open("errors.txt", "w") as error_file:
            error_file.write(e.stderr)
        return False, e.stderr
def fixCode(prompt, filename, original_code, errors):
    llm = Ollama(model="llama3.1")
    new_prompt = f"{prompt}\n\nHere is the code that was generated:\n```python\n{original_code}\n```\n\nHere are the errors encountered:\n{errors}\n\nPlease fix the errors and provide the corrected code."
    full_response = llm.invoke(new_prompt)
    fixed_code = extractPythonCode(full_response)
    with open(filename, "w") as file:
        file.write(fixed_code)
    print(f"Fixed code has been saved to {filename}")
    return fixed_code
def addDocstring(prompt, filename, code):
    llm = Ollama(model="llama3.1")
    new_prompt = f"Please add docstrings to the following code:\n```python\n{code}\n```\n\n{prompt}"
    full_response = llm.invoke(new_prompt)
    docstring_code = extractPythonCode(full_response)
    with open(filename, "w") as file:
        file.write(docstring_code)
    print(f"Docstring-added code has been saved to {filename}")
    return docstring_code
def generateAndRunCode(prompt, filename, max_attempts=7):
    attempt = 0
    code = saveCode(prompt, filename)
    while attempt < max_attempts:
        success, result = runCode(filename)
        if success:
            print("Code ran successfully.")
            docstring_code = addDocstring(prompt, filename, code)
            success, result = runCode(filename)
            if success:
                print("Final test ran successfully.")
            else:
                print("Final test failed.")
            break
        else:
            print(f"Attempt {attempt + 1} failed. Fixing errors...")
            code = fixCode(prompt, filename, code, result)
        attempt += 1
    else:
        print("Maximum attempts reached. Code could not be fixed.")
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate and save Python code from an AI')
    parser.add_argument('prompt', type=str, help='The prompt for the AI ("python quicksort")')
    parser.add_argument('filename', type=str, help='The filename to save the generated code ("quicksort.py")')
    args = parser.parse_args()
    generateAndRunCode(args.prompt, args.filename)
