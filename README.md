# HTML to React Converter

This project provides a serverless function that converts HTML to React JSX. It's designed to run on Vercel's serverless platform and can be easily deployed and integrated into your workflow.

## Features

- Converts basic HTML to JSX syntax
- Handles self-closing tags (e.g., `<img>`, `<br>`)
- Converts `class` attributes to `className`
- Converts `for` attributes to `htmlFor`
- Transforms inline styles to React style objects
- Wraps the converted HTML in a functional React component

## Setup

1. Clone this repository:
   ```
   git clone https://github.com/teebarg/html-converter
   cd html-converter
   ```

2. Install the Vercel CLI if you haven't already:
   ```
   npm install -g vercel
   ```

3. Deploy to Vercel:
   ```
   vercel
   ```

## Project Structure

- `api/hello.py`: The main Python function that handles the HTML to JSX conversion
- `vercel.json`: Configuration file for Vercel deployment
- `README.md`: This file


## Running Locally

```bash
npm i -g vercel
vercel dev
```

Your Python API is now available at `http://localhost:3000/api`.

## Usage

To use the converter, send a POST request to your deployed Vercel function URL with the HTML content in the request body. The function will return a JavaScript file containing a React component.

Example using curl:

```bash
curl -X POST -H "Content-Type: text/plain" -d '<div class="hello" style="color: red;">Hello, World!<img src="example.jpg" alt="Example"></div>' https://your-vercel-url.vercel.app/api/convert
```

## Limitations

This is a basic converter and may not handle all complex HTML structures or React-specific features. It's designed for simple conversions and may need to be extended for more complex use cases.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT License](LICENSE)
