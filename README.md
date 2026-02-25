🎵 CoverComposer: Detailed Project Summary
CoverComposer is a production-ready, CPU-only AI music generation platform designed for high-stability and secure containerized deployment. It leverages the MusicGen architecture by Meta AI to generate short, high-quality audio tracks based on user prompts.

🏗️ Core Architecture & Components
1. User Interface (app.py)
Framework: Streamlit 1.32.0.
Features:
Dynamic parameter selection (Mood, Genre, Style, Tempo).
Custom free-text prompt enhancement.
In-browser audio playback and high-quality WAV download.
Defensive error handling with real-time UI status updates.
2. AI Core Engine (/core)
Model: facebook/musicgen-small (Transformer-based).
Generator: Orchestrates model inference using torch and transformers with strict torch.no_grad() execution.
Model Loader: Implements a singleton-like pattern to ensure the model is loaded only once into CPU memory.
Prompt Builder: Translates high-level UI selections into structured AI prompts for the LLM-based music generator.
3. Service Layer (/services)
Device Manager: Automatically detects hardware and optimizes the execution for CPU (limiting threads to prevent system lock).
Config Manager: Handles dynamic loading of configuration settings and secret management.
4. Utilities (/utils)
Audio Utils: Processes raw tensors from the model into 32kHz WAV files using scipy and soundfile.
File Manager: Manages the storage lifecycle of generated assets in assets/generated_audio.
💻 Technical Stack
Languages: Python 3.10.
AI Libraries: PyTorch 2.1.2, Transformers 4.36.2.
Audio Processing: Scipy, Soundfile, Libsndfile1.
Web App: Streamlit.
🚜 Deployment Infrastructure
🐳 Docker Configuration
Dockerfile: Hardened python:3.10-slim image.
Security: Runs as a non-root appuser.
Persistence: Environment variable HF_HOME redirects model weights to a persistent cache directory.
Health Checks: Built-in Docker HEALTHCHECK on /_streamlit/health with a 60s cold-start window.
🚢 Orchestration (docker-compose.yml)
Resource Controls: CPU limits (1.0) and Memory limits (2Gi).
Volumes: Maps local folders for model caching and audio output to ensure data persistence across restarts.
☸️ Kubernetes Ready
Probes: Advanced readinessProbe and livenessProbe with 40s initial delays to accommodate model loading into RAM.
Scaling: Standard Deployment with 1 replica and a ClusterIP Service exposing the app on Port 80.
🛡️ Key Features & Constraints
GPU-Free: Fully optimized for standard server CPUs.
Memory Efficient: Engineered to stay within a 4GB RAM footprint (2Gi limit in K8s).
Cold-Start Hardened: Stabilized boot sequence to prevent container kills during AI model initialization.
Production-Demo Ready: Includes .dockerignore, logging, and automated cleanup scripts.
