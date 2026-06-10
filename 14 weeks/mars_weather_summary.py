import csv
import os
import struct
import zlib
from datetime import datetime
from dotenv import load_dotenv

import mysql.connector

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', '3306')),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
}

CSV_FILE_NAME = 'mars_weathers_data.CSV'
PNG_FILE_NAME = 'mars_weather_summary.png'
TABLE_NAME = 'mars_weather'


class MySQLHelper:
    def __init__(self, config):
        self.config = config
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = mysql.connector.connect(**self.config)
        self.cursor = self.connection.cursor(dictionary=True)

    def execute(self, query, params=None):
        if params is None:
            params = ()
        self.cursor.execute(query, params)
        self.connection.commit()

    def executemany(self, query, params_list):
        self.cursor.executemany(query, params_list)
        self.connection.commit()

    def fetch_one(self, query, params=None):
        if params is None:
            params = ()
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def fetch_all(self, query, params=None):
        if params is None:
            params = ()
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self):
        if self.cursor is not None:
            self.cursor.close()

        if self.connection is not None:
            self.connection.close()


def create_table(db):
    query = f'''
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            weather_id INT PRIMARY KEY AUTO_INCREMENT,
            mars_date DATETIME NOT NULL,
            temp INT,
            storm INT
        )
    '''
    db.execute(query)


def reset_table(db):
    db.execute(f'DELETE FROM {TABLE_NAME}')
    db.execute(f'ALTER TABLE {TABLE_NAME} AUTO_INCREMENT = 1')


def parse_mars_date(date_text):
    date_text = date_text.strip()

    try:
        return datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        return datetime.strptime(date_text, '%Y-%m-%d %H:%M:%S')


def read_csv_data(csv_path):
    rows = []

    with open(csv_path, 'r', encoding='utf-8-sig', newline='') as file:
        reader = csv.DictReader(file)

        for item in reader:
            mars_date = parse_mars_date(item['mars_date'])

            temp = int(round(float(item['temp'])))

            if 'storm' in item:
                storm = int(item['storm'])
            else:
                storm = int(item['stom'])

            rows.append((mars_date, temp, storm))

    return rows


def insert_weather_data(db, rows):
    query = f'''
        INSERT INTO {TABLE_NAME} (mars_date, temp, storm)
        VALUES (%s, %s, %s)
    '''
    db.executemany(query, rows)


def get_summary(db):
    query = f'''
        SELECT
            COUNT(*) AS total_count,
            MIN(mars_date) AS first_date,
            MAX(mars_date) AS last_date,
            ROUND(AVG(temp), 2) AS avg_temp,
            MIN(temp) AS min_temp,
            MAX(temp) AS max_temp,
            ROUND(AVG(storm), 2) AS avg_storm,
            MIN(storm) AS min_storm,
            MAX(storm) AS max_storm
        FROM {TABLE_NAME}
    '''
    return db.fetch_one(query)


def get_chart_data(db):
    query = f'''
        SELECT mars_date, temp, storm
        FROM {TABLE_NAME}
        ORDER BY mars_date ASC
    '''
    return db.fetch_all(query)


def png_pack(tag, data):
    chunk = tag + data
    return (
        struct.pack('!I', len(data))
        + chunk
        + struct.pack('!I', zlib.crc32(chunk) & 0xffffffff)
    )


def save_png(path, width, height, pixels):
    raw_data = bytearray()

    for y in range(height):
        raw_data.append(0)

        for x in range(width):
            raw_data.extend(pixels[y][x])

    png_data = b'\x89PNG\r\n\x1a\n'
    png_data += png_pack(b'IHDR', struct.pack('!IIBBBBB', width, height, 8, 2, 0, 0, 0))
    png_data += png_pack(b'IDAT', zlib.compress(bytes(raw_data), 9))
    png_data += png_pack(b'IEND', b'')

    with open(path, 'wb') as file:
        file.write(png_data)


def create_canvas(width, height, color):
    return [[color for _ in range(width)] for _ in range(height)]


def set_pixel(pixels, x, y, color):
    height = len(pixels)
    width = len(pixels[0])

    if 0 <= x < width and 0 <= y < height:
        pixels[y][x] = color


