# Story Graph Library

This library provides functionality for creating interactive story graphs with questions and answers.

## Key Components

### graph.py
Contains the `StoryGraph` class which is the main class for creating, saving and loading story graphs. It handles:
- Creating graph structures from stories and questions
- Saving/loading graphs to/from JSON files 
- Visualizing graphs using networkx

### utils.py
Contains core data structures:
- `StoryNode`: Base node class representing story segments
- `QuestionNode`: Node class for questions, inherits from StoryNode
- Both classes handle serialization/deserialization and parent/child relationships

### writer.py
Contains the `Writer` class for generating stories:
- Generates stories with specified parameters like characters, age group, language
- Inserts breakpoints to split stories into segments
- Saves stories to files

### asker.py
Contains the `Asker` class for question generation:
- Generates questions for each story segment
- Supports different difficulty levels
- Returns questions with answers and metadata

### answer_checker.py
Contains the `AnswerChecker` class for validating answers:
- Checks if listener answers match ground truth
- Handles different question types and languages

### resumer.py
Contains the `Resumer` class for story progression:
- Manages story flow and question order
- Tracks progress through the story graph

## Usage

See `scripts/main.py` for example usage of all components. The library supports:
- Story generation in multiple languages
- Question generation with varying difficulty
- Answer validation
- Graph visualization and persistence
