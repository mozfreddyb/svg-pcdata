import json
from html5lib.html5parser import HTMLParser
from html5lib import treebuilders
#from html5lib.treewalkers.dom import TreeWalker
from xml.etree.ElementTree import Element

# Function to check if an element has child elements
def has_child_elements(html_content, context, oddlyparsed):
    # Parse the HTML content into a DOM tree using html5lib
    try:
        parser = HTMLParser(tree=treebuilders.getTreeBuilder('dom'))
        fragment = parser.parseFragment(stream=html_content, container='body')
        # first node should be context (== math/svg)
        if len(fragment.childNodes) == 1:
            if fragment.firstChild.localName == context:
                if fragment.firstChild.firstChild.localName == oddlyparsed:
                    interesting_node = fragment.firstChild.firstChild
                    result = f"Wow, we have an {oddlyparsed} elementin SVG/MATHML that has children: {[child.localName for child in interesting_node.childNodes]}"

                    return [True, result]
        # In this case, the content broke out of e.g. svg+style and went next to the svg.
        # This would happen for `p` or `b` element as they dont exist in svg.
        elif len(fragment.childNodes) == 2:
            if fragment.firstChild.localName == context:
                    result = "We found a case where content broke out"
                    result += "The element that broke out was " + repr(fragment.childNodes[1].localName)
                    return [True, result]
        return [False, None]

    except Exception as e:
        print(f"Error parsing HTML: {e}")
        return [False, None]

# Function to process each column (either script or xmp) and check all entries in the array
def check_html_entries(oddlyparsed, column_data):
    for outer in ["svg"]: # XXX, "math"]:
        for html_content in column_data:
            html_with_context = f"<{outer}><{oddlyparsed}>{html_content}</{oddlyparsed}></{outer}>"
            check_result = has_child_elements(html_with_context, outer, oddlyparsed)
            if check_result[0] == True:
                return check_result[1]
    return None

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
