import PIL.Image
import google.generativeai
import os
import streamlit as st


def main():
    # gRPC does not support SOCKS5 proxy, so use REST
    google.generativeai.configure(
        api_key=os.environ.get("GEMINI_API_KEY", ""),
        transport="rest"
    )

    gemini_model = google.generativeai.GenerativeModel(
        os.environ.get("GEMINI_MODEL") or "gemini-1.5-flash"
    )

    st.title("Gemini Vision UI")
    files = st.file_uploader(
        "Please upload image files", accept_multiple_files=True, type=["jpeg", "jpg", "png"])

    if files:
        # Display image files in two columns
        columns = st.columns(2)
        column_index = 0

        for file in files:
            columns[column_index].image(file)
            column_index = (column_index + 1) % 2

    # Accept messages from the user
    if prompt := st.chat_input("Please enter a question about the images"):
        response = "Please upload image files."

        # Display user's message
        with st.chat_message("user"):
            st.markdown(prompt)

        # For the assistant, display an empty message and update it later
        with st.chat_message("assistant"):
            message_assiatant = st.empty()

        if files:
            images = [PIL.Image.open(file) for file in files]

            # Large images are resized to 2048x2048
            for image in images:
                image.thumbnail((2048, 2048))

            prompts = []
            prompts.append(prompt)
            prompts.extend(images)
            response = ""

            for response_chunk in gemini_model.generate_content(
                contents=prompts,
                stream=True
            ):
                for response_part in response_chunk.parts:
                    response += response_part.text

                message_assiatant.markdown(response + "▌")

        message_assiatant.markdown(response)


if __name__ == "__main__":
    main()
