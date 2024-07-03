from abc import ABC, abstractmethod
import io
import os
import json
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseUpload, MediaFileUpload

from utils.FileType import FileType

class CustomHandler(ABC):
    def __init__(self, type: FileType):
        self.type = type

    @abstractmethod
    def process(self, file):
        pass

    def save_to_local(self, raw_data, output_data):
        filename = raw_data['filename']
        json_data = json.dumps(output_data, indent=4)

        local_path = os.path.join('./saved_files', f'{filename}.json')
        with open(local_path, 'w') as f:
            f.write(json_data)

        if 'images' in raw_data:
            images_dir = os.path.join('./saved_files', f'{filename}_images')
            os.makedirs(images_dir, exist_ok=True)
            for idx, image in enumerate(raw_data['images'], start=1):
                image_path = os.path.join(images_dir, f'image_{idx}.png')
                image.save(image_path)

        return local_path

    def save_to_cloud(self, raw_data, output_data):
        filename = raw_data['filename']
        json_data = json.dumps(output_data, indent=4)

        SCOPES = ['https://www.googleapis.com/auth/drive']
        SERVICE_ACCOUNT_FILE = 'credentials.json'

        creds = None
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

        drive_service = build('drive', 'v3', credentials=creds)

        file_metadata = {
            'name': f'{filename}.json',
            'mimeType': 'application/json'
        }
        media = io.BytesIO(json_data.encode())
        media_body = MediaIoBaseUpload(media, mimetype='application/json')

        file = drive_service.files().create(body=file_metadata,
                                            media_body=media_body,
                                            fields='id').execute()

        print(f'File ID: {file.get("id")}')

        if 'images' in raw_data:
            images_dir = os.path.join('./saved_files', f'{filename}_images')
            os.makedirs(images_dir, exist_ok=True)
            for idx, image in enumerate(raw_data['images'], start=1):
                image_path = os.path.join(images_dir, f'image_{idx}.png')
                image.save(image_path)

                file_metadata = {
                    'name': f'image_{idx}.png',
                    'parents': [file.get('id')]
                }
                media = MediaFileUpload(image_path, mimetype='image/png')

                drive_service.files().create(body=file_metadata,
                                             media_body=media,
                                             fields='id').execute()

        return file.get('id')
