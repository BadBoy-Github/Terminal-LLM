# Hugging Face Terminal Chatbot

A small Python terminal chatbot that keeps conversation history and calls a free text-generation model through the Hugging Face Inference Providers API using `requests`.

## Setup (Windows PowerShell)

Create and activate the virtual environment, then install the dependency:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Create a Hugging Face access token at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens). Copy the template to `.env` and replace the placeholder with your token:

```powershell
Copy-Item .env.example .env
```

Open `.env` and set `HF_TOKEN=hf_your_token_here`. The chatbot loads this file automatically; `.env` is excluded from Git. Environment variables already set in PowerShell take precedence. You can optionally set `HF_MODEL` in `.env` to choose another supported model.

Run the chatbot:

```powershell
python chatbot.py
```

Type `/reset` to clear the conversation or `/exit` to quit. The default is the 3B `ibm-granite/granite-4.2-3b` model, verified with this token. Hugging Face model/provider availability and free usage limits can change. To select another chat-completion model listed by Hugging Face Inference Providers, add `HF_MODEL` to `.env`:

```dotenv
HF_MODEL=ibm-granite/granite-4.2-3b
```
