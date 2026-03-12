import os

def anaylze_mission_log():
    file_name = 'mission_computer_main.log'
    error_file_name = 'error_log.txt'

    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            lines = f.readlines()

            if not lines:
                print('Empty Log File')
                return

            # Full Content Print
            print('=== [Full Log Content Print] ===')
            for line in lines:
                print(line.strip())

            # Data Main Content Distribute (If First Line Header)
            header = lines[0]
            log_data = lines[1:]

            # Bonus Homework: Trouble Parts(unstable, explosion)
            with open(error_file_name, 'w', encoding='utf-8') as ef:
                print('\n=== [Trouble Works Log] ===')
                for line in log_data:
                    if 'unstable' in line or 'explosion' in line:
                        ef.write(line)
                        print(f'Detect Part: {line.strip()}')
                    print(f'Import Complete: {error_file_name} save in')

    except FileNotFoundError:
        print(f'Error: {file_name} cannot find that file')
    except Exception as e:
        print(f'UnSeen Trouble: {e}')

if __name__ == '__main__':
    anaylze_mission_log()