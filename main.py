import logging

from src.integrations.sample_module import SampleClass

logger = logging.getLogger("main")


def handler(event, context):
    in_text = event.get(
        'text', 'Hello World. Does GitHub Actions work?')
    logger.info(in_text)
    out_text = SampleClass().compute(in_text)
    response = {
        "text": out_text
    }
    logger.info("Successful execution")
    return response


if __name__ == "__main__":
    event = {
        "text": "Hey there!"
    }
    handler(event, {})
