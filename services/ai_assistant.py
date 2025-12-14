"""
AI Assistant Service - Gemini Integration
=========================================

This module provides AI-powered analysis and recommendations using
Google's Gemini language model.

Requirements:
- google-genai package installed
- gemini_api_key in .streamlit/secrets.toml or GEMINI_API_KEY / GOOGLE_API_KEY environment variable set

Configuration:
- DEFAULT_MODEL: "gemini-2.5-flash"
- max_output_tokens: 2048 (default)
- temperature: 0.7 (default)

Usage:
    ai = AIAssistant()
    response = ai.ask("How can we improve security?")
    advice = ai.generate_security_advice("10 incidents, 3 phishing")
"""

import os
import logging
from typing import Optional
import streamlit as st

# ---------------------------------------------------------------------------
# Logging Configuration
# ---------------------------------------------------------------------------
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# ---------------------------------------------------------------------------
# Default Settings
# ---------------------------------------------------------------------------
DEFAULT_MODEL = "gemini-2.5-flash"

# ---------------------------------------------------------------------------
# Conditional SDK Import
# ---------------------------------------------------------------------------
# Try to import the Google GenAI client; don't crash if not installed
try:
    from google import genai  # type: ignore
except Exception as e:
    genai = None
    logger.debug("google.genai not available: %s", e)


class AIAssistant:
    """
    Wrapper around Google's Gemini API for AI-powered insights.
    Designed to fail gracefully when dependencies are missing.
    """
    
    def __init__(self, api_key: Optional[str] = None, default_model: str = DEFAULT_MODEL):
        """
        Initialize the AI Assistant.
        
        Args:
            api_key: Optional API key (defaults to environment variable)
            default_model: Model to use for generation (default: gemini-2.5-flash)
        
        Notes:
            - Checks for API key in .streamlit/secrets.toml first, then environment variables
            - Sets self.enabled = False if SDK or key unavailable
        """
        # Get API key from parameter, .streamlit/secrets.toml, or environment variables
        if api_key:
            self.api_key = api_key
        elif "gemini_api_key" in st.secrets:
            self.api_key = st.secrets["gemini_api_key"]
        else:
            self.api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        
        self.default_model = default_model
        self.client = None
        self.enabled = False
        
        # Check SDK availability
        if not genai:
            logger.warning("google.genai SDK not installed; AI functionality disabled.")
            return
        
        # Check API key availability
        if not self.api_key:
            logger.warning("GEMINI_API_KEY / GOOGLE_API_KEY not set; AI functionality disabled.")
            return
        
        # Try to initialize the client
        try:
            self.client = genai.Client(api_key=self.api_key)
            self.enabled = True
            logger.info("Gemini client initialized successfully.")
        except Exception as e:
            logger.exception("Failed to initialize Gemini client: %s", e)
            self.enabled = False
    
    def ask(self, prompt: str, model: Optional[str] = None, max_output_tokens: int = 2048, temperature: float = 0.7) -> str:
        """
        Send a prompt to the AI model and get a text response.
        
        Args:
            prompt: The question or instruction for the AI
            model: Model to use (default: self.default_model)
            max_output_tokens: Maximum response length (default: 2048)
            temperature: Creativity setting 0.0-1.0 (default: 0.7)
        
        Returns:
            str: AI-generated response or error/guidance message
        
        Notes:
            - Returns guidance message if AI is not enabled
            - Handles various response formats from the API
        """
        # Validate input
        if not prompt or not prompt.strip():
            return "Empty prompt provided."
        
        # Return guidance if AI not configured
        if not self.enabled or not self.client:
            return (
                "AI assistant is not configured. To enable it:\n\n"
                "1. Install the Google GenAI SDK: `pip install google-genai`\n"
                "2. Set your API key in .streamlit/secrets.toml or as an environment variable.\n\n"
                "The rest of the app works without AI features."
            )
        
        model_to_use = model or self.default_model
        
        try:
            # Import types for configuration
            from google.genai import types
            
            # Configure generation parameters
            config = types.GenerateContentConfig(
                max_output_tokens=max_output_tokens,
                temperature=temperature,
            )
            
            # Call the API
            response = self.client.models.generate_content(
                model=model_to_use,
                contents=prompt,
                config=config,
            )
            
            # Extract text from response
            if hasattr(response, "text"):
                return response.text
            
            # Handle dict-style responses
            if isinstance(response, dict):
                return response.get("text") or response.get("output") or str(response)
            
            # Fallback to string representation
            return str(response)
            
        except Exception as e:
            logger.exception("Error during AI generation: %s", e)
            return f"Error generating response: {e}"
