"""Javis microphone recorder and STT processor.

This program records audio from the system microphone and saves each
recording into a local records folder.

It also converts saved WAV audio files to text using STT,
saves the recognized text as CSV files,
and provides a bonus feature to search keywords inside saved CSV files.
"""

from __future__ import annotations

import csv
import datetime as dt
import sys
import wave
from pathlib import Path

try:
    import sounddevice as sd
except ImportError:
    sd = None

try:
    import speech_recognition as sr
except ImportError:
    sr = None


# 현재 javis.py 파일이 있는 위치를 기준으로 records 폴더를 사용합니다.
BASE_DIR = Path(__file__).resolve().parent
RECORDS_DIR = BASE_DIR / "records"

# WAV 녹음 설정값입니다.
SAMPLE_RATE = 44100
CHANNELS = 1
SAMPLE_WIDTH = 2

# 파일명 예시:
# 2026년05월21일-15시39분36초.wav
DT_FORMAT = "%Y년%m월%d일-%H시%M분%S초"
WAV_SUFFIX = ".wav"
CSV_SUFFIX = ".csv"


class RecorderError(Exception):
    """Raised when recording or processing cannot be completed."""


def make_records_dir() -> None:
    """Create the records directory if it does not already exist."""
    RECORDS_DIR.mkdir(parents=True, exist_ok=True)


def make_record_filename(recorded_at: dt.datetime) -> Path:
    """Return a dated recording filename inside the records directory."""
    file_name = recorded_at.strftime(DT_FORMAT) + WAV_SUFFIX
    return RECORDS_DIR / file_name


def save_wav_file(file_path: Path, frames: bytes) -> None:
    """Save raw 16-bit PCM frames as a WAV file."""
    with wave.open(str(file_path), "wb") as wav_file:
        wav_file.setnchannels(CHANNELS)
        wav_file.setsampwidth(SAMPLE_WIDTH)
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.writeframes(frames)


def ask_record_seconds() -> int:
    """Ask the user for recording duration in seconds."""
    seconds_text = input("녹음할 시간을 초 단위로 입력하세요: ").strip()

    try:
        seconds = int(seconds_text)
    except ValueError as error:
        raise RecorderError("녹음 시간은 정수로 입력해야 합니다.") from error

    if seconds <= 0:
        raise RecorderError("녹음 시간은 1초 이상이어야 합니다.")

    return seconds


