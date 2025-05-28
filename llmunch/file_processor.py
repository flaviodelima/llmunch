from pathlib import Path
import sys

class FileProcessor:
    @staticmethod
    def validate_directory(directory_path):
        """Check if directory exists"""
        if not directory_path.is_dir():
            raise ValueError(f"Directory '{directory_path}' does not exist")

    @staticmethod
    def normalize_extension(extension):
        """Ensure extension starts with a dot"""
        return extension if extension.startswith('.') else f'.{extension}'

    @staticmethod
    def find_matching_files(directory_path, extensions):
        """Find files with given extensions"""
        all_files = []
        for extension in extensions:
            all_files.extend(directory_path.rglob(f'*{extension}'))
        return all_files

    @staticmethod
    def read_file_content(file_path):
        """Read file content with error handling"""
        try:
            return file_path.read_text(encoding='utf-8')
        except Exception as e:
            print(f"Skipping {file_path}: {e}", file=sys.stderr)
            return None

    @staticmethod
    def process_files(directory_path, files, output_file_path):
        """Process files and write to output"""
        processed_files = 0
        with open(output_file_path, 'w', encoding='utf-8') as out_file:
            for file_path in files:
                if not file_path.is_file():
                    continue
                content = FileProcessor.read_file_content(file_path)
                if content is None:
                    continue
                
                relative_path = file_path.relative_to(directory_path)
                out_file.write(f'---- {relative_path} ----\n')
                out_file.write(content.rstrip('\n') + '\n')
                out_file.write(f'---- end of {relative_path} ----\n\n')
                processed_files += 1
        return processed_files