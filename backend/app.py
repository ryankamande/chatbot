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
class Conversation(BaseModel):
    messages: List[Dict[str, str]] = [{"role": "system", "content": "You are a helpful assistant."}]
    active: bool = True


# Initialize in memory dictionary to store conversations
conversations: Dict[str, Conversation] = {}

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
        # Append the user's message to the conversation
        conversation.messages.append({
            "role": input.role,
            "content": input.message
        })
        
        response = query_groq_api(conversation)

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