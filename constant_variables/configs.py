from decouple import config

BUCKET_NAME = config("BUCKET_NAME")
DATABASE_URL = config("DATABASE_URL")
CONTEXTUALIZE_Q_SYSTEM_PROMPT = """Given a chat history and the latest user question which might reference context in the chat history, formulate a standalone question which can be understood without the chat history. Do NOT answer the question, just reformulate it if needed and otherwise return it as is."""
DEFAULT_SYSTEM_PROMPT = """You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature. If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information."""
DOC_EXTENSIONS = [".txt"]
KEY_FILE_LOCATION = config("KEY_FILE_LOCATION")
OPENAI_BASE_URL = config("OPENAI_BASE_URL")
OPENAI_EMBEDDINGS_MODEL = config("OPENAI_EMBEDDINGS_MODEL")
OPENAI_CHAT_MODEL = config("OPENAI_CHAT_MODEL")
