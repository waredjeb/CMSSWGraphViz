#!/usr/bin/env python3
"""
Parse CMSSW dumpConfig.py output to extract module definitions,
parameters, and InputTag references.
"""

import sys
import re
import json
from pathlib import Path
from typing import Dict, List, Any


def extract_balanced_block(text, start_pos):
    """
    Extract a balanced parentheses/braces block starting from start_pos.
    Returns (block_content, end_pos).
    """
    depth = 0
    i = start_pos
    start_char = text[i]

    if start_char == '(':
        open_char, close_char = '(', ')'
    elif start_char == '{':
        open_char, close_char = '{', '}'
    else:
        return "", start_pos

    block = ""
    in_string = False
    escape_next = False

    while i < len(text):
        char = text[i]

        # Handle string escaping
        if escape_next:
            escape_next = False
            block += char
            i += 1
            continue

        if char == '\\':
            escape_next = True
            block += char
            i += 1
            continue

        # Handle strings
        if char in ('"', "'"):
            in_string = not in_string
            block += char
            i += 1
            continue

        if not in_string:
            if char == open_char:
                depth += 1
            elif char == close_char:
                depth -= 1
                if depth == 0:
                    return block, i

        block += char
        i += 1

    return block, i


def parse_input_tag(tag_str):
    """
    Parse an InputTag string like "module:instance:process" or "module:instance" or "module".
    Returns dict with module, instance, process fields.
    """
    parts = tag_str.split(':')

    return {
        "module": parts[0] if len(parts) > 0 else "",
        "instance": parts[1] if len(parts) > 1 else "",
        "process": parts[2] if len(parts) > 2 else ""
    }


def parse_input_tags(param_block):
    """
    Extract all InputTag, VInputTag, and ESInputTag from a parameter block.
    Returns list of {field, module, instance, process} dicts.
    """
    input_tags = []

    # Pattern for single InputTag: fieldName = cms.InputTag("module:instance:process")
    single_pattern = r'(\w+)\s*=\s*cms\.(InputTag|ESInputTag)\s*\(\s*["\']([^"\']+)["\']\s*(?:,\s*["\']([^"\']*)["\']\s*)?(?:,\s*["\']([^"\']*)["\']\s*)?\)'

    for match in re.finditer(single_pattern, param_block):
        field_name = match.group(1)
        tag_type = match.group(2)
        module = match.group(3)
        instance = match.group(4) if match.group(4) else ""
        process = match.group(5) if match.group(5) else ""

        # Handle colon-separated format
        if ':' in module:
            parts = parse_input_tag(module)
            module = parts["module"]
            instance = parts["instance"] if not instance else instance
            process = parts["process"] if not process else process

        input_tags.append({
            "field": field_name,
            "type": tag_type,
            "module": module,
            "instance": instance,
            "process": process
        })

    # Pattern for VInputTag: fieldName = cms.VInputTag(...)
    # Need to match balanced parentheses, so use a more robust approach
    vinput_pattern = r'(\w+)\s*=\s*cms\.VInputTag\s*\('

    for match in re.finditer(vinput_pattern, param_block):
        field_name = match.group(1)
        start_pos = match.end() - 1  # Position of opening paren

        # Extract balanced parentheses content
        vinput_content, _ = extract_balanced_block(param_block, start_pos)

        # Try to find cms.InputTag objects first
        inner_input_tags = re.findall(
            r'cms\.InputTag\s*\(\s*["\']([^"\']+)["\']\s*(?:,\s*["\']([^"\']*)["\']\s*)?(?:,\s*["\']([^"\']*)["\']\s*)?\)',
            vinput_content
        )

        if inner_input_tags:
            # VInputTag contains cms.InputTag objects
            for idx, tag_tuple in enumerate(inner_input_tags):
                module = tag_tuple[0]
                instance = tag_tuple[1] if tag_tuple[1] else ""
                process = tag_tuple[2] if tag_tuple[2] else ""

                # Handle colon-separated format
                if ':' in module:
                    parts = parse_input_tag(module)
                    module = parts["module"]
                    instance = parts["instance"] if not instance else instance
                    process = parts["process"] if not process else process

                input_tags.append({
                    "field": field_name,
                    "type": "VInputTag",
                    "index": idx,
                    "module": module,
                    "instance": instance,
                    "process": process
                })
        else:
            # VInputTag contains simple strings
            # Pattern: "string1", "string2", "string3"
            simple_strings = re.findall(r'["\']([^"\']+)["\']', vinput_content)

            for idx, tag_str in enumerate(simple_strings):
                # Parse as module:instance:process or just module
                if ':' in tag_str:
                    parts = parse_input_tag(tag_str)
                    module = parts["module"]
                    instance = parts["instance"]
                    process = parts["process"]
                else:
                    # Just a module name
                    module = tag_str
                    instance = ""
                    process = ""

                input_tags.append({
                    "field": field_name,
                    "type": "VInputTag",
                    "index": idx,
                    "module": module,
                    "instance": instance,
                    "process": process
                })

    return input_tags


