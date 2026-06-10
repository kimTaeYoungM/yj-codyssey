# Mars Weather Summary 과제 수행 전체 과정 정리

이 문서는 `mars_weathers_data.CSV` 파일을 Python으로 읽어서 MySQL DB에 저장하고, 요약 결과 이미지를 생성한 뒤, GitHub에 안전하게 업로드하기까지의 전체 과정을 정리한 문서입니다.

---

## 1. 과제 목표

이번 과제의 목표는 다음과 같습니다.

1. MySQL에 `mars_db` 데이터베이스를 생성합니다.
2. `mars_weather` 테이블을 생성합니다.
3. Python으로 `mars_weathers_data.CSV` 파일을 읽습니다.
4. CSV 데이터를 MySQL 테이블에 삽입합니다.
5. DB에 저장된 데이터를 조회하여 요약 통계를 만듭니다.
6. 요약 결과를 `mars_weather_summary.png` 이미지 파일로 생성합니다.
7. 보너스 과제로 `MySQLHelper` 클래스를 사용하여 DB 연결과 쿼리 실행을 구조화합니다.
8. GitHub에 업로드할 때 DB 비밀번호가 노출되지 않도록 `.env`와 `.gitignore`를 사용합니다.

---

## 2. 프로젝트 폴더 구조

최종적으로 권장되는 폴더 구조는 다음과 같습니다.

```text
14 weeks/
 ├─ .venv/                    # Python 가상환경, GitHub에 올리지 않음
 ├─ .env                      # 실제 DB 접속 정보, GitHub에 올리지 않음
 ├─ .env.example              # 환경변수 예시 파일, GitHub에 올림
 ├─ .gitignore                # Git 무시 규칙
 ├─ README.md                 # 과제 설명 파일, 선택 사항
 ├─ requirements.txt          # 설치 패키지 목록
 ├─ mars_weather_summary.py   # 과제 실행 Python 코드
 ├─ mars_weathers_data.CSV    # 과제 CSV 데이터
 ├─ mars_weather_summary.png  # Python 실행 결과 이미지
 └─ sql/
     └─ init_mars_db.sql      # DB와 테이블 생성 SQL
```

---

## 3. VS Code에서 작업 폴더로 이동

PowerShell 또는 VS Code 터미널에서 과제 폴더로 이동합니다.

```powershell
cd "C:\codyssey\problem essential\yj-codyssey\14 weeks"
```

현재 위치 확인:

```powershell
pwd
```

정상 예시:

```text
C:\codyssey\problem essential\yj-codyssey\14 weeks
```

---

## 4. Python 가상환경 생성

과제 폴더 안에서 가상환경을 생성합니다.

```powershell
python -m venv .venv
```

만약 `python` 명령어가 동작하지 않으면 아래 명령어를 사용합니다.

```powershell
py -m venv .venv
```

생성 후 폴더 구조는 다음과 비슷해집니다.

```text
14 weeks/
 └─ .venv/
```

---

## 5. 가상환경 활성화

PowerShell에서 다음 명령어를 실행합니다.

```powershell
.\.venv\Scripts\Activate.ps1
```

정상 활성화되면 터미널 앞에 `(.venv)`가 표시됩니다.

```text
(.venv) PS C:\codyssey\problem essential\yj-codyssey\14 weeks>
```

### 실행 정책 오류가 발생하는 경우

아래와 같은 오류가 발생할 수 있습니다.

```text
이 시스템에서 스크립트를 실행할 수 없으므로 ...
```

그럴 때는 현재 터미널에서만 임시로 실행을 허용합니다.

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

그다음 다시 활성화합니다.

```powershell
.\.venv\Scripts\Activate.ps1
```

---

## 6. 필요한 Python 패키지 설치

먼저 pip를 최신화합니다.

```powershell
python -m pip install --upgrade pip
```

MySQL 연결용 패키지를 설치합니다.

```powershell
pip install mysql-connector-python
```

`.env` 파일을 읽기 위한 패키지도 설치합니다.

```powershell
pip install python-dotenv
```

설치 목록을 `requirements.txt`로 저장합니다.

```powershell
pip freeze > requirements.txt
```

이후 다른 환경에서는 아래 명령어로 동일한 패키지를 설치할 수 있습니다.

```powershell
pip install -r requirements.txt
```

---

## 7. MySQL 데이터베이스 생성

