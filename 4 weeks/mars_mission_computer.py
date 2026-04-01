# import random
# from datetime import datetime

# class DummySensor:
#     def __init__(self):
#         self.env_values = {
#             'mars_base_internal_temperature': 0,
#             'mars_base_external_temperature': 0,
#             'mars_base_internal_humidity': 0,
#             'mars_base_external_illuminance': 0,
#             'mars_base_internal_co2': 0,
#             'mars_base_internal_oxygen': 0
#         }

#     def set_env(self):
#         # 각 범위에 맞는 랜덤 값 생성 (소수점 둘째자리까지 반올림 예시)
#         self.env_values['mars_base_internal_temperature'] = round(random.uniform(18, 30), 2)
#         self.env_values['mars_base_external_temperature'] = round(random.uniform(0, 21), 2)
#         self.env_values['mars_base_internal_humidity'] = round(random.uniform(50, 60), 2)
#         self.env_values['mars_base_external_illuminance'] = round(random.uniform(500, 715), 2)
#         self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 3)
#         self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4, 7), 2)

#     def get_env(self):
#         # 보너스 과제: 파일에 로그 남기기
#         now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         log_msg = f"{now} | {self.env_values}\n"
        
#         with open('sensor_log.txt', 'a', encoding = 'utf-8') as f:
#             f.write(log_msg)
            
#         return self.env_values

# # 메인 실행부
# if __name__ == '__main__':
#     # 인스턴스 생성 (이름은 ds로 지정)
#     ds = DummySensor()
    
#     # 메서드 호출 및 결과 확인
#     ds.set_env()
#     current_data = ds.get_env()
    
#     print('현재 화성 기지 환경 데이터:')
#     for key, value in current_data.items():
#         print(f'{key}: {value}')

import random
from datetime import datetime
import os

class DummySensor:
    # 유지 보수 편이성을 위해 범위를 클래스 변수로 관리
    ENV_RANGES = {
        'mars_base_internal_temperature': (18, 30),
        'mars_base_external_temperature': (0, 21),
        'mars_base_internal_humidity': (50, 60),
        'mars_base_external_illuminance': (500, 715),
        'mars_base_internal_co2': (0.02, 0.1),
        'mars_base_internal_oxygen': (4, 7)
    }

    def __init__(self):
        # 인스턴스 변수 보호 (Encapsulation)
        self._env_values = {key: 0 for key in self.ENV_RANGES.keys()}
        self._log_file = 'sensor_log.txt'

    def set_env(self):
        # 각 범위 내에서 random 값이 잘 설정되도록 구현
        for key, (low, high) in self.ENV_RANGES.items():
            val = random.uniform(low, high)
            # CO2는 소수점 세자리, 나머지는 두자리 예시 (요구사항에 맞게 조절)
            precision = 3 if 'co2' in key else 2
            self._env_values[key] = round(val, precision)

    def get_env(self):
        # 보너스 과제: 파일 로그 남기기 및 헤더 중복 방지
        file_exists = os.path.exists(self._log_file)
        
        with open(self._log_file, 'a', encoding = 'utf-8') as f:
            # 파일이 없거나 비어있을 때만 헤더 작성
            if not file_exists or os.path.getsize(self._log_file) == 0:
                header = 'timestamp,' + ','.join(self._env_values.keys()) + '\n'
                f.write(header)
            
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            values_str = ','.join(map(str, self._env_values.values()))
            f.write(f'{now},{values_str}\n')
            
        return self._env_values

# 메인 실행부
if __name__ == '__main__':
    # 인스턴스 생성 (요구 명칭: ds)
    ds = DummySensor()
    
    # 메서드 호출 및 결과 확인
    ds.set_env()
    current_data = ds.get_env()
    
    print('현재 화성 기지 환경 데이터:')
    for key, value in current_data.items():
        # 가독성을 위해 출력 포맷 조정
        print(f'{key}: {value}')