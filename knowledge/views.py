import base64
import os
import secrets
import shutil

from api_services.google_storage_api import GoogleStorageAPI
from constant_variables.configs import (
    BUCKET_NAME,
    DATABASE_URL,
    DOC_EXTENSIONS,
    OPENAI_BASE_URL,
    OPENAI_EMBEDDINGS_MODEL,
)
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from helpers.file_helper import FileHelper
from helpers.google_api_helper import GoogleApiHelper
from knowledge.models import Knowledge
from knowledge.serializers import KnowledgeCreateSerializer, KnowledgeDeleteSerializer
from langchain_community.vectorstores.pgvector import PGVector
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rest_framework.views import APIView
from vector_db.models import Collection


class KnowledgeView(APIView):
    def __init__(self):
        self.google_storage = GoogleStorageAPI()
        self.file_helper = FileHelper()
        self.google_api_helper = GoogleApiHelper()
        self.connection_string = DATABASE_URL

    def post(self, request):
        try:
            serializer = KnowledgeCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data
            file = validated_data.get("file")

            file_name = file.name
            _, file_extension = os.path.splitext(file_name)
            file_extension = file_extension.lower()

            if file_extension not in DOC_EXTENSIONS:
                return JsonResponse({"message": "Please upload a txt file"}, status=400)

            safe_string = base64.urlsafe_b64encode(secrets.token_bytes(24)).decode(
                "utf-8"
            )
            tmp_storage_path = f"tmp/{safe_string}"

            os.makedirs(tmp_storage_path, exist_ok=True)
            file_path = os.path.join(tmp_storage_path, file_name)
            FileSystemStorage(location=tmp_storage_path).save(file_name, file)

            storage_path = f"knowledges/{safe_string}_{file_name}"
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
            embeddings = OpenAIEmbeddings(
                check_embedding_ctx_length=False,
                base_url=OPENAI_BASE_URL,
                model=OPENAI_EMBEDDINGS_MODEL,
            )
            collection_name = f"langchain_{safe_string}"

            PGVector.from_documents(
                embedding=embeddings,
                documents=docs,
                collection_name=collection_name,
                connection_string=self.connection_string,
                use_jsonb=True,
            )

            collection_id = Collection.objects.get(name=collection_name).uuid

            Knowledge.objects.create(
                url=knowledge_url,
                collection_id=collection_id,
            )
            shutil.rmtree(tmp_storage_path)

            return JsonResponse({"message": "Successfully created embeddings"})
        except Exception as e:
            shutil.rmtree(tmp_storage_path)
            error_message = str(e)
            return JsonResponse({"message": error_message}, status=500)

    def delete(self, request):
        try:
            serializer = KnowledgeDeleteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data

            url = validated_data.get("url")

            openai_api_key = validated_data.get("openai_api_key")
            os.environ["OPENAI_API_KEY"] = openai_api_key

            collection_id = Knowledge.objects.get(url=url).collection_id
            collection_name = Collection.objects.get(uuid=collection_id).name

            embeddings = OpenAIEmbeddings()

            store = PGVector(
                connection_string=self.connection_string,
                collection_name=collection_name,
                embedding_function=embeddings,
                use_jsonb=True,
            )
            store.delete_collection()

            Knowledge.objects.filter(url=url).delete()

            blob_name = self.google_api_helper.get_blob_name(url)
            self.google_storage.delete_blob(BUCKET_NAME, blob_name)

            return JsonResponse({"message": "Successfully deleted"})
        except Exception as e:
            error_message = str(e)
            return JsonResponse({"message": error_message}, status=500)
