from flask import Flask, request, jsonify
import os
import json
from job import Job

app = Flask(__name__)

@app.route('/fetch-data', methods=['POST'])
def fetch_data():
    data = request.get_json()
    date = data.get("date")
    feature = data.get("feature")

    if not date or not feature:
        return jsonify({"error": "Invalid data format"}), 400

    # Определяем директорию для хранения данных
    raw_dir = os.path.join(os.getcwd(), "path", "to", "my_dir", "raw", feature)
    os.makedirs(raw_dir, exist_ok=True)

    # Создаем экземпляр Job и запускаем его
    job = Job(raw_dir=raw_dir, date=date, feature=feature)
    job.run()

    return jsonify({"status": "Data fetched successfully"}), 200

@app.route('/view-data', methods=['GET'])
def view_data():
    feature = request.args.get('feature')
    date = request.args.get('date')

    # Проверка наличия параметров
    if not feature or not date:
        return jsonify({"error": "Feature and date parameters are required"}), 400

    # Строим путь к данным для данного металла
    raw_dir = os.path.join(os.getcwd(), "path", "to", "my_dir", "raw", feature)
    print(f"Checking directory: {raw_dir}")  # Диагностика пути

    # Проверяем, существует ли директория для металла
    if not os.path.exists(raw_dir):
        return jsonify({"error": "Feature directory not found"}), 404

    # Ищем файл по дате
    file_name = f"{date}.json"
    file_path = os.path.join(raw_dir, file_name)

    if not os.path.exists(file_path):
        return jsonify({"error": f"Data not found for the feature '{feature}' and date '{date}'"}), 404

    # Чтение данных из файла
    with open(file_path, 'r') as f:
        data = json.load(f)

    return jsonify({"data": data}), 200




if __name__ == '__main__':
    app.run(port=8081)

