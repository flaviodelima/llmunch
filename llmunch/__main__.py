import argparse
from pathlib import Path
import sys
from llmunch.file_processor import FileProcessor
from llmunch.project_builder import ProjectBuilder

def main():
    parser = argparse.ArgumentParser(description='Combine text files into one or rebuild project structure.')
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Combine command
    combine_parser = subparsers.add_parser('combine', help='Combine files into one')
    combine_parser.add_argument('output', help='Output file name')
    combine_parser.add_argument('-d', '--directory', default='.', 
                              help='Directory to search (default: current dir)')
    combine_parser.add_argument('-e', '--extension', nargs='+', default=['*'], 
                              help='File extension(s) to include (e.g., txt py)')

    # Rebuild command
    rebuild_parser = subparsers.add_parser('rebuild', help='Rebuild project from LLMunch output')
    rebuild_parser.add_argument('input', help='LLMunch output file to process')
    rebuild_parser.add_argument('-o', '--output-dir', default='.', 
                              help='Output directory (default: current dir)')
    
    args = parser.parse_args()
    
    try:
        if args.command == 'combine':
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
            
        elif args.command == 'rebuild':
            processed = ProjectBuilder.rebuild_project(args.input, args.output_dir)
            print(f"Successfully rebuilt {processed} files into '{args.output_dir}'")
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()