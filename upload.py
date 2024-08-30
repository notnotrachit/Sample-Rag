
import streamlit as st
from PIL import Image
from app import upload_image, generate_image_description, generate_embeddings, save_embedding


st.write("Upload Image")
uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])


if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    

    if st.button("Process and Store"):
        placeholder = st.empty()
        placeholder.text("Generating description...")
        # placeholder.spinner("Generating Image...")
        with st.status("Uploading Image", expanded=True) as status:
            st.write("Uploading Image to supabase...")
            url = upload_image(image, uploaded_file.name, uploaded_file.type)
            st.write("Generating description...")
            description = generate_image_description(url)
            placeholder.text(f"Description: {description}")
            st.write("Generating embeddings...")
            embedding = generate_embeddings(description)
            st.write("Saving embeddings...")
            save_embedding(uploaded_file.name, embedding, url)
            status.update(
                label="Upload complete!", state="complete", expanded=False
            )
            st.success(f"Image processed and stored. Description: {description}")
