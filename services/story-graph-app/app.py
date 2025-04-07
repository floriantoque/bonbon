from bb.lib.story_graph import Asker, StoryGraph
import gradio as gr
import os
import json
from pathlib import Path


def get_available_stories():
    workspace_data = Path(os.getenv("BONBON_WORKSPACE_DATA")) / "story_texts"
    return [f.name for f in workspace_data.glob("*.txt")]


def create_questions(story_path: str, language: str):
    story_full_path = (
        Path(os.getenv("BONBON_WORKSPACE_DATA")) / "story_texts" / story_path
    )
    with open(story_full_path, "r") as f:
        story = f.read()
    asker = Asker()
    all_questions = asker.generate_questions(
        story=story,
        breakpoint_symbol="||",
        questions_difficulty=["easy", "hard"],
    )

    graph = StoryGraph(breakpoint_symbol="||")
    graph.create_graph(
        story=story, question_answer_list=all_questions, language=language
    )

    story_dict = graph.get_story_dict()
    # Convert the dictionary to a JSON string with double quotes
    return json.dumps(story_dict, ensure_ascii=False, indent=2)


def save_story_dict(story_dict: str, story_file_name: str):
    story_name = story_file_name.replace(".txt", "")
    story_graph = StoryGraph()
    story_graph.load_graph(story_dict)
    story_graph.plot_graph(
        Path(os.getenv("BONBON_WORKSPACE_DATA"))
        / "story_graphs"
        / f"{story_name}.svg"
    )
    story_graph.save_graph(
        Path(os.getenv("BONBON_WORKSPACE_DATA"))
        / "story_graphs"
        / f"{story_name}.json"
    )


def create_demo():
    with gr.Blocks() as demo:
        gr.Markdown("# Story Graph App")
        gr.Markdown(
            "This app allows you to create and visualize story graphs."
        )

        with gr.Row():
            with gr.Column():
                story_dropdown = gr.Dropdown(
                    choices=get_available_stories(),
                    label="Select Story",
                    interactive=True,
                    value=None,
                )
                language = gr.Dropdown(
                    choices=["French", "English"],
                    label="Language",
                    interactive=True,
                    value="French",
                )
                create_questions_button = gr.Button(
                    "Create Questions", variant="primary"
                )
                story_dict = gr.Textbox(label="Story Dict", value="", lines=10)
                save_story_dict_button = gr.Button(
                    "Save Story Graph", variant="primary"
                )

        create_questions_button.click(
            fn=create_questions,
            inputs=[story_dropdown, language],
            outputs=[story_dict],
        )
        save_story_dict_button.click(
            fn=save_story_dict,
            inputs=[story_dict, story_dropdown],
            outputs=[],
        )
    return demo


def main():
    demo = create_demo()
    demo.launch()


if __name__ == "__main__":
    main()
