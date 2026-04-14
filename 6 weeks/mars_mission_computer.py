import platform
import json
import psutil


class MissionComputer:
    def __init__(self):
        self.settings = self._load_settings()

    def _load_settings(self):
        """
        setting.txt 파일을 읽어 출력할 정보 항목 리스트를 반환합니다.
        파일이 없거나 읽기 오류 발생 시 모든 항목을 출력하도록 예외 처리합니다.
        """
        try:
            with open('setting.txt', 'r', encoding='utf-8') as f:
                # 줄바꿈 제거 및 공백 제거 후 리스트화
                return [line.strip() for line in f.readlines() if line.strip()]
        except FileNotFoundError:
            # 설정 파일이 없으면 전체 항목을 출력하도록 빈 리스트 혹은 기본값 반환
            return []
        except Exception as e:
            print(f'설정 파일을 읽는 중 오류 발생: {e}')
            return []

    def _filter_data(self, data):
        """
        설정 파일에 명시된 항목만 필터링합니다.
        설정이 비어있으면 모든 데이터를 반환합니다.
        """
        if not self.settings:
            return data
        return {k: v for k, v in data.items() if k in self.settings}

    def get_mission_computer_info(self):
        """
        시스템 정보를 가져와 JSON 형식으로 출력합니다.
        """
        try:
            info = {
                'os': platform.system(),
                'os_version': platform.version(),
                'cpu_type': platform.processor(),
                'cpu_cores': psutil.cpu_count(logical=True),
                'memory_size': f'{round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB'
            }
            
            filtered_info = self._filter_data(info)
            json_output = json.dumps(filtered_info, indent=4)
            print('--- 시스템 정보 ---')
            print(json_output)
            return json_output
            
        except Exception as e:
            error_msg = json.dumps({'error': f'시스템 정보 획득 실패: {e}'})
            print(error_msg)
            return error_msg

    def get_mission_computer_load(self):
        """
        실시간 부하 정보를 가져와 JSON 형식으로 출력합니다.
        """
        try:
            # cpu_percent의 interval은 실시간 변화를 측정하기 위해 1초로 설정
            load = {
                'cpu_usage': f'{psutil.cpu_percent(interval=1)}%',
                'memory_usage': f'{psutil.virtual_memory().percent}%'
            }
            
            filtered_load = self._filter_data(load)
            json_output = json.dumps(filtered_load, indent=4)
            print('--- 실시간 부하 정보 ---')
            print(json_output)
            return json_output
            
        except Exception as e:
            error_msg = json.dumps({'error': f'부하 정보 획득 실패: {e}'})
            print(error_msg)
            return error_msg


if __name__ == '__main__':
    # MissionComputer 클래스를 runComputer라는 이름으로 인스턴스화
    runComputer = MissionComputer()

    # 각 메소드 호출을 통한 정보 출력 확인
    runComputer.get_mission_computer_info()
    runComputer.get_mission_computer_load()
    