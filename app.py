import os
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from llama_cpp import Llama

from rag.db import search, add, col
from rag.ingest import ingest_file

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ----------------------------
# MODEL
# ----------------------------
llm = Llama(
    model_path="models/llama-3.2-1b-instruct-q4_k_m.gguf",
    n_ctx=2048,
    n_threads=4,
    n_batch=256,
    verbose=False
)

chat_memory = []
uploaded_files = []

# ----------------------------
# PROMPT BUILDER
# ----------------------------
def build_prompt(user_input):
    docs = search(user_input)
    context = "\n".join(docs) if docs else "No memory found."

    history = ""
    for m in chat_memory[-8:]:
        history += f"User: {m['u']}\nAI: {m['a']}\n"

    return f"""
Context:
{context}

Conversation:
{history}

User: {user_input}
Assistant:
""".strip()

# ----------------------------
# HOME
# ----------------------------
@app.route("/")
def home():
    return render_template("index.html")

# ----------------------------
# CHAT
# ----------------------------
@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json.get("message", "")

        prompt = build_prompt(user_input)

        response = llm(
            prompt,
            stream=False,
            max_tokens=200,
            temperature=0.7,
            stop=["User:"]
        )

        text = response["choices"][0]["text"].strip()

        chat_memory.append({
    "id": len(chat_memory),
    "u": user_input,
    "a": text
})

        add(f"User: {user_input}\nAI: {text}")

        return text

    except Exception as e:
        print("CHAT ERROR:", e)
        return jsonify({"error": str(e)}), 500

# ----------------------------
# UPLOAD FILES
# ----------------------------
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")

    if not file:
        return jsonify({"error": "No file"}), 400

    filename = secure_filename(file.filename)
    path = os.path.join(UPLOAD_FOLDER, filename)

    file.save(path)

    chunks = ingest_file(path)

    uploaded_files.append({
        "name": filename,
        "chunks": len(chunks)
    })

    return jsonify({
        "file": filename,
        "chunks": len(chunks)
    })

# ----------------------------
# RESET CHAT
# ----------------------------
@app.route("/reset", methods=["POST"])
def reset():
    global chat_memory, uploaded_files

    chat_memory = []
    uploaded_files = []

    try:
        col.delete(where={})
    except:
        pass

    return jsonify({"status": "reset"})

# ----------------------------
# EDIT MESSAGE + REGENERATE AI (FIXED CORE FEATURE)
# ----------------------------
@app.route("/update_last", methods=["POST"])
def update_last():

    try:

        data = request.json

        msg_id = data.get("id")
        new_msg = data.get("message", "").strip()

        if msg_id is None:
            return jsonify({"error": "Missing id"}), 400

        if msg_id >= len(chat_memory):
            return jsonify({"error": "Invalid message id"}), 400

        # UPDATE USER MESSAGE
        chat_memory[msg_id]["u"] = new_msg

        # BUILD HISTORY BEFORE THIS MESSAGE
        history = ""

        for m in chat_memory[:msg_id]:

            history += f"User: {m['u']}\n"
            history += f"AI: {m['a']}\n"

        # SEARCH MEMORY
        docs = search(new_msg)

        context = "\n".join(docs) if docs else "No memory found."

        # PROMPT
        prompt = f"""
Context:
{context}

Conversation:
{history}

User: {new_msg}
Assistant:
""".strip()

        # GENERATE NEW RESPONSE
        response = llm(
            prompt,
            stream=False,
            max_tokens=200,
            temperature=0.7,
            stop=["User:"]
        )

        new_answer = response["choices"][0]["text"].strip()

        # UPDATE AI RESPONSE
        chat_memory[msg_id]["a"] = new_answer

        return jsonify({
            "status": "updated",
            "response": new_answer
        })

    except Exception as e:

        print("UPDATE ERROR:", e)

        return jsonify({
            "error": str(e)
        }), 500

# ----------------------------
# RUN
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)