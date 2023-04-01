# BookGPT

BookGPT is a Python-based tool that allows users to create an interactive summary of a PDF book using OpenAI's GPT-4 model. Users can ask questions about the book, and the tool will provide concise and relevant answers based on the book's content.

## Usage

1. Install the required Python packages by running `pip install -r requirements.txt`.
2. Make sure to have your OpenAI API key ready. If you don't have one, you can obtain it from the [OpenAI website](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key).
3. Run the `start.py` script using the command `python start.py`.
4. Follow the prompts to provide the necessary information, including the URL of the PDF file, book title, author, and the path where you want to store the curated book.
5. The tool will generate a curated book with an interactive summary of the provided PDF file. You can ask questions about the book, and the tool will answer them based on the book's content.

## Demo

Here's a demo of how to use the BookGPT tool:

```commandline
$ python start.py
Enter the URL of the PDF file: https://example.com/sample.pdf
Enter the book title: Sample Book Title
Enter the book author: Sample Book Author
Enter the path where you want to store the curated book: /path/to/save/book.pkl
This is a book. Give yourself a proper name and introduce yourself with a brief summary. Please also provide three questions a reader may want to ask you. ...
Ask a question about the book or type 'exit' to quit: What is the main theme of the book?
The main theme of the book is ...
Ask a question about the book or type 'exit' to quit: exit
```
