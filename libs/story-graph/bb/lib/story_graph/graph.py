"""Graph module for story interaction.

This module provides functionality to create, save, and load story graphs,
as well as to start and continue story interactions.
"""

import json
from bb.lib.story_graph.asker import QuestionAnswer
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout
from bb.lib.story_graph.resumer import Resumer
from bb.lib.story_graph.answer_checker import AnswerChecker
from bb.lib.story_graph.utils import StoryNode, QuestionNode
from typing import Literal


class StoryGraph:
    def __init__(self, breakpoint_symbol: str = "||"):
        """Initialize the StoryGraph with a breakpoint symbol.

        Args:
            breakpoint_symbol (str): The symbol used to split the story into breakpoints.
        """
        self.graph_nodes: dict[str, StoryNode | QuestionNode] = {}
        self.breakpoint_symbol = breakpoint_symbol
        self.language = None

    def save_graph(self, filename: str):
        """Save the story graph to a file.

        Parameters
        ----------
        filename (str): The filename to save the story graph to.
        """
        # Convert nodes to dictionaries using their to_dict methods
        nodes_dict = {
            node_id: node.to_dict() for node_id, node in self.graph_nodes.items()
        }
        story_dict = {
            "nodes": nodes_dict,
            "language": self.language,
        }

        with open(filename, "w") as f:
            json.dump(story_dict, f, indent=2)

    def load_graph(self, filename: str):
        """Load the story graph from a file.

        Parameters
        ----------
        filename (str): The filename to load the story graph from.
        """
        with open(filename, "r") as f:
            story_dict = json.load(f)

        # Recreate nodes from dictionaries
        self.graph_nodes = {}
        for node_id, node_dict in story_dict["nodes"].items():
            if node_dict["type"] == "StoryNode":
                node = StoryNode.from_dict(node_dict)
            elif node_dict["type"] == "QuestionNode":
                node = QuestionNode.from_dict(node_dict)
            self.graph_nodes[node_id] = node
        self.language = story_dict["language"]

    def create_graph(
        self,
        story: str,
        question_answer_list: list[QuestionAnswer],
        language: Literal["French", "English"],
    ):
        """Create the story graph from a story and a list of question and answers.

        Parameters
        ----------
        story (str): The story to create the graph from.
        question_answer_list (list[QuestionAnswer]): The list of question and answers to create the graph from.
        language (Literal["French", "English"]): The language of the story.
        """
        self.language = language
        # Check that the number of questions and answers are the same
        if len(question_answer_list) != story.count(self.breakpoint_symbol):
            raise ValueError("The number of questions and answers must be the same")
        # Check that the story contains the breakpoint symbol
        if self.breakpoint_symbol not in story:
            raise ValueError("The story must contain the breakpoint symbol")

        # First add all the story nodes
        story_nodes = []
        for story_idx, story_part in enumerate(story.split(self.breakpoint_symbol)):
            story_node = StoryNode(f"story_{story_idx}", story_part, None, None)
            self.graph_nodes[story_node.id] = story_node
            story_nodes.append(story_node)

        # Then add the question nodes
        for story_idx, story_node in enumerate(story_nodes):
            if story_idx < len(question_answer_list):
                for question_idx, question_answer in enumerate(
                    question_answer_list[story_idx]
                ):
                    question_node = QuestionNode(
                        id=f"question_{story_idx}_{question_idx}",
                        content=question_answer.question,
                        answer=question_answer.answer,
                        difficulty=question_answer.difficulty,
                        cognitive_area=question_answer.cognitive_area,
                        children=[],
                        parents=[],
                    )
                    story_node.add_child(question_node.id)
                    question_node.add_parent(story_node.id)
                    self.graph_nodes[question_node.id] = question_node
                    # Add the edge between the question node and the next story node
                    next_story_node = self.graph_nodes[f"story_{story_idx + 1}"]
                    question_node.add_child(next_story_node.id)
                    next_story_node.add_parent(question_node.id)

    def plot_graph(self, filename: str):
        """Plot the story graph.

        Parameters
        ----------
        filename (str): The filename to save the plot to.
        """
        G = nx.DiGraph()
        # Add all nodes and edges
        for node in self.graph_nodes.values():
            G.add_node(node.id)
            for child_id in node.children:
                G.add_node(child_id)
                G.add_edge(node.id, child_id)

        pos = graphviz_layout(G, prog="sfdp")
        plt.figure(figsize=(12, 8))
        nx.draw_networkx(
            G,
            pos,
            with_labels=True,
            node_size=1000,
            node_color="lightblue",
            font_size=8,
        )
        plt.axis("off")
        plt.savefig(filename)

    def start_story(
        self,
        node_id: str = "story_0",
        resume: bool = False,
        question_to_pass: list[str] | None = None,
    ):
        """Start the story from a given node. Play the story only with text and user input.

        Parameters
        ----------
        node_id (str): The id of the node to start the story from.
        resume (bool): Whether to resume the story from the given node.
        question_to_pass (list[str]): The list of question ids to pass.

        Raises
        ------
        ValueError: If the node id is invalid.
        """
        idx = int(node_id.split("_")[1])
        if "story" in node_id:
            current_node = self.graph_nodes[node_id]
        elif "question" in node_id:
            current_node = self.graph_nodes[node_id]
        else:
            raise ValueError(f"Invalid node id: {node_id}")

        if idx > 0 and resume:
            resumer = Resumer()
            resume_story_node = resumer.resume_story(current_node)
            print(f"Resume : {resume_story_node.id}")
        else:
            if not isinstance(current_node, QuestionNode):
                print(current_node.content)
                if len(current_node.children) == 0:
                    print("No more story to tell")
                    return
                else:
                    hard_children = [
                        self.graph_nodes[child_id]
                        for child_id in current_node.children
                        if self.graph_nodes[child_id].difficulty == "hard"
                    ]
                    medium_children = [
                        self.graph_nodes[child_id]
                        for child_id in current_node.children
                        if self.graph_nodes[child_id].difficulty == "medium"
                    ]
                    easy_children = [
                        self.graph_nodes[child_id]
                        for child_id in current_node.children
                        if self.graph_nodes[child_id].difficulty == "easy"
                    ]
                    if len(hard_children) > 0:
                        next_node_id = hard_children[0].id
                        self.start_story(next_node_id, resume=False)
                    elif len(medium_children) > 0:
                        next_node_id = medium_children[0].id
                        self.start_story(next_node_id, resume=False)
                    elif len(easy_children) > 0:
                        next_node_id = easy_children[0].id
                        self.start_story(next_node_id, resume=False)
                    else:
                        print("No more story to tell")
                        return

            else:
                listener_answer = self.ask_question(current_node)

                answer_checker = AnswerChecker()
                content = self.graph_nodes[current_node.parents[0]].content
                question = current_node.content
                correct = answer_checker.is_correct(
                    content=content,
                    question=question,
                    gt_answer=current_node.answer,
                    listener_answer=listener_answer,
                )
                if correct:
                    print("Bonne reponse!")
                    next_node_id = current_node.children[0]
                    self.start_story(next_node_id, resume=False)
                else:
                    print(
                        "Mauvaise reponse !"
                        f"La question etait trop difficile, elle etait de niveau: {current_node.difficulty} "
                        f"La reponse etait: {current_node.answer}"
                    )
                    if question_to_pass is None:
                        question_to_pass = [current_node.id]
                    else:
                        question_to_pass.append(current_node.id)
                    parent_node = self.graph_nodes[current_node.parents[0]]
                    hard_children = [
                        self.graph_nodes[child_id]
                        for child_id in parent_node.children
                        if self.graph_nodes[child_id].difficulty == "hard"
                        and child_id not in question_to_pass
                    ]
                    medium_children = [
                        self.graph_nodes[child_id]
                        for child_id in parent_node.children
                        if self.graph_nodes[child_id].difficulty == "medium"
                        and child_id not in question_to_pass
                    ]
                    easy_children = [
                        self.graph_nodes[child_id]
                        for child_id in parent_node.children
                        if self.graph_nodes[child_id].difficulty == "easy"
                        and child_id not in question_to_pass
                    ]

                    if len(hard_children) > 0:
                        next_node_id = hard_children[0].id
                        print("Other question, level hard")
                        self.start_story(
                            next_node_id,
                            resume=False,
                            question_to_pass=question_to_pass,
                        )
                    elif len(medium_children) > 0:
                        print("Other question, level medium")
                        next_node_id = medium_children[0].id
                        self.start_story(
                            next_node_id,
                            resume=False,
                            question_to_pass=question_to_pass,
                        )
                    elif len(easy_children) > 0:
                        print("Other question, level easy")
                        next_node_id = easy_children[0].id
                        self.start_story(
                            next_node_id,
                            resume=False,
                            question_to_pass=question_to_pass,
                        )
                    else:
                        print(
                            "Malheureusement toutes les questions ont ete repondues incorrectement"
                            "mais ce n'est pas grave. On continue l'histoire !"
                        )
                        next_node_id = current_node.children[0]
                        self.start_story(next_node_id, resume=False)

    def ask_question(self, question_node: QuestionNode):
        """Ask a question to the user.

        Parameters
        ----------
        question_node (QuestionNode): The question node to ask.
        """
        print(question_node.content)
        answer = input("Your answer: ")
        return answer

    def get_node(self, node_id: str) -> StoryNode | QuestionNode:
        return self.graph_nodes[node_id]

    def get_next_question_node_id(
        self, node_id: str, question_to_pass: list[str] | None = None
    ) -> str | None:
        """Get the next question node id. Starting from a story node or a question node
        for which the user has answered incorrectly.

        Parameters
        ----------
        node_id (str): The id of the node to get the next question node id from.
        question_to_pass (list[str]): The list of question ids to pass.

        Returns
        -------
        str | None: The id of the next question node or None if there are no more question nodes.
        """
        story_node_id = node_id
        if isinstance(self.graph_nodes[node_id], QuestionNode):
            story_node_id = self.graph_nodes[node_id].parents[0]

        question_node_ids = self.graph_nodes[story_node_id].children
        question_dict = {"easy": [], "medium": [], "hard": []}
        if question_to_pass is not None:
            question_node_ids = [
                question_node_id
                for question_node_id in question_node_ids
                if question_node_id not in question_to_pass
            ]
        for question_node_id in question_node_ids:
            question_dict[self.graph_nodes[question_node_id].difficulty].append(
                question_node_id
            )
        for difficulty in ["hard", "medium", "easy"]:
            if len(question_dict[difficulty]) > 0:
                return question_dict[difficulty][0]
        return None
