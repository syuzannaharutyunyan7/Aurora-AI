import os
import subprocess
import sys

# ----------------------------
# REQUIRED PACKAGES
# ----------------------------
REQUIREMENTS = [
    "flask",
    "werkzeug",
    "chromadb",
    "sentence-transformers",
    "llama-cpp-python",
    "pywebview"
]

# ----------------------------
# INSTALL DEPENDENCIES
# ----------------------------
def install_dependencies():
    for package in REQUIREMENTS:
        try:
            __import__(package.split("-")[0])
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call([
                sys.executable,
                "-m",
                "pip",
                "install",
                package,
                "--prefer-binary"
            ])

# ----------------------------
# CHECK MODEL FILE
# ----------------------------
def check_model():
    model_path = "models/llama-3.2-1b-instruct-q4_k_m.gguf"

    if not os.path.exists(model_path):
        print("\n❌ Model file not found!")
        print("Please download it and place it inside /models folder:")
        print(model_path)
        sys.exit(1)

# ----------------------------
# START APP
# ----------------------------
def start_app():
    from app import app
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )

# ----------------------------
# MAIN
# ----------------------------
if __name__ == "__main__":
    install_dependencies()
    check_model()
    start_app()
