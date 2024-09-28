# **Image Retrieval-Augmented Generation (RAG) System with Supabase Vector & Azure OpenAI**

This project demonstrates how to build a **Retrieval-Augmented Generation (RAG)** system using **Supabase Vector** and **Azure OpenAI**. The system allows users to upload images, generate descriptions using Azure OpenAI’s models, and perform searches based on semantic similarity using vector embeddings stored in Supabase.

## **Features**

- **Image Upload**: Users can upload images, which are stored in Supabase Storage.
- **Image Description Generation**: Descriptions are generated for the uploaded images using Azure OpenAI’s GPT models.
- **Vector Embeddings**: The image descriptions are converted into vector embeddings, stored in Supabase Vector, enabling efficient semantic search.
- **Query Functionality**: Users can input queries to search for related images based on their embeddings.

## **Technologies Used**

- **Python**: Core programming language for backend and logic.
- **Streamlit**: Used to build the UI for image upload, query, and display.
- **Supabase Vector**: For vector storage and semantic search.
- **Azure OpenAI**: For generating image descriptions and embeddings.
- **Supabase Storage**: For storing uploaded images.

## **Prerequisites**

- **Python 3.8+**
- **Streamlit**
- **Supabase Account** (with API key and connection string)
- **Azure OpenAI Account** (with API key)

## **Installation**

1. **Clone the Repository**:
    
    ```bash
    git clone https://github.com/notnotrachit/Sample-Rag.git
    cd Sample-Rag
    
    ```
    
2. **Install the Required Packages**:
    
    ```bash
    pip install -r requirements.txt
    
    ```
    
3. **Environment Variables**:
Create a `.env` file in the root directory of your project and add the following variables:
    
    ```bash
    SUPABASE_URL=your_supabase_url
    SUPABASE_KEY=your_supabase_key
    SUPABASE_CONNECTION_STRING=your_supabase_connection_string
    AZURE_OPENAI_API_KEY=your_azure_openai_api_key
    AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
    
    ```
    

## **How to Run**

1. **Run the Streamlit App**:
Run the following command in the terminal:
    
    ```bash
    streamlit run app.py
    
    ```
    
    This will launch the web app where you can upload images, generate descriptions, and search for related images.
    
2. **Upload an Image**:
    - Select an image using the upload button.
    - The system will automatically generate a description for the uploaded image using Azure OpenAI.
3. **Query Images**:
    - Use the search box to input a query.
    - The system will return the most relevant image based on its embeddings.

## **Key Functions**

- `upload_image(image, name, img_type)`: Uploads an image to Supabase Storage and returns its public URL.
- `generate_image_description(url)`: Generates a text description for the image using Azure OpenAI.
- `generate_embeddings(description)`: Converts the image description into vector embeddings using Azure OpenAI.
- `save_embedding(name, embedding, url)`: Saves the embedding to Supabase Vector for later retrieval.
- `query_images(query)`: Searches for the most relevant image in the vector database based on the query.

## **Environment Setup**

### Supabase

- Create a Supabase project and enable **Storage** for storing images.
- Set up **Supabase Vector** (or `vecs`) to store vector embeddings for semantic search.


test
### Azure OpenAI

- Sign up for Azure OpenAI and obtain your API key and endpoint.
- Make sure you’ve deployed the necessary models, like `gpt-4o` and `text-embedding-3-small`.
