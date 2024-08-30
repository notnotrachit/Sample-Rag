import os
from supabase import create_client, Client
from dotenv import load_dotenv
from io import BytesIO 
import os
import requests
import vecs
load_dotenv()



url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

res = supabase.storage.get_bucket("images")
vx = vecs.create_client(os.environ.get("SUPABASE_CONNECTION_STRING"))


# supabase.storage.from_("images").upload(file=b"hello", path="hello.txt")

def upload_image(image, name, img_type):
    # return 'ok'
    temp = BytesIO()

    image.save(temp, format='PNG')
    res = supabase.storage.from_("images").upload(file=temp.getvalue(), path=f"{name}" ,file_options={
        "content-type": img_type
    })
    url = supabase.storage.from_('images').get_public_url(name)
    url = url.replace(" ", "%20")
    return url
    # return image_url


def generate_image_description(url):
    headers = {
        "Content-Type": "application/json",
        "api-key": os.getenv("AZURE_OPENAI_API_KEY"),
    }

    payload = {
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "content": "Generate a description for this image:"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": url
                        }
                    }
                ]
            }
        ],
        "temperature": 0.7,
        "top_p": 0.95,
        "max_tokens": 800
    }

    ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")+"openai/deployments/gpt-4o/chat/completions?api-version=2024-02-15-preview"

    try:
        response = requests.post(ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.RequestException as e:
        raise SystemExit(f"Failed to make the request. Error: {e}")
    # print(response.json()["choices"][0]["message"]["content"])
    return response.json()["choices"][0]["message"]["content"]


def generate_embeddings(description):
    headers = {
        "Content-Type": "application/json",
        "api-key": os.getenv("AZURE_OPENAI_API_KEY"),
    }

    payload = {
        "input": description,
        "model": "text-embedding-3-small"
    }

    ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")+"openai/deployments/text-embedding-3-small/embeddings?api-version=2024-02-15-preview"
    
    try:
        response = requests.post(ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.RequestException as e:
        raise SystemExit(f"Failed to make the request. Error: {e}")
    return response.json()["data"][0]["embedding"]

def save_embedding(name, embedding, url):
    embeddings = vx.get_or_create_collection(name="docs", dimension=1536)
    vectors = [
        (name, embedding, {
            "url": url
        })
    ]
    embeddings.upsert(vectors)


def query_images(query):
    embeddings = generate_embeddings(query)
    docs = vx.get_collection(name="docs")
    results = docs.query(embeddings, limit=1, include_metadata=True)
    print(results[0][1]["url"])
    return results[0][1]["url"]

    # return data


def query_ai(messages, query):
    print(messages)
    print(query)
    headers = {
        "Content-Type": "application/json",
        "api-key": os.getenv("AZURE_OPENAI_API_KEY"),
    }
    messages.append({
        "role": "user",
        "content": query
    })
    payload = {
        "messages": messages,
        "temperature": 0.7,
        "top_p": 0.95,
        "max_tokens": 800
    }
    ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")+"openai/deployments/gpt-4o/chat/completions?api-version=2024-02-15-preview"

    try:
        response = requests.post(ENDPOINT, headers=headers, json=payload)
        print(response.json())
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.RequestException as e:
        raise SystemExit(f"Failed to make the request. Error: {e}")
    return response.json()["choices"][0]["message"]["content"]