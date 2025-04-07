"""Answer checker module for evaluating user responses.

This module provides functionality to check and evaluate user answers against
ground truth answers using LLM.
"""

from bb.lib.llm.llm import LLMMistral


class AnswerChecker:
    """Class for checking and evaluating user answers.

    This class implements methods to compare user answers with ground truth
    answers using LLM.

    """

    def __init__(self) -> None:
        """Initialize the AnswerChecker with LLM. Here we use Mistral model by default."""
        self.llm = LLMMistral()

    def is_correct(
        self,
        content: str,
        question: str,
        gt_answer: str,
        listener_answer: str,
    ) -> bool:
        """Check if the listener answer is correct.

        This method uses a LLM to check if the listener answer is correct. So it is
        not a perfect checker, but it is a good enough checker for our purposes.

        Parameters
        ----------
        content: str, The information context.
        question: str, The question to be answered.
        gt_answer: str, The expected answer.
        listener_answer: str, The listener's answer.

        Returns
        -------
            bool: True if the listener answer is correct, False otherwise.
        """
        prompt = (
            f"The information is: {content}"
            f"The question is: {question}"
            f"The expected answer is something like: '{gt_answer}' and the listener answer is: '{listener_answer}'"
            f"The listener answer is correct if it is close to the expected answer."
            f"The listener answer is correct if it is a synonym of the expected answer."
            f"The listener answer is correct if it is a similar answer to the expected answer."
            "Tell me if the listener answer is correct or not by answering with True or False uniquely."
        )
        response = self.llm.generate_text(prompt).lower()
        correct = False if response == "false" else True

        if response not in ["true", "false"]:
            print(f"Invalid response from LLM: {response}, returning True by default.")

        return correct
