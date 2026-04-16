# 과제 리포트: 단위문제 8 - 불안정한 미션 컴퓨터

## 1. 과제 개요
본 과제는 우주 기지에 설치된 '미션 컴퓨터'의 상태를 파악하기 위해 시스템 정보 및 실시간 부하 정보를 가져오는 모듈을 구현하는 것을 목표로 합니다.

## 2. 수행 과제 및 요구사항
* **MissionComputer 클래스 확장**: 시스템 정보 및 부하 정보 조회 메소드 추가
* **시스템 정보 조회 (`get_mission_computer_info`)**: OS, CPU, 메모리 정보 추출 및 JSON 출력
* **실시간 부하 정보 조회 (`get_mission_computer_load`)**: CPU, 메모리 실시간 사용량 추출 및 JSON 출력
* **보너스 과제**: `setting.txt`를 통한 출력 항목 필터링 기능 구현

## 3. 구현 코드
```python
import platform
import json
import psutil

class MissionComputer:
    def __init__(self):
        self.settings = self._load_settings()

    def _load_settings(self):
        try:
            with open('setting.txt', 'r', encoding='utf-8') as f:
                return [line.strip() for line in f.readlines() if line.strip()]
        except FileNotFoundError:
            return []
        except Exception as e:
            return []

    def _filter_data(self, data):
        if not self.settings:
            return data
        return {k: v for k, v in data.items() if k in self.settings}

    def get_mission_computer_info(self):
        try:
            info = {
                'os': platform.system(),
                'os_version': platform.version(),
                'cpu_type': platform.processor(),
                'cpu_cores': psutil.cpu_count(logical=True),
                'memory_size': f'{round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB'
            }
            filtered_info = self._filter_data(info)
            return json.dumps(filtered_info, indent=4)
        except Exception as e:
            return json.dumps({'error': str(e)})

    def get_mission_computer_load(self):
        try:
            load = {
                'cpu_usage': f'{psutil.cpu_percent(interval=1)}%',
                'memory_usage': f'{psutil.virtual_memory().percent}%'
            }
            filtered_load = self._filter_data(load)
            return json.dumps(filtered_load, indent=4)
        except Exception as e:
            return json.dumps({'error': str(e)})

if __name__ == '__main__':
    runComputer = MissionComputer()
    print(runComputer.get_mission_computer_info())
    print(runComputer.get_mission_computer_load())
```

## 4. 기술적 상세 설명
* **안정성**: 예외 처리를 통해 시스템 정보 접근 권한이나 파일 읽기 오류 발생 시에도 안정적으로 동작합니다.
* **확장성**: `setting.txt` 파일을 통해 코드 수정 없이 출력 항목을 제어할 수 있습니다.
* **표준 준수**: PEP 8 가이드를 준수하여 코드의 가독성을 확보하였습니다.
