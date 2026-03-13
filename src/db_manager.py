import psycopg2
from psycopg2.extras import register_uuid
import uuid
import json
from process import Process



class DbManager():
    def __init__(self) -> None:
        self.__conn = None
        try:
            self.__conn = psycopg2.connect(
                dbname="onlab",
                user="postgres",
                password="1234",
                host="localhost",
                port="8020"
            )
            self.__conn.autocommit = True
            self.create_tables()
            print("Connected to postgres")
        except Exception as e:
            print("Error:", e)

    def create_tables(self):
        if self.__conn is None:
            return

        cur = self.__conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                name TEXT NOT NULL
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS processes (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                user_id UUID REFERENCES users(id),
                data JSONB NOT NULL
            )
        """)
        cur.close()

    def create_user(self, name: str):
        if self.__conn is None:
            return None

        user_id = uuid.uuid4()
        register_uuid(user_id)

        cur = self.__conn.cursor()
        cur.execute(
            "INSERT INTO users (id, name) VALUES (%s, %s)",
            (user_id, name,)
        )
        cur.close()

        return user_id

    def get_user_id_by_name(self, name: str):
        if self.__conn is None:
            return None

        cur = self.__conn.cursor()
        cur.execute(
            "SELECT id FROM users WHERE name = %s",
            (name,)
        )
        result = cur.fetchone()
        cur.close()

        return result[0] if result else None

    def create_process(self, user_id, name: str, created: str) -> Process | None:
        if self.__conn is None:
            return None

        pr_id = uuid.uuid4()
        register_uuid(pr_id)

        new_proc = Process(pr_id, name)
        new_proc.created = created
        process_data = Process.serialize(new_proc)

        cur = self.__conn.cursor()
        cur.execute(
            "INSERT INTO processes (id, user_id, data) VALUES (%s, %s, %s)",
            (pr_id, user_id, json.dumps(process_data))
        )
        cur.close()

        return new_proc

    def get_processes(self, user_id) -> list[Process]:
        if self.__conn is None:
            return []

        processes = []

        cur = self.__conn.cursor()
        cur.execute(
            "SELECT id, data FROM processes WHERE user_id = %s",
            (user_id,)
        )
        result = cur.fetchall()
        cur.close()

        for entry in result:
            processes.append(Process.deserialize(entry[0], entry[1]))

        return processes
