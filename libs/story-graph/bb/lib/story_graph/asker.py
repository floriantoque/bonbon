"""Question and answer module for story interaction.

This module provides functionality to handle questions and answers in the
story context, including different difficulty levels and cognitive areas.
"""

import time
from dataclasses import dataclass
from typing import Literal

from bb.lib.llm.llm import LLMMistral
from rich.progress import Progress


@dataclass
class QuestionAnswer:
    """Class representing a question and its expected answer.

    This class encapsulates a question along with its expected answer,
    difficulty level, and cognitive area.

    Attributes:
        question (str): The question text.
        answer (str): The expected answer.
        difficulty (Literal["easy", "medium", "hard"]): Difficulty level of
            the question.
        cognitive_area (Literal["short_memory", "multiple_choice",
            "long_memory"]|None): Cognitive area targeted by the question. None by default.
    """

    question: str
    answer: str
    difficulty: Literal["easy", "medium", "hard"]
    cognitive_area: Literal["short_memory", "multiple_choice", "long_memory"] | None = (
        None
    )


class Asker:
    def __init__(self):
        """Initialize the Asker with LLM. Here we use Mistral model by default."""
        self.llm = LLMMistral()

    def generate_questions(
        self,
        story: str,
        breakpoint_symbol: str = "||",
        questions_difficulty: list[str] = ["easy", "medium", "hard"],
        age_of_the_audience: int = 6,
        language: str = "French",
    ) -> list[list[QuestionAnswer]]:
        """Generate questions for each breakpoint in the story.

        This method splits the story into breakpoints and generates questions
        for each breakpoint. It uses the class llm model to generate the questions.

        Parameters
        ----------
        story (str): The story to generate questions from.
        breakpoint_symbol (str): The symbol used to split the story into breakpoints.
        questions_difficulty (list[str]): The difficulty levels of the questions to generate.
        age_of_the_audience (int): The age of the audience.
        language (str): The language of the story.

        Returns
        -------
        list[list[QuestionAnswer]]: A list of lists of QuestionAnswer objects.
            Each inner list contains QuestionAnswer objects for a specific breakpoint.

        Raises:
            ValueError: If the output does not contain double pipes ||.
        """
        splits = story.split(breakpoint_symbol)
        all_questions = []
        with Progress() as progress:
            task = progress.add_task("Generating questions...", total=len(splits) - 1)
            for i in range(len(splits) - 1):
                questions = []
                for difficulty in questions_difficulty:
                    prompt = (
                        f"Generate a question based on the story: {splits[i]}."
                        f"The question should be at the difficulty level: {difficulty}."
                        f"The question should be in the language: {language}."
                        f"The question should be adapted for a {age_of_the_audience} years old."
                        "Ask a question not a riddle. The goal is to develop the child's "
                        "intelligence in different cognitive skills."
                        "The question should be related to the story and have the answer in the story."
                        "The format of the output should be question and the answer separated by double pipes ||, like this: what is the color of the cat? || orange"
                    )
                    output = self.llm.generate_text(prompt)
                    if "||" not in output:
                        print(output)
                        raise ValueError("Output does contain double pipes ||")
                    question = output.split("||")[0]
                    answer = output.split("||")[1]

                    # wait 1 second to avoid rate limit
                    # TODO remove this because it is scrappy
                    time.sleep(1)

                    questions.append(QuestionAnswer(question, answer, difficulty))
                all_questions.append(questions)
                progress.update(task, advance=1)
        return all_questions
