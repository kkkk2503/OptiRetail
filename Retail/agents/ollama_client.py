import subprocess

DEFAULT_MODEL = "distilbert"  # Default fallback model

def summarize_text(text: str, model: str = DEFAULT_MODEL) -> str:
    """
    Uses the local Ollama tool to generate a summary from the input text.
    The function builds a command-line call to Ollama with the specified model and returns its output.
    """
    prompt = f"Summarize: {text}"
    try:
        # Build the command, e.g., "ollama query <model> 'Summarize: ...'"
        command = ["ollama", "query", model, prompt]
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30  # adjust timeout as needed
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            error_msg = result.stderr.strip()
            return (f"Ollama error (code {result.returncode}): {error_msg}")
    except Exception as e:
        return (f"Exception calling Ollama: {e}")
