import json
from html5lib.html5parser import HTMLParser
#from html5lib.treewalkers.dom import TreeWalker
from xml.etree.ElementTree import Element

# Function to check if an element has child elements
def has_child_elements(html_content, context):
    print(f"Trying has_child_element for", html_content)
    # Parse the HTML content into a DOM tree using html5lib
    try:
        parser = HTMLParser()
        fragment = parser.parseFragment(stream=html_content, container='body')
        print(fragment, fragment)
        breakpoint()
        # Check if the root element has any child elements
        for node in fragment:
            if isinstance(node, Element):
                # XXX this is where the check needs to be but isn't....
                if node.tag == context:
                    print("context was", context, "node is", node)
                    return True
        return False

    except Exception as e:
        print(f"Error parsing HTML: {e}")
        return False

# Function to process each column (either script or xmp) and check all entries in the array
def check_html_entries(context_element, column_data):
    for outer in ["svg", "math"]:
        for html_content in column_data:
            html_with_context = f"<{outer}><{context_element}>{html_content}</{context_element}></{outer}>"
            if has_child_elements(html_with_context, outer):
                return True
    return False

# Parse the JSONL file and process each line
def process_jsonl(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Parse each line leas a JSON object
            data = json.loads(line)

            # Extract the relevant fields

            url = data.get('url', 'N/A')
            page = data.get('page', 'N/A')
            row_num = data.get('row_num', 'N/A')

            # Check if any entry in 'script' or 'xmp' array has child elements
            for subelement in ['style', 'xmp', 'iframe', 'noembed', 'noframes', 'noscript', 'script']:
                contents_all = data.get(f"{subelement}_contents_all")
                if contents_all:
                    if check_html_entries(subelement, contents_all):
                        print(f"ID: {row_num}, URL: {page}, Column: {subelement}, HTML entries: {script_html}")


# Example usage
file_path = 'sample.json'  # Replace with the path to your JSONL file
process_jsonl(file_path)