MySQL Workbench에서 새 SQL 탭을 열고 아래 SQL을 실행합니다.

```sql
CREATE DATABASE IF NOT EXISTS mars_db
DEFAULT CHARACTER SET utf8mb4
DEFAULT COLLATE utf8mb4_unicode_ci;

USE mars_db;

DROP TABLE IF EXISTS mars_weather;

CREATE TABLE mars_weather (
    weather_id INT AUTO_INCREMENT PRIMARY KEY,
    mars_date DATETIME NOT NULL,
    temp INT,
    storm INT
);
```

이 SQL은 다음 작업을 수행합니다.

- `mars_db` 데이터베이스 생성
- `mars_weather` 테이블이 이미 있으면 삭제
- 새 `mars_weather` 테이블 생성
- `weather_id`는 자동 증가 기본키
- `mars_date`는 날짜 데이터
- `temp`는 온도
- `storm`은 폭풍 관련 값

---

## 8. 과제용 MySQL 계정 생성

`root` 계정 정보를 Python 코드에 직접 넣는 것은 위험합니다. 과제 전용 계정을 만드는 것이 좋습니다.

MySQL Workbench에서 아래 SQL을 실행합니다.

```sql
CREATE USER IF NOT EXISTS 'mars_user'@'localhost' IDENTIFIED BY '1234';

GRANT ALL PRIVILEGES ON mars_db.* TO 'mars_user'@'localhost';

FLUSH PRIVILEGES;
```

여기서는 예시로 비밀번호를 `1234`로 두었습니다. 실제로는 본인이 원하는 비밀번호로 변경해도 됩니다.

---

## 9. `.env` 파일 만들기

`14 weeks` 폴더 안에 `.env` 파일을 만듭니다.

```text
.env
```

내용 예시:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=mars_user
DB_PASSWORD=1234
DB_NAME=mars_db
```

이 파일에는 실제 DB 접속 정보가 들어갑니다.

따라서 `.env`는 GitHub에 올리면 안 됩니다.

---

## 10. `.env.example` 파일 만들기

GitHub에는 실제 비밀번호가 없는 예시 파일만 올립니다.

파일명:

```text
.env.example
```

내용:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_NAME=mars_db
```

`.env.example`은 다른 사람이 프로젝트를 실행할 때 어떤 환경변수가 필요한지 알려주는 용도입니다.

---

## 11. `.gitignore` 파일 만들기

`.gitignore` 파일을 만들고 아래 내용을 작성합니다.

```gitignore
.venv/
**/.venv/

.env
**/.env

__pycache__/
**/__pycache__/
*.pyc
```

필요하면 13주차 녹음 파일도 무시할 수 있습니다.

```gitignore
13 weeks/records/
```

주의할 점은 `.env`는 반드시 무시해야 한다는 것입니다.

---

## 12. Python 코드에서 `.env` 사용하기

`mars_weather_summary.py`에서 DB 접속 정보를 직접 쓰지 않고 `.env`에서 읽어오도록 작성합니다.

```python
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', '3306')),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
}
```

나쁜 예시는 다음과 같습니다.

```python
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '1234',
    'database': 'mars_db',
}
```

위처럼 실제 비밀번호를 코드에 직접 쓰면 GitHub 업로드 시 보안 문제가 생길 수 있습니다.

---

## 13. 보너스 과제: MySQLHelper 클래스 구조

보너스 과제에서는 MySQL 연결과 쿼리 실행을 클래스로 분리합니다.

예시 구조:

```python
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
```

이 클래스를 사용하면 메인 코드가 더 간단해집니다.

```python
db = MySQLHelper(DB_CONFIG)
db.connect()
db.execute(...)
db.fetch_one(...)
db.close()
```

---

## 14. CSV 파일 배치

`mars_weather_summary.py`와 `mars_weathers_data.CSV`는 같은 폴더에 있어야 합니다.

```text
14 weeks/
 ├─ mars_weather_summary.py
 └─ mars_weathers_data.CSV
```

코드에서 파일 이름을 다음처럼 지정했다면 대소문자까지 맞추는 것이 좋습니다.

```python
CSV_FILE_NAME = 'mars_weathers_data.CSV'
```

---

## 15. Python 코드 실행

가상환경이 활성화된 상태에서 실행합니다.

```powershell
python mars_weather_summary.py
```

