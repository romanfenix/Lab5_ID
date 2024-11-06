import os
import json
from firebase_admin import credentials, initialize_app, firestore

# Инициализация Firebase
cred = credentials.Certificate("config/firebase_credentials.json")
initialize_app(cred)
db = firestore.client()

class Job:
    def __init__(self, raw_dir, date, feature):
        self.raw_dir = raw_dir
        self.date = date
        self.feature = feature

    def clean_directory(self):
        """Очистка директории перед записью"""
        if os.path.exists(self.raw_dir):
            for file in os.listdir(self.raw_dir):
                file_path = os.path.join(self.raw_dir, file)
                os.unlink(file_path)

    def fetch_sales_data(self):
        """Извлечение данных о продажах из Firestore по конкретной дате и металлу"""
        print(f"Fetching data for date: {self.date}, feature: {self.feature}")  # Диагностика
        sales_data = db.collection('Lab5').where('Date', '==', self.date).get()  # Изменили имя коллекции

        if not sales_data:
            print(f"No data found for date {self.date}.")  # Диагностика
            return []

        result = []
        for sale in sales_data:
            sale_dict = sale.to_dict()
            print(f"Document fetched: {sale_dict}")  # Печать каждого документа

            # Проверяем наличие металла и добавляем только нужные данные
            if self.feature in sale_dict:
                result.append({"date": sale_dict["Date"], self.feature: sale_dict[self.feature]})
            else:
                print(f"Feature {self.feature} not found in document.")  # Диагностика

        if not result:
            print(f"No data for feature {self.feature} on date {self.date}.")  # Диагностика

        return result  # Proper indentation here

    def save_data(self, sales_data):
        """Сохранение данных в файл JSON"""
        if not sales_data:
            print("No sales data to save.")
            return

        # Очищаем директорию перед записью
        self.clean_directory()

        # Сохраняем данные в файл
        file_name = f"{self.date}.json"
        file_path = os.path.join(self.raw_dir, file_name)

        with open(file_path, 'w') as f:
            json.dump(sales_data, f)

    def run(self):
        """Основной метод для выполнения задачи"""
        sales_data = self.fetch_sales_data()
        self.save_data(sales_data)
