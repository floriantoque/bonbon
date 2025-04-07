import os
from pathlib import Path

import numpy as np
from bb.lib.llm.llm import LLMMistral
from bb.lib.speech_to_text.stt import STTWav2Vec2
from bb.lib.story_graph.answer_checker import AnswerChecker
from bb.lib.story_graph.graph import StoryGraph
from bb.lib.story_graph.utils import QuestionNode
from bb.lib.text_to_speech.tts import TTSCoqui


class StoryPlayer:
    def __init__(self, story_graph: StoryGraph):
        self.story_graph = story_graph
        self.data_path = Path(os.getenv("BONBON_WORKSPACE_DATA"))

    def play(self, current_story_node_id: str) -> tuple[str, list[str]]:
        print(f"Playing story: {current_story_node_id}")
        node = self.story_graph.get_node(current_story_node_id)

        # Generate audio for the story node content
        content = node.content
        tts = TTSCoqui()
        output_path = self.data_path / "current_story_node_content.wav"
        tts.generate_audio(content, output_path)
        print(f"Content generated: {content}")

        children_node_ids = node.children

        return output_path, children_node_ids

    def is_question_node(self, current_story_node_id: str) -> bool:
        node = self.story_graph.get_node(current_story_node_id)
        if isinstance(node, QuestionNode):
            return True
        else:
            return False

    def get_node_id_after_answer(
        self,
        current_question_node_id: str,
        sound_recorder: tuple[int, np.ndarray],
        question_to_pass: list[str] | None = None,
    ) -> tuple[bool, str, list[str]]:
        stt = STTWav2Vec2("French")
        sampling_rate, audio = sound_recorder

        transcription = stt.transcribe_audio(sampling_rate=sampling_rate, audio=audio)

        answer_checker = AnswerChecker()
        parent_node_id = self.story_graph.get_node(current_question_node_id).parents[0]
        answer_correct = answer_checker.is_correct(
            content=self.story_graph.get_node(parent_node_id).content,
            question=self.story_graph.get_node(current_question_node_id).content,
            gt_answer=self.story_graph.get_node(current_question_node_id).answer,
            listener_answer=transcription,
        )
        print("--------------------------------")
        print(f"Answer is correct: {answer_correct}")
        print(
            f"Expected answer: {self.story_graph.get_node(current_question_node_id).answer}"
        )
        print(f"Listener answer: {transcription}")
        print("--------------------------------")
        if answer_correct:
            next_node_id = self.story_graph.get_node(current_question_node_id).children[
                0
            ]
        else:
            question_to_pass.append(current_question_node_id)
            next_node_id = self.story_graph.get_next_question_node_id(
                current_question_node_id, question_to_pass
            )
            if next_node_id is None:
                next_node_id = self.story_graph.get_node(
                    current_question_node_id
                ).children[0]

        return answer_correct, next_node_id, question_to_pass

    def play_answer_feedback(
        self, answer_correct: bool, current_question_node_id: str
    ) -> str:
        # Generate prompt for the feedback
        if answer_correct:
            prompt = (
                "Create a short feedback for the correct answer. Like this one: "
                "Well done !! You gave the correct answer. Give only the positive feedback."
            )
        else:
            prompt = (
                "Create a super short feedback for the incorrect answer. "
                "Give only the negative but encouraging feedback. Example "
                "of the feedback: Unfortunately the answer is wrong, you will do "
                "better next time. "
            )

        story_language = "French"

        if story_language == "French":
            prompt += " Give the feedback in French"
        # Generate feedback text
        llm = LLMMistral()
        text = llm.generate_text(prompt)

        # Generate audio for the feedback
        tts = TTSCoqui()
        output_path = self.data_path / "answer_feedback.wav"
        tts.generate_audio(text, output_path)

        return output_path
