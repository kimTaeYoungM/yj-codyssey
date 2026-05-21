# Javis 녹음 프로그램

## 구성 파일

- `javis.py`: 과제 제출용 Python 코드
- `requirements.txt`: 마이크 녹음에 필요한 외부 라이브러리
- `records/`: 프로그램 실행 중 자동 생성되는 녹음 파일 저장 폴더

## 실행 방법

VS Code 터미널에서 아래 순서대로 실행합니다.

```bash
pip install -r requirements.txt
python javis.py
```

## 기능

1. 시스템 마이크를 사용해 음성을 녹음합니다.
2. 녹음 파일은 `records` 폴더에 저장됩니다.
3. 파일 이름은 녹음 날짜와 시간을 기준으로 `YYYY년MM월DD일-HH시MM분SS초.wav` 형식으로 저장됩니다.
4. 보너스 기능으로 특정 날짜 범위의 녹음 파일 목록을 확인할 수 있습니다.

## 날짜 범위 조회 입력 예시

```text
시작 날짜를 입력하세요(YYYY-MM-DD): 2026-05-01
종료 날짜를 입력하세요(YYYY-MM-DD): 2026-05-21
```
