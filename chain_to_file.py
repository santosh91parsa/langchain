#!/usr/bin/env python3
"""
Example 2: Chain to File Output (Simplified)

Demonstrates:
- Automatic environment variable resolution (no manual os.environ unpacking needed)
- Clean LCEL chaining (|)
- Direct output file writing using pathlib
"""

from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Load .env if present (ChatOpenAI automatically reads OPENAI_API_KEY and OPENAI_BASE_URL)
load_dotenv()

# 1. Initialize model (environment variables are detected automatically)
model = ChatOpenAI(model="glm-5.2")

# 2. Define prompt template
prompt = ChatPromptTemplate.from_template("Explain {topic} in two sentences.")

# 3. Wire into chain and invoke
chain = prompt | model
reply = chain.invoke({"topic": "how DNS resolves a domain name"})

# 4. Save output to file
out_dir = Path("output")
out_dir.mkdir(exist_ok=True)
out_file = out_dir / "dns_resolution.txt"
out_file.write_text(reply.content)

print(f"✓ Saved reply to {out_file}:\n")
print(reply.content)
