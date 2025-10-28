"""
Extraction Agent

Extracts structured signal from user check-in input:
- Body signals (location: sensation pairs)
- Triggers (contextual factors)
- Temporal context (past/present/future)
- Specificity score (0-10)
"""

import json
import logging
from typing import Dict
from tenacity import retry, stop_after_attempt, wait_exponential

from .chat_service import ChatService

logger = logging.getLogger("lumina.extraction_agent")


# Prompt template with few-shot examples
EXTRACTION_PROMPT = """Extract structured information from this check-in.

Return ONLY valid JSON with this exact structure:
{{
  "body_signals": ["location: sensation", ...],
  "triggers": ["contextual factor", ...],
  "temporal": "past" | "present" | "future",
  "specificity_score": 0-10
}}

SPECIFICITY SCORING (0-10):
- 0-3: Vague emotional labels ("stressed", "tired", "anxious")
- 4-6: Some body awareness ("shoulders tight", "chest heavy")
- 7-10: Specific sensations + context ("left shoulder blade sharp pulling, meeting in 5 min")

EXAMPLES:

Input: "stressed"
Output: {{"body_signals": [], "triggers": [], "temporal": "present", "specificity_score": 2}}

Input: "shoulders tight"
Output: {{"body_signals": ["shoulders: tight"], "triggers": [], "temporal": "present", "specificity_score": 5}}

Input: "chest tight, breath shallow, meeting in 10 min"
Output: {{"body_signals": ["chest: tight", "breath: shallow"], "triggers": ["meeting"], "temporal": "future", "specificity_score": 8}}

Input: "was anxious yesterday about the presentation"
Output: {{"body_signals": [], "triggers": ["presentation"], "temporal": "past", "specificity_score": 3}}

Input: "jaw clenched, shoulders up to ears, about to call mom"
Output: {{"body_signals": ["jaw: clenched", "shoulders: up to ears"], "triggers": ["call mom"], "temporal": "future", "specificity_score": 9}}

Now extract from this check-in:

Input: "{user_input}"
Output:"""


class ExtractionAgent:
    """Agent for extracting structured signals from user input"""

    def __init__(self, chat_service: ChatService = None):
        """
        Initialize extraction agent.

        Args:
            chat_service: Optional ChatService instance (creates new if not provided)
        """
        self.chat_service = chat_service or ChatService()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def extract(self, user_input: str) -> Dict:
        """
        Extract structured signal from user input.

        Args:
            user_input: Raw user check-in text

        Returns:
            dict: {body_signals, triggers, temporal, specificity_score}
        """
        logger.info(f"Extracting signal from: {user_input[:50]}...")

        # Build prompt
        prompt = EXTRACTION_PROMPT.format(user_input=user_input)

        # Call LLM
        try:
            response = self.chat_service.generate(
                prompt=prompt,
                temperature=0.3,  # Low temperature for consistency
                max_tokens=200
            )

            # Parse JSON
            extraction = self._parse_json(response)

            # Validate
            extraction = self._validate_extraction(extraction)

            # Log detailed extraction results
            logger.info(
                f"Extraction complete - "
                f"Specificity: {extraction['specificity_score']}/10, "
                f"Body signals: {extraction['body_signals']}, "
                f"Triggers: {extraction['triggers']}, "
                f"Temporal: {extraction['temporal']}"
            )

            return extraction

        except Exception as e:
            logger.error(f"Extraction failed: {e}")
            # Return fallback
            return self._fallback_extraction(user_input)

    def _parse_json(self, response: str) -> Dict:
        """
        Parse JSON from LLM response.

        Args:
            response: LLM response text

        Returns:
            dict: Parsed JSON

        Raises:
            ValueError: If JSON is malformed
        """
        # Try to find JSON in response
        response = response.strip()

        # Remove markdown code blocks if present
        if response.startswith("```"):
            lines = response.split("\n")
            response = "\n".join(lines[1:-1]) if len(lines) > 2 else response

        # Parse JSON
        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse JSON: {e}")
            # Try to extract JSON from text
            start = response.find("{")
            end = response.rfind("}") + 1
            if start >= 0 and end > start:
                return json.loads(response[start:end])
            raise ValueError(
                f"Could not parse JSON from response: {response[:100]}")

    def _validate_extraction(self, extraction: Dict) -> Dict:
        """
        Validate and clean extraction output.

        Args:
            extraction: Raw extraction dict

        Returns:
            dict: Validated extraction
        """
        # Ensure required fields
        validated = {
            "body_signals": extraction.get("body_signals", []),
            "triggers": extraction.get("triggers", []),
            "temporal": extraction.get("temporal", "present"),
            "specificity_score": extraction.get("specificity_score", 5)
        }

        # Validate types
        if not isinstance(validated["body_signals"], list):
            logger.warning(
                f"Invalid body_signals type: {type(validated['body_signals'])}, converting to empty list")
            validated["body_signals"] = []

        if not isinstance(validated["triggers"], list):
            logger.warning(
                f"Invalid triggers type: {type(validated['triggers'])}, converting to empty list")
            validated["triggers"] = []

        # Validate temporal
        if validated["temporal"] not in ["past", "present", "future"]:
            logger.warning(
                f"Invalid temporal value: {validated['temporal']}, defaulting to 'present'")
            validated["temporal"] = "present"

        # Validate specificity score (0-10 range)
        try:
            score = float(validated["specificity_score"])
            original_score = score

            # Clamp to 0-10 range
            validated["specificity_score"] = max(0.0, min(10.0, score))

            if validated["specificity_score"] != original_score:
                logger.warning(
                    f"Specificity score {original_score} out of range, "
                    f"clamped to {validated['specificity_score']}"
                )
        except (ValueError, TypeError) as e:
            logger.warning(
                f"Invalid specificity_score: {validated['specificity_score']}, defaulting to 5.0")
            validated["specificity_score"] = 5.0

        return validated

    def _fallback_extraction(self, user_input: str) -> Dict:
        """
        Fallback extraction when LLM fails.

        Args:
            user_input: User input text

        Returns:
            dict: Basic extraction
        """
        logger.warning("Using fallback extraction")

        # Simple heuristic: count words as proxy for specificity
        word_count = len(user_input.split())
        specificity = min(10, max(2, word_count // 2))

        return {
            "body_signals": [],
            "triggers": [],
            "temporal": "present",
            "specificity_score": specificity
        }


# Node function for LangGraph
def extraction_agent_node(state: Dict) -> Dict:
    """
    LangGraph node function for extraction agent.

    Args:
        state: MultiAgentState dict

    Returns:
        dict: Updated state with extraction
    """
    agent = ExtractionAgent()
    extraction = agent.extract(state["user_input"])

    return {"extraction": extraction}
