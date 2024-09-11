# LLM Projects

This repository contains two distinct projects that leverage large language models (LLMs) for generating, refining, and summarizing Python code and text.

## Project 1: Code Generator and Executor

### Description
This project uses an LLM to generate, save, and execute Python code based on a provided prompt. It includes functionality for generating code, fixing errors, and adding docstrings to the code. The code is then executed and tested, with the option to retry if errors occur.

### Files
- `code_generator.py`: The main script for generating, saving, and running Python code based on an LLM's response.

### Dependencies

    langchain_community (Ollama LLMs)

### Key Functions

    extractPythonCode(full_text): Extracts Python code from the LLM's response.
    saveCode(prompt, filename): Generates and saves code based on the prompt.
    runCode(filename): Executes the generated code and handles errors.
    fixCode(prompt, filename, original_code, errors): Fixes errors in the generated code.
    addDocstring(prompt, filename, code): Adds docstrings to the code.
    generateAndRunCode(prompt, filename, max_attempts=7): Manages the code generation and execution process with multiple attempts.

Project 2: Pooled AI Summarizer
Description

This project leverages multiple specialized LLMs to collaboratively generate and refine a summary based on a given prompt. It utilizes various models for different roles and combines their responses iteratively to produce a comprehensive final summary.
Files

    multiLLM.py: The main script for using multiple LLMs to generate and refine a summary.
