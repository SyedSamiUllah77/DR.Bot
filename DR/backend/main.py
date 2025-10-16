# Medical RAG Chatbot - FastAPI Backend with Gemini Integration

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
from typing import List, Optional

app = FastAPI(title="Medical RAG Chatbot API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class ChatRequest(BaseModel):
    query: str
    conversation_history: Optional[List[dict]] = []

class ChatResponse(BaseModel):
    response: str
    sources: Optional[List[dict]] = []

# Load medical dataset
def load_medical_data():
    try:
        with open("../data/medical_dataset.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Warning: medical_dataset.json not found")
        return []

medical_data = load_medical_data()

# Enhanced RAG retrieval function
def retrieve_relevant_context(query: str, top_k: int = 5):
    """
    Enhanced keyword-based retrieval from medical dataset.
    Searches through keywords and content, returns top matches.
    In production, use embeddings + vector similarity for better results.
    """
    query_lower = query.lower()
    query_terms = query_lower.split()
    
    # Score each document based on keyword and content matching
    scored_docs = []
    
    for doc in medical_data:
        score = 0
        keywords = [k.lower() for k in doc.get("keywords", [])]
        content_lower = doc.get("content", "").lower()
        title_lower = doc.get("title", "").lower()
        
        # Check keyword matches (higher weight)
        for keyword in keywords:
            if keyword in query_lower:
                score += 10
            # Partial matches
            for term in query_terms:
                if term in keyword or keyword in term:
                    score += 5
        
        # Check title matches (high weight)
        for term in query_terms:
            if term in title_lower:
                score += 8
        
        # Check content matches (lower weight)
        for term in query_terms:
            if len(term) > 3 and term in content_lower:
                score += 2
        
        if score > 0:
            scored_docs.append((score, doc))
    
    # Sort by score and return top_k
    scored_docs.sort(reverse=True, key=lambda x: x[0])
    relevant_docs = [doc for score, doc in scored_docs[:top_k]]
    
    return relevant_docs

# Enhanced response generation with strict medical-only scope
def generate_response_with_gemini(query: str, context: List[dict]):
    # Prepare context from retrieved documents
    if not context:
        return "I'm a medical information assistant and I couldn't find relevant information about that in my medical database. I can only answer questions related to health conditions, symptoms, and medical topics. Please try asking a medical question or consult a healthcare professional."

    context_text = "\n\n---\n\n".join([
        f"**{doc.get('title', 'Unknown')}**\n{doc.get('content', '')}"
        for doc in context
    ])

    # Gemini API integration
    try:
        import os
        from dotenv import load_dotenv
        import google.generativeai as genai
        
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            print("Warning: GEMINI_API_KEY not found in environment")
            raise ValueError("API key not configured")
        
        print(f"Configuring Gemini with API key: {api_key[:10]}...")
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')  # Using latest stable model
        
        prompt = f'''You are a specialized Medical Information Assistant powered by a RAG (Retrieval-Augmented Generation) system. Your role is STRICTLY LIMITED to answering medical and health-related questions based ONLY on the medical database provided.

STRICT RULES:
1. ONLY answer questions about health, medical conditions, symptoms, diseases, and treatments
2. Use ONLY the medical information provided below - DO NOT use your general knowledge
3. If asked non-medical questions (weather, sports, politics, coding, etc.), politely refuse and redirect to medical topics
4. If the medical database doesn't contain relevant information, say so clearly
5. Always remind users this is educational information and they should consult healthcare professionals
6. Be empathetic, clear, and professional
7. If a question seems medical but the database has no relevant info, suggest they consult a doctor

User Question: {query}

Medical Database Information:
{context_text}

RESPONSE FORMAT:
- Start with a direct, helpful answer to their medical question
- Use information from the medical database above
- Include relevant symptoms, treatments, when to seek care
- End with: "⚠️ This is educational information only. Please consult a healthcare professional for proper diagnosis and treatment."

If the question is NOT medical (e.g., asking about weather, sports, coding, general knowledge):
Respond: "I'm a specialized medical information assistant. I can only answer questions about health conditions, symptoms, diseases, and medical topics based on my medical database. Please ask a medical or health-related question."

Now provide your response:'''
        
        print(f"Sending request to Gemini API...")
        response = model.generate_content(prompt)
        print(f"Received response from Gemini API")
        return response.text
        
    except Exception as e:
        print(f"Gemini API error: {type(e).__name__}: {str(e)}")
        import traceback
        print(traceback.format_exc())
        
        # Fallback to basic response
        response = f"Based on the medical information I found:\n\n{context_text[:500]}...\n\n"
        response += f"\n**Regarding your medical question about '{query}':**\n"
        response += f"The information above from {len(context)} medical source(s) may be relevant to your inquiry. "
        response += "\n\n⚠️ **Important:** This is educational information only. Please consult a healthcare professional for proper diagnosis and treatment."
        return response

@app.get("/diseases")
def list_diseases():
    # Get list of all diseases in the database
    return {
        "total": len(medical_data),
        "diseases": [{"id": doc["id"], "title": doc["title"]} for doc in medical_data]
    }

@app.get("/")
def root():
    return {"message": "Medical RAG Chatbot API", "status": "running", "total_diseases": len(medical_data)}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Retrieve relevant context
        context_docs = retrieve_relevant_context(request.query)
        
        # Generate response using Gemini + RAG context
        response_text = generate_response_with_gemini(request.query, context_docs)
        
        return ChatResponse(
            response=response_text,
            sources=context_docs
        )
    
    except Exception as e:
        import traceback
        print(f"Error in /chat endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "healthy", "dataset_loaded": len(medical_data)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