def draw_line(pixels, x1, y1, x2, y2, color):
    dx = abs(x2 - x1)
    dy = -abs(y2 - y1)

    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1

    error = dx + dy

    while True:
        set_pixel(pixels, x1, y1, color)

        if x1 == x2 and y1 == y2:
            break

        e2 = 2 * error

        if e2 >= dy:
            error += dy
            x1 += sx

        if e2 <= dx:
            error += dx
            y1 += sy


def draw_rect(pixels, x1, y1, x2, y2, color):
    for y in range(y1, y2 + 1):
        for x in range(x1, x2 + 1):
            set_pixel(pixels, x, y, color)


FONT = {
    'A': ['01110', '10001', '10001', '11111', '10001', '10001', '10001'],
    'C': ['01111', '10000', '10000', '10000', '10000', '10000', '01111'],
    'D': ['11110', '10001', '10001', '10001', '10001', '10001', '11110'],
    'E': ['11111', '10000', '10000', '11110', '10000', '10000', '11111'],
    'G': ['01111', '10000', '10000', '10111', '10001', '10001', '01111'],
    'H': ['10001', '10001', '10001', '11111', '10001', '10001', '10001'],
    'I': ['11111', '00100', '00100', '00100', '00100', '00100', '11111'],
    'L': ['10000', '10000', '10000', '10000', '10000', '10000', '11111'],
    'M': ['10001', '11011', '10101', '10101', '10001', '10001', '10001'],
    'N': ['10001', '11001', '10101', '10011', '10001', '10001', '10001'],
    'O': ['01110', '10001', '10001', '10001', '10001', '10001', '01110'],
    'P': ['11110', '10001', '10001', '11110', '10000', '10000', '10000'],
    'R': ['11110', '10001', '10001', '11110', '10100', '10010', '10001'],
    'S': ['01111', '10000', '10000', '01110', '00001', '00001', '11110'],
    'T': ['11111', '00100', '00100', '00100', '00100', '00100', '00100'],
    'U': ['10001', '10001', '10001', '10001', '10001', '10001', '01110'],
    'V': ['10001', '10001', '10001', '10001', '10001', '01010', '00100'],
    'W': ['10001', '10001', '10001', '10101', '10101', '11011', '10001'],
    'Y': ['10001', '10001', '01010', '00100', '00100', '00100', '00100'],
    '0': ['01110', '10001', '10011', '10101', '11001', '10001', '01110'],
    '1': ['00100', '01100', '00100', '00100', '00100', '00100', '01110'],
    '2': ['01110', '10001', '00001', '00010', '00100', '01000', '11111'],
    '3': ['11110', '00001', '00001', '01110', '00001', '00001', '11110'],
    '4': ['00010', '00110', '01010', '10010', '11111', '00010', '00010'],
    '5': ['11111', '10000', '10000', '11110', '00001', '00001', '11110'],
    '6': ['01111', '10000', '10000', '11110', '10001', '10001', '01110'],
    '7': ['11111', '00001', '00010', '00100', '01000', '01000', '01000'],
    '8': ['01110', '10001', '10001', '01110', '10001', '10001', '01110'],
    '9': ['01110', '10001', '10001', '01111', '00001', '00001', '11110'],
    '.': ['00000', '00000', '00000', '00000', '00000', '01100', '01100'],
    '-': ['00000', '00000', '00000', '11111', '00000', '00000', '00000'],
    ':': ['00000', '01100', '01100', '00000', '01100', '01100', '00000'],
    ' ': ['00000', '00000', '00000', '00000', '00000', '00000', '00000'],
}


def draw_text(pixels, x, y, text, color, scale=2):
    current_x = x

    for char in text.upper():
        pattern = FONT.get(char, FONT[' '])

        for row_index, row in enumerate(pattern):
            for col_index, value in enumerate(row):
                if value == '1':
                    draw_rect(
                        pixels,
                        current_x + col_index * scale,
                        y + row_index * scale,
                        current_x + col_index * scale + scale - 1,
                        y + row_index * scale + scale - 1,
                        color
                    )

        current_x += 6 * scale


