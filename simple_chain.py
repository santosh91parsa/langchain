#!/usr/bin/env python3
"""
Simple LangChain Chain Example

Demonstrates wiring three core components:
1. Chat Model (ChatOpenAI)
2. Prompt Template (ChatPromptTemplate)
3. Pipeline operator (|) to invoke the chain
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Load OPENAI_API_KEY and OPENAI_BASE_URL from environment or .env
load_dotenv()


def main():
    # 1. The chat model (supports deepseek-v4-flash, deepseek-v4-pro, glm-5.2, gpt-oss-120b, minimax-m3)
    model = ChatOpenAI(model="gpt-oss-120b")

    # 2. The prompt template
    prompt = ChatPromptTemplate.from_template(
        "Explain what is {topic} in two sentences"
    )

    # 3. Piping them into a chain
    chain = prompt | model

    # 4. Invoke with parameters
    topic = "DNS"
    print(f"Invoking chain for topic: '{topic}'...\n")
    reply = chain.invoke({"topic": topic})

    # 5. Print the extracted content
    print("--- Model Reply ---")
    print(reply.content)


if __name__ == "__main__":
    main()
