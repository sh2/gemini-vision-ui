import base64
import io
import json
import os
import PIL.Image
import streamlit as st
from google import genai
from google.genai.types import Content, Part
from st_img_pastebutton import paste as paste_image


def main():
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", ""))

    st.set_page_config(page_title="Gemini Vision UI")
    st.title("Gemini Vision UI")

    model_options = [
        "gemini-2.5-pro",
        "gemini-2.5-flash"
    ]

    model_id = st.selectbox("Language model", model_options, index=1)

    if not model_id:
        model_id = model_options[1]

    upload_method = st.radio("Select upload method", [
                             "Upload image files", "Paste from Clipboard"])

    if upload_method == "Upload image files":
        files = st.file_uploader(
            "Please upload image files", accept_multiple_files=True, type=["jpeg", "jpg", "png"])

        if files:
            # Display image files in two columns
            columns = st.columns(2)
            column_index = 0

            for file in files:
                columns[column_index].image(file)
                column_index = (column_index + 1) % 2
    else:
        pasted_image = paste_image("Paste from Clipboard")

        if pasted_image:
            st.image(pasted_image)

    clear = st.button("Clear Chat History")

    if clear or "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        role = "assistant" if message["role"] == "model" else message["role"]
        with st.chat_message(role):
            st.markdown(message["parts"])

    # Accept messages from the user
    if prompt := st.chat_input("Please enter a question about the images"):
        st.session_state.messages.append({"role": "user", "parts": prompt})
        images = []
        contents = []
        response = ""

        # Display user's message
        with st.chat_message("user"):
            st.markdown(prompt)

        # For the assistant, display an empty message and update it later
        with st.chat_message("assistant"):
            message_assiatant = st.empty()

        # Prepare image files
        if upload_method == "Upload image files":
            if files:
                images = [PIL.Image.open(file) for file in files]
        else:
            if pasted_image:
                image_binary = base64.b64decode(pasted_image.split(",")[1])
                image = PIL.Image.open(io.BytesIO(image_binary))
                images = [image]

        # Large images are resized to 2048x2048
        for image in images:
            image.thumbnail((2048, 2048))

        # Add the first message
        parts = []

        for image in images:
            img_byte_arr = io.BytesIO()
            image.convert("RGB").save(img_byte_arr, format='JPEG')
            img_byte_arr = img_byte_arr.getvalue()

            parts.append(
                Part.from_bytes(
                    data=img_byte_arr,
                    mime_type="image/jpeg"
                )
            )

        parts.append(Part.from_text(
            text=st.session_state.messages[0]["parts"]))

        contents.append(Content(role="user", parts=parts))

        # Add the second and subsequent messages
        for message in st.session_state.messages[1:]:
            contents.append(
                Content(role=message["role"], parts=[Part.from_text(text=message["parts"])]))

        for response_chunk in client.models.generate_content_stream(
            model=model_id,
            contents=contents,
        ):
            last_chunk = response_chunk

            if response_chunk.text:
                response += response_chunk.text
                message_assiatant.markdown(response + "▌")

        message_assiatant.markdown(response)

        st.session_state.messages.append(
            {"role": "model", "parts": response})

        print(json.dumps(last_chunk.model_dump(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
