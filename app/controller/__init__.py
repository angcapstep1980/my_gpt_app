from openai import AzureOpenAI
import os

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

def call_llm(history, t):
    try:
        messages = history.copy()
        # Dici al modello di usare markdown per formattare
        if not messages or messages[0]['role']!= 'system':
            messages.insert(0, {
                'role': 'system',
                'content': 'Sei un assistente utile. Usa markdown per formattare le risposte: **grassetto**, elenchi, ```codice```, tabelle, titoli con #, ecc.'
            })
        response = client.chat.completions.create(
            messages=messages, # history = [{'role':'user', 'content':'...'},...]
            max_tokens=2200,
            temperature=t,
            top_p=1.0,
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT")
            #, response_format={"type": "json_object"} # usalo solo se ti serve che la risposta sia in formato JSON
        )
        # Questo è il testo che ha generato il modello
        return response.choices[0].message.content

    except Exception as e:
        return f"Scusa, c'è stato un errore nel contattare il modello: {e}"