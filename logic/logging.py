import logging
import json

log_file = "./gui/config/log.json"


class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
        }
        return json.dumps(log_data)


def makeLog(log_file=log_file):
    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Create a file handler for writing logs to a JSON file
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)

    # Create a JSON formatter
    json_formatter = JSONFormatter()

    # Set the formatter for the file handler
    fh.setFormatter(json_formatter)

    # Add the file handler to the logger
    logger.addHandler(fh)
