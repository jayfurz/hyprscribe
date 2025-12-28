import ollama

class Assistant:
    def __init__(self, model="llama3"):
        self.model = model

    def chat(self, user_text):
        print(f"Sending to Ollama ({self.model})...")
        try:
            response = ollama.chat(model=self.model, messages=[
                {
                    'role': 'user',
                    'content': user_text,
                },
            ])
            return response['message']['content']
        except Exception as e:
            return f"Error connecting to Ollama: {e}"
