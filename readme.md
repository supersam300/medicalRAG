# Pharmacy Chatbot (AI Pharmacist)

An AI-powered assistant that helps users identifying common medicines for everyday ailments. Built with **Gradio**, **Ollama**, and **LiteLLM**, this bot behaves like a pharmacist, validating symptoms and prescribing over-the-counter remedies from a curated list.

## Features

-   **AI Chat Interface**: Conversational interface powered by Llama 3.2.
-   **Medicine Prescription Tool**: Automatically identifies ailments (Fever, Cold, Allergies, etc.) and suggests active ingredients and common brands.
-   **Local Inference**: Runs entirely locally using Ollama.

## prerequisites

-   Python 3.9+
-   [Ollama](https://ollama.com/) installed and running.
-   `llama3.2` model pulled in Ollama.

```bash
ollama pull llama3.2
```

## Installation

1.  Clone the repository.
2.  Install dependencies:

```bash
pip install -r req.txt
```

## Usage

1.  Ensure Ollama is running (`ollama serve`).
2.  Run the application:

```bash
python main_2.py
```

3.  Open the Gradio URL (usually `http://127.0.0.1:7860`) in your browser.
4.  Ask questions like:
    *   "I have a fever and body pain."
    *   "What should I take for acidity?"
    *   "Medicine for a runny nose?"

## Tech Stack

-   **Gradio**: User Interface.
-   **LiteLLM**: LLM abstraction.
-   **Ollama**: Local LLM backend.
-   **OpenAI SDK**: Compatible API client.
