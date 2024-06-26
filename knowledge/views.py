import base64
import os
import secrets
import shutil

from api_services.google_storage_api import GoogleStorageAPI
from constant_variables.configs import DATABASE_URL, BUCKET_NAME, DOC_EXTENSIONS
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from helpers.file_helper import FileHelper
from knowledge.serializers import KnowledgeSerializer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rest_framework.views import APIView
from langchain_openai import OpenAIEmbeddings


class KnowledgeView(APIView):
    def __init__(self):
        self.google_storage = GoogleStorageAPI()
        self.file_helper = FileHelper()
        self.connection_string = DATABASE_URL

    def post(self, request):
        try:
            serializer = KnowledgeSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data

            file = validated_data.get("file")
            file_name = file.name
            _, file_extension = os.path.splitext(file_name)
            file_extension = file_extension.lower()

            if file_extension not in DOC_EXTENSIONS:
                return JsonResponse({"message": "Please upload a txt file"}, status=400)

            url_safe_string = base64.urlsafe_b64encode(secrets.token_bytes(24)).decode(
                "utf-8"
            )
            tmp_storage_path = f"tmp/{url_safe_string}"
            os.makedirs(tmp_storage_path, exist_ok=True)
            file_path = os.path.join(tmp_storage_path, file_name)
            FileSystemStorage(location=tmp_storage_path).save(file_name, file)

            storage_path = f"knowledges/{url_safe_string}/{file_name}"
            knowledge_url = self.google_storage.upload_blob(
                BUCKET_NAME, file_path, storage_path
            )
            openai_api_key = validated_data.get("openai_api_key")
            os.environ["OPENAI_API_KEY"] = openai_api_key
            loader = self.file_helper.get_loader(file_path, file_extension)

            if loader is None:
                return JsonResponse(
                    {"message": f"File extension {file_extension} is not supported"},
                    status=400,
                )

            knowledge = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len,
            )
            docs = text_splitter.split_documents(knowledge)
            embeddings = OpenAIEmbeddings()

            #  TODO: Add embedding

            shutil.rmtree(tmp_storage_path)
        except Exception as e:
            error_message = str(e)
            return JsonResponse({"message": error_message}, status=500)
