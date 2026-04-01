import random
from datetime import datetime
import os

class DummySensor:
    # 1. 유지 보수 편이성: 범위를 클래스 변수로 분리하여 변경이 용이하게 함
    _RANGES = {
        'internal_temp': (18, 30),
        'external_temp': (0, 21),
        'internal_humidity': (50, 60),
        'external_illuminance': (500, 715),
        'internal_co2': (0.02, 0.1),
        'internal_oxygen': (4, 7)
    }

    def __init__(self):
        # 2. 프로그램 안정성: 변수 캡슐화 (_ 접두사 사용)
        self._env_values = {
            'mars_base_internal_temperature': 0,
            'mars_base_external_temperature': 0,
            'mars_base_internal_humidity': 0,
            'mars_base_external_illuminance': 0,
            'mars_base_internal_co2': 0,
            'mars_base_internal_oxygen': 0
        }
        self._log_file = 'sensor_log.txt'

    def set_env(self):
        # 3. 요구 기능 충족: random 값이 범위 내에서 적절히 생성되도록 구현
        # 딕셔너리 키 순서에 맞춰 범위를 매칭하여 값을 채움
        ranges = list(self._RANGES.values())
        for i, key in enumerate(self._env_values.keys()):
            low, high = ranges[i]
            val = random.uniform(low, high)
            # CO2는 소수점 세자리, 나머지는 두자리로 정밀도 차별화
            precision = 3 if 'co2' in key else 2
            self._env_values[key] = round(val, precision)

    def get_env(self):
        # 4. 보너스 과제: 로그 헤더 저장 및 중복 방지 로직
        is_empty = not os.path.exists(self._log_file) or os.path.getsize(self._log_file) == 0
        
        with open(self._log_file, 'a', encoding = 'utf-8') as f:
            # 파일이 처음 생성되거나 비어있을 때만 헤더(컬럼명)를 작성
            if is_empty:
                header = 'timestamp,' + ','.join(self._env_values.keys()) + '\n'
                f.write(header)
            
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # 값들을 쉼표(,)로 구분하여 한 줄로 기록
            values_str = ','.join(map(str, self._env_values.values()))
            f.write(f'{now},{values_str}\n')
            
        return self._env_values

# 메인 실행부
if __name__ == '__main__':
    # 인스턴스 명칭 'ds' 사용 준수
    ds = DummySensor()
    
    # 메서드 순차 호출
    ds.set_env()
    current_data = ds.get_env()
    
    print('현재 화성 기지 환경 데이터:')
    for key, value in current_data.items():
        print(f'{key}: {value}')