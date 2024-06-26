import chardet

from langchain_community.document_loaders.text import TextLoader


class FileHelper:
    def __init__(self) -> None:
        pass

    @staticmethod
    def detect_encoding(file_path):
        with open(file_path, "rb") as file:
            raw_data = file.read(10000)
            result = chardet.detect(raw_data)
            return result["encoding"]

    def get_loader(self, file_path, file_extension):
        loader = None

        if file_extension == ".txt":
            encoding = self.detect_encoding(file_path)
            loader = TextLoader(file_path, encoding=encoding)

        return loader
