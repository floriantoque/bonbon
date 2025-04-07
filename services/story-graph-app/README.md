# Story Graph App

A Gradio application that helps create interactive story graphs with questions and answers for children's stories.

## Overview

The Story Graph App is a service that:
- Takes story text files as input
- Automatically generates questions about the story content
- Creates a graph structure connecting story segments with questions
- Supports both French and English stories
- Visualizes the story flow as an SVG graph
- Saves story graphs as JSON files for use in the Story Player App

## Installation

```bash
uv sync --reinstall
```

## Usage

```bash
uv run python app.py
```

This will start the Gradio web interface at `http://localhost:7860`.

