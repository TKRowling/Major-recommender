# Cloudflare Workers AI RAG Deployment Update

This project now uses this hosted RAG flow:

```text
Vercel frontend
→ Render Flask backend
→ FAISS semantic retrieval
→ Cloudflare Workers AI
→ chatbot answer