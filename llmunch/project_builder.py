import os
from pathlib import Path

class ProjectBuilder:
    @staticmethod
    def parse_llmunch_file(input_file):
        """Parse an LLMunch output file back into individual files"""
        current_file = None
        current_content = []
        files = {}
        
        with open(input_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('---- ') and 'end of' not in line:
                    # Start of new file
                    if current_file:
                        files[current_file] = ''.join(current_content).rstrip('\n')
                    current_file = line.strip()[5:-5].strip()
                    current_content = []
                elif line.startswith('---- end of '):
                    # End of current file
                    if current_file:
                        files[current_file] = ''.join(current_content).rstrip('\n')
                        current_file = None
                elif current_file is not None:
                    current_content.append(line)
        
        return files

    @staticmethod
    def rebuild_project(input_file, output_dir='.'):
        """Rebuild project structure from LLMunch output"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        files = ProjectBuilder.parse_llmunch_file(input_file)
        
        for relative_path, content in files.items():
            full_path = output_path / relative_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content, encoding='utf-8')
        
        return len(files)