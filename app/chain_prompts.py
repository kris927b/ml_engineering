"""Module containing functions for performing the processes."""

import os

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser

from langchain_openai import ChatOpenAI

from app.prompts import PROMPT_A1, PROMPT_A2, PROMPT_B, PROMPT_C
from app.data import ProcessA1, ProcessA2, ProcessB, ProcessC
from app.utils import convert_to_base64


def chain_of_prompts(
    image_data: bytes, heatmap_data: bytes
) -> tuple[ProcessA1, ProcessA2]:
    """Process A1 + A2 in a series of prompts.

    Args:
        image_data (bytes): Input image as bytes
        heatmap_data (bytes): Input heatmap as bytes

    Returns:
        tuple[ProcessA1, ProcessA2]: Result in the form of data models
    """

    parser_a1 = PydanticOutputParser(pydantic_object=ProcessA1)
    parser_a2 = PydanticOutputParser(pydantic_object=ProcessA2)

    prompt_1 = build_message_object(PROMPT_A1, image_data, parser_a1)
    prompt_2 = build_message_object(PROMPT_A2, heatmap_data, parser_a2)

    model = ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_SECRET"))

    chain_a1 = model | parser_a1
    chain_a2 = model | parser_a2

    messages = [prompt_1]

    out_a1 = chain_a1.invoke(messages)
    messages.append(AIMessage(content=out_a1.json()))
    messages.append(prompt_2)

    out_a2 = chain_a2.invoke(messages)

    return out_a1, out_a2


def single_prompt(image_data: bytes) -> ProcessB:
    """Running a single prompt in the form of process B

    Args:
        image_data (bytes): Input image as bytes

    Returns:
        ProcessB: Output from model in the form of ProcessB data model
    """
    parser = PydanticOutputParser(pydantic_object=ProcessB)

    prompt = build_message_object(PROMPT_B, image_data, parser)

    model = ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_SECRET"))

    chain = model | parser

    out = chain.invoke([prompt])

    return out


def summarization_prompt(
    out_a1: ProcessA1, out_a2: ProcessA2, out_b: ProcessB
) -> ProcessC:
    """Function for running a summarization prompt, sumarising previous outputs.

    Args:
        A1 (ProcessA1): Output of process A1
        A2 (ProcessA2): Output of process A2
        B (ProcessB): Output of process B

    Returns:
        ProcessC: Output in the form of data model ProcessC
    """
    parser = PydanticOutputParser(pydantic_object=ProcessC)

    prompt = PromptTemplate(
        template=PROMPT_C,
        input_variables=["input"],
        partial_variables={"response_template": parser.get_format_instructions()},
    )

    model = ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_SECRET"))

    chain = prompt | model | parser

    out = chain.invoke({"input": {**out_a1.dict(), **out_a2.dict(), **out_b.dict()}})

    return out


def build_message_object(
    prompt: str, image: bytes, parser: PydanticOutputParser
) -> HumanMessage:
    """Build a message object from a prompt and an image.

    Args:
        prompt (str): Prompt as input to the model
        image (bytes): Image in bytes
        parser (PydanticOutputParser): Pydantic parser built using one of the data models

    Returns:
        HumanMessage: A message object that can be used as input to an LLM
    """
    text_obj = {
        "type": "text",
        "text": prompt.format(response_template=parser.get_format_instructions()),
    }
    return HumanMessage(
        content=[
            text_obj,
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{convert_to_base64(image)}"
                },
            },
        ]
    )