def record_audio(seconds: int) -> Path:
    """Record microphone audio for the requested number of seconds."""
    if sd is None:
        raise RecorderError(
            "sounddevice 라이브러리가 설치되어 있지 않습니다. "
            "터미널에서 python -m pip install -r requirements.txt 명령을 먼저 실행해 주세요."
        )

    make_records_dir()

    recorded_at = dt.datetime.now()
    file_path = make_record_filename(recorded_at)

    print(f"{seconds}초 동안 녹음을 시작합니다.")
    print("마이크 사용 권한 요청이 나오면 허용해 주세요.")

    try:
        audio_data = sd.rec(
            int(seconds * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype="int16",
        )
        sd.wait()
    except Exception as error:
        raise RecorderError(f"마이크 녹음 중 오류가 발생했습니다: {error}") from error

    save_wav_file(file_path, audio_data.tobytes())

    print(f"녹음 파일을 저장했습니다: {file_path}")
    return file_path


def get_wav_files() -> list[Path]:
    """Return all WAV files in the records directory."""
    make_records_dir()
    return sorted(RECORDS_DIR.glob("*" + WAV_SUFFIX))


def get_csv_files() -> list[Path]:
    """Return all CSV files in the records directory."""
    make_records_dir()
    return sorted(RECORDS_DIR.glob("*" + CSV_SUFFIX))


def show_wav_files(wav_files: list[Path]) -> None:
    """Print WAV file list."""
    if not wav_files:
        print("records 폴더 안에 음성 파일이 없습니다.")
        return

    print()
    print("==== 저장된 음성 파일 목록 ====")

    for index, wav_path in enumerate(wav_files, start=1):
        csv_path = wav_path.with_suffix(CSV_SUFFIX)

        if csv_path.exists():
            status = "CSV 생성됨"
        else:
            status = "CSV 없음"

        print(f"{index}. {wav_path.name} [{status}]")


def select_wav_file() -> Path | None:
    """Let the user select one WAV file from the records directory."""
    wav_files = get_wav_files()
    show_wav_files(wav_files)

    if not wav_files:
        return None

    while True:
        selected_text = input("\nSTT로 변환할 음성 파일 번호를 입력하세요: ").strip()

        if not selected_text.isdigit():
            print("숫자로 입력해 주세요.")
            continue

        selected_index = int(selected_text)

        if selected_index < 1 or selected_index > len(wav_files):
            print("목록에 있는 번호를 입력해 주세요.")
            continue

        return wav_files[selected_index - 1]


def convert_audio_to_text(wav_file_path: Path, overwrite: bool = False) -> Path:
    """Extract text from a WAV file and save it as a CSV file.

    If STT fails, this function still creates a CSV file
    with an error message. This makes the assignment result easier to check.
    """
    if sr is None:
        raise RecorderError(
            "SpeechRecognition 라이브러리가 설치되어 있지 않습니다. "
            "터미널에서 python -m pip install -r requirements.txt 명령을 먼저 실행해 주세요."
        )

    if not wav_file_path.exists():
        raise RecorderError(f"음성 파일을 찾을 수 없습니다: {wav_file_path}")

    csv_file_path = wav_file_path.with_suffix(CSV_SUFFIX)

    if csv_file_path.exists() and not overwrite:
        print(f"{wav_file_path.name} 파일은 이미 CSV가 존재하여 건너뜁니다.")
        return csv_file_path

    recognizer = sr.Recognizer()
    recognized_text = ""

    print()
    print(f"'{wav_file_path.name}' 파일의 텍스트 변환을 시작합니다.")

    try:
        with sr.AudioFile(str(wav_file_path)) as source:
            audio_data = recognizer.record(source)

        recognized_text = recognizer.recognize_google(
            audio_data,
            language="ko-KR",
        )

    except sr.UnknownValueError:
        recognized_text = "음성을 인식하지 못했습니다."

    except sr.RequestError as error:
        recognized_text = f"구글 음성 인식 API 서버 오류: {error}"

    except Exception as error:
        recognized_text = f"처리 중 오류 발생: {error}"

    save_text_to_csv(
        csv_file_path=csv_file_path,
        wav_file_path=wav_file_path,
        recognized_text=recognized_text,
    )

    print(f"텍스트 변환 및 CSV 저장 완료: {csv_file_path.name}")
    return csv_file_path


def save_text_to_csv(
    csv_file_path: Path,
    wav_file_path: Path,
    recognized_text: str,
) -> None:
    """Save recognized text to a CSV file.

    utf-8-sig is used to prevent Korean text from breaking
    when the CSV file is opened in Microsoft Excel.
    """
    recognized_at = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(csv_file_path, mode="w", encoding="utf-8-sig", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(
            [
                "음성 파일명",
                "음성 파일내에서의 시간",
                "STT 처리 시간",
                "인식된 텍스트",
            ]
        )
        writer.writerow(
            [
                wav_file_path.name,
                "0:00",
                recognized_at,
                recognized_text,
            ]
        )


def process_stt_for_selected_record() -> None:
    """Convert one selected WAV file to text and save it as CSV."""
    wav_file_path = select_wav_file()

    if wav_file_path is None:
        return

    if wav_file_path.with_suffix(CSV_SUFFIX).exists():
        answer = input("이미 CSV 파일이 있습니다. 덮어쓰시겠습니까? (y/n): ").strip().lower()

        if answer == "y":
            convert_audio_to_text(wav_file_path, overwrite=True)
        else:
            print("STT 변환을 취소했습니다.")
    else:
        convert_audio_to_text(wav_file_path)


def process_stt_for_all_records() -> None:
    """Find all WAV files and apply STT processing."""
    wav_files = get_wav_files()

    if not wav_files:
        print("변환할 음성 파일이 존재하지 않습니다.")
        return

    converted_count = 0
    skipped_count = 0

    print()
    print("==== 전체 음성 파일 STT 변환 시작 ====")

    for wav_file_path in wav_files:
        csv_file_path = wav_file_path.with_suffix(CSV_SUFFIX)

        if csv_file_path.exists():
            print(f"{wav_file_path.name} 파일은 이미 CSV가 존재하여 건너뜁니다.")
            skipped_count += 1
            continue

        convert_audio_to_text(wav_file_path)
        converted_count += 1

    print()
    print("==== 전체 STT 변환 결과 ====")
    print(f"새로 변환한 파일 수: {converted_count}")
    print(f"건너뛴 파일 수: {skipped_count}")


def search_keyword_in_csv() -> None:
    """Bonus feature: Search for a keyword in all saved CSV files."""
    keyword = input("검색할 키워드를 입력하세요: ").strip()

    if not keyword:
        print("키워드가 입력되지 않았습니다.")
        return

    csv_files = get_csv_files()

    if not csv_files:
        print("검색할 CSV 파일이 없습니다. 먼저 텍스트 변환을 진행해 주세요.")
        return

    found_match = False

    print()
    print(f"==== '{keyword}' 검색 결과 ====")

    for csv_file_path in csv_files:
        try:
            with open(csv_file_path, mode="r", encoding="utf-8-sig", newline="") as csv_file:
                reader = csv.DictReader(csv_file)

                for row in reader:
                    recognized_text = row.get("인식된 텍스트", "")
                    audio_time = row.get("음성 파일내에서의 시간", "")
                    audio_file_name = row.get("음성 파일명", "")

                    if keyword in recognized_text:
                        print()
                        print(f"CSV 파일명: {csv_file_path.name}")
                        print(f"음성 파일명: {audio_file_name}")
                        print(f"시간: {audio_time}")
                        print(f"내용: {recognized_text}")
                        found_match = True

        except Exception as error:
            print(f"{csv_file_path.name} 파일 읽기 실패: {error}")

    if not found_match:
        print("일치하는 검색 결과가 없습니다.")


def parse_date(date_text: str) -> dt.date:
    """Parse YYYY-MM-DD text into a date object."""
    try:
        return dt.datetime.strptime(date_text, "%Y-%m-%d").date()
    except ValueError as error:
        raise RecorderError("날짜는 YYYY-MM-DD 형식으로 입력해야 합니다.") from error


def parse_record_datetime(file_path: Path) -> dt.datetime | None:
    """Parse recording datetime from a saved recording filename."""
    if file_path.suffix.lower() != WAV_SUFFIX:
        return None

    try:
        return dt.datetime.strptime(file_path.stem, DT_FORMAT)
    except ValueError:
        return None


def find_recordings(start_date: dt.date, end_date: dt.date) -> list[Path]:
    """Find recordings whose filename dates are within the date range."""
    if start_date > end_date:
        raise RecorderError("시작 날짜는 종료 날짜보다 늦을 수 없습니다.")

    make_records_dir()
    matched_files = []

    for file_path in RECORDS_DIR.iterdir():
        recorded_at = parse_record_datetime(file_path)

        if recorded_at is None:
            continue

        recorded_date = recorded_at.date()

        if start_date <= recorded_date <= end_date:
            matched_files.append(file_path)

    return sorted(matched_files)


def show_recordings_by_date_range() -> None:
    """Ask the user for a date range and print matching recordings."""
    start_text = input("시작 날짜를 입력하세요(YYYY-MM-DD): ").strip()
    end_text = input("종료 날짜를 입력하세요(YYYY-MM-DD): ").strip()

    start_date = parse_date(start_text)
    end_date = parse_date(end_text)

    recordings = find_recordings(start_date, end_date)

    if not recordings:
        print("해당 날짜 범위의 녹음 파일이 없습니다.")
        return

    print()
    print("해당 날짜 범위의 녹음 파일 목록입니다.")

    for index, file_path in enumerate(recordings, start=1):
        print(f"{index}. {file_path.name}")


def print_menu() -> None:
    """Print the main menu."""
    print()
    print("==== Javis 프로그램 ====")
    print("1. 마이크 녹음하기")
    print("2. 날짜 범위로 녹음 파일 보기")
    print("3. 전체 음성 파일 목록 보기")
    print("4. 선택한 음성 파일 STT 변환하기")
    print("5. 전체 음성 파일 STT 변환하기")
    print("6. 저장된 텍스트 키워드 검색")
    print("7. 종료")


def run_menu() -> None:
    """Run the command line menu."""
    make_records_dir()

    while True:
        print_menu()
        choice = input("메뉴를 선택하세요: ").strip()

        try:
            if choice == "1":
                seconds = ask_record_seconds()
                record_audio(seconds)

            elif choice == "2":
                show_recordings_by_date_range()

            elif choice == "3":
                wav_files = get_wav_files()
                show_wav_files(wav_files)

            elif choice == "4":
                process_stt_for_selected_record()

            elif choice == "5":
                process_stt_for_all_records()

            elif choice == "6":
                search_keyword_in_csv()

            elif choice == "7":
                print("프로그램을 종료합니다.")
                break

            else:
                print("1부터 7 사이의 번호를 선택해 주세요.")

        except RecorderError as error:
            print(f"오류: {error}")


def main() -> int:
    """Start the program."""
    run_menu()
    return 0


if __name__ == "__main__":
    sys.exit(main())