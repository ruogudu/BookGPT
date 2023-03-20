import os

import questionary

from config import local_secret_path


# Get the API key from the user
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
