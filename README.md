# llmunch
A tool for prepping software project data for LLMs

## Usage
### Combine files into single output
```bash
llmunch combine output.txt -d /path/to/project -e py txt
```

### Rebuild project from LLMunch output
```bash
llmunch rebuild output.txt -o /path/to/reconstructed_project
```

## Features
### Combine Mode
The combine mode takes a directory and a list of file extensions and combines all files with those extensions into a single output file. It:
- Recursively scans the directory for files with the specified extensions
- Combines the contents of all files into a single output file
- Adds clean file markers to separate each file's content

### Rebuild Mode
The rebuild mode takes an LLMunch output file and reconstructs the original project structure. It:
- Recreates original directory structure
- Preserves exact file contents
- Handles nested directories

## Installation
```bash
pip install .
```

or
```bash
pip install -e .
```
for development (editable install)
