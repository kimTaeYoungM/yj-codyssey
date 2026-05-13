# 문제 2-2: 카이사르 암호 해독 과정 정리

## 1. 과제 목표

이번 과제는 `emergency_storage_key` 폴더 안에 있는 `password.txt` 파일을 읽어 와서, 그 안에 들어 있는 카이사르 암호문을 해독하는 Python 프로그램을 작성하는 것입니다.

압축 파일을 해제하기 위한 바깥쪽 `password.txt`에는 `mars06`이라는 비밀번호가 들어 있고, 실제 Python 코드로 해독해야 하는 암호문은 `emergency_storage_key/password.txt` 안에 들어 있습니다.

---

## 2. 파일 구조 정리

현재 과제는 `problem 2 - 2` 폴더 안에서 수행합니다.

최종 파일 구조는 아래처럼 두는 것이 좋습니다.

```text
problem 2 - 2
├── emergency_storage_key
│   ├── password.txt        # 카이사르 암호문: B ehox Ftkl
│   └── result.txt          # 실행 후 생성되는 해독 결과 파일
├── door_hacking.py         # Python 코드 작성 파일
├── emergency_storage_key.zip
└── password.txt            # zip 파일 해제용 비밀번호: mars06
```

---

## 3. 각 파일의 역할

### 3.1 바깥쪽 password.txt

```text
problem 2 - 2/password.txt
```

이 파일에는 다음 내용이 들어 있습니다.

```text
mars06
```

이 파일은 `emergency_storage_key.zip` 압축 파일을 풀기 위한 비밀번호입니다.
Python 코드에서 읽어야 하는 대상이 아닙니다.

---

### 3.2 emergency_storage_key 폴더 안의 password.txt

```text
problem 2 - 2/emergency_storage_key/password.txt
```

이 파일에는 다음 카이사르 암호문이 들어 있습니다.

```text
B ehox Ftkl
```

Python 코드가 실제로 읽고 해독해야 하는 파일은 이 파일입니다.

---

## 4. Python 파일 이름

Python 파일 이름은 다음과 같이 작성합니다.

```text
door_hacking.py
```

파일 이름의 의미는 “문을 열기 위해 암호를 해독하는 프로그램”이라는 뜻이므로, 과제 스토리와 잘 어울립니다.

---

## 5. door_hacking.py 코드

`problem 2 - 2` 폴더 안에 `door_hacking.py` 파일을 만들고, 아래 코드를 작성합니다.

```python
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
```

---

## 6. 코드 설명

### 6.1 함수 정의

```python
def caesar_cipher_decode(target_text):
```

카이사르 암호를 해독하기 위한 함수입니다.
과제 조건에 맞게 함수 이름을 `caesar_cipher_decode`로 작성합니다.

---

### 6.2 0부터 25까지 모든 자리수 확인

```python
for shift in range(26):
```

카이사르 암호는 알파벳 26개를 기준으로 이동하기 때문에, 가능한 자리수는 `0`부터 `25`까지입니다.

따라서 모든 경우를 출력해서 사람이 직접 눈으로 읽을 수 있는 문장을 찾습니다.

---

### 6.3 대문자 처리

```python
if 'A' <= char <= 'Z':
    decoded_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
```

문자가 대문자라면 대문자 범위 안에서만 이동하도록 처리합니다.

예를 들어 `B`를 19칸 뒤로 이동하면 `I`가 됩니다.

---

### 6.4 소문자 처리

```python
elif 'a' <= char <= 'z':
    decoded_char = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
```

문자가 소문자라면 소문자 범위 안에서만 이동하도록 처리합니다.

---

### 6.5 공백 처리

```python
else:
    result += char
```

공백이나 특수문자는 알파벳이 아니므로 그대로 유지합니다.

예를 들어 `B ehox Ftkl`에서 단어 사이의 공백은 그대로 남습니다.

---

### 6.6 파일 읽기

```python
with open('emergency_storage_key/password.txt', 'r') as file:
    encrypted_text = file.read().strip()
```

