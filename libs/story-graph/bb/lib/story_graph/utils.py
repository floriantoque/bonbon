from dataclasses import dataclass
from typing import Any, Dict, List, Literal


@dataclass
class StoryNode:
    """A node in the story graph.

    Attributes
    ----------
    id (str): The id of the node.
    content (str): The content of the node.
    children (List[Any]): The children of the node.
    parents (List[Any]): The parents of the node.
    """

    id: str
    content: str
    children: List[Any]
    parents: List[Any]

    def __post_init__(self):
        if self.children is None:
            self.children = []
        if self.parents is None:
            self.parents = []

    def add_child(self, child_id: str):
        self.children.append(child_id)

    def add_parent(self, parent_id: str):
        self.parents.append(parent_id)

    def to_dict(self) -> Dict:
        """Convert the node to a dictionary for JSON serialization."""
        return {
            "id": self.id,
            "content": self.content,
            "type": self.__class__.__name__,
            "children": [child_id for child_id in self.children],
            "parents": [parent_id for parent_id in self.parents],
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "StoryNode":
        """Create a node from a dictionary."""
        return cls(
            id=data["id"],
            content=data["content"],
            children=data["children"],
            parents=data["parents"],
        )


@dataclass
class QuestionNode(StoryNode):
    """A question node in the story graph. Be careful, this node is a child of a story node.
    So QuestionNode is also a StoryNode.

    Attributes
    ----------
    answer (str): The answer to the question.
    difficulty (Literal["easy", "medium", "hard"]): The difficulty of the question.
    cognitive_area (Literal["short_memory", "multiple_choice", "long_memory"]): The cognitive area of the question.
    """

    answer: str
    difficulty: Literal["easy", "medium", "hard"]
    cognitive_area: (
        Literal[
            "short_memory",
            "multiple_choice",
            "long_memory",
        ]
        | None
    ) = None

    def to_dict(self) -> Dict:
        """Convert the question node to a dictionary for JSON serialization."""
        base_dict = super().to_dict()
        base_dict.update(
            {
                "answer": self.answer,
                "difficulty": self.difficulty,
                "cognitive_area": self.cognitive_area,
            }
        )
        return base_dict

    @classmethod
    def from_dict(cls, data: Dict) -> "QuestionNode":
        """Create a question node from a dictionary."""
        return cls(
            id=data["id"],
            content=data["content"],
            answer=data["answer"],
            difficulty=data["difficulty"],
            cognitive_area=data["cognitive_area"],
            children=data["children"],
            parents=data["parents"],
        )
