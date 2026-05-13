def caesar_cipher_decode(target_text):
    for shift in range(26):
        result = ''

        for char in target_text:
            if 'A' <= char <= 'Z':
                decoded_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
                result += decoded_char

            elif 'a' <= char <= 'z':
                decoded_char = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
                result += decoded_char

            else:
                result += char

        print(str(shift) + ': ' + result)


try:
    with open('emergency_storage_key/password.txt', 'r') as file:
        encrypted_text = file.read().strip()

    print('암호문:', encrypted_text)
    print('카이사르 암호 해독 결과')
    print()

    caesar_cipher_decode(encrypted_text)

    number = input('눈으로 확인 가능한 암호의 자리수를 입력하세요: ')

    if number.isdigit():
        shift = int(number)

        if 0 <= shift <= 25:
            result = ''

            for char in encrypted_text:
                if 'A' <= char <= 'Z':
                    decoded_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
                    result += decoded_char

                elif 'a' <= char <= 'z':
                    decoded_char = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
                    result += decoded_char

                else:
                    result += char

            with open('emergency_storage_key/result.txt', 'w') as file:
                file.write(result)

            print('최종 암호가 emergency_storage_key/result.txt 파일에 저장되었습니다.')
            print('최종 암호:', result)

        else:
            print('자리수는 0부터 25 사이의 숫자여야 합니다.')

    else:
        print('숫자만 입력해야 합니다.')

except FileNotFoundError:
    print('emergency_storage_key/password.txt 파일을 찾을 수 없습니다.')

except Exception as error:
    print('오류가 발생했습니다.')
    print(error)