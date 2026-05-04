from typing import Optional, Any
import json
import re


def trimAndLoadJson(
    input_string: str,
    metric: Optional[Any] = None,
) -> Any:
    """Parse a JSON object out of a noisy LLM response.

    The function is tolerant of common deviations LLMs introduce around their
    JSON payloads:

    1. Locate the first ``{`` and the last ``}`` and slice out that span.
    2. If no closing ``}`` is present, append one synthetically.
    3. Strip trailing commas before ``]`` or ``}``.
    4. Drop ASCII control characters (``\\x00``-``\\x1F``, ``\\x7F``) — these
       are illegal in JSON and a frequent cause of parse failures.
    5. ``json.loads`` the cleaned string.

    Args:
        input_string: The raw LLM response that should contain a JSON object.
        metric: Optional metric object; if provided and parsing fails, the
            error message is attached to ``metric.error`` before raising.

    Returns:
        The parsed Python object.

    Raises:
        ValueError: When the input is not a string, is empty, lacks an
            opening brace, or remains invalid JSON after cleanup.
    """
    if not isinstance(input_string, str):
        raise ValueError("Input must be a string.")

    input_string = input_string.strip()
    if not input_string:
        raise ValueError("Input string is empty.")

    # Locate the JSON span.
    start = input_string.find("{")
    end_pos = input_string.rfind("}")

    if start == -1:
        raise ValueError("No opening brace '{' found in input string.")

    # Synthesise a closing brace if missing.
    if end_pos == -1:
        input_string += "}"
        end_pos = len(input_string) - 1

    json_str = input_string[start : end_pos + 1]

    # Strip trailing commas, e.g. {"k": "v",} -> {"k": "v"}, [1,2,] -> [1,2].
    json_str = re.sub(r",(\s*[\]}])", r"\1", json_str)

    # Drop ASCII control characters that are invalid inside JSON.
    json_str = re.sub(r"[\x00-\x1F\x7F]", "", json_str)

    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        error_msg = (
            "Evaluation LLM outputted an invalid JSON. "
            "Please use a better evaluation model."
        )
        if metric is not None:
            setattr(metric, "error", error_msg)
        raise ValueError(error_msg) from e
    except Exception as e:
        raise Exception(f"An unexpected error occurred while parsing JSON: {str(e)}") from e


def checklist_to_markdown(checklist_items):
    """Render a list of ``{interview_item, purpose}`` dicts as a markdown table.

    Used by stage 4 to format the OSCE checklist into the scenario-draft prompt.
    """
    markdown = "| Interview item | Purpose |\n"
    markdown += "|----------------|---------|\n"

    for item in checklist_items:
        interview_item = item.get('interview_item', '')
        purpose = item.get('purpose', '')
        markdown += f"| {interview_item} | {purpose} |\n"

    return markdown
