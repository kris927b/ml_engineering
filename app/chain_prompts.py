from langchain_core.messages import AIMessage, HumanMessage

from langchain_openai import ChatOpenAI

import os

from app.prompts import PROMPT_A1, PROMPT_A2, PROMPT_B
from app.utils import convert_to_base64


def chain_of_prompts(image_data: bytes, heatmap_data: bytes) -> tuple[str, str]:
    prompt_1 = build_prompt_object(PROMPT_A1, image_data)
    prompt_2 = build_prompt_object(PROMPT_A2, heatmap_data)

    model = ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_SECRET"))

    messages = [prompt_1]

    out_a1 = model.invoke(messages).content
    messages.append(AIMessage(content=out_a1))
    messages.append(prompt_2)

    out_a2 = model.invoke(messages).content

    return out_a1, out_a2


def single_prompt(image_data: bytes) -> str:
    prompt = build_prompt_object(PROMPT_B, image_data)

    model = ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_SECRET"))

    out = model.invoke([prompt]).content

    return out


def build_prompt_object(prompt: str, image: str) -> HumanMessage:
    return HumanMessage(
        content=[
            {"type": "text", "text": prompt},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{convert_to_base64(image)}"
                },
            },
        ]
    )
