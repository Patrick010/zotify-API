import json
import yaml
import sys

def summarize_doc(_):
    """Mock function to simulate summarizing a document."""
    return "Mock document description"

def summarize_code_nlp(_):
    """Mock function to simulate summarizing code."""
    return "Mock code description"

def generate_mock_descriptions():
    """
    Loads artifacts from TRACE_INDEX.yml, generates mock descriptions for them,
    and saves the result to a JSON file.
    """
    trace_index_path = 'project/reports/TRACE_INDEX.yml'
    output_path = 'scripts/trace_description_intermediate.json'
    descriptions = {}
    processed_files = 0
    failures = 0

    try:
        with open(trace_index_path, 'r', encoding='utf-8') as f:
            trace_index = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Trace index file not found at {trace_index_path}")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        sys.exit(1)

    artifacts = trace_index.get('artifacts', [])

    for artifact in artifacts:
        file_path = artifact.get('file')
        file_type = artifact.get('type')

        if not file_path:
            failures += 1
            continue

        processed_files += 1

        try:
            if file_type == 'doc':
                description = summarize_doc(file_path)
            elif file_type == 'code':
                description = summarize_code_nlp(file_path)
            else:
                # As per instructions, default to "No description available" if there's an error or unknown type
                description = "No description available"
            descriptions[file_path] = description
        except Exception:
            descriptions[file_path] = "No description available"
            failures += 1

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(descriptions, f, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"Error writing to output file {output_path}: {e}")
        # Not counted as a processing failure, but still a critical error
        sys.exit(1)

    print(f"Processing complete.")
    print(f"  - Processed files: {processed_files}")
    print(f"  - Failures: {failures}")

if __name__ == "__main__":
    generate_mock_descriptions()