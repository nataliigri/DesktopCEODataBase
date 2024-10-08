import unittest
from database import Database, Field, Record

class TestDatabaseFunctions(unittest.TestCase):
    def setUp(self):
        self.db = Database("test_db")
        self.db.create_table("users")
        self.db.create_table("orders")

        self.db.add_field_to_table("users", Field("id", "integer"))
        self.db.add_field_to_table("users", Field("name", "string"))
        self.db.add_field_to_table("orders", Field("id", "integer"))
        self.db.add_field_to_table("orders", Field("item", "string"))

        self.db.add_record_to_table("users", {"id": 1, "name": "Nata"})
        self.db.add_record_to_table("orders", {"id": 1, "item": "iPhone"})

    def test_add_record(self):
        self.db.add_record_to_table("users", {"id": 2, "name": "John"})
        records = self.db.view_table("users")["records"]
        self.assertEqual(len(records), 2)

    def test_invalid_field(self):
        with self.assertRaises(Exception):
            self.db.add_record_to_table("users", {"invalid_field": "test"})

    def test_join_tables(self):
        joined_data = self.db.join_tables("users", "orders", "id")
        self.assertEqual(len(joined_data), 1)

if __name__ == '__main__':
    unittest.main()
