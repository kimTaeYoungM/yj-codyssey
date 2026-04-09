import json
import time
import random  # DummySensor의 동작을 시뮬레이션하기 위해 사용


class DummySensor:
    '''
    문제 3에서 제작한 클래스 (가상의 구현 예시)
    '''
    def get_current_values(self):
        '''
        화성 기지의 환경 데이터를 딕셔너리 형태로 반환합니다.
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
    화성 기지의 환경 데이터를 관리하고 출력하는 미션 컴퓨터 클래스
    '''
    def __init__(self):
        # 환경 데이터를 저장할 딕셔너리 속성 초기화
        self.env_values = {
            'mars_base_internal_temperature': 0,
            'mars_base_external_temperature': 0,
            'mars_base_internal_humidity': 0,
            'mars_base_external_illuminance': 0,
            'mars_base_internal_co2': 0,
            'mars_base_internal_oxygen': 0
        }
        # 문제 3에서 제작한 DummySensor 인스턴스화
        self.ds = DummySensor()
        
        # 보너스 과제: 5분 평균 계산을 위한 데이터 저장 리스트 및 타이머
        self.data_history = []
        self.start_time = time.time()

    def get_sensor_data(self):
        '''
        센서로부터 데이터를 가져와 출력하고, 보너스 과제 로직을 수행합니다.
        '''
        try:
            while True:
                # 1. 센서의 값을 가져와서 env_values에 담기
                # (DummySensor의 메소드명은 실제 구현에 맞춰 수정하십시오)
                new_data = self.ds.get_current_values()
                self.env_values.update(new_data)
                
                # 보너스 과제용 데이터 누적
                self.data_history.append(new_data)

                # 2. env_values의 값을 json 형태로 화면에 출력
                print(json.dumps(self.env_values))

                # 보너스 과제: 5분(300초)마다 평균값 출력
                current_time = time.time()
                if current_time - self.start_time >= 300:
                    self._print_five_minute_average()
                    self.start_time = current_time
                    self.data_history = []

                # 3. 위의 동작을 5초에 한 번씩 반복
                time.sleep(5)
                
        except KeyboardInterrupt:
            # 보너스 과제: 특정 키(Ctrl+C) 입력 시 중단 및 메시지 출력
            print('\nSytem stoped...')

    def _print_five_minute_average(self):
        '''
        저장된 데이터들의 5분 평균값을 계산하여 출력합니다.
        '''
        if not self.data_history:
            return

        print('--- 5-Minute Average Report ---')
        keys = self.env_values.keys()
        averages = {}
        
        for key in keys:
            total = sum(data[key] for data in self.data_history)
            averages[key] = round(total / len(self.data_history), 2)
            
        print(json.dumps(averages))
        print('-------------------------------')


# MissionComputer 클래스를 RunComputer라는 이름으로 인스턴스화
RunComputer = MissionComputer()

# 지속적으로 환경 데이터를 출력하도록 메소드 호출
if __name__ == '__main__':
    RunComputer.get_sensor_data()