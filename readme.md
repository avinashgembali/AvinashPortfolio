# Avinash Gembali — Portfolio

A personal developer portfolio built with **Angular 17**, **Tailwind CSS**, **Angular Animations**, and **EmailJS** for the contact form. Includes an **AI-powered chatbot** built with RAG (Retrieval-Augmented Generation) that answers questions about Avinash using his resume as a knowledge base.

---

## Full Stack Overview

```
AvinashPortfolio/
├── frontend/   ← Angular 17 SPA (UI, animations, contact form, chatbot UI)
└── backend/    ← Python FastAPI (RAG pipeline, /chat API)
```

---

## Tech Stack

### Frontend

| Layer | Technology |
|---|---|
| Framework | Angular 17 (standalone components) |
| Styling | Tailwind CSS 3 + custom CSS |
| Animations | Angular Animations + CSS Intersection Observer |
| Contact form | EmailJS (`@emailjs/browser`) |
| Carousel | Swiper.js |
| Font | Poppins (Google Fonts) |
| Language | TypeScript 5.4 |

### Backend (RAG Chatbot)

| Layer | Technology |
|---|---|
| Backend framework | FastAPI (Python 3.11) |
| Embeddings | Google `gemini-embedding-2` |
| Vector database | MongoDB Atlas Vector Search |
| LLM | Google Gemini (`gemini-2.5-flash-lite` → `gemini-2.5-flash` fallback) |
| Environment | python-dotenv |

---

## Prerequisites

