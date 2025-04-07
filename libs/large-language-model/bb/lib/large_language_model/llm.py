import os
from mistralai import Mistral
from tenacity import retry, stop_after_attempt, wait_fixed


class LLM:
    """Base class for Large Language Models.

    This abstract class defines the interface for different LLM
    implementations.
    """

    def __init__(self):
        """Initialize the LLM base class."""
        pass

    def get_api_key(self) -> str:
        """Get the API key for the LLM service.

        Returns
        -------
        str: The API key string
        """
        raise NotImplementedError("Subclasses must implement this method")

    def get_model(self) -> str:
        """Get the model identifier/name to use.

        Returns
        -------
        str: The model identifier string
        """
        raise NotImplementedError("Subclasses must implement this method")

    def generate_text(self, prompt: str) -> str:
        """Generate text response for the given prompt.

        Parameters
        ----------
        prompt : str
            The input prompt text

        Returns
        -------
        str: The generated response text
        """
        raise NotImplementedError("Subclasses must implement this method")


class LLMMistral(LLM):
    """Mistral AI large language model implementation."""

    def __init__(self):
        """Initialize the Mistral LLM client."""
        super().__init__()
        self.client = Mistral(api_key=self.get_api_key())
        self.model = self.get_model()

    def get_api_key(self) -> str:
        """Get the Mistral API key from environment variables.

        Returns
        -------
        str: The Mistral API key
        """
        return os.getenv("MISTRAL_API_KEY", "")

    def get_model(self) -> str:
        """Get the specific Mistral model to use.

        Returns
        -------
        str: The Mistral model identifier
        """
        return "mistral-small-2503"

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def generate_text(self, prompt: str) -> str:
        """Generate text using the Mistral chat completion API.

        Parameters
        ----------
        prompt : str
            The input prompt text

        Returns
        -------
        str: The generated response from Mistral

        Notes
        -----
        Uses retry decorator to attempt the API call up to 3 times with
        2 second delays.
        """
        messages = [{"role": "user", "content": prompt}]
        chat_response = self.client.chat.complete(model=self.model, messages=messages)
        return chat_response.choices[0].message.content
