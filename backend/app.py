import os
from typing import List, Dict
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, ValidationError
from groq import Groq
from fastapi.middleware.cors import CORSMiddleware
import json

load_dotenv()

#loadgroq api key from .env file
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Check if GROQ_API_KEY exists
if not os.getenv("GROQ_API_KEY"):
    raise ValueError("GROQ_API_KEY is not set in the .env file")

# Initialize FastAPI app
app = FastAPI()

# CORS middleware to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the Groq API client
client = Groq(api_key=GROQ_API_KEY)


# Define the request model
class UserInput(BaseModel):
    message: str
    role: str = "user"
    conversation_id: str 

# Define the conversation model
FINANCE_SYSTEM_PROMPT = (
    "You are FinGuide, an educational financial assistant.\n"
    "Goal: Help users understand personal finance topics (budgeting, saving, debt, investing, retirement, taxes at a high level) in clear, neutral, and practical terms.\n"
    "Boundaries:\n"
    "- You are not a licensed advisor and cannot give personalized financial, legal, tax, or investment advice.\n"
    "- Provide general information and education only.\n"
    "- Do not request or store sensitive personal data (SSNs, account numbers).\n"
    "Style: Be concise, structured, and friendly. Ask 1-3 clarifying questions when information is missing.\n"
    "Formatting: Use short sections with brief headings and bullet points where helpful.\n"
    "When discussing investing, always mention risk, diversification, time horizon, and fees.\n"
    "If performing calculations, show the formula and the numbers used.\n"
    "If quoting figures, include currency and units (e.g., USD) where applicable.\n"
)


class Conversation(BaseModel):
    messages: List[Dict[str, str]] = [
        {"role": "system", "content": FINANCE_SYSTEM_PROMPT}
    ]
    active: bool = True


# Initialize in memory dictionary to store conversations
conversations: Dict[str, Conversation] = {}

# Lightweight finance knowledge base (local RAG)
try:
    # Import is optional at runtime; app still works without the module
    from LLM_RAG_Finance.knowledge import get_relevant_context
except Exception:
    def get_relevant_context(query: str, k: int = 3, max_chars: int = 800) -> str:
        return ""


def _prune_old_context(conversation: Conversation, keep_recent: int = 10) -> None:
    """Prune repeated context system messages and keep the conversation trim."""
    pruned: List[Dict[str, str]] = []
    for m in conversation.messages:
        if m.get("role") == "system" and m.get("content", "").startswith("Relevant finance context:"):
            # Skip old context; we'll re-inject fresh context per turn
            continue
        pruned.append(m)
    # Keep only first system + last N messages to reduce token usage
    if pruned:
        head = pruned[0:1]
        tail = pruned[1:][-keep_recent:]
        conversation.messages = head + tail

# grok query
def query_groq_api(conversation: Conversation) -> str:
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=conversation.messages,
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )
        
        response = ""
        for chunk in completion:
            response += chunk.choices[0].delta.content or ""
        
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error with Groq API: {str(e)}")
    
# chat completion endpoint
def get_or_create_conversation(conversation_id: str) -> Conversation:
    if conversation_id not in conversations:
        conversations[conversation_id] = Conversation()
    return conversations[conversation_id]

# Debug endpoint to see raw request
@app.post("/debug/")
async def debug_endpoint(request: Request):
    body = await request.body()
    headers = dict(request.headers)
    print(f"Raw body: {body}")
    print(f"Headers: {headers}")
    try:
        json_body = await request.json()
        print(f"JSON body: {json_body}")
        return {"received": json_body, "headers": headers}
    except Exception as e:
        return {"error": str(e), "raw_body": body.decode(), "headers": headers}

# Alternative endpoint that accepts any JSON
@app.post("/test/")
async def test_endpoint(request: Request):
    try:
        body = await request.json()
        return {"success": True, "received": body}
    except Exception as e:
        raw_body = await request.body()
        return {"success": False, "error": str(e), "raw_body": raw_body.decode()}

# Chat endpoint - support both /chat and /chat/
@app.post("/chat/")
async def chat(request: Request, input: UserInput):
    # Debug logging
    print(f"Received request: {input}")
    print(f"Message: {input.message}")
    print(f"Conversation ID: {input.conversation_id}")
    print(f"Role: {input.role}")
    
    # Retrieve or create a conversation based on the provided conversation_id
    conversation = get_or_create_conversation(input.conversation_id)

    if not conversation.active:
        raise HTTPException(
            status_code=400, 
            detail="The chat session has ended. Please start a new session."
        )
        
    try:
        # Prune old context and keep the thread concise
        _prune_old_context(conversation)

        # Try to retrieve lightweight finance context and inject as a transient system message
        try:
            ctx = get_relevant_context(input.message, k=3, max_chars=800)
        except Exception:
            ctx = ""
        if ctx:
            conversation.messages.append({
                "role": "system",
                "content": f"Relevant finance context:\n{ctx}\n(Use this context only if helpful; otherwise proceed normally.)",
            })

        # Append the user's message to the conversation
        conversation.messages.append({
            "role": input.role,
            "content": input.message
        })
        
        response = query_groq_api(conversation)

        # Add a one-time disclaimer on the first assistant reply in a session
        is_first_reply = len([m for m in conversation.messages if m["role"] == "assistant"]) == 0
        if is_first_reply:
            disclaimer = (
                "Important: I’m an AI for educational finance information and not a licensed advisor. "
                "This is general guidance, not financial, legal, or tax advice."
            )
            response = f"{disclaimer}\n\n{response}"

        # Append the assistant's response to the conversation
        conversation.messages.append({
            "role": "assistant",
            "content": response
        })
        
        # Return the response and conversation ID
        return {
            "response": response,
            "conversation_id": input.conversation_id
        }
    
    # Handle any exceptions that occur during the process    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)