정상 실행 예시:

```text
작업이 완료되었습니다.
삽입된 데이터 수: 1000
요약 이미지 파일: C:\codyssey\problem essential\yj-codyssey\14 weeks\mars_weather_summary.png
```

이 메시지가 나오면 다음 작업이 성공한 것입니다.

1. Python에서 MySQL 접속 성공
2. CSV 데이터 1000개 읽기 성공
3. DB 삽입 성공
4. 요약 통계 조회 성공
5. PNG 이미지 생성 성공

---

## 16. MySQL Workbench에서 데이터 확인

MySQL Workbench에서 아래 SQL을 실행합니다.

```sql
USE mars_db;

SELECT *
FROM mars_weather
LIMIT 10;
```

데이터 개수 확인:

```sql
SELECT COUNT(*)
FROM mars_weather;
```

결과가 `1000`이면 CSV 데이터가 정상 삽입된 것입니다.

요약 통계 확인:

```sql
SELECT
    COUNT(*) AS total_count,
    MIN(mars_date) AS first_date,
    MAX(mars_date) AS last_date,
    AVG(temp) AS avg_temp,
    MIN(temp) AS min_temp,
    MAX(temp) AS max_temp,
    AVG(storm) AS avg_storm,
    MIN(storm) AS min_storm,
    MAX(storm) AS max_storm
FROM mars_weather;
```

---

## 17. 자주 발생한 오류와 해결

### 17-1. Access denied for user 'root'@'localhost'

오류 예시:

```text
Access denied for user 'root'@'localhost' (using password: YES)
```

원인:

- Python 코드에 적은 MySQL 계정 또는 비밀번호가 실제와 다름
- `root` 비밀번호가 틀림
- Workbench에는 저장된 비밀번호로 접속되지만 Python 설정과 다름

해결:

1. `root` 대신 과제용 계정 `mars_user`를 사용합니다.
2. `.env`의 `DB_USER`, `DB_PASSWORD`를 확인합니다.
3. Python 코드가 `.env`를 읽고 있는지 확인합니다.

---

### 17-2. No module named mysql

오류 원인:

- 가상환경에 `mysql-connector-python`이 설치되지 않음

해결:

```powershell
pip install mysql-connector-python
```

---

### 17-3. No module named dotenv

오류 원인:

- `python-dotenv`가 설치되지 않음

해결:

```powershell
pip install python-dotenv
```

---

### 17-4. CSV 파일을 찾을 수 없습니다

원인:

- `mars_weather_summary.py`와 `mars_weathers_data.CSV`가 같은 폴더에 없음
- 파일명이 다름
- 확장자 대소문자가 다름

해결:

```powershell
ls
```

위 명령어로 현재 폴더에 CSV 파일이 있는지 확인합니다.

---

### 17-5. mysqldump 명령어를 찾을 수 없음

오류 예시:

```text
'mysqldump' 용어가 cmdlet, 함수, 스크립트 파일 또는 실행할 수 있는 프로그램 이름으로 인식되지 않습니다.
```

원인:

- `mysqldump.exe`가 Windows PATH에 등록되지 않음

해결:

전체 경로로 실행합니다.

```powershell
& "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe" -u mars_user -p mars_db mars_weather > mars_weather_dump.sql
```

MySQL Server 버전이 8.4라면 경로를 바꿉니다.

```powershell
& "C:\Program Files\MySQL\MySQL Server 8.4\bin\mysqldump.exe" -u mars_user -p mars_db mars_weather > mars_weather_dump.sql
```

---

## 18. DB를 GitHub에 올리는 방법

MySQL DB 자체를 GitHub에 직접 올리는 것이 아니라, 보통 다음 파일을 올립니다.

1. DB 생성 SQL
2. CSV 원본 데이터
3. Python 코드
4. 결과 이미지
5. 실행 방법 문서
6. 필요하면 DB dump SQL

권장 방식:

```text
sql/init_mars_db.sql
mars_weathers_data.CSV
mars_weather_summary.py
mars_weather_summary.png
requirements.txt
.env.example
.gitignore
```

---

## 19. `sql/init_mars_db.sql` 작성

`14 weeks/sql/init_mars_db.sql` 파일을 만들고 아래 내용을 작성합니다.

