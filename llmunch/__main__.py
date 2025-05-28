import argparse
from pathlib import Path
import sys

def validate_directory(directory_path):
    """Check if the directory exists and is valid."""
    if not directory_path.is_dir():
        print(f"Error: Directory '{directory_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

def normalize_extension(extension):
    """Ensure the extension starts with a dot."""
    return extension if extension.startswith('.') else f'.{extension}'

def find_matching_files(directory_path, extensions):
    """Find all files with the given extensions in directory and subdirectories."""
    all_files = []
    for extension in extensions:
        all_files.extend(list(directory_path.rglob(f'*{extension}')))
    
    if not all_files:
        extensions_str = "', '".join(extensions)
        print(f"No files found with extension(s) '{extensions_str}' in '{directory_path}'", file=sys.stderr)
        sys.exit(1)
    return all_files

def read_file_content(file_path):
    """Read file content with error handling."""
    try:
        return file_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Skipping {file_path}: {e}", file=sys.stderr)
        return None

def format_file_header(relative_path):
    """Format the file start marker with the relative path."""
    return f'---- {relative_path} ----\n'

def format_file_footer(relative_path):
    """Format the file end marker with the relative path."""
    return f'---- end of {relative_path} ----\n\n'

def format_file_content(content):
    """Ensure proper formatting of file content with newlines."""
    # Remove any trailing newlines to prevent double spacing
    content = content.rstrip('\n')
    return content + '\n'

def process_files(directory_path, files, output_file_path):
    """Process all files and write to output with start/end markers."""
    processed_files = 0
    
    with open(output_file_path, 'w', encoding='utf-8') as out_file:
        for file_path in files:
            if not file_path.is_file():
                continue

            content = read_file_content(file_path)
            if content is None:
                continue

            relative_path = file_path.relative_to(directory_path)
            
            out_file.write(format_file_header(relative_path))
            out_file.write(format_file_content(content))
            out_file.write(format_file_footer(relative_path))
            
            processed_files += 1

    return processed_files

def main():
    parser = argparse.ArgumentParser(description='Combine text files into one.')
    parser.add_argument('output', help='Output file name')
    parser.add_argument('-d', '--directory', default='.', help='Directory to search')
    parser.add_argument('-e', '--extension', nargs='+', default=['*'], 
                       help='File extension(s) to include (e.g., txt py). Default: all files')
    args = parser.parse_args()

    extensions = [normalize_extension(ext) for ext in args.extension]
    dir_path = Path(args.directory)
    validate_directory(dir_path)

    files = find_matching_files(dir_path, extensions)
    processed_files = process_files(dir_path, files, args.output)

    if processed_files == 0:
        print("No files were processed.", file=sys.stderr)
        sys.exit(1)
    print(f"Successfully combined {processed_files} files into '{args.output}'.")

if __name__ == '__main__':
    main()    
