"""
This module contains the Resumer class, which is used to resume a story.
"""

from bb.lib.llm.llm import LLMMistral
from bb.lib.story_graph.utils import QuestionNode, StoryNode


class Resumer:
    def __init__(self):
        """Initialize the Resumer with a LLM."""
        self.llm = LLMMistral()

    def get_previous_content(
        self, node: StoryNode | QuestionNode, contents: list[str] | None = None
    ) -> str:
        """Get the previous content of a node.

        Parameters
        ----------
        node (StoryNode | QuestionNode): The node to get the previous content of.
        contents (list[str]): The contents of the previous nodes.
        """
        if contents is None:
            contents = []

        if node.id == "story_0":
            contents.append(node.content)
            return "".join(contents[::-1])
        if isinstance(node, QuestionNode):
            return self.get_previous_content(node.parents[0], contents)
        if isinstance(node, StoryNode):
            contents.append(node.content)
            return self.get_previous_content(node.parents[0], contents)

    def resume_story(self, node: StoryNode | QuestionNode):
        """Resume the story from a node.

        Parameters
        ----------
        node (StoryNode | QuestionNode): The node to resume the story from.
        """
        previous_content = self.get_previous_content(node)
        return self.llm.generate_text("Resume the following story: " + previous_content)
