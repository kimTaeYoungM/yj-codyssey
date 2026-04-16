import json
import time
import random
import platform
import os
import psutil  # 시스템 정보 및 부하 측정을 위한 외부 라이브러리


class DummySensor:
    '''
    화성 기지의 환경 데이터를 시뮬레이션하는 클래스
    '''
    def get_current_values(self):
        '''
        환경 데이터를 딕셔너리 형태로 반환합니다.
        '''
        return {
            'mars_base_internal_temperature': round(random.uniform(18.0, 24.0), 2),
            'mars_base_external_temperature': round(random.uniform(-100.0, -20.0), 2),
            'mars_base_internal_humidity': round(random.uniform(30.0, 50.0), 2),
            'mars_base_external_illuminance': round(random.uniform(0.0, 1000.0), 2),
            'mars_base_internal_co2': round(random.uniform(400.0, 600.0), 2),
            'mars_base_internal_oxygen': round(random.uniform(18.0, 22.0), 2)
        }


class MissionComputer:
    '''
    환경 데이터 관리 및 미션 컴퓨터의 하드웨어 상태를 정밀 모니터링하는 클래스
    '''
    def __init__(self):
        # 환경 데이터 초기화
        self.env_values = {
            'mars_base_internal_temperature': 0,
            'mars_base_external_temperature': 0,
            'mars_base_internal_humidity': 0,
            'mars_base_external_illuminance': 0,
            'mars_base_internal_co2': 0,
            'mars_base_internal_oxygen': 0
        }
        self.ds = DummySensor()
        self.data_history = []
        self.start_time = time.time()
        
        # 보너스 과제: 설정 파일 로드
        self.display_settings = self._load_settings()

    def _load_settings(self):
        '''
        setting.txt 파일을 읽어 출력할 항목 리스트를 가져옵니다.
        '''
        settings = []
        try:
            if os.path.exists('setting.txt'):
                with open('setting.txt', 'r', encoding='utf-8') as f:
                    settings = [line.strip() for line in f.readlines() if line.strip()]
        except Exception as e:
            print(f'설정 파일을 읽는 중 오류 발생: {e}')
        return settings

    def _filter_output(self, data_dict):
        '''
        설정된 항목만 필터링하여 반환합니다.
        설정이 비어있으면 모든 항목을 반환합니다.
        '''
        if not self.display_settings:
            return data_dict
        return {k: v for k, v in data_dict.items() if k in self.display_settings}

    def get_mission_computer_info(self):
        '''
        미션 컴퓨터의 정적 시스템 사양을 가져와 JSON 형식으로 출력합니다.
        '''
        try:
            # 부팅 시간 포맷팅
            bt_timestamp = psutil.boot_time()
            bt_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(bt_timestamp))

            info = {
                'os': platform.system(),
                'os_version': platform.version(),
                'node_name': platform.node(),
                'architecture': platform.architecture()[0],
                'cpu_type': platform.processor(),
                'cpu_cores': os.cpu_count(),
                'memory_size': f'{round(psutil.virtual_memory().total / (1024**3), 2)} GB',
                'boot_time': bt_str
            }
            filtered_info = self._filter_output(info)
            print(json.dumps(filtered_info, indent=4))
            return filtered_info
        except Exception as e:
            print(f'시스템 정보 호출 중 예외 발생: {e}')

    def get_mission_computer_load(self):
        '''
        미션 컴퓨터의 동적 부하 상태(온도, 주파수, 사용률 등)를 JSON 형식으로 출력합니다.
        '''
        try:
            load = {
                'cpu_usage': f'{psutil.cpu_percent(interval=1)}%',
                'cpu_freq': f'{psutil.cpu_freq().current:.2f} MHz' if psutil.cpu_freq() else 'N/A',
                'memory_usage': f'{psutil.virtual_memory().percent}%',
                'disk_usage': f'{psutil.disk_usage("/").percent}%'
            }

            # 하드웨어 온도 정보 (지원되는 환경에서만 추가)
            if hasattr(psutil, 'sensors_temperatures'):
                temps = psutil.sensors_temperatures()
                if temps:
                    # 첫 번째 센서의 온도값 추출 시도
                    for name, entries in temps.items():
                        load['cpu_temp'] = f'{entries[0].current}°C'
                        break

            filtered_load = self._filter_output(load)
            print(json.dumps(filtered_load, indent=4))
            return filtered_load
        except Exception as e:
            print(f'부하 정보 호출 중 예외 발생: {e}')

    def get_sensor_data(self):
        '''
        실시간 환경 데이터를 수집하고 5분마다 보고서를 출력합니다.
        '''
        try:
            print('\n--- Monitoring Started ---')
            while True:
                new_data = self.ds.get_current_values()
                self.env_values.update(new_data)
                self.data_history.append(new_data)

                filtered_env = self._filter_output(self.env_values)
                print(json.dumps(filtered_env))

                current_time = time.time()
                if current_time - self.start_time >= 300:
                    self._print_five_minute_average()
                    self.start_time = current_time
                    self.data_history = []

                time.sleep(5)
        except KeyboardInterrupt:
            print('\nSystem stopped by user.')

    def _print_five_minute_average(self):
        if not self.data_history:
            return

        print('\n--- 5-Minute Average Report ---')
        averages = {}
        for key in self.env_values.keys():
            total = sum(data[key] for data in self.data_history)
            averages[key] = round(total / len(self.data_history), 2)
        
        filtered_avg = self._filter_output(averages)
        print(json.dumps(filtered_avg))
        print('-------------------------------\n')


# 인스턴스화
runComputer = MissionComputer()

if __name__ == '__main__':
    # 1. 정적 시스템 사양 출력
    print('=== Mission Computer Static Info ===')
    runComputer.get_mission_computer_info()
    
    # 2. 실시간 하드웨어 상태 출력
    print('\n=== Mission Computer Real-time Status ===')
    runComputer.get_mission_computer_load()
    
    # 3. 환경 데이터 모니터링 실행
    runComputer.get_sensor_data()