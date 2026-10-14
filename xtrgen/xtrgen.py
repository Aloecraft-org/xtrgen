#!/usr/bin/env python3
'''
Fill {{placeholder}} tokens in a template from a JSON or YAML config.

plain string replacement, no escaping, no nesting.

File: ./xtrgen/xtrgen.py
License: Apache-2.0 (disclaimer at bottom of file)
'''
import argparse, json, os, tempfile

def load_config(config_input):
    if os.path.exists(config_input):
        ext = os.path.splitext(config_input)[1].lower()
        with open(config_input, 'r', encoding='utf-8') as config_file:
            if ext in ('.yml', '.yaml'):
                import yaml  # PyYAML, only needed for YAML configs
                return yaml.safe_load(config_file)
            return json.load(config_file)

def load_template(template_input):
    if os.path.exists(template_input):
        with open(template_input, 'r', encoding='utf-8') as template_file:
            return template_file.read()
    try:
        return str(template_input)
    except Exception:
        raise ValueError("Template is not a valid file path or string.")

def save_output(output_path, content):
    out_dir = os.path.dirname(os.path.abspath(output_path))
    fd, tmp_path = tempfile.mkstemp(dir=out_dir, prefix='.tmp-', text=True)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as output_file:
            output_file.write(content)
        os.replace(tmp_path, output_path)
    except BaseException:
        os.unlink(tmp_path)
        raise

def fill_template(config, template_content):
    """Replaces placeholders in the template content with config values."""
    output_content = template_content
    for key, value in config.items():        
        output_content = output_content.replace("{{"+key+"}}", str(value))
    return output_content

def main():
    parser = argparse.ArgumentParser(description='Generate a file from a template and configuration.')
    parser.add_argument('--config', required=True, help='Path to the config file OR a JSON string.')
    parser.add_argument('--template', required=True, help='Path to the template file OR a JSON string.')
    parser.add_argument('--out', help='Path to the output file. If omitted or "-", prints to stdout.')
    args = parser.parse_args()

    # 1. Load inputs
    config_data = load_config(args.config)
    template_content = load_template(args.template)

    # 2. Process template
    output_content = fill_template(config_data, template_content)

    # 3. Handle output
    if args.out and args.out != '-':
        save_output(args.out, output_content)
    else:
        print(output_content)

if __name__ == '__main__':
    main()

# Copyright Michael Godfrey 2026 | aloecraft.org <michael@aloecraft.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.