import re
from dataclasses import dataclass
from typing import Any

# The regex to parse a TactiCom message. Group 1 to 5 matches the prefix, answer code, command, ask code and arguments
PARSING_REGEX = re.compile(r"(\w+)\+(?:\[([\w-]+)])?(\w+)(?:\[([\w-]+)])?(?:=(.+|[^\S\r\n]*)?)?")


@dataclass
class TactiMessage:
    """
    Represent a TactiCom message
    """
    prefix: str
    answer_code: str | None
    command: str
    ask_code: str | None
    arguments: list[Any]

    def __str__(self):
        return serialize_tactimessage(self)


def parse_tactimessage(message: str) -> TactiMessage:
    """
    Parse a TactiCom message from a string to a TactiMessage object

    :param message: the message to parse
    :return: the parsed message
    """
    match = PARSING_REGEX.match(message)
    if match is None:
        raise ValueError("Invalid message: " + message)

    prefix = match.group(1)
    answer_code = match.group(2)
    command = match.group(3)
    ask_code = match.group(4)
    arguments = match.group(5)

    if arguments is not None:
        arguments = arguments.split(",")
    else:
        arguments = []

    return TactiMessage(prefix, answer_code, command, ask_code, arguments)


def serialize_tactimessage(message: TactiMessage) -> str:
    """
    Serialize a TactiMessage to a string

    :param message: the message to serialize
    :return: the serialized message
    """
    message_str = message.prefix + "+"
    if message.answer_code is not None:
        message_str += "[" + message.answer_code + "]"
    message_str += message.command
    if message.ask_code is not None:
        message_str += "[" + message.ask_code + "]"
    if message.arguments:
        message_str += "=" + ",".join(map(str, message.arguments))
    return message_str
