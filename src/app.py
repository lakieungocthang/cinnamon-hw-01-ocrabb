import streamlit as st
from PIL import Image
from utils.FileType import FileType
from factory.HandlerFactory import HandlerFactory
from package.CustomHandler import CustomHandler

def main():
    st.title("File Processing App")

    uploaded_file = st.file_uploader("Choose a file", type=["png", "jpg", "jpeg", "pdf", "docx"])

    if uploaded_file is not None:
        file_type = uploaded_file.type
        handler = None

        # Determine the handler based on file type
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

        if handler is not None:
            result = handler.process(uploaded_file)

            # Save options
            save_option = st.radio("Save output to:", ("Local", "Google Drive"))

            if st.button("Save"):
                if save_option == "Local":
                    local_path = CustomHandler(handler.type).save_to_local(uploaded_file, result)
                    st.success(f"Saved to local successfully. File path: {local_path}")
                elif save_option == "Google Drive":
                    file_id = CustomHandler(handler.type).save_to_cloud(uploaded_file, result)
                    st.success(f"Saved to Google Drive successfully. File ID: {file_id}")

if __name__ == "__main__":
    main()
