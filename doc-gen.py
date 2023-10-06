import os
import re

# doc-gen.py
#
# This script generates the MODULE_DEFINITIONS.md file from the source code.
# It is used to generate the documentation for the Rell modules.
#
# Usage:
#   python3 doc-gen.py
#
# The script will generate the MODULE_DEFINITIONS.md file in the current directory.
# It will overwrite the file if it already exists.
#
# The script will ignore the lib and test directories.
#
# The script will generate the documentation for the following types of files:
#   - function.rell
#   - operation.rell
#   - query.rell
#
# The script will generate the documentation for the following types of comments:
#   - @operation
#   - @query
#   - @function
#   - @arg
#   - @description
# For example:
#   @operation operation_name
#   @arg {arg_name}: arg_type - arg_description
#   @description description
#


def parse_operation(line, current_token, documentation):
    operation_match = re.search(r'@operation\s+(\w+)', line)
    if operation_match:
        current_token = operation_match.group(1)
        documentation[current_token] = {'args': [], 'type': 'operation'}
    return current_token


def parse_query(line, current_token, documentation):
    query_match = re.search(r'@query\s+(\w+)', line)
    if query_match:
        current_token = query_match.group(1)
        documentation[current_token] = {'args': [], 'type': 'query'}
    return current_token


def parse_function(line, current_token, documentation):
    function_match = re.search(r'@function\s+(\w+)', line)
    if function_match:
        current_token = function_match.group(1)
        documentation[current_token] = {'args': [], 'type': 'function'}
    return current_token


def parse_arguments(line, current_token, documentation):
    arg_match = re.search(r'@arg\s+\{([^}]*)\}: (\w+)\s*-\s*([^@]*)', line)
    if arg_match and current_token:
        arg_type, arg_name, arg_description = arg_match.groups()
        documentation[current_token]['args'].append({
            'type': arg_type.strip(),
            'name': arg_name.strip(),
            'description': arg_description.strip()
        })
    return current_token


def parse_description(line, current_token, documentation):
    description_match = re.search(r'@description\s*(.*)', line)
    if description_match and current_token:
        documentation[current_token]['description'] = description_match.group(1).strip()
    return current_token


def parse_documentation(source_code):
    documentation = {}
    current_token = None

    lines = source_code.split('\n')

    for line in lines:
        current_token = parse_operation(line, current_token, documentation)
        current_token = parse_query(line, current_token, documentation)
        current_token = parse_function(line, current_token, documentation)
        current_token = parse_arguments(line, current_token, documentation)
        current_token = parse_description(line, current_token, documentation)

    return documentation


def generate_markdown_documentation(documentation, directory_name):
    markdown = ""

    categories = {'Queries': 'query', 'Operations': 'operation', 'Functions (internal only)': 'function'}

    for category, keyword in categories.items():
        category_docs = [f"\n\n## {category}\n\n"]

        for token, details in documentation.items():
            if 'args' in details and details['type'] == keyword:
                category_docs.append(f"\n\n### Name: `{token}`\n\n")
                if 'description' in details:
                    category_docs.append("Description:\n\n")
                    category_docs.append(f"> {details['description']}\n\n")

                if details['args']:
                    category_docs.append("### Arguments\n\n")
                    category_docs.append("|Name|Type|Description|\n|----|----|-----|\n")
                    for arg in details['args']:
                        category_docs.append(f"|`{arg['type']}`|`{arg['name']}`|{arg['description']}|\n")

        if len(category_docs) > 1:  # Check if there are entries for the category
            markdown += ''.join(category_docs)

    return markdown


def process_directory(directory_path, output_file):
    processed_directories = set()  # Keep track of processed directories
    for root, dirs, files in os.walk(directory_path):
        # remove lib and test directories
        if 'lib' in dirs:
            dirs.remove('lib')
        if 'test' in dirs:
            dirs.remove('test')

        dirs.sort()

        directory_name = os.path.basename(root)
        if not directory_name:
            continue  # Skip the iteration if the directory name is empty

        if directory_name not in processed_directories:
            # Print the directory name only once
            with open(output_file, 'a') as output:
                output.write(f"\n# {directory_name.capitalize()}\n\n")
            processed_directories.add(directory_name)

            for file in files:
                if file.endswith(('function.rell', 'operation.rell', 'query.rell')):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as file_content:
                        source_code = file_content.read()
                        parsed_documentation = parse_documentation(source_code)
                        markdown_documentation = generate_markdown_documentation(
                            parsed_documentation, directory_name)
                        with open(output_file, 'a') as output:
                            output.write(markdown_documentation)


output_file_path = "MODULE_DEFINITIONS.md"

if os.path.exists(output_file_path):
    # If it exists, delete it
    os.remove(output_file_path)
    print(f"Updating outdated {output_file_path}")

source_directory_path = "./src/"
process_directory(source_directory_path, output_file_path)
