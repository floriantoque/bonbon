"""Story creator application using Gradio interface.

This module provides a Gradio interface for creating and saving stories
using the Writer class.
"""

import gradio as gr
from pathlib import Path
from bb.lib.story_graph.writer import Writer
import os


def create_story(
    number_phrases: int,
    characters: list[str],
    age_of_the_audience: int,
    language: str,
    story_context: str,
    number_of_breakpoints: int,
    breakpoint_symbol: str,
) -> str:
    """Create a story using the Writer class.

    Parameters
    ----------
    number_phrases: int
        The number of phrases in the story.
    characters: list[str]
        The characters in the story.
    age_of_the_audience: int
        The age of the audience.
    language: str
        The language of the story.
    story_context: str
        The context of the story.
    number_of_breakpoints: int
        The number of breakpoints in the story.
    breakpoint_symbol: str
        The symbol used to represent the breakpoints in the story.

    Returns
    -------
    str, story
    """

    characters = characters.lower().split(",")
    writer = Writer(
        number_of_breakpoints=number_of_breakpoints,
        breakpoint_symbol=breakpoint_symbol,
    )

    # Create story
    story = writer.generate_story(
        number_phrases=number_phrases,
        characters=characters,
        age_of_the_audience=age_of_the_audience,
        language=language,
        story_context=story_context,
    )

    return story


def save_story(story: str, filename: str):
    writer = Writer()
    workspace_data = Path(os.getenv("BONBON_WORKSPACE_DATA"))
    writer.save_story(story, workspace_data / filename)


def create_demo():
    """Create the Gradio interface."""
    with gr.Blocks(title="Story Creator") as demo:
        gr.Markdown("# Story Creator")

        with gr.Row():
            with gr.Column():
                number_phrases = gr.Number(label="Number of phrases", value=15)
                characters = gr.Textbox(
                    label="Characters (separated by commas)",
                    value="mickey,dora l'exploratrice",
                )
            with gr.Column():
                age_of_the_audience = gr.Number(
                    label="Age of the audience", value=6
                )
                language = gr.Dropdown(
                    choices=["French", "English"],
                    label="Language",
                    value="French",
                )
            with gr.Column():
                number_of_breakpoints = gr.Number(
                    label="Number of breakpoints", value=3
                )
                breakpoint_symbol = gr.Textbox(
                    label="Breakpoint symbol", value="||"
                )
        with gr.Row():
            with gr.Column():
                story_context = gr.Textbox(label="Story context", value="")

        with gr.Row():
            with gr.Column():
                create_button = gr.Button("Create Story", variant="primary")

                story = gr.Textbox(label="Story", value="", lines=10)
                filename = gr.Textbox(label="Filename", value="")
                save_button = gr.Button("Save Story", variant="primary")

        create_button.click(
            fn=create_story,
            inputs=[
                number_phrases,
                characters,
                age_of_the_audience,
                language,
                story_context,
                number_of_breakpoints,
                breakpoint_symbol,
            ],
            outputs=story,
        )

        save_button.click(
            fn=save_story,
            inputs=[story, filename],
            outputs=story,
        )

    return demo


if __name__ == "__main__":
    demo = create_demo()
    demo.launch()
