import streamlit as st
from PIL import Image
import io
from utils.FileType import FileType
from factory.HandlerFactory import HandlerFactory
def main():
    st.title("File Processing App")

    uploaded_file = st.file_uploader("Choose a file", type=["png", "jpg", "jpeg", "pdf", "docx"])

    if uploaded_file is not None:
        file_type = uploaded_file.type
        if file_type in ["image/png", "image/jpeg"]:
            handler = HandlerFactory.create_handler(FileType.IMAGE)
            if uploaded_file is not None:
                image = Image.open(uploaded_file)
                st.image(image, caption='Uploaded Image', use_column_width=True)
        elif file_type == "application/pdf":
            handler = HandlerFactory.create_handler(FileType.PDF)
        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            handler = HandlerFactory.create_handler(FileType.DOCX)
        else:
            st.error("Unsupported file type")
            return

        result = handler.process(uploaded_file)

        # Xử lý result ở đây

        save_option = st.radio("Save output to:", ("Local", "Google Drive"))

        if st.button("Save"):
            if save_option == "Local":
                st.success("Saved to local successfully.")
            elif save_option == "Google Drive":
                st.success("Saved to Google Drive successfully.")

if __name__ == "__main__":
    main()
