# api/convert_html_to_react.py
from bs4 import BeautifulSoup

from http.server import BaseHTTPRequestHandler
import json
import re

from functools import lru_cache

@lru_cache(maxsize=128)
def camel_case(s):
    return re.sub(r'[-_\s]([a-zA-Z])', lambda m: m.group(1).upper(), s)

def convert_style_to_jsx(style_string: str):
    if not style_string:
        return '{}'
    style_dict = {}
    for item in style_string.split(';'):
        if ':' in item:
            key, value = item.split(':', 1)
            style_dict[camel_case(key.strip())] = value.strip()
    return '{{' + ', '.join(f'{k}: "{v}"' for k, v in style_dict.items()) + '}}'

def convert_html_to_jsx(element):
    """
    Converts HTML elements to JSX format recursively.

    Args:
        element: BeautifulSoup element to convert.

    Returns:
        str: JSX formatted string representing the HTML element.
    """

def convert_html_to_jsx(element):
    tag_name = element.name
    if tag_name is None:
        return element.string

    attributes = []
    for attr, value in element.attrs.items():
        if attr in ["data-slot", "data-in-range", "data-orientation", "aria-label", "aria-labelledby", "aria-describedby", "aria-hidden", "aria-expanded"]:
            attr = attr
        elif attr == 'class':
            attr = 'className'
        elif attr == 'for':
            attr = 'htmlFor'
        else:
            attr = camel_case(attr)

        if attr == 'style':
            attributes.append(f'style={convert_style_to_jsx(value)}')
            continue

        attributes.append(f'{attr}="{" ".join(value) if isinstance(value, list) else value }"')

    attributes_str = ' '.join(attributes)

    if len(element.contents) == 0:
        return f'<{tag_name} {attributes_str} />'

    children = ''.join([convert_html_to_jsx(child) for child in element.contents])

    return f'<{tag_name} {attributes_str}>{children}</{tag_name}>'

def convert_html_to_jsx2(html):
    # Basic conversion rules
    jsx = html.replace('class=', 'className=')
    jsx = re.sub(r'for=', 'htmlFor=', jsx)

    # Convert inline styles
    def convert_style(match):
        style = match.group(1)
        style_dict = {k.strip(): v.strip() for k, v in [s.split(':') for s in style.split(';') if s]}
        return 'style={' + json.dumps(style_dict) + '}'

    jsx = re.sub(r'style="([^"]*)"', convert_style, jsx)

    # Wrap in a functional component
    jsx = f"""
import React from 'react';

export default function ConvertedComponent() {{
  return (
    {jsx}
  );
}}
"""
    return jsx

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        html_content = self.rfile.read(content_length).decode('utf-8')

        soup = BeautifulSoup(html_content, 'html.parser')

        converted_jsx = convert_html_to_jsx(soup)

        # Wrap in a functional component
        jsx = f"""
import React from 'react';

interface Props {{}}

const Component: React.FC<Props> = () => {{
  return (
    {converted_jsx}
  );
}}

export default Component;
"""


        self.send_response(200)
        self.send_header('Content-type', 'application/javascript')
        self.end_headers()
        self.wfile.write(jsx.encode())
        return


# @vercel/python@3.9
# from http.server import BaseHTTPRequestHandler
# import json
# import re

# def convert_html_to_jsx(html):
#     # Basic conversion rules
#     jsx = html.replace('class=', 'className=')
#     jsx = re.sub(r'for=', 'htmlFor=', jsx)

#     def camel_case(s):
#       return re.sub(r'[-_\s]([a-zA-Z])', lambda m: m.group(1).upper(), s)
    
#     # Convert inline styles
#     def convert_style(match):
#         style = match.group(1)
#         style_dict = {k.strip(): v.strip() for k, v in [s.split(':') for s in style.split(';') if s]}
#         # return 'style={' + json.dumps(style_dict) + '}'
#         return 'style={' + camel_case(match) + '}'
    
#     jsx = re.sub(r'style="([^"]*)"', camel_case, jsx)
    
#     # Handle self-closing tags
#     self_closing_tags = ['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 
#                          'link', 'meta', 'param', 'source', 'track', 'wbr']
    
#     for tag in self_closing_tags:
#         jsx = re.sub(f'<{tag}([^>]*)>', f'<{tag}\\1 />', jsx)
    
#     # Remove any remaining "/" just before ">" in non-self-closing tags
#     jsx = re.sub(r'([^/])/>(?!})', r'\1>', jsx)
    
#     # Wrap in a functional component
#     jsx = f"""
# import React from 'react';

# export default function ConvertedComponent() {{
#   return (
#     {jsx}
#   );
# }}
# """
#     return jsx

# class handler(BaseHTTPRequestHandler):
#     def do_POST(self):
#         content_length = int(self.headers['Content-Length'])
#         post_data = self.rfile.read(content_length).decode('utf-8')
        
#         converted_jsx = convert_html_to_jsx(post_data)
        
#         self.send_response(200)
#         self.send_header('Content-type', 'application/javascript')
#         self.end_headers()
#         self.wfile.write(converted_jsx.encode())
#         return
    