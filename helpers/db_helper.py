from django.db import connections


class DBHelper:
    def __init__(self) -> None:
        pass

    def have_embeddings(self):
        with connections["default"].cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM knowledge")
            row = cursor.fetchone()
        return row[0] > 0 if row else False