def normalize(value, min_value, max_value, top, bottom):
    if max_value == min_value:
        return (top + bottom) // 2

    ratio = (value - min_value) / (max_value - min_value)
    return int(bottom - ratio * (bottom - top))


def create_summary_png(summary, chart_rows, output_path):
    width = 1000
    height = 620

    white = (255, 255, 255)
    black = (30, 30, 30)
    gray = (210, 210, 210)
    dark_gray = (90, 90, 90)
    temp_color = (220, 80, 80)
    storm_color = (70, 110, 220)

    pixels = create_canvas(width, height, white)

    draw_text(pixels, 40, 30, 'MARS WEATHER SUMMARY', black, scale=3)

    total_count = summary['total_count']
    avg_temp = summary['avg_temp']
    min_temp = summary['min_temp']
    max_temp = summary['max_temp']
    avg_storm = summary['avg_storm']
    min_storm = summary['min_storm']
    max_storm = summary['max_storm']

    first_date = str(summary['first_date'])[:10]
    last_date = str(summary['last_date'])[:10]

    draw_text(pixels, 45, 95, f'COUNT: {total_count}', black, scale=2)
    draw_text(pixels, 45, 125, f'DATE: {first_date} - {last_date}', black, scale=2)
    draw_text(pixels, 45, 155, f'TEMP AVG: {avg_temp} MIN: {min_temp} MAX: {max_temp}', black, scale=2)
    draw_text(pixels, 45, 185, f'STORM AVG: {avg_storm} MIN: {min_storm} MAX: {max_storm}', black, scale=2)

    chart_left = 80
    chart_right = 940
    chart_top = 260
    chart_bottom = 560

    draw_line(pixels, chart_left, chart_top, chart_left, chart_bottom, black)
    draw_line(pixels, chart_left, chart_bottom, chart_right, chart_bottom, black)

    for i in range(6):
        y = chart_top + i * 60
        draw_line(pixels, chart_left, y, chart_right, y, gray)

    temps = [row['temp'] for row in chart_rows]
    storms = [row['storm'] for row in chart_rows]

    temp_min = min(temps)
    temp_max = max(temps)
    storm_min = min(storms)
    storm_max = max(storms)

    row_count = len(chart_rows)

    temp_points = []
    storm_points = []

    for index, row in enumerate(chart_rows):
        x = chart_left + int(index * (chart_right - chart_left) / max(row_count - 1, 1))

        temp_y = normalize(row['temp'], temp_min, temp_max, chart_top, chart_bottom)
        storm_y = normalize(row['storm'], storm_min, storm_max, chart_top, chart_bottom)

        temp_points.append((x, temp_y))
        storm_points.append((x, storm_y))

    for index in range(len(temp_points) - 1):
        x1, y1 = temp_points[index]
        x2, y2 = temp_points[index + 1]
        draw_line(pixels, x1, y1, x2, y2, temp_color)

    for index in range(len(storm_points) - 1):
        x1, y1 = storm_points[index]
        x2, y2 = storm_points[index + 1]
        draw_line(pixels, x1, y1, x2, y2, storm_color)

    draw_rect(pixels, 80, 585, 110, 600, temp_color)
    draw_text(pixels, 120, 584, 'TEMP', dark_gray, scale=2)

    draw_rect(pixels, 230, 585, 260, 600, storm_color)
    draw_text(pixels, 270, 584, 'STORM', dark_gray, scale=2)

    save_png(output_path, width, height, pixels)


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, CSV_FILE_NAME)
    png_path = os.path.join(base_dir, PNG_FILE_NAME)

    if not os.path.exists(csv_path):
        print(f'CSV 파일을 찾을 수 없습니다: {csv_path}')
        return

    db = MySQLHelper(DB_CONFIG)

    try:
        db.connect()

        create_table(db)
        reset_table(db)

        rows = read_csv_data(csv_path)
        insert_weather_data(db, rows)

        summary = get_summary(db)
        chart_rows = get_chart_data(db)

        create_summary_png(summary, chart_rows, png_path)

        print('작업이 완료되었습니다.')
        print(f'삽입된 데이터 수: {summary["total_count"]}')
        print(f'요약 이미지 파일: {png_path}')

    finally:
        db.close()


if __name__ == '__main__':
    main()