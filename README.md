# Aurora AI

Aurora is a lightweight, fully local AI assistant built with Python. It combines a local language model with a memory system (RAG), allowing it to chat, remember information, and understand uploaded files — all running entirely on your own machine.

The goal of this project was to build something similar to ChatGPT, but fully offline, private, and customizable.

---

# What Aurora does

* Chat with a local AI model (no internet needed after setup)
* Remember past conversations using vector memory
* Read and understand files (PDF, DOCX, TXT)
* Search relevant context using embeddings (RAG system)
* Edit messages and regenerate responses
* Run completely locally on CPU
* Simple and clean web interface

---

# How it works

Aurora is not just a basic chatbot — it works in a more intelligent way.

When you send a message:

1. Aurora checks its memory for related information
2. It searches uploaded documents if available
3. It builds a combined context (memory + files + chat history)
4. This context is sent to the AI model
5. The model generates a response using all available information

This makes Aurora more context-aware compared to normal chatbots.

---

# AI Model

Aurora runs a local open-source model using GGUF format.

## Model used

Llama 3.2 1B Instruct (Q4_K_M quantized version)

## Runtime

llama.cpp (via llama-cpp-python)

## Why this model

This model was chosen because it is:

* Lightweight and fast
* Works on normal laptops (CPU only)
* Fully offline after setup
* Easy to integrate into a Python system

---

# Model Source

The model is downloaded from Hugging Face:

[https://huggingface.co/hugging-quants/Llama-3.2-1B-Instruct-Q4_K_M-GGUF](https://huggingface.co/hugging-quants/Llama-3.2-1B-Instruct-Q4_K_M-GGUF)

## Important

* The model file is not included in this repository
* Users must download it manually
* All rights belong to the original model creators
* This project only uses the model for inference

---

# Memory System (RAG)

Aurora uses a Retrieval-Augmented Generation system to improve responses.

Instead of relying only on the model’s built-in knowledge, it also uses stored memory.

## How it works

* Text is converted into embeddings
* Stored in a vector database (ChromaDB)
* When a question is asked, similar past data is retrieved
* That context is added to the prompt

This helps Aurora generate more accurate and personalized responses.

---

# File Support

You can upload:

* PDF files
* DOCX files
* TXT files

Aurora will automatically:

* Extract text
* Split it into chunks
* Store it in memory
* Use it during conversations

---

# Tech Stack

* Python
* Flask
* llama-cpp-python
* ChromaDB
* sentence-transformers
* HTML, CSS, JavaScript

---

# Project Structure

```txt
Aurora-AI/
│
├── app.py
├── rag/
│   ├── db.py
│   └── ingest.py
│
├── templates/
│   └── index.html
│
├── data/
│   ├── facts.txt
│   ├── qa.json
│   └── wiki.txt
│
├── models/        (not uploaded)
├── memory/        (not uploaded)
├── uploads/       (not uploaded)
└── venv/          (not uploaded)
```

---

# Installation

```bash
git clone https://github.com/yourusername/Aurora-AI.git
cd Aurora-AI
```

## Create virtual environment

Mac/Linux:

```bash
python -m venv venv
source venv/bin/activate
```

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

---

# Download Model

Download the GGUF model from Hugging Face and place it inside:

```txt
models/
```

Example:

```txt
models/llama-3.2-1b-instruct-q4_k_m.gguf
```

---

# Run Aurora

```bash
python app.py
```

Then open:

[http://127.0.0.1:5000](http://127.0.0.1:5000)

---

# Notes

* Aurora runs fully offline after setup
* No user data is sent to external servers
* The model is not included due to size and licensing

---

# Future Improvements

* Streaming responses
* Multi-chat history system
* Voice input and output
* Better long-term memory summarization
* Desktop application version
* Cloud deployment option

---

# License

This project is open-source and free to use for educational and personal purposes.

The language model is provided by its original creators and follows its own license.

---
