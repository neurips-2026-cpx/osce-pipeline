import logging
from datetime import datetime


def setup_logging():
    """Initialise file-based logging to ``logging.txt`` (append mode, UTF-8)."""
    logging.basicConfig(
        filename='logging.txt',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        encoding='utf-8',
        filemode='a',
    )

    # To also stream logs to the console, uncomment:
    # console = logging.StreamHandler()
    # console.setLevel(logging.INFO)
    # console.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    # logging.getLogger('').addHandler(console)


def log_llm_interaction(script_name, step_name, input_data, output_data):
    """Log a single LLM call: script, step, input variables, and output content."""
    logger = logging.getLogger()

    logger.info("=" * 80)
    logger.info(f"SCRIPT: {script_name}")
    logger.info(f"STEP: {step_name}")
    logger.info(f"TIMESTAMP: {datetime.now().isoformat()}")
    logger.info("-" * 40 + " INPUT " + "-" * 40)

    if isinstance(input_data, dict):
        for key, value in input_data.items():
            logger.info(f"[INPUT] {key}:")
            if isinstance(value, str) and len(value) > 500:
                logger.info(f"  {value}... ({len(value)} chars total)")
            else:
                logger.info(f"  {value}")
    else:
        logger.info(f"[INPUT] {input_data}")

    logger.info("-" * 40 + " OUTPUT " + "-" * 40)

    if hasattr(output_data, 'content'):
        content = output_data.content
        logger.info("[OUTPUT] Content:")
        if len(content) > 1000:
            logger.info(f"  {content}... ({len(content)} chars total)")
        else:
            logger.info(f"  {content}")
    elif isinstance(output_data, str):
        logger.info("[OUTPUT] String:")
        if len(output_data) > 1000:
            logger.info(f"  {output_data}... ({len(output_data)} chars total)")
        else:
            logger.info(f"  {output_data}")
    else:
        logger.info(f"[OUTPUT] {output_data}")

    logger.info("=" * 80)
    logger.info("")


def log_error(script_name, step_name, error_message, additional_info=None):
    """Log an error with script, step, and optional context."""
    logger = logging.getLogger()
    logger.error("=" * 80)
    logger.error(f"ERROR in {script_name} - {step_name}")
    logger.error(f"TIMESTAMP: {datetime.now().isoformat()}")
    logger.error(f"ERROR MESSAGE: {error_message}")
    if additional_info:
        logger.error(f"ADDITIONAL INFO: {additional_info}")
    logger.error("=" * 80)
    logger.error("")


def log_step_start(script_name, step_name, description=""):
    """Log the start of a pipeline step."""
    logger = logging.getLogger()
    logger.info(f"[START] {script_name} - {step_name}")
    if description:
        logger.info(f"  Description: {description}")


def log_step_end(script_name, step_name, success=True, message=""):
    """Log the completion (success or failure) of a pipeline step."""
    logger = logging.getLogger()
    status = "SUCCESS" if success else "FAILED"
    logger.info(f"[{status}] {script_name} - {step_name}")
    if message:
        logger.info(f"  Message: {message}")
    logger.info("")
