# api/convert_html_to_react.py
# from bs4 import BeautifulSoup

from http.server import BaseHTTPRequestHandler
import json
import re

# def html_to_react(html_string):
#     soup = BeautifulSoup(html_string, 'html.parser')
#     react_component = str(soup)
#     return react_component

# class handler(BaseHTTPRequestHandler):

#     def html_to_react(html_string):
#         soup = BeautifulSoup(html_string, 'html.parser')
#         react_component = str(soup)
#         return react_component

#     def do_GET(self):
#         self.send_response(200)
#         self.send_header('Content-type', 'text/plain')
#         self.end_headers()
#         message = f"Hello! Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
#         self.wfile.write(message.encode())
#         return


# def handler(request):
#     body = request.json()
#     html_string = body.get('html')

#     # Convert HTML to React component
#     react_component = html_to_react(html_string)

#     return {
#         'statusCode': 200,
#         'headers': {'Content-Type': 'application/json'},
#         'body': json.dumps({'reactComponent': react_component})
#     }

def convert_html_to_jsx(html):
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
        post_data = self.rfile.read(content_length).decode('utf-8')
        print("🚀 ~ post_data:", post_data)

        converted_jsx = convert_html_to_jsx(post_data)

        self.send_response(200)
        self.send_header('Content-type', 'application/javascript')
        self.end_headers()
        self.wfile.write(converted_jsx.encode())
        return
