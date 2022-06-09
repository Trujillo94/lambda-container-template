import logging

logger = logging.getLogger("main")


def handler(event, context):
    text = event.get(
        'text', 'Hello World. Does GitHub Actions work?')
    print(text)
    logger.info(text)
    response = {
        "text": text
    }
    logger.info("Successful execution")
    return response


if __name__ == "__main__":
    event = {
        "text": "Hey there!"
    }
    handler(event, {})
