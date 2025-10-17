from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QTextEdit, QVBoxLayout,QMessageBox,
    QWidget, QLabel, QHBoxLayout, QTableWidget, QTableWidgetItem
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from api.openai_api import get_image_description
from utils.file_handler import get_image_files, encode_image_to_base64
from utils.config import DB_PATH

import sqlite3
import time
import json
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OpenAI 이미지 설명 프로그램")
        self.setGeometry(100, 100, 700, 500)
        self.image_path = []
        self.init_ui()
        self.init_db()

    def init_ui(self):
        self.image_label = QLabel("이미지를 불러오세요")
        self.image_label.setFixedSize(300, 300)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 1px solid black;")

        self.load_button = QPushButton("이미지 열기")
        self.load_button.clicked.connect(self.load_image)

        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("GPT에게 보낼 추가 프롬프트 입력")

        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)

        self.generate_button = QPushButton("GPT 설명 생성")
        self.generate_button.clicked.connect(self.generate_description)

        top_layout = QHBoxLayout()
        top_layout.addWidget(self.image_label)
        top_layout.addWidget(self.load_button)

        layout = QVBoxLayout()
        layout.addLayout(top_layout)
        layout.addWidget(self.text_input)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.result_output)
        # layout = QVBoxLayout() 안쪽에 추가
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(5)  # DB 컬럼 수 (file_name, sign_lang, sign_text, day_night, confidence)
        self.result_table.setHorizontalHeaderLabels([
            "File Name", 
            "Sign Lang", 
            "Sign Text", 
            "Day/Night", 
            "Confidence"
        ])
        layout.addWidget(self.result_table)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.result_table.setEditTriggers(QTableWidget.AllEditTriggers)
        self.result_table.cellChanged.connect(self.update_db_from_table)

    def init_db(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS signlens_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prompt TEXT,
                response TEXT,       
                image TEXT,
                file_name TEXT,
                sign_lang TEXT,
                sign_text TEXT,
                day_night TEXT,
                processing_time REAL,
                confidence TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def load_image(self):
        try:
            paths = get_image_files()
            if paths:
                first_image = paths[0]
                pixmap = QPixmap(first_image).scaled(self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio)
                if pixmap.isNull():
                    raise ValueError("이미지를 불러올 수 없습니다.")
                self.image_label.setPixmap(pixmap)
                self.image_paths = paths
        except Exception as e:
            QMessageBox.warning(self, "오류", f"이미지 불러오기 실패: {e}")

    def generate_description(self):
        if not self.image_paths:
            self.result_output.setPlainText("이미지를 먼저 불러와 주세요.")
            return

        start_time = time.time()
        prompt = self.text_input.toPlainText()

        if not prompt.strip():
            prompt = '''
                이미지를 확인하고 정보를 추출해주세요.
                이미지는 간판 이미지입니다
                간판에 적힌 상호명, 상호명이 사용된 언어의 종류를 찾으세요
                촬영 시간이 낮인지 밤인지 확인하세요
                정보 확인이 확실한지에 따라서 신뢰도를 평가(확실=1/애매=-1/불확실=0)하고 답변해주세요.
                다음 정보는 JSON으로 답변하고, 누락 없이 반드시 답변하세요
                {
                    "상호명": "...",
                    "언어": "...",
                    "촬영시간": "...",
                    "신뢰도": ...
                }

                '''
        for image_path in self.image_paths:
            result_json_str = get_image_description(image_path, prompt)
            base64_image = encode_image_to_base64(image_path)
            self.load_latest_entries_to_table()
            # 기존 JSON 파싱 및 DB 저장 코드 반복

        # 1차 JSON 파싱
        try:
            result_json = json.loads(result_json_str)
        except json.JSONDecodeError:
            result_json = {"raw": result_json_str}

        # 2차 파싱: raw 안에 실제 정보가 들어있음
        raw_content = result_json.get("raw", "")
        try:
            # ```json``` 태그 제거
            raw_content = raw_content.replace("```json", "").replace("```", "").strip()
            extracted_json = json.loads(raw_content)
        except json.JSONDecodeError:
            extracted_json = {}

        # DB에 저장할 정보 추출
        sign_text = extracted_json.get("상호명", "")
        sign_lang = extracted_json.get("언어", "")
        day_night = extracted_json.get("촬영시간", "")
        confidence = extracted_json.get("신뢰도", 0)  # 확실=1, 애매=-1, 불확실=0

        # DB 저장
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            with open(image_path, "rb") as f:
                image_blob = f.read()
                cursor.execute('''
                    INSERT INTO signlens_logs (
                        prompt, response, image, file_name,
                        sign_lang, sign_text, day_night, processing_time, confidence
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    prompt,
                    str(result_json),  # 원본 GPT 응답
                    image_blob,
                    os.path.basename(image_path),
                    sign_lang,
                    sign_text,
                    day_night,
                    time.time() - start_time,
                    confidence
                ))
            conn.commit()

                # DB 저장 후
        conn.commit()
        row_count = self.result_table.rowCount()
        self.result_table.insertRow(row_count)
        self.load_latest_entries_to_table(5)

    def load_latest_entries_to_table(self, num_rows=5):
        # 최근 처리한 한 행만 가져오기
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
                SELECT file_name, sign_lang, sign_text, day_night, confidence
                FROM signlens_logs
                ORDER BY id DESC
                LIMIT {num_rows}
            ''')
            rows = cursor.fetchall()

        self.result_table.setRowCount(len(rows))
        for row_idx, row in enumerate(rows):
            for col_idx, value in enumerate(row):
                if col_idx == 0:  # 파일 이름만
                    display_value = os.path.basename(str(value))
                else:
                    display_value = str(value)
                self.result_table.setItem(row_idx, col_idx, QTableWidgetItem(display_value))
    
    def update_db_from_table(self, row, column):
        """
        사용자가 테이블에서 값을 수정하면 DB에 반영
        """
        if row < 0:
            return

        # DB 컬럼 매핑 (테이블 열 순서와 맞춰서)
        db_columns = ["file_name", "sign_lang", "sign_text", "day_night", "confidence"]

        col_name = db_columns[column]
        new_value = self.result_table.item(row, column).text()

        # file_name으로 해당 row를 찾아 업데이트
        file_name_item = self.result_table.item(row, 0)
        if not file_name_item:
            return
        file_name = file_name_item.text()

        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
                UPDATE signlens_logs
                SET {col_name} = ?
                WHERE file_name LIKE ?
            ''', (new_value, f"%{file_name}"))  # 경로 포함될 수 있으니 LIKE 사용
            conn.commit()


    def process_images_in_batches(self, image_paths, batch_size=10, sub_batch_size=5):
        """
        image_paths: 처리할 이미지 전체 리스트
        batch_size: 한 번에 처리할 묶음 개수
        sub_batch_size: batch 안에서 나누어 API 호출
        """
        total = len(image_paths)
        for i in range(0, total, batch_size):
            batch = image_paths[i:i+batch_size]
            # batch 내에서 sub_batch 처리
            for j in range(0, len(batch), sub_batch_size):
                sub_batch = batch[j:j+sub_batch_size]
                for img_path in sub_batch:
                    self.process_single_image(img_path)  # 기존 generate_description 기능과 동일


    def process_single_image(self, img_path):
        self.image_path = [img_path]
        self.generate_description()  # 기존 기능 재사용