# BookGPT

BookGPT is a Python-based tool that allows users to create an interactive summary of a PDF book using OpenAI's GPT-4 model. Users can ask questions about the book, and the tool will provide concise and relevant answers based on the book's content.

## Usage

1. Install the required Python packages by running `pip install -r requirements.txt`.
2. Make sure to have your OpenAI API key ready. If you don't have one, you can obtain it from the [OpenAI website](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key).
3. Run the `start.py` script with the desired command: `curate-book`, `chat-with-book`, or `help`.

### Curate Book

To curate a book and store it to the local cache, run the following command:

```commandline
$ python start.py curate-book
```
Follow the prompts to provide the necessary information, including the URL or path of the PDF file, and the path where you want to store the curated book.

### Chat with Book
To load a curated book from the local cache and interact with it, run the following command:

```commandline
$ python start.py chat-with-book
```
Follow the prompts to provide the path to the cached book file. The tool will then introduce the book and allow you to ask questions about it.

## Help
To display help information on using the tool, run the following command:

```commandline
$ python start.py help
```

## Demo
Here's a demo of how to use the BookGPT tool to curate a book and chat with it:

```commandline
$ python start.py curate-book
Enter the URL of the PDF file: https://example.com/sample.pdf
Enter the path where you want to store the curated book: /path/to/save/book.curated_book

$ python start.py chat-with-book
Enter the path to the cached Book file: /path/to/save/book.curated_book
This is a book. Give yourself a proper name and introduce yourself with a brief summary. Please also provide three questions a reader may want to ask you. ...

Ask a question about the book or type 'exit' to quit: What is the main theme of the book?
The main theme of the book is ...
Ask a question about the book or type 'exit' to quit: exit

```
