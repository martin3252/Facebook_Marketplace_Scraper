import os

from langchain_openai import OpenAI
from langchain.prompts.few_shot import FewShotPromptTemplate

from utils import process_car_list_for_gpt
from gpt_prompts import (
    examples,
    example_prompt,
    prefix_conversation,
    suffix_conversation
)

os.environ["OPENAI_API_KEY"] = "INPUT YOUR OPENAI API KEY"

llm = OpenAI()


prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix=prefix_conversation,
    suffix=suffix_conversation,
    input_variables=["Question"],
)


def call_GPT(car_list):
    data = process_car_list_for_gpt(car_list)

    question = """Can you help me to find the top three best cars for me?"""
    question = question + "\n" + data

    gpt_input = prompt.format(question=question)
    gpt_result = llm.invoke(gpt_input)
    return gpt_result
