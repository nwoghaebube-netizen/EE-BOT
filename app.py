import gradio as gr
import requests
import os

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")

SYSTEM_PROMPT = "You are E.E Bot, a helpful AI assistant created by Ebube. Your name is E.E Bot. Whenever anyone asks your name, say your name is E.E Bot and you were created by Ebube. Never say you were made by Meta or Anthropic or Google or anyone else. When you are given search results, always use them to give up to date answers. Prioritize search results over your training data."

def search_web(query):
    try:
        response = requests.post(
            "https://api.tavily.com/search",
            headers={"Content-Type": "application/json"},
            json={
                "api_key": TAVILY_API_KEY,
                "query": query,
                "search_depth": "basic",
                "max_results": 5
            }
        )
        data = response.json()
        results = []
        for item in data.get("results", []):
            results.append(f"- {item['title']}: {item['content']}")
        return "\n".join(results) if results else None
    except:
        return None

def ask_ai(message, history):
    search_results = search_web(message)

    augmented_message = message
    if search_results:
        augmented_message = f"""User question: {message}

Current web search results:
{search_results}

Answer using the search results above for up to date information."""

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for human, assistant in history:
        messages.append({"role": "user", "content": human})
        messages.append({"role": "assistant", "content": assistant})
    messages.append({"role": "user", "content": augmented_message})

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": messages
        }
    )
    data = response.json()
    if "choices" not in data:
        return f"API Error: {data.get('error', {}).get('message', 'Unknown error')}"
    return data["choices"][0]["message"]["content"]

demo = gr.ChatInterface(
    fn=ask_ai,
    title="E.E Bot",
    description="Welcome! I am E.E Bot, created by Ebube. Ask me anything!"
)
demo.launch()
