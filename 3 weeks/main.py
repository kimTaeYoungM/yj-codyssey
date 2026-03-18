import pickle  # 보너스 과제: 객체 직렬화를 위해 파이썬 표준 라이브러리 사용

def manage_mars_inventory():
    input_file = 'Mars_Base_Inventory_List.csv'
    output_csv = 'Mars_Base_Inventory_danger.csv'
    output_bin = 'Mars_Base_Inventory_List.bin'
    
    inventory_data = []
    header = ''

    # 1 & 2. 파일 읽기 및 리스트 객체로 변환
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            header = f.readline().strip()  # 첫 줄(헤더) 저장
            
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                # 쉼표로 분리하여 리스트 생성
                fields = line.split(',')
                
                # 인화성 지수(마지막 열)를 숫자로 변환 (실수형)
                try:
                    fields[4] = float(fields[4])
                except (ValueError, IndexError):
                    # 숫자가 아니거나 데이터가 부족한 경우 0.0으로 처리하거나 제외
                    fields[4] = 0.0
                
                inventory_data.append(fields)
                
        print(f"'{input_file}' 파일을 성공적으로 읽어왔습니다.")
    except FileNotFoundError:
        print(f"오류: '{input_file}' 파일을 찾을 수 없습니다.")
        return
    except Exception as e:
        print(f"파일을 읽는 도중 오류가 발생했습니다: {e}")
        return

    # 3. 인화성이 높은 순(내림차순)으로 정렬
    # key=lambda x: x[4]는 리스트의 5번째 요소(인화성 지수)를 기준으로 함
    sorted_inventory = sorted(inventory_data, key=lambda x: x[4], reverse=True)
    
    print('\n[전체 목록 중 인화성 상위 5개]')
    for item in sorted_inventory[:5]:
        print(item)

    # 4. 인화성 지수가 0.7 이상인 목록 필터링 및 출력
    danger_list = [item for item in sorted_inventory if item[4] >= 0.7]
    
    print(f'\n[인화성 지수 0.7 이상 위험 물질 - 총 {len(danger_list)}건]')
    for item in danger_list:
        print(item)

    # 5. 인화성 지수 0.7 이상 목록을 CSV 포맷으로 저장
    try:
        with open(output_csv, 'w', encoding='utf-8') as f:
            f.write(header + '\n')
            for item in danger_list:
                # 리스트 요소들을 다시 문자열로 합침
                line = ','.join([str(val) for val in item])
                f.write(line + '\n')
        print(f"\n위험 물질 목록이 '{output_csv}'에 저장되었습니다.")
    except Exception as e:
        print(f"CSV 저장 중 오류 발생: {e}")

    # [보너스 과제] 이진 파일 형태로 저장 및 읽기
    try:
        # 이진 파일 쓰기 (wb 모드)
        with open(output_bin, 'wb') as f:
            pickle.dump(sorted_inventory, f)
        print(f"이진 파일 '{output_bin}' 저장이 완료되었습니다.")
        
        # 이진 파일 읽기 (rb 모드)
        with open(output_bin, 'rb') as f:
            loaded_data = pickle.load(f)
            print('\n[이진 파일에서 복구된 데이터 상위 3개]')
            for row in loaded_data[:3]:
                print(row)
    except Exception as e:
        print(f"이진 파일 처리 중 오류 발생: {e}")

if __name__ == '__main__':
    manage_mars_inventory()