```sql
CREATE DATABASE IF NOT EXISTS mars_db
DEFAULT CHARACTER SET utf8mb4
DEFAULT COLLATE utf8mb4_unicode_ci;

USE mars_db;

DROP TABLE IF EXISTS mars_weather;

CREATE TABLE mars_weather (
    weather_id INT AUTO_INCREMENT PRIMARY KEY,
    mars_date DATETIME NOT NULL,
    temp INT,
    storm INT
);
```

이 파일은 비밀번호가 없기 때문에 GitHub에 올려도 괜찮습니다.

---

## 20. mysqldump로 DB 백업 파일 만들기

명령어로 DB 내용을 SQL 파일로 내보낼 수 있습니다.

```powershell
& "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe" -u mars_user -p mars_db mars_weather > mars_weather_dump.sql
```

성공하면 현재 폴더에 아래 파일이 생깁니다.

```text
mars_weather_dump.sql
```

GitHub에 올리기 전에는 혹시 민감 정보가 들어갔는지 확인합니다.

```powershell
Select-String -Path .\mars_weather_dump.sql -Pattern "password","IDENTIFIED","root"
```

일반적으로 dump 파일에는 DB 비밀번호가 들어가지 않습니다. 그래도 확인하는 습관이 좋습니다.

---

## 21. GitHub 업로드 전 보안 확인

아래 명령어로 Git 상태를 확인합니다.

```powershell
git status
```

올라가면 안 되는 파일:

```text
.env
.venv/
```

올라가도 되는 파일:

```text
.env.example
.gitignore
requirements.txt
mars_weather_summary.py
mars_weathers_data.CSV
mars_weather_summary.png
sql/init_mars_db.sql
mars_weather_dump.sql
```

단, `mars_weather_dump.sql`은 개인정보나 비밀번호가 없는지 확인한 뒤 올립니다.

---

## 22. sparse-checkout 관련 문제

`git add .` 실행 시 아래와 같은 메시지가 나올 수 있습니다.

```text
The following paths and/or pathspecs matched paths that exist
outside of your sparse-checkout definition
```

원인:

- 현재 Git 저장소가 sparse-checkout 모드로 일부 폴더만 추적하도록 설정되어 있음

빠른 해결:

```powershell
git add --sparse .
```

근본 해결:

```powershell
cd "C:\codyssey\problem essential\yj-codyssey"
git sparse-checkout disable
```

그 후 다시 과제 폴더로 이동합니다.

```powershell
cd ".\14 weeks"
git add .
```

---

## 23. GitHub 업로드 명령어

현재 과제 폴더에서 파일을 추가합니다.

```powershell
git add --sparse .
```

상태 확인:

```powershell
git status
```

`.env`가 없는지 반드시 확인합니다.

커밋:

```powershell
git commit -m "Add mars weather summary assignment"
```

푸시:

```powershell
git push
```

---

## 24. 최종 제출 전 체크리스트

아래 항목을 확인합니다.

- [ ] `.venv`가 GitHub에 올라가지 않는다.
- [ ] `.env`가 GitHub에 올라가지 않는다.
- [ ] `.env.example`에는 실제 비밀번호가 없다.
- [ ] `mars_weather_summary.py`에 실제 DB 비밀번호가 직접 적혀 있지 않다.
- [ ] `requirements.txt`가 있다.
- [ ] `mars_weathers_data.CSV`가 있다.
- [ ] `mars_weather_summary.png`가 생성되었다.
- [ ] MySQL Workbench에서 `SELECT COUNT(*) FROM mars_weather;` 결과가 1000이다.
- [ ] GitHub에 업로드 전 `git status`를 확인했다.

---

## 25. 결론

이번 과제는 단순히 Python 코드만 작성하는 것이 아니라, 다음 흐름을 모두 경험하는 과제입니다.

```text
CSV 파일
   ↓
Python 파일 읽기
   ↓
MySQL DB 저장
   ↓
SQL 요약 조회
   ↓
PNG 결과 생성
   ↓
.env로 비밀번호 보호
   ↓
.gitignore로 민감 파일 제외
   ↓
GitHub 업로드
```

가장 중요한 보안 원칙은 다음입니다.

```text
실제 DB 비밀번호는 코드에 직접 쓰지 않는다.
실제 DB 비밀번호가 들어간 .env 파일은 GitHub에 올리지 않는다.
GitHub에는 .env.example만 올린다.
```