- [Node.js](https://nodejs.org/) v18 or later + npm v9 or later
- Angular CLI v17: `npm install -g @angular/cli@17`
- Python 3.11
- MongoDB Atlas account (free tier)
- Google AI Studio API key (free)

---

## Part 1 — Frontend Setup

### Clone & Install

```bash
git clone https://github.com/your-username/AvinashPortfolio.git
cd AvinashPortfolio/frontend
npm install
```

### Environment Setup (EmailJS + API URL)

Copy the example environment file:

```bash
cp src/environments/environment.example.ts src/environments/environment.ts
```

Fill in your credentials in `src/environments/environment.ts`:

```typescript
export const environment = {
  emailjs: {
    serviceId:  'YOUR_SERVICE_ID',
    templateId: 'YOUR_TEMPLATE_ID',
    publicKey:  'YOUR_PUBLIC_KEY',
  },
  apiUrl: 'http://localhost:3000',  // change to your deployed backend URL in production
};
```

> Never commit `environment.ts` — it is in `.gitignore`.

### EmailJS Setup

[EmailJS](https://www.emailjs.com/) sends emails directly from the browser with no backend. Free plan: 200 emails/month.

1. Sign up at [emailjs.com](https://www.emailjs.com)
2. **Email Services** → Add New Service → connect Gmail/Outlook → copy **Service ID**
3. **Email Templates** → Create New Template → use these variables:

| Variable | Maps to |
|---|---|
| `{{from_name}}` | Sender's name |
| `{{subject}}` | Message subject |
| `{{message}}` | Message body |
| `{{to_email}}` | Your email |
| `{{reply_to}}` | Sender's email |

4. Copy **Template ID**
5. **Account → General** → copy **Public Key**
6. Paste all three into `environment.ts`

### Run Locally

```bash
cd frontend
ng serve
```

Open [http://localhost:4200](http://localhost:4200).

### Build for Production

```bash
ng build
```

Output goes to `dist/frontend/browser/` — deploy to Vercel, Netlify, or GitHub Pages.

---

## Part 2 — RAG Chatbot Backend

### What is RAG?

RAG (Retrieval-Augmented Generation) lets the AI answer questions about *you specifically* using your resume as a knowledge base, instead of guessing.

```
Step 1 — STORE:    Resume → split into chunks → Gemini converts each to a vector → saved in MongoDB Atlas
Step 2 — RETRIEVE: User question → converted to a vector → MongoDB finds the 3 most similar chunks
Step 3 — GENERATE: Relevant chunks + question sent to Gemini → accurate, grounded answer returned
```

### Architecture

```
ONE-TIME INGESTION (run once)
──────────────────────────────────────────────
resume.txt
    │
    ▼
Split into 12 chunks
(personal info, education, experience duration,
 internship, projects, skills, achievements,
 adaptability, openness to technologies, summary)
    │
    ▼
Gemini gemini-embedding-2
    → vector: [0.12, 0.87, -0.34, ...]  (3072 dimensions)
    │
    ▼
MongoDB Atlas — portfolio.resume_chunks
    { _id, text, embedding: [...] }


EVERY USER MESSAGE (runtime)
──────────────────────────────────────────────
User: "What projects has Avinash built?"
    │
    ▼
Gemini gemini-embedding-2  →  question vector
    │
    ▼
MongoDB Atlas $vectorSearch  →  top 3 matching chunks
    │
    ▼
Prompt:
  "Answer about Avinash using ONLY this context:
   [chunk1] [chunk2] [chunk3]
   Question: What projects has Avinash built?"
    │
    ▼
Gemini gemini-2.5-flash-lite (fallback: gemini-2.5-flash)
    → "Avinash built BatBazaar..."
    │
    ▼
FastAPI  →  Angular chatbot UI
```

### Backend Project Structure

```
backend/
├── main.py          ← FastAPI server with /chat endpoint
├── ingest.py        ← One-time script: embeds resume → stores in MongoDB Atlas
├── resume.txt       ← Resume as plain text (the knowledge base)
├── requirements.txt ← Python dependencies
├── .env             ← API keys (never committed)
├── .gitignore
└── venv/            ← Python virtual environment
```

### Backend Setup — Step by Step

**1. Create virtual environment with Python 3.11**

```bash
cd backend

# Mac
/opt/homebrew/bin/python3.11 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Create `.env` file**

```env
GOOGLE_API_KEY=your_google_ai_studio_key_here
MONGODB_URI=mongodb+srv://<user>:<password>@cluster0.xxxxx.mongodb.net/
```

- Get `GOOGLE_API_KEY` free at [aistudio.google.com](https://aistudio.google.com) → Get API key
- Get `MONGODB_URI` from MongoDB Atlas → your cluster → Connect → Drivers

**4. Run ingestion (one time only)**

```bash
python ingest.py
```

Expected output:
```
Dropped existing collection.
Embedding 12 chunks...
  embedded: personal_info
  embedded: career_objective
  embedded: education
  embedded: experience_duration
  embedded: internship
  embedded: project_helper_management
  embedded: project_batbazaar
  embedded: technical_skills
  embedded: achievements
  embedded: adaptability
  embedded: openness_to_technologies
  embedded: summary

Ingested 12 chunks into MongoDB Atlas.
Database: portfolio | Collection: resume_chunks
```

**5. Create Vector Search index in MongoDB Atlas**

This is required after every run of `ingest.py` because ingest drops and recreates the collection, which also deletes the index.

1. Go to [cloud.mongodb.com](https://cloud.mongodb.com) → open your cluster
2. Click **"Atlas Search"** in the left sidebar
3. Click **"Create Search Index"**
4. Choose **"Atlas Vector Search"** → Next
5. Select database: `portfolio`, collection: `resume_chunks`
6. Switch to **JSON editor** and paste:

```json
{
  "fields": [
    {
      "type": "vector",
      "path": "embedding",
      "numDimensions": 3072,
      "similarity": "cosine"
    }
  ]
}
```

7. Name the index exactly: **`vector_index`**
8. Click **Create** — wait 1-2 minutes until status shows **Active**

> **Important:** Every time you re-run `ingest.py`, the collection is dropped and the Vector Search index is deleted with it. You must recreate the index in Atlas UI after each ingestion.

**6. Start the API server**

```bash
source venv/bin/activate
uvicorn main:app --port 3000
```

Server runs at `http://localhost:3000`.

---

## API Reference

### `POST /chat`

**Request:**
```json
{ "message": "What are Avinash's skills?" }
```

**Response:**
```json
{ "answer": "Avinash's technical skills include Java, Python, JavaScript, Angular, React..." }
```

### `GET /health`

Returns `{ "status": "ok" }`.

---

## Code Walkthrough

### `ingest.py` — how embedding and storage works

```python
# 1. For each resume chunk, call Gemini to get a 3072-dimension vector
def embed_text(text):
    response = client.models.embed_content(model="gemini-embedding-2", contents=text)
    return list(response.embeddings[0].values)

# 2. Store as a MongoDB document: { _id, text, embedding }
collection.insert_many([
    { "_id": "technical_skills", "text": "...", "embedding": [0.12, 0.87, ...] },
    ...
])
```

### `main.py` — how each chat request works

```python
@app.post("/chat")
async def chat(req: ChatRequest):
    # Step 1: Embed the user's question
    query_embedding = embed_query(req.message)

    # Step 2: Run $vectorSearch in MongoDB Atlas — finds 3 closest chunks
    results = collection.aggregate([{
        "$vectorSearch": {
            "index": "vector_index",
            "path": "embedding",
            "queryVector": query_embedding,
            "numCandidates": 20,
            "limit": 3
        }
    }])

    # Step 3: Build prompt with retrieved context
    context = "\n\n".join([doc["text"] for doc in results])
    prompt = f"Answer about Avinash using ONLY this context:\n{context}\nQuestion: {req.message}"

    # Step 4: Ask Gemini — tries gemini-2.5-flash-lite first, falls back on quota errors
    response = gemini.models.generate_content(model="gemini-2.5-flash-lite", contents=prompt)
    return { "answer": response.text }
```

---

## Updating Your Resume

Edit `resume.txt`, then re-run:

```bash
python ingest.py
```

Then recreate the Vector Search index in Atlas UI (the index is deleted when the collection is dropped).

---

## Common Questions

**Q: Why split into chunks instead of sending the whole resume?**
Sending only the relevant 3 chunks keeps the answer focused. Sending the full resume every time adds noise and wastes tokens.

**Q: Why not keyword search?**
Keyword search requires exact word matches. Semantic search (via embeddings) understands meaning — "what frameworks does he know?" correctly retrieves the skills chunk even though the word "frameworks" isn't in it.

**Q: Why MongoDB Atlas instead of a local vector database?**
A local vector database breaks on cloud deployments because serverless platforms don't have persistent filesystems. MongoDB Atlas runs in the cloud and works reliably on any deployment platform.

**Q: Can I swap Gemini for a different LLM?**
Yes — only `embed_text()` and `generate_content()` need to change. The RAG pipeline itself is completely model-agnostic.

**Q: Why does the chatbot use multiple models?**
The free tier quota for each Gemini model is limited (20–500 requests/day). The backend tries `gemini-2.5-flash-lite` first, then falls back to `gemini-2.5-flash` and `gemini-3.1-flash-lite` if quota is exhausted on one model.

---

## Project Structure (full)

```
AvinashPortfolio/
├── frontend/
│   └── src/app/
│       ├── components/
│       │   ├── hero/          ← AI chatbot button + showcase live here
│       │   ├── chatbot/       ← Chat dialog component
│       │   ├── navbar/
│       │   ├── about/
│       │   ├── resume/
│       │   ├── domains/
│       │   ├── skills/
│       │   ├── projects/
│       │   ├── hire-me/
│       │   ├── contact/       ← EmailJS integration
│       │   └── footer/
│       └── services/
│           ├── portfolio.service.ts  ← all portfolio content data
│           └── chat.service.ts       ← calls /chat backend endpoint
│
└── backend/
    ├── main.py        ← FastAPI server
    ├── ingest.py      ← one-time ingestion script
    ├── resume.txt     ← knowledge base
    ├── requirements.txt
    └── .env           ← GOOGLE_API_KEY, MONGODB_URI
```

---

## Personalising for Your Own Use

| File | What to change |
|---|---|
| `backend/resume.txt` | Replace with your own resume content |
| `frontend/src/environments/environment.ts` | Your EmailJS keys + backend URL |
| `frontend/src/app/services/portfolio.service.ts` | Your name, skills, projects, experience |
| `frontend/src/assets/Gembali_Avinash_Resume.pdf` | Replace with your own resume PDF |
| `frontend/src/assets/images/` | Replace profile pic and project screenshots |

After updating `resume.txt`, re-run `python ingest.py` and recreate the Vector Search index in Atlas UI.

---

## License

MIT — free to fork and personalise.