현재 실행 위치가 `problem 2 - 2` 폴더이므로, 하위 폴더인 `emergency_storage_key` 안의 `password.txt`를 읽습니다.

중요한 점은 바깥쪽 `password.txt`가 아니라 아래 파일을 읽어야 한다는 것입니다.

```text
emergency_storage_key/password.txt
```

---

### 6.7 최종 결과 저장

```python
with open('emergency_storage_key/result.txt', 'w') as file:
    file.write(result)
```

눈으로 확인한 자리수를 입력하면, 해당 자리수로 복호화한 최종 결과를 `result.txt`에 저장합니다.

최종 파일은 아래 위치에 생성됩니다.

```text
emergency_storage_key/result.txt
```

---

## 7. 실행 방법

VS Code 터미널에서 현재 위치가 `problem 2 - 2` 폴더인지 확인합니다.

터미널에 아래처럼 보이면 정상입니다.

```bash
/c/codyssey/problem essential/problem 2 - 2
```

그다음 아래 명령어로 실행합니다.

```bash
python door_hacking.py
```

만약 `python` 명령어가 작동하지 않으면 아래 명령어를 사용합니다.

```bash
python3 door_hacking.py
```

---

## 8. 실행 결과

실행하면 아래처럼 0부터 25까지 모든 해독 결과가 출력됩니다.

```text
13: O rubk Sgxy
14: N qtaj Rfwx
15: M pszi Qevw
16: L oryh Pduv
17: K nqxg Octu
18: J mpwf Nbst
19: I love Mars
20: H knud Lzqr
21: G jmtc Kypq
22: F ilsb Jxop
23: E hkra Iwno
24: D gjqz Hvmn
25: C fipy Gulm
눈으로 확인 가능한 암호의 자리수를 입력하세요:
```

여기서 사람이 읽을 수 있는 문장은 다음 줄입니다.

```text
19: I love Mars
```

따라서 입력 칸에 `19`를 입력하고 Enter를 누릅니다.

```text
눈으로 확인 가능한 암호의 자리수를 입력하세요: 19
```

---

## 9. 최종 결과

정상 실행되면 아래와 같은 문구가 출력됩니다.

```text
최종 암호가 emergency_storage_key/result.txt 파일에 저장되었습니다.
최종 암호: I love Mars
```

그리고 아래 위치에 `result.txt` 파일이 생성됩니다.

```text
problem 2 - 2
└── emergency_storage_key
    ├── password.txt
    └── result.txt
```

`result.txt` 안에는 다음 내용이 저장됩니다.

```text
I love Mars
```

---

## 10. 정리

이번 과제에서 중요한 핵심은 다음과 같습니다.

1. 바깥쪽 `password.txt`는 zip 파일 해제용 비밀번호 파일입니다.
2. Python 코드가 읽어야 하는 파일은 `emergency_storage_key/password.txt`입니다.
3. 카이사르 암호문은 `B ehox Ftkl`입니다.
4. 모든 자리수를 출력하면 `19: I love Mars`가 나옵니다.
5. 따라서 최종 입력값은 `19`입니다.
6. 최종 결과는 `emergency_storage_key/result.txt`에 저장됩니다.

---

## 11. 제출 전 확인 사항

제출 전에 아래 내용을 확인합니다.

```text
problem 2 - 2
├── emergency_storage_key
│   ├── password.txt
│   └── result.txt
├── door_hacking.py
├── emergency_storage_key.zip
└── password.txt
```

확인해야 할 내용은 다음과 같습니다.

- `door_hacking.py` 파일이 존재하는지 확인합니다.
- `emergency_storage_key/password.txt` 안에 `B ehox Ftkl`이 있는지 확인합니다.
- 프로그램 실행 후 `emergency_storage_key/result.txt` 파일이 생성되었는지 확인합니다.
- `result.txt` 안에 `I love Mars`가 저장되어 있는지 확인합니다.
- 실행 중 경고 메시지나 오류 메시지가 없는지 확인합니다.