def parse_simple_params(param_block):
    """
    Extract simple parameters (int32, string, bool, double, etc.).
    Returns dict of {paramName: {type, value}}.
    """
    params = {}

    # Pattern for simple types
    simple_pattern = r'(\w+)\s*=\s*cms\.(int32|uint32|int64|uint64|string|bool|double|untracked\.string|untracked\.int32|untracked\.bool)\s*\(([^)]+)\)'

    for match in re.finditer(simple_pattern, param_block):
        param_name = match.group(1)
        param_type = match.group(2)
        param_value = match.group(3).strip().strip('"\'')

        params[param_name] = {
            "type": param_type,
            "value": param_value
        }

    return params


def parse_config_file(config_path, max_snippet_lines=50):
    """
    Parse CMSSW config dump file.

    Returns:
        dict mapping module_name -> {type, plugin, parameters, inputTags, rawSnippet}
    """
    print(f"Parsing config file: {config_path}")

    with open(config_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    modules = {}

    # Pattern for module definitions
    # process.moduleName = cms.EDProducer("PluginName", ...
    module_pattern = r'process\.(\w+)\s*=\s*cms\.(EDProducer|EDFilter|EDAnalyzer|OutputModule|ESProducer|ESSource)\s*\(\s*["\']([^"\']+)["\']\s*'

    for match in re.finditer(module_pattern, content):
        module_name = match.group(1)
        module_type = match.group(2)
        plugin_name = match.group(3)

        # Find the start of the parameter block
        param_start = match.end()

        # Extract the balanced parameter block
        if param_start < len(content) and content[param_start] in (',', ')'):
            # Find opening paren for parameters
            paren_pos = content.find('(', match.start())
            if paren_pos != -1:
                block, block_end = extract_balanced_block(content, paren_pos)

                # Parse InputTags
                input_tags = parse_input_tags(block)

                # Parse simple parameters
                simple_params = parse_simple_params(block)

                # Extract raw snippet (limited lines)
                snippet_start = match.start()
                snippet_end = min(block_end + 1, len(content))
                raw_snippet = content[snippet_start:snippet_end]

                # Limit snippet to max lines
                snippet_lines = raw_snippet.split('\n')
                if len(snippet_lines) > max_snippet_lines:
                    raw_snippet = '\n'.join(snippet_lines[:max_snippet_lines]) + '\n...(truncated)'

                modules[module_name] = {
                    "type": module_type,
                    "plugin": plugin_name,
                    "parameters": simple_params,
                    "inputTags": input_tags,
                    "rawSnippet": raw_snippet
                }

    print(f"  Parsed {len(modules)} modules")

    return modules


def main():
    if len(sys.argv) < 2:
        print("Usage: python parse_config.py <path_to_config_file>")
        sys.exit(1)

    config_path = sys.argv[1]

    if not Path(config_path).exists():
        print(f"Error: File not found: {config_path}")
        sys.exit(1)

    modules = parse_config_file(config_path)

    print(json.dumps(modules, indent=2))


if __name__ == "__main__":
    main()
