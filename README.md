# Kodiks Ai Lib

## Overview

This is a helper library for Kodiks Ai Core workflow product. The idea of this library is to wrap all reusable code to simplify and improve workflow implementation.

Supported functionality:

- API to communicate with RabbitMQ for event receiver/producer
- Workflow call helper
- Logger call helper


## Instructions

Version number should be updated in __init__.py and pyproject.toml

1. Install Poetry

```
pip install poetry
```

2. Add pika and requests libraries

```
poetry add pika
poetry add requests
```

3. Build

```
poetry build
```

4. Publish to TestPyPI

```
poetry publish -r kodiks-ai-lib
```

5. Install from TestPyPI

```
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple  kodiks-ai-lib
```

6. Publish to PyPI

```
poetry publish
```

7. Install from PyPI

```
pip install kodiks-ai-lib
```

8. Test imported library from CMD

```
python -m kodiks_ai_lib
```

9. Import EventReceiver

```
from kodiks_ai_lib.events.event_receiver import EventReceiver
```

10. Import EventProducer

```
from kodiks_ai_lib.events.event_producer import EventProducer
```

## Structure

```
.
├── LICENSE
├── poetry.lock
├── pyproject.toml
├── kodiks_ai_lib
│   ├── __init__.py
│   ├── __main__.py
│   ├── events
│       ├── __init__.py
│       ├── exchange_producer.py
│       ├── exchange_receiver.py
│       ├── event_producer.py
│       └── event_receiver.py
│   ├── logger
│       ├── __init__.py
│       └── logger_helper.py
│   ├── workflow
│       ├── __init__.py
│       └── workflow_helper.py
└── README.md
```

## License

Licensed under the Apache License, Version 2.0. Copyright 2024-2024 Kodiks AI, [Copy of the license](https://github.com/kodiks/kodiks-ai-lib/blob/master/LICENSE).