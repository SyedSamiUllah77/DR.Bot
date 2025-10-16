# 🏥 Medical RAG Chatbot# 🏥 Medical RAG Chatbot



A Retrieval-Augmented Generation (RAG) medical chatbot powered by FastAPI, Google Gemini AI, and a curated 60-disease knowledge base.A comprehensive medical information chatbot using **Retrieval-Augmented Generation (RAG)** with 50 disease profiles, built with FastAPI backend and vanilla JavaScript frontend.



## 🌟 Features## 📋 Features



- 📚 **60 Medical Conditions** - Major diseases + common ailments- ✅ **50 Medical Conditions** covering infectious diseases, chronic conditions, cancers, and mental health

- 🤖 **Gemini AI** - Google Gemini 2.5 Flash integration- ✅ **Enhanced RAG System** with intelligent keyword matching and scoring

- 🔍 **RAG Architecture** - Accurate, context-aware responses- ✅ **FastAPI Backend** with REST API endpoints

- 🚫 **Medical-Only** - Refuses non-medical questions- ✅ **Modern Chat Interface** with gradient design

- 🌐 **Modern UI** - Clean, responsive chat interface- ✅ **Real-time Communication** between frontend and backend

- ✅ **Source Citations** showing which medical documents were referenced

## 🛠️ Tech Stack- ✅ **Ready for Gemini AI** integration (placeholder code included)



- **Backend:** FastAPI (Python)## 🗂️ Project Structure

- **AI:** Google Gemini 2.5 Flash

- **Frontend:** HTML, CSS, JavaScript```

- **Database:** JSON (60 diseases)medical-rag-chatbot/

│

## 📦 Installation├── backend/

│   ├── main.py                # FastAPI app with enhanced RAG logic

```bash│   └── requirements.txt       # Python dependencies

# Clone repository│

git clone https://github.com/YOUR_USERNAME/medical-rag-chatbot.git├── data/

cd medical-rag-chatbot│   └── medical_dataset.json   # 50 diseases with comprehensive info

│

# Create virtual environment├── frontend/

python -m venv venv│   ├── index.html             # Chat UI

venv\Scripts\activate  # Windows│   ├── styles.css             # Modern styling

│   └── script.js              # API integration

# Install dependencies│

cd backend└── README.md                  # This file

pip install -r requirements.txt```



# Set environment variable## 🚀 Getting Started

echo GEMINI_API_KEY=your_key_here > .env

### Prerequisites

# Run backend

python main.py- Python 3.8 or higher

- Modern web browser

# Open frontend (new terminal)

cd ../frontend### Installation

python -m http.server 3000

```1. **Navigate to backend directory:**

   ```powershell

Visit: `http://localhost:3000/chatbot.html`   cd "d:\MED BOT\DR\backend"

   ```

## 🎯 How It Works

2. **Install Python dependencies:**

1. **User Query** → RAG retrieves relevant diseases   ```powershell

2. **Scoring** → Ranks by keyword/title/content match   pip install -r requirements.txt

3. **Context** → Top 5 diseases sent to Gemini   ```

4. **AI Response** → Natural answer using ONLY database content

5. **Output** → Conversational response + sources### Running the Application



## 🔒 Safety1. **Start the Backend Server:**

   ```powershell

- ✅ Strict medical scope (refuses off-topic questions)   cd "d:\MED BOT\DR\backend"

- ✅ No AI hallucination (constrained to database)   python main.py

- ✅ Source transparency   ```

- ✅ Medical disclaimer included   

   The API will be available at: `http://localhost:8000`

## ⚠️ Disclaimer

2. **Open the Frontend:**

Educational tool only. Always consult healthcare professionals for medical advice.   - Simply open `frontend/index.html` in your web browser

   - Or use a local server (e.g., Live Server in VS Code)

## 📄 License

## 📊 API Endpoints

MIT License

### Health Check
```
GET http://localhost:8000/health
```
Returns server status and dataset information.

### Chat Endpoint
```
POST http://localhost:8000/chat
Content-Type: application/json

{
  "query": "What are the symptoms of diabetes?",
  "conversation_history": []
}
```
Returns AI response with relevant sources.

### List Diseases
```
GET http://localhost:8000/diseases
```
Returns list of all 50 diseases in the database.

## 🔧 Configuration

### Adding Google Gemini AI Integration

To enable AI-powered responses with Google Gemini:

1. **Get a Gemini API key** from [Google AI Studio](https://makersuite.google.com/app/apikey)

2. **Create a `.env` file** in the backend directory:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

3. **Uncomment the Gemini code** in `backend/main.py` (lines marked with TODO)

4. **Restart the server**

## 📚 Medical Dataset

The chatbot includes information on **50 diseases**:

### Infectious Diseases (30)
- Influenza, COVID-19, Tuberculosis, Measles, Chickenpox, Shingles
- Hepatitis A/B/C, HIV/AIDS, HPV
- Diphtheria, Tetanus, Pertussis, Meningococcal Disease, Rubella
- Rotavirus, Dengue, Zika, Ebola, Malaria, Lyme Disease
- Chlamydia, Gonorrhea, Syphilis, Cholera, Typhoid Fever
- Polio, Anthrax, Legionnaires' Disease

### Chronic & Non-Communicable Diseases (20)
- **Cardiovascular:** Ischemic Heart Disease, Stroke, Heart Failure, Hypertensive Heart Disease
- **Respiratory:** COPD, Pneumonia, Asthma
- **Metabolic:** Diabetes Mellitus, Chronic Kidney Disease, Liver Cirrhosis
- **Neurological:** Alzheimer's Disease, Parkinson's Disease
- **Cancers:** Lung, Colorectal, Breast, Prostate, Stomach
- **Mental Health:** Major Depressive Disorder, Bipolar Disorder, Schizophrenia

## 🔍 How It Works

1. **User Query:** User types a medical question in the chat interface
2. **RAG Retrieval:** Backend searches through 50 disease profiles using enhanced keyword matching and scoring
3. **Context Building:** Top relevant documents are retrieved and formatted
4. **Response Generation:** System generates response based on retrieved context (ready for Gemini AI)
5. **Source Display:** Frontend shows the response with source citations

## ⚠️ Disclaimer

This chatbot provides **educational information only** and is **NOT** a substitute for professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare professionals for medical concerns.

## 🛠️ Tech Stack

- **Backend:** Python, FastAPI, Pydantic
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Data Format:** JSON
- **AI (Optional):** Google Gemini API

## 📝 Future Enhancements

- [ ] Integrate Google Gemini API for intelligent responses
- [ ] Add vector embeddings for semantic search (Sentence Transformers)
- [ ] Implement conversation history and context awareness
- [ ] Add multilingual support
- [ ] Create user authentication system
- [ ] Add medical image analysis capabilities
- [ ] Deploy to cloud (AWS, Azure, or GCP)

## 🤝 Contributing

Feel free to enhance this project by:
- Adding more disease profiles
- Improving the RAG algorithm
- Enhancing the UI/UX
- Adding new features

## 📄 License

This project is for educational purposes only.

## 🆘 Support

If you encounter any issues:
1. Make sure the backend server is running on port 8000
2. Check browser console for errors
3. Verify all dependencies are installed
4. Ensure the medical_dataset.json file is properly formatted

---

**Built with ❤️ for medical education and information access**
