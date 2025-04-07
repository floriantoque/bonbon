# Large Language Model Library

This library provides a modular interface for interacting with Large Language Models (LLMs), with current support for Mistral AI's models.

## Features

- Abstract base class `LLM` for implementing different LLM providers
- Built-in implementation for Mistral AI (`LLMMistral`)
- Automatic retries with exponential backoff for API calls
- Environment-based configuration

## Installation
To install the package and its dependencies, run:
`uv sync --reinstall`

## Usage

To use the LLM interface, create an instance of the appropriate subclass and call the `generate_text` method:   

```python
from bb.lib.large_language_model import LLMMistral

llm = LLMMistral()
print(llm.generate_text("What is the capital of France?"))
```

