import os
from pathlib import Path

from bb.lib.story_graph import AnswerChecker
from bb.lib.story_graph.asker import Asker
from bb.lib.story_graph.graph import StoryGraph
from bb.lib.story_graph.utils import QuestionNode, StoryNode
from bb.lib.story_graph.writer import Writer


def check_answer_checker():
    checker = AnswerChecker()
    is_correct = checker.is_correct(
        content="Mickey et Donald sont amis.",
        question="Qui sont Mickey et Donald ?",
        gt_answer="Mickey et Donald",
        listener_answer="Mickey et Donald",
    )
    print(f"Answer checker result: {is_correct} (ground truth: True)")

    is_correct = checker.is_correct(
        content="Mickey et Donald sont amis.",
        question="Est-ce que Mickey et Donald sont amis ?",
        gt_answer="Oui",
        listener_answer="Non",
    )
    print(f"Answer checker result: {is_correct} (ground truth: False)")


def check_asker():
    asker = Asker()
    story = (
        "Mickey et Donald sont les personnages principaux de l'histoire.||"
        "Ils vont faire du manège et manger une glace.||"
    )
    questions = asker.generate_questions(
        story=story, breakpoint_symbol="||", questions_difficulty=["easy", "hard"]
    )
    print(f"story: {story}")
    print(f"questions: {questions}")


def check_writer():
    workspace_data = Path(os.getenv("BONBON_WORKSPACE_DATA"))
    writer = Writer(number_of_breakpoints=3, breakpoint_symbol="||")
    story = writer.generate_story(
        number_phrases=15,
        characters=["Mickey", "Donald"],
        age_of_the_audience=10,
        language="French",
        story_context="Mickey et donald vont faire un tour de la terre avec la fusée utilisée le mois dernier par Thomas Pesquet",
    )
    writer.save_story(story, workspace_data / "mickey_donald_tour_de_la_terre.txt")
    print(f"Generated story: {story}")


def check_graph():
    workspace_data = Path(os.getenv("BONBON_WORKSPACE_DATA"))
    story_path = workspace_data / "mickey_donald_tour_de_la_terre.txt"

    with open(story_path, "r") as f:
        story = f.read()

    asker = Asker()
    all_questions = asker.generate_questions(
        story=story, breakpoint_symbol="||", questions_difficulty=["easy", "hard"]
    )

    graph = StoryGraph(breakpoint_symbol="||")
    graph.create_graph(
        story=story, question_answer_list=all_questions, language="French"
    )
    graph.plot_graph(workspace_data / "story_graph_mickey_donald_tour_de_la_terre.svg")
    graph.save_graph(workspace_data / "story_graph_mickey_donald_tour_de_la_terre.json")

    graph.load_graph(workspace_data / "story_graph_mickey_donald_tour_de_la_terre.json")
    print(
        f"Graph loaded from {story_path}.\n"
        f"Language: {graph.language}\n"
        f"Story graph nodes: {graph.graph_nodes}"
    )


def main():
    # print("\nChecking answer checker...")
    # check_answer_checker()

    # print("\nChecking asker...")
    # check_asker()

    # print("\nChecking writer...")
    # check_writer()

    print("\nChecking graph...")
    check_graph()


if __name__ == "__main__":
    main()
