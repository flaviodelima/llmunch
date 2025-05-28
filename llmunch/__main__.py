import argparse
from pathlib import Path
import sys
from llmunch.file_processor import FileProcessor

def main():
    parser = argparse.ArgumentParser(description='Combine text files into one.')
    parser.add_argument('output', help='Output file name')
    parser.add_argument('-d', '--directory', default='.', 
                       help='Directory to search (default: current dir)')
    parser.add_argument('-e', '--extension', nargs='+', default=['*'], 
                       help='File extension(s) to include (e.g., txt py)')
    
    args = parser.parse_args()
    
    try:
        extensions = [FileProcessor.normalize_extension(ext) for ext in args.extension]
        dir_path = Path(args.directory)
        
        FileProcessor.validate_directory(dir_path)
        files = FileProcessor.find_matching_files(dir_path, extensions)
        
        if not files:
            extensions_str = "', '".join(extensions)
            print(f"No files found with extension(s) '{extensions_str}' in '{dir_path}'", 
                  file=sys.stderr)
            sys.exit(1)
            
        processed = FileProcessor.process_files(dir_path, files, args.output)
        print(f"Successfully combined {processed} files into '{args.output}'")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()