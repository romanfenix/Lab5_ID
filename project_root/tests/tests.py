import unittest
import os
import json
import tempfile
from app.job import Job

class TestJob(unittest.TestCase):
    def setUp(self):
        # Создание временной директории для тестов
        self.raw_dir = tempfile.mkdtemp()
        self.date = "2019-02-12"
        self.feature = "Iridium"
        self.job = Job(self.raw_dir, self.date, self.feature)

    def tearDown(self):
        # Очистка тестовой директории
        for file in os.listdir(self.raw_dir):
            file_path = os.path.join(self.raw_dir, file)
            os.unlink(file_path)
        os.rmdir(self.raw_dir)

    def test_clean_directory(self):
        with open(os.path.join(self.raw_dir, "temp_file.json"), "w") as f:
            f.write("test")
        self.job.clean_directory()
        self.assertEqual(len(os.listdir(self.raw_dir)), 0)  # Проверяем, что директория очищена

    def test_fetch_sales_data(self):
        # Проверка, что метод возвращает список
        sales_data = self.job.fetch_sales_data()
        self.assertIsInstance(sales_data, list)  # Проверяем, что данные в виде списка

    def test_save_data(self):
        sales_data = [{"date": "2024-11-04", "silver": 1000}]
        self.job.save_data(sales_data)
        file_path = os.path.join(self.raw_dir, f"{self.date}.json")
        self.assertTrue(os.path.exists(file_path))  # Проверка, что файл существует
        with open(file_path, 'r') as f:
            data = json.load(f)
            self.assertEqual(data, sales_data)  # Проверка содержимого файла

if __name__ == '__main__':
    unittest.main()
