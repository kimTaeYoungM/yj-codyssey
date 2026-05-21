"""Simple microphone recorder for the unit assignment.

This program records audio from the system microphone and saves each
recording into a local records folder. It also provides a bonus feature that
lists saved recordings within a selected date range.
"""

from __future__ import annotations

import datetime as dt
import sys
import wave
from pathlib import Path

try:
    import sounddevice as sd
except ImportError:
    sd = None


RECORDS_DIR = Path(__file__).resolve().parent / 'records'
SAMPLE_RATE = 44100
CHANNELS = 1
SAMPLE_WIDTH = 2
DT_FORMAT = '%Y년%m월%d일-%H시%M분%S초'
FILE_SUFFIX = '.wav'


class RecorderError(Exception):
    """Raised when recording cannot be completed."""


def make_records_dir() -> None:
    """Create the records directory if it does not already exist."""
    RECORDS_DIR.mkdir(parents=True, exist_ok=True)


def make_record_filename(recorded_at: dt.datetime) -> Path:
    """Return a dated recording filename inside the records directory."""
    filename = recorded_at.strftime(DT_FORMAT) + FILE_SUFFIX
    return RECORDS_DIR / filename


def save_wav_file(file_path: Path, frames: bytes) -> None:
    """Save raw 16-bit PCM frames as a WAV file."""
    with wave.open(str(file_path), 'wb') as wav_file:
        wav_file.setnchannels(CHANNELS)
        wav_file.setsampwidth(SAMPLE_WIDTH)
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.writeframes(frames)


def record_audio(seconds: int) -> Path:
    """Record microphone audio for the requested number of seconds."""
    if sd is None:
        raise RecorderError(
            'sounddevice 라이브러리가 설치되어 있지 않습니다. '
            '터미널에서 pip install sounddevice 명령을 먼저 실행해 주세요.'
        )

    if seconds <= 0:
        raise RecorderError('녹음 시간은 1초 이상이어야 합니다.')

    make_records_dir()
    recorded_at = dt.datetime.now()
    file_path = make_record_filename(recorded_at)

    print(f'{seconds}초 동안 녹음을 시작합니다.')
    print('마이크 사용 권한 요청이 나오면 허용해 주세요.')

    try:
        audio_data = sd.rec(
            int(seconds * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype='int16',
        )
        sd.wait()
    except Exception as error:
        raise RecorderError(f'마이크 녹음 중 오류가 발생했습니다: {error}') from error

    save_wav_file(file_path, audio_data.tobytes())
    print(f'녹음 파일을 저장했습니다: {file_path}')
    return file_path


def parse_date(date_text: str) -> dt.date:
    """Parse YYYY-MM-DD text into a date object."""
    try:
        return dt.datetime.strptime(date_text, '%Y-%m-%d').date()
    except ValueError as error:
        raise RecorderError('날짜는 YYYY-MM-DD 형식으로 입력해야 합니다.') from error


def parse_record_datetime(file_path: Path) -> dt.datetime | None:
    """Parse recording datetime from a saved recording filename."""
    if file_path.suffix.lower() != FILE_SUFFIX:
        return None

    try:
        return dt.datetime.strptime(file_path.stem, DT_FORMAT)
    except ValueError:
        return None


def find_recordings(start_date: dt.date, end_date: dt.date) -> list[Path]:
    """Find recordings whose filename dates are within the date range."""
    if start_date > end_date:
        raise RecorderError('시작 날짜는 종료 날짜보다 늦을 수 없습니다.')

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
    start_text = input('시작 날짜를 입력하세요(YYYY-MM-DD): ').strip()
    end_text = input('종료 날짜를 입력하세요(YYYY-MM-DD): ').strip()

    start_date = parse_date(start_text)
    end_date = parse_date(end_text)
    recordings = find_recordings(start_date, end_date)

    if not recordings:
        print('해당 날짜 범위의 녹음 파일이 없습니다.')
        return

    print('해당 날짜 범위의 녹음 파일 목록입니다.')
    for index, file_path in enumerate(recordings, start=1):
        print(f'{index}. {file_path.name}')


def ask_record_seconds() -> int:
    """Ask the user for recording duration in seconds."""
    seconds_text = input('녹음할 시간을 초 단위로 입력하세요: ').strip()

    try:
        seconds = int(seconds_text)
    except ValueError as error:
        raise RecorderError('녹음 시간은 정수로 입력해야 합니다.') from error

    return seconds


def print_menu() -> None:
    """Print the main menu."""
    print()
    print('==== Javis 녹음 프로그램 ====')
    print('1. 마이크 녹음하기')
    print('2. 날짜 범위로 녹음 파일 보기')
    print('3. 종료')


def run_menu() -> None:
    """Run the command line menu."""
    make_records_dir()

    while True:
        print_menu()
        choice = input('메뉴를 선택하세요: ').strip()

        try:
            if choice == '1':
                seconds = ask_record_seconds()
                record_audio(seconds)
            elif choice == '2':
                show_recordings_by_date_range()
            elif choice == '3':
                print('프로그램을 종료합니다.')
                break
            else:
                print('1, 2, 3 중에서 선택해 주세요.')
        except RecorderError as error:
            print(f'오류: {error}')


def main() -> int:
    """Start the program."""
    run_menu()
    return 0


if __name__ == '__main__':
    sys.exit(main())
