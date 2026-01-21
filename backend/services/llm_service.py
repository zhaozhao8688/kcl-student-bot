"""
OpenRouter LLM Service using OpenAI SDK.
"""

from openai import OpenAI
from typing import List, Dict, Any, Optional
from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class LLMService:
    """Service for interacting with LLMs via OpenRouter."""

    def __init__(self):
        """Initialize OpenRouter client."""
        self.client = OpenAI(
            base_url=settings.openrouter_base_url,
            api_key=settings.openrouter_api_key,
            default_headers={
                "HTTP-Referer": "http://localhost:3000",
                "X-Title": "KCL Student Bot"
            }
        )
        self.default_model = settings.default_model
        logger.info(f"LLM Service initialized with model: {self.default_model}")

    def generate(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """
        Generate a response from the LLM.

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: Model to use (defaults to settings.default_model)
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens in response

        Returns:
            Generated text response
        """
        try:
            model = model or self.default_model

            logger.info(f"Generating response with model: {model}")
            logger.debug(f"Messages: {messages}")

            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )

            content = response.choices[0].message.content
            logger.info(f"Generated response of length: {len(content)}")

            return content

        except Exception as e:
            logger.error(f"Error generating LLM response: {str(e)}")
            raise

    async def agenerate(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """
        Async version of generate method.

        Args:
            messages: List of message dictionaries
            model: Model to use
            temperature: Sampling temperature
            max_tokens: Maximum tokens

        Returns:
            Generated text response
        """
        # For now, using sync version
        # Can be updated to use AsyncOpenAI client if needed
        return self.generate(messages, model, temperature, max_tokens)


# Lazy initialization for singleton
_llm_service_instance = None


def get_llm_service() -> LLMService:
    """
    Get or create LLM service instance (lazy initialization).
    This allows the service to be recreated if settings change.
    """
    global _llm_service_instance
    if _llm_service_instance is None:
        _llm_service_instance = LLMService()
    return _llm_service_instance


def reset_llm_service():
    """
    Reset the LLM service instance.
    Useful when API keys or settings change.
    """
    global _llm_service_instance
    _llm_service_instance = None
    logger.info("LLM service instance reset")


# Singleton instance (backward compatibility)
llm_service = get_llm_service()
