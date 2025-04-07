import os
from pathlib import Path
from pathlib import Path
import os
from bb.lib.story_graph.graph import StoryGraph
from bb.service.story_player_app.player import StoryPlayer
import gradio as gr

# Configuration
BONBON_WORKSPACE_DATA = os.getenv("BONBON_WORKSPACE_DATA")
STORY_DIRECTORY = Path(BONBON_WORKSPACE_DATA, "story_graphs")


def get_available_stories():
    """Get all available story files from the story directory."""
    if not STORY_DIRECTORY.exists():
        STORY_DIRECTORY.mkdir(parents=True)
    return [f.name for f in STORY_DIRECTORY.glob("*.json")]


def load_story(story_file):
    """Load the selected story file."""
    print(f"Loading story: {story_file}")
    story_graph = StoryGraph()
    story_graph.load_graph(filename=STORY_DIRECTORY / story_file)
    play_button = gr.Button("Play the story", visible=True)
    current_story_node_id = gr.Textbox(
        label="Current Story Node ID", visible=True, value="story_0"
    )
    return story_graph, play_button, current_story_node_id


def play_story(story_graph, current_story_node_id, question_to_pass):
    """Play the story."""
    story_player = StoryPlayer(story_graph)
    audio_output, children_node_ids = story_player.play(current_story_node_id)

    # Case 1: End of story
    if len(children_node_ids) == 0:
        print("End of story")
        return audio_output, None, None, None

    is_question_node = story_player.is_question_node(current_story_node_id)
    new_story_node_id = current_story_node_id
    if is_question_node:
        play_button_visible = False
        sound_recorder_visible = True
    else:
        play_button_visible = True
        sound_recorder_visible = False
        new_story_node_id = story_player.story_graph.get_next_question_node_id(
            current_story_node_id, question_to_pass
        )

    play_button = gr.Button(
        "Continue the story", visible=play_button_visible, variant="primary"
    )
    sound_recorder = gr.Audio(
        label="Sound Recorder",
        visible=sound_recorder_visible,
        recording=False,
        format="wav",
        sources="microphone",
    )

    return audio_output, new_story_node_id, play_button, sound_recorder


def get_node_id_after_answer(
    story_graph, current_question_node_id, sound_recorder, question_to_pass
):
    """Check if the answer is correct."""
    if question_to_pass is None:
        question_to_pass = []
    story_player = StoryPlayer(story_graph)
    answer_correct, next_story_node_id, question_to_pass = (
        story_player.get_node_id_after_answer(
            current_question_node_id, sound_recorder, question_to_pass
        )
    )
    audio_output = story_player.play_answer_feedback(
        answer_correct, current_question_node_id
    )

    play_button = gr.Button("Continue the story", visible=True, variant="primary")
    sound_recorder = gr.Audio(
        label="Sound Recorder",
        visible=False,
        recording=False,
        format="wav",
        sources="microphone",
        value=None,
    )

    return (
        audio_output,
        next_story_node_id,
        play_button,
        sound_recorder,
        question_to_pass,
    )
