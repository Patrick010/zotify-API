import yaml
import sys
import re

def enrich_code_file_index(code_file_index_path):
    """
    Enriches a CODE_FILE_INDEX.md file with descriptions from TRACE_INDEX.yml.
    """
    # Load the TRACE_INDEX.yml file
    with open('project/reports/TRACE_INDEX.yml', 'r') as f:
        trace_index = yaml.safe_load(f)

    # Create a mapping from file path to description
    description_map = {
        item['path']: item.get('description', '')
        for item in trace_index['artifacts']
    }

    # Read the CODE_FILE_INDEX.md file
    with open(code_file_index_path, 'r') as f:
        lines = f.readlines()

    new_lines = []
    header_found = False
    for line in lines:
        if re.match(r'\|.*Path.*\|', line):
            header_found = True
            new_lines.append(line)
            continue

        if header_found and line.strip().startswith('|'):
            parts = [p.strip() for p in line.split('|')]
            if len(parts) > 2:
                path_part = parts[1]
                path_match = re.search(r'`([^`]+)`', path_part)
                if path_match:
                    path = path_match.group(1)
                    if path in description_map and description_map[path]:
                        # Reconstruct the line with the new description
                        # This assumes a certain table structure.
                        # It's brittle but better than the pandas version for this specific format.
                        # | Path | Type | Description | Status | Linked Docs | Notes |

                        # Find which part is the description
                        header_line = lines[[i for i, l in enumerate(lines) if '| Path' in l][0]]
                        headers = [h.strip() for h in header_line.split('|') if h.strip()]
                        try:
                            desc_index = headers.index('Description') + 1 # +1 for leading empty part

                            # Ensure the parts list is long enough
                            while len(parts) <= desc_index:
                                parts.append('')

                            parts[desc_index] = f" {description_map[path]} "
                            new_line = '|'.join(parts) + '\n'
                            new_lines.append(new_line)
                        except ValueError:
                            new_lines.append(line) # Append original if 'Description' header not found
                    else:
                        new_lines.append(line)
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    # Write the updated content back to the file
    with open(code_file_index_path, 'w') as f:
        f.writelines(new_lines)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python enrich_code_file_index.py <path_to_code_file_index.md>")
        sys.exit(1)

    code_file_index_path = sys.argv[1]
    enrich_code_file_index(code_file_index_path)
    print(f"Successfully enriched {code_file_index_path}")