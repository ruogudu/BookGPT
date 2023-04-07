import os
import requests
import questionary
import pickle

from book_constructors.pdf_constructor import PDFConstructor, PDFWrapper
from chatgpt_wrapper import ChatGPTWrapper
from config import local_secret_path


def get_api_key():
    secret_path = os.path.expanduser(local_secret_path)
    temp_api_key = None
    try:
        with open(secret_path, "r") as file:
            data = file.read()
            use_local = questionary.confirm(
                "Found API key from ~/.bookgpt/, would you like to use it?"
            ).ask()
            if use_local:
                temp_api_key = data
            else:
                temp_api_key = None
    except FileNotFoundError:
        pass
    if temp_api_key:
        return temp_api_key
    temp_api_key = questionary.text(
        "What is your OpenAI API key? (See https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)"
    ).ask()
    if temp_api_key:
        save = questionary.confirm(
            "Would you like to save the API key to ~/.bookgpt/ ?"
        ).ask()
        if save:
            os.makedirs(os.path.dirname(secret_path), exist_ok=True)
            with open(secret_path, "w") as file:
                file.write(temp_api_key)
    return temp_api_key


def get_pdf_url():
    while True:
        url = questionary.text("Enter the URL of the PDF file:").ask()
        if url.lower().endswith(".pdf"):
            try:
                response = requests.head(url)
                if response.status_code == 200:
                    return url
                else:
                    print("Invalid URL. Please try again.")
            except Exception as e:
                print("Invalid URL. Please try again.")
        else:
            print("The URL does not point to a PDF file. Please try again.")


def get_save_path():
    path = questionary.path(
        "Enter the path where you want to store the curated book:"
    ).ask()
    return path


def get_book_title_and_author():
    title = questionary.text("Enter the book title:").ask()
    author = questionary.text("Enter the book author:").ask()
    return title, author


def load_book_from_cache(cache_path):
    with open(cache_path, "rb") as file:
        book = pickle.load(file)
    return book


def main():
    api_key = get_api_key()
    pdf_url = get_pdf_url()
    book_title, book_author = get_book_title_and_author()
    save_path = get_save_path()

    ChatGPTWrapper.init(api_key)
    pdf_wrapper = PDFWrapper.from_url(pdf_url)

    pdf_constructor = PDFConstructor(book_title, book_author, pdf_wrapper)
    book = pdf_constructor.construct_book()

    # Check if user wants to load from cache
    load_from_cache = questionary.confirm(
        "Would you like to load the Book from cache?"
    ).ask()
    if load_from_cache:
        cache_path = questionary.path(
            "Enter the path to the cached Book file:"
        ).ask()
        book = load_book_from_cache(cache_path)
    else:
        with open(save_path, "wb") as file:
            pickle.dump(book, file)

    print(book.get_intro())

    while True:
        question = questionary.text(
            "Ask a question about the book or type 'exit' to quit:"
        ).ask()
        if question.lower() == "exit":
            break
        answer = book.ask_question(question)
        print(answer)


if __name__ == "__main__":
    main()
