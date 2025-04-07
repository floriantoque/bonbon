import gradio as gr
import os
from bb.service.story_player_app.utils import (
    get_available_stories,
    load_story,
    play_story,
    get_node_id_after_answer,
)

BONBON_WORKSPACE_DATA = os.getenv("BONBON_WORKSPACE_DATA")


def create_demo():
    """Create the Gradio interface."""
    with gr.Blocks(title="Bonbon Story Player") as demo:
        gr.Markdown("# Bonbon Story Player")

        story_graph = gr.State(None)
        question_to_pass = gr.State(None)
        with gr.Row():
            with gr.Column():
                story_dropdown = gr.Dropdown(
                    choices=get_available_stories(),
                    label="Select Story",
                    interactive=True,
                    value=None,
                )
                current_story_node_id = gr.Textbox(
                    label="Current Story Node ID", visible=False
                )
                audio_output = gr.Audio(
                    label="Story Audio", visible=True, autoplay=True
                )
                play_button = gr.Button(
                    "Continue the story", visible=False, variant="primary"
                )
                sound_recorder = gr.Audio(
                    label="Sound Recorder",
                    visible=False,
                    recording=False,
                    format="wav",
                    sources="microphone",
                )

        # Automatically load story when selection changes
        story_dropdown.change(
            fn=load_story,
            inputs=[story_dropdown],
            outputs=[story_graph, play_button, current_story_node_id],
        )

        play_button.click(
            fn=play_story,
            inputs=[story_graph, current_story_node_id, question_to_pass],
            outputs=[audio_output, current_story_node_id, play_button, sound_recorder],
        )

        sound_recorder.stop_recording(
            fn=get_node_id_after_answer,
            inputs=[
                story_graph,
                current_story_node_id,
                sound_recorder,
                question_to_pass,
            ],
            outputs=[
                audio_output,
                current_story_node_id,
                play_button,
                sound_recorder,
                question_to_pass,
            ],
        )

    return demo


if __name__ == "__main__":
    demo = create_demo()
    demo.launch(allowed_paths=[BONBON_WORKSPACE_DATA])
