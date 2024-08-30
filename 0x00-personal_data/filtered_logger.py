#!/usr/bin/env python3
"""Module for Personal Data"""
from typing import List
import re
import logging
from os import environ
import mysql.connector


FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Function to hide personal data"""
    for field in fields:
        message = re.sub(f'{field}=.*?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields


    def format(self, record: logging.LogRecord) -> str:
        """the format method"""
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)
        
        
def get_logger() -> logging.Logger:
    """ Returns Logger"""

    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(list(FIELDS)))
    logger.addHandler(handler)

    return logger


def main():
    """main function"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")


if __name__ == "__main__":
    main()
