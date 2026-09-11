# Introduction to LangChain: Building a Simple Chain

A simple LangChain chain is three pieces wired together:
1. **A Chat Model** pointed at the API
2. **A Prompt Template** with a variable
3. **A Pipe (`|`)** that joins them

Here is a breakdown of each piece, followed by the complete working example.

---

## 1. The Chat Model

LangChain's OpenAI-compatible model lives in the `langchain-openai` package and is called `ChatOpenAI`.

It automatically reads the standard environment variables:
* `OPENAI_BASE_URL` — for the API endpoint URL
* `OPENAI_API_KEY` — for the authentication key

Because it reads these directly from the environment, you don't paste either secret into your code. You only choose which model answers:

```python
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-oss-120b")
```

> **Available models:**
> Any of the available models can be used here:
> * `deepseek-v4-flash`
> * `deepseek-v4-pro`
> * `glm-5.2`
> * `gpt-oss-120b`
> * `minimax-m3`

---

## 2. The Prompt Template

A template is your prompt wording with a named placeholder in it. You define the structure once and fill in the variable dynamically at call time:

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template(
    "Explain what is {topic} in two sentences"
)
```

---

## 3. Piping Them into a Chain

The `|` (pipe) operator joins the components together so the filled-in prompt flows into the model as a unified pipeline (LangChain Expression Language / LCEL).

Call `.invoke()` with your dictionary of variables and read the answer directly off `.content`:

```python
chain = prompt | model
reply = chain.invoke({"topic": "DNS"})
print(reply.content)
```

### Why this is better:
* The filled template automatically becomes the formatted user message.
* The model executes the completion.
* `reply.content` holds the exact text you would have otherwise extracted by manually parsing `response.choices[0].message.content`.
* **Result:** The exact same API call under the hood, but with far less boilerplate wiring.

---

## 🚀 Examples

### Example 1: Basic Console Output ([`simple_chain.py`](simple_chain.py))

```python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

model = ChatOpenAI(model="gpt-oss-120b")
prompt = ChatPromptTemplate.from_template("Explain what is {topic} in two sentences")
chain = prompt | model

reply = chain.invoke({"topic": "DNS"})
print(reply.content)
```

### Example 2: Chain with File Output ([`chain_to_file.py`](chain_to_file.py))

A simplified pattern demonstrating file persistence:
* No manual unpacking of `os.environ` keys (`ChatOpenAI` reads them automatically).
* Clean `pathlib.Path` usage at top-level.
* Saves output directly to disk.

```python
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# Model automatically uses OPENAI_BASE_URL and OPENAI_API_KEY
model = ChatOpenAI(model="glm-5.2")
prompt = ChatPromptTemplate.from_template("Explain {topic} in two sentences.")
chain = prompt | model

reply = chain.invoke({"topic": "how DNS resolves a domain name"})

# Persist output
out_dir = Path("output")
out_dir.mkdir(exist_ok=True)
(out_dir / "dns_resolution.txt").write_text(reply.content)
```

---

## 🧪 Environment & Lab Setup

If you are running in a preconfigured lab environment or VM, your AI keys are already set in your environment:
* `$OPENAI_BASE_URL`
* `$OPENAI_API_KEY`

To test locally or on another machine:
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Export environment variables (or create a .env file)
export OPENAI_API_KEY="your-api-key"
export OPENAI_BASE_URL="your-api-url"

# 3. Run either script
python simple_chain.py
python chain_to_file.py
```

