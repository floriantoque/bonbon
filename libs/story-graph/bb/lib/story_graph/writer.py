"""Writer module for generating stories.

This module provides functionality to generate stories using an LLM.
"""

import os
import random
from pathlib import Path

from bb.lib.llm.llm import LLMMistral


class Writer:
    def __init__(
        self,
        number_of_breakpoints: int = 3,
        breakpoint_symbol: str = "||",
    ):
        """Initialize the Writer with a number of breakpoints and a breakpoint symbol.

        Parameters
        ----------
        number_of_breakpoints (int): The number of breakpoints to generate.
        breakpoint_symbol (str): The symbol to use to split the story into breakpoints.

        Mistral llm is used by default.
        """
        self.llm = LLMMistral()
        self.number_of_breakpoints = number_of_breakpoints
        self.breakpoint_symbol = breakpoint_symbol

    def generate_story(
        self,
        number_phrases: int = 15,
        characters: list[str] = ["Mickey", "Donald"],
        age_of_the_audience: int = 6,
        language: str = "French",
        story_context: str = "",
    ) -> str:
        """Generate a story with a given number of phrases, characters, age of the audience and language.

        Parameters
        ----------
        number_phrases (int): The number of phrases to generate.
        characters (list[str]): The characters to generate the story about.
        """
        prompt = (
            f"Generate a story with {number_phrases} phrases. "
            f"The story should be suitable for an audience of {age_of_the_audience} years old. "
            f"The story should be about {characters}. "
            f"The story should contain a quest and be funny. "
            f"The story should contain vocabulary for {age_of_the_audience} years old. "
            f"The story should be in {language}. "
            f"The story should contain uniquely the story, no other text. "
            f"The story should contain breakpoints symbolized as breakpoint symbol: {self.breakpoint_symbol} where "
            f"a question can be asked about information already given in the story. Add only {self.number_of_breakpoints} breakpoints. "
            f"Add in the beginning of the story something like Today we will tell you a story about {characters}. "
            " and the quest .. Please help me to lead the characters to their goal. "
            "the story will be told by a narrator like in Tonie stories. "
        )
        if story_context:
            prompt += f" This is the context of the story: {story_context}"
        story = self.llm.generate_text(prompt)
        story = self.handle_breakpoints(
            story=story,
        )
        # Remove all newlines
        story = story.replace("\n", " ")
        return story

    def handle_breakpoints(self, story: str) -> str:
        """Handle the breakpoints in the story. If the number of breakpoints is less
        than the number of breakpoints to generate, the story is returned as is.
        Otherwise, the story is modified to contain only the breakpoints to generate.
        The breakpoints are randomly selected.

        Parameters
        ----------
        story (str): The story to handle the breakpoints in.
        """
        current_breakpoints = story.count(self.breakpoint_symbol)

        if current_breakpoints <= self.number_of_breakpoints:
            return story

        # Find all breakpoint positions
        breakpoint_positions = []
        pos = 0
        while True:
            pos = story.find(self.breakpoint_symbol, pos)
            if pos == -1:
                break
            breakpoint_positions.append(pos)
            pos += 2

        # Randomly select which breakpoints to keep
        positions_to_keep = random.sample(
            breakpoint_positions, self.number_of_breakpoints
        )

        # Replace breakpoints not in positions_to_keep with spaces
        result = list(story)
        for pos in breakpoint_positions:
            if pos not in positions_to_keep:
                result[pos] = ""
                result[pos + 1] = ""

        return "".join(result)

    def save_story(self, story: str, filepath: str):
        """Save the story to a file.

        Parameters
        ----------
        story (str): The story to save.
        filename (str): The filename to save the story to.
        """
        with open(filepath, "w") as f:
            f.write(story)
