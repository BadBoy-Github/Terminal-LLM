import os

from dotenv import load_dotenv
import requests


load_dotenv()

API_URL = "https://router.huggingface.co/v1/chat/completions"
MODEL = os.getenv("HF_MODEL")
SYSTEM_PROMPT = "You are a helpful assistant. Keep your answers clear and concise."


def get_reply(messages, token):
    response = requests.post(
        API_URL,
        headers={"Authorization": f"Bearer {token}"},
        json={
            "model": MODEL,
            "messages": messages,
            "max_tokens": 512,
        },
        timeout=60,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()


def main():
    token = os.getenv("HF_TOKEN")
    if not token:
        print("Set HF_TOKEN in your .env file or environment variables.")
        print("Get a token at https://huggingface.co/settings/tokens")
        return

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    print(f"Chatbot ready using {MODEL}. Type /reset to clear the conversation or /exit to quit.\n")

    while True:
        try:
            user_text = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_text:
            continue
        if user_text.lower() == "/exit":
            print("Goodbye!")
            break
        if user_text.lower() == "/reset":
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            print("Conversation cleared.\n")
            continue

        messages.append({"role": "user", "content": user_text})
        try:
            reply = get_reply(messages, token)
        except requests.exceptions.HTTPError as error:
            messages.pop()
            detail = error.response.text if error.response is not None else str(error)
            print(f"\nHugging Face returned an error: {detail}\n")
            continue
        except requests.exceptions.RequestException as error:
            messages.pop()
            print(f"\nCould not reach Hugging Face: {error}\n")
            continue
        except (KeyError, IndexError, TypeError, ValueError):
            messages.pop()
            print("\nThe API returned an unexpected response. Try again.\n")
            continue

        messages.append({"role": "assistant", "content": reply})
        print(f"Assistant: {reply}\n")


if __name__ == "__main__":
    main()