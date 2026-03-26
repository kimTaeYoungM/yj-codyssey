import random
from datetime import datetime

class DummySensor:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0,
            'mars_base_external_temperature': 0,
            'mars_base_internal_humidity': 0,
            'mars_base_external_illuminance': 0,
            'mars_base_internal_co2': 0,
            'mars_base_internal_oxygen': 0
        }

    def set_env(self):
        # 각 범위에 맞는 랜덤 값 생성 (소수점 둘째자리까지 반올림 예시)
        self.env_values['mars_base_internal_temperature'] = round(random.uniform(18, 30), 2)
        self.env_values['mars_base_external_temperature'] = round(random.uniform(0, 21), 2)
        self.env_values['mars_base_internal_humidity'] = round(random.uniform(50, 60), 2)
        self.env_values['mars_base_external_illuminance'] = round(random.uniform(500, 715), 2)
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 3)
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4, 7), 2)

    def get_env(self):
        # 보너스 과제: 파일에 로그 남기기
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_msg = f"{now} | {self.env_values}\n"
        
        with open('sensor_log.txt', 'a', encoding = 'utf-8') as f:
            f.write(log_msg)
            
        return self.env_values

# 메인 실행부
if __name__ == '__main__':
    # 인스턴스 생성 (이름은 ds로 지정)
    ds = DummySensor()
    
    # 메서드 호출 및 결과 확인
    ds.set_env()
    current_data = ds.get_env()
    
    print('현재 화성 기지 환경 데이터:')
    for key, value in current_data.items():
        print(f'{key}: {value}')