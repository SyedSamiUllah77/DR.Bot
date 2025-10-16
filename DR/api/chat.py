from http.server import BaseHTTPRequestHandler
import json
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

# Load medical dataset
def load_medical_data():
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "medical_dataset.json")
    try:
        with open(data_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading data: {e}")
        return []

medical_data = load_medical_data()

def retrieve_relevant_context(query: str, top_k: int = 5):
    query_lower = query.lower()
    query_terms = query_lower.split()
    scored_docs = []
    
    for doc in medical_data:
        score = 0
        keywords = [k.lower() for k in doc.get("keywords", [])]
        content_lower = doc.get("content", "").lower()
        title_lower = doc.get("title", "").lower()
        
        # Keyword matches
        for keyword in keywords:
            if keyword in query_lower:
                score += 10
            for term in query_terms:
                if term in keyword or keyword in term:
                    score += 5
        
        # Title matches
        for term in query_terms:
            if term in title_lower:
                score += 8
        
        # Content matches
        for term in query_terms:
            if len(term) > 3 and term in content_lower:
                score += 2
        
        if score > 0:
            scored_docs.append((score, doc))
    
    scored_docs.sort(reverse=True, key=lambda x: x[0])
    return [doc for score, doc in scored_docs[:top_k]]

def generate_response(query: str, context: list):
    if not context:
        return "I'm a medical information assistant and I couldn't find relevant information about that in my medical database. I can only answer questions related to health conditions, symptoms, and medical topics. Please try asking a medical question."
    
    context_text = "\n\n".join([
        f"**{doc.get('title', '')}**\n{doc.get('content', '')}"
        for doc in context
    ])
    
    if not GEMINI_AVAILABLE:
        response = f"Based on the medical information I found:\n\n{context_text[:500]}...\n\n"
        response += f"**Regarding your question about '{query}':**\n"
        response += f"The information above from {len(context)} medical source(s) may be relevant.\n\n"
        response += "⚠️ This is educational information only. Please consult a healthcare professional for proper diagnosis and treatment."
        return response
    
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not configured")
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"""You are a specialized Medical Information Assistant powered by a RAG system. Your role is STRICTLY LIMITED to answering medical and health-related questions based ONLY on the medical database provided.

STRICT RULES:
1. ONLY answer questions about health, medical conditions, symptoms, diseases, and treatments
2. Use ONLY the medical information provided below - DO NOT use your general knowledge
3. If asked non-medical questions (weather, sports, politics, coding, etc.), politely refuse and redirect to medical topics
4. If the medical database doesn't contain relevant information, say so clearly
5. Always remind users this is educational information and they should consult healthcare professionals
6. Be empathetic, clear, and professional

User Question: {query}

Medical Database Information:
{context_text}

RESPONSE FORMAT:
- Start with a direct, helpful answer to their medical question
- Use information from the medical database above
- Include relevant symptoms, treatments, when to seek care
- End with: "⚠️ This is educational information only. Please consult a healthcare professional for proper diagnosis and treatment."

If the question is NOT medical:
Respond: "I'm a specialized medical information assistant. I can only answer questions about health conditions, symptoms, diseases, and medical topics based on my medical database. Please ask a medical or health-related question."

Now provide your response:"""
        
        response = model.generate_content(prompt)
        return response.text
    
    except Exception as e:
        print(f"Gemini error: {e}")
        response = f"Based on the medical information I found:\n\n{context_text[:500]}...\n\n"
        response += f"**Regarding your question about '{query}':**\n"
        response += f"The information above from {len(context)} medical source(s) may be relevant.\n\n"
        response += "⚠️ This is educational information only. Please consult a healthcare professional for proper diagnosis and treatment."
        return response

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))
            
            query = data.get('query', '') or data.get('message', '')
            
            if not query:
                raise ValueError("No query provided")
            
            context = retrieve_relevant_context(query)
            response_text = generate_response(query, context)
            
            result = {
                'response': response_text,
                'sources': [{'id': doc.get('id'), 'title': doc.get('title')} for doc in context[:5]]
            }
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
        
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            error_response = {'error': str(e)}
            self.wfile.write(json.dumps(error_response).encode())
