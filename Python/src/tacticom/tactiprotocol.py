import re
from dataclasses import dataclass
from typing import Any

PARSING_REGEX = re.compile(r"(\w+)\+(?:\[([\w-]+)\])?(\w+)(?:\[([\w-]+)\])?(?:=(.+|[^\S\r\n]*)?)?")


@dataclass
class TactiMessage:
    prefix: str
    answer_code: str | None
    command: str
    ask_code: str | None
    arguments: list[Any]


def parse(message: str) -> TactiMessage:
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


def serialize(message: TactiMessage) -> str:
    message_str = message.prefix + "+"
    if message.answer_code is not None:
        message_str += "[" + message.answer_code + "]"
    message_str += message.command
    if message.ask_code is not None:
        message_str += "[" + message.ask_code + "]"
    if message.arguments:
        message_str += "=" + ",".join(map(str, message.arguments))
    return message_str
