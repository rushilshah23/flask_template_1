from src import create_app
from src.utils.database import DBAdapter

class TestApp:
    __instance = None

    @staticmethod
    def get_instance():
        if TestApp.__instance is None:
            TestApp()
        return TestApp.__instance


    @staticmethod
    def destruct_instance():
        if TestApp.__instance is not None:
            TestApp.__instance.test_db.delete_db()
            TestApp.__instance = None
            print("Database deleted ...\nTesting finished")



    def __init__(self):
        if TestApp.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.app = create_app(env_mode="testing")
            with self.app.app_context():
                self.test_db = DBAdapter(db_name=self.app.config.get("DB_URL"))
                self.test_db.init_db()
                self.test_db.create_user("admin","admin@gmail.com","123456")


            self.client = self.app.test_client()
            TestApp.__instance = self


    
# Usage:
# test_app = TestApp.get_instance()
# app = test_app.app
# client = test_app.client
