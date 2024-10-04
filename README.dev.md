# Kodiks-Ai-Lib Development Tools

## Required Extensions

To develop this project, it is recommended to install the following Visual Studio Code extensions:

- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [Black Formatter](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter)
- [Flake8](https://marketplace.visualstudio.com/items?itemName=ms-python.flake8)

## Pre-commit Configuration

To format and check your code using `pre-commit`, follow these steps:

1. Install `pre-commit`:

    ```bash
    pre-commit install
    ```

2. Run checks on all files:

    ```bash
    pre-commit run --all-files
    ```

## Running Tests

    This project uses `pytest` for running unit tests. Follow the steps below to run the tests locally.

```bash
poetry install --with dev
```

#### Running the Tests
- -s parameter: This ensures that loguru outputs log messages directly to the console during test execution, making it easier to observe real-time logs. (pytest -s)

```bash
pytest
```
#### Running Specific Tests
```bash
pytest kodiks_ai_lib/tests/decorator_timeout_test.py
```

## Black and Flake8 Settings

Add the following settings to your `settings.json` file for `Black` and `Flake8`:

```json
{
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.formatOnSave": true,
    "black-formatter.args": [
        "--line-length",
        "120"
    ],
    "[python]": {
        "editor.codeActionsOnSave": {
            "source.organizeImports": "always"
        }
    },
    "flake8.args": [
        "--max-line-length",
        "120",
        "--extend-ignore",
        "E203"
    ]
}
