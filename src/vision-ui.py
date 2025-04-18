import base64
import google.generativeai
import io
import os
import streamlit as st
import PIL.Image

from st_img_pastebutton import paste as paste_image


def main():
    # gRPC does not support SOCKS5 proxy, so use REST
    google.generativeai.configure(
        api_key=os.environ.get("GEMINI_API_KEY", ""),
        transport="rest"
    )

    st.title("Gemini Vision UI")

    model_options = [
        "gemini-2.0-flash",
        "gemini-2.0-flash-lite",
        "gemini-2.5-pro-exp-03-25",
        "gemini-2.5-flash-preview-04-17"
    ]

    model_code = st.selectbox("Language Model", model_options, index=0)

    if not model_code:
        model_code = model_options[0]

    gemini_model = google.generativeai.GenerativeModel(model_code)

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
            st.markdown(message["parts"][0])

    # Accept messages from the user
    if prompt := st.chat_input("Please enter a question about the images"):
        st.session_state.messages.append({"role": "user", "parts": [prompt]})
        prompts = []
        images = []
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

                # Large images are resized to 2048x2048
                for image in images:
                    image.thumbnail((2048, 2048))
        else:
            if pasted_image:
                image_binary = base64.b64decode(pasted_image.split(",")[1])
                image = PIL.Image.open(io.BytesIO(image_binary))
                images = [image]

        # Add the first message
        parts = st.session_state.messages[0]["parts"]
        parts.extend(images)
        prompts.append({"role": "user", "parts": parts})

        # Add the second and subsequent messages
        for message in st.session_state.messages[1:]:
            prompts.append(message)

        for response_chunk in gemini_model.generate_content(
            contents=prompts,
            stream=True
        ):
            for response_part in response_chunk.parts:
                response += response_part.text

            message_assiatant.markdown(response + "▌")

        message_assiatant.markdown(response)

        st.session_state.messages.append(
            {"role": "model", "parts": [response]})


if __name__ == "__main__":
    main()
