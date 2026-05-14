# 문제 2-2: 카이사르 암호 해독 및 보너스 과제 수행 과정 정리

## 1. 과제 목표

이번 과제는 `emergency_storage_key` 폴더 안에 있는 `password.txt` 파일을 읽어 와서, 그 안에 들어 있는 카이사르 암호문을 해독하는 Python 프로그램을 작성하는 것입니다.

기본 과제에서는 `0`부터 `25`까지 모든 자리수를 출력한 뒤 사람이 직접 정답을 확인합니다.

보너스 과제에서는 `dictionary.txt`라는 텍스트 사전을 만들고, 복호화 결과 안에 사전에 있는 단어와 일치하는 키워드가 발견되면 반복을 멈추도록 수정합니다.

즉, 보너스 과제의 핵심은 다음과 같습니다.

```text
카이사르 암호문 복호화
→ 각 자리수 결과 확인
→ dictionary.txt의 단어와 비교
→ 일치하는 단어 발견 시 반복 중단
→ result.txt에 최종 결과 저장
```

---

## 2. 파일 구조 정리

현재 과제는 `problem 2 - 2` 폴더 안에서 수행합니다.

보너스 과제까지 포함한 최종 파일 구조는 아래처럼 구성합니다.

```text
problem 2 - 2
├── emergency_storage_key
│   ├── password.txt        # 카이사르 암호문: B ehox Ftkl
│   ├── dictionary.txt      # 보너스 과제용 텍스트 사전
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

따라서 Python 코드에서 읽어야 하는 대상이 아닙니다.

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

### 3.3 emergency_storage_key 폴더 안의 dictionary.txt

```text
problem 2 - 2/emergency_storage_key/dictionary.txt
```

이 파일은 보너스 과제에서 사용하는 텍스트 사전입니다.

복호화 결과 안에 이 파일에 적힌 단어가 포함되어 있으면, 프로그램은 그 결과를 정답 후보로 판단하고 반복을 멈춥니다.

예시는 아래와 같습니다.

```text
mars
earth
moon
space
rocket
storage
emergency
password
security
system
key
secret
decode
mission
launch
base
station
oxygen
planet
backup
data
file
code
access
admin
```

이번 암호문을 복호화하면 `I love Mars`가 나오므로, `dictionary.txt` 안에 `mars`가 들어 있어야 자동으로 정답을 찾을 수 있습니다.

---

## 4. Python 파일 이름

Python 파일 이름은 다음과 같이 작성합니다.

```text
door_hacking.py
```

파일 이름의 의미는 “문을 열기 위해 암호를 해독하는 프로그램”이라는 뜻이므로, 과제 스토리와 잘 어울립니다.

---

## 5. 보너스 과제용 door_hacking.py 코드

`problem 2 - 2` 폴더 안에 `door_hacking.py` 파일을 만들고, 아래 코드를 작성합니다.

```python
def caesar_decode(target_text, shift):
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

    return result


def load_dictionary(dictionary_path):
    words = []

    with open(dictionary_path, 'r', encoding='utf-8') as file:
        for line in file:
            word = line.strip()

            if word != '':
                words.append(word.lower())

    return words


def find_password_by_dictionary(encrypted_text, dictionary_words):
    for shift in range(26):
        decoded_text = caesar_decode(encrypted_text, shift)

        print(str(shift) + ': ' + decoded_text)

        for word in dictionary_words:
            if word in decoded_text.lower():
                print()
                print('사전에 있는 단어와 일치하는 키워드를 발견했습니다.')
                print('발견된 단어:', word)
                print('사용된 자리수:', shift)
                print('해독 결과:', decoded_text)

                return shift, decoded_text

    return None, None


try:
    password_path = 'emergency_storage_key/password.txt'
    dictionary_path = 'emergency_storage_key/dictionary.txt'
    result_path = 'emergency_storage_key/result.txt'

    with open(password_path, 'r', encoding='utf-8') as file:
        encrypted_text = file.read().strip()

    dictionary_words = load_dictionary(dictionary_path)

    print('암호문:', encrypted_text)
    print()
    print('카이사르 암호 해독 결과')
    print()

    shift, result = find_password_by_dictionary(encrypted_text, dictionary_words)

    if result is not None:
        with open(result_path, 'w', encoding='utf-8') as file:
            file.write(result)

        print()
        print('최종 암호가 emergency_storage_key/result.txt 파일에 저장되었습니다.')
        print('최종 암호:', result)

    else:
        print()
        print('사전에 있는 단어와 일치하는 키워드를 찾지 못했습니다.')
        print('dictionary.txt 파일에 더 많은 단어를 추가해 보십시오.')

except FileNotFoundError as error:
    print('필요한 파일을 찾을 수 없습니다.')
    print(error)

except Exception as error:
    print('오류가 발생했습니다.')
    print(error)
```

---

## 6. 코드 설명

### 6.1 caesar_decode 함수

```python
def caesar_decode(target_text, shift):
```

이 함수는 암호문과 자리수를 입력받아 해당 자리수만큼 카이사르 암호를 복호화합니다.

기본 과제 코드에서는 모든 자리수를 출력하는 함수가 중심이었지만, 보너스 과제에서는 각 자리수의 결과를 반환해야 하므로 `return result` 형태로 작성합니다.

---

### 6.2 대문자 처리

```python
if 'A' <= char <= 'Z':
    decoded_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
```

문자가 대문자라면 `A`부터 `Z` 범위 안에서만 이동하도록 처리합니다.

예를 들어 `B`를 19칸 복호화하면 `I`가 됩니다.

---

### 6.3 소문자 처리

```python
elif 'a' <= char <= 'z':
    decoded_char = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
```

문자가 소문자라면 `a`부터 `z` 범위 안에서만 이동하도록 처리합니다.

---

### 6.4 공백과 특수문자 처리

```python
else:
    result += char
```

공백이나 특수문자는 알파벳이 아니므로 그대로 유지합니다.

예를 들어 `B ehox Ftkl`에서 단어 사이의 공백은 그대로 남습니다.

---

### 6.5 dictionary.txt 읽기

```python
def load_dictionary(dictionary_path):
```

이 함수는 `dictionary.txt` 파일을 읽어서 단어 목록을 만듭니다.

```python
word = line.strip()

if word != '':
    words.append(word.lower())
```

각 줄의 단어를 읽고, 빈 줄은 제외합니다.

또한 `.lower()`를 사용하여 소문자로 변환합니다.

이렇게 하면 `Mars`, `MARS`, `mars`처럼 대소문자가 달라도 같은 단어로 비교할 수 있습니다.

---

### 6.6 사전 단어와 복호화 결과 비교

```python
if word in decoded_text.lower():
```

복호화 결과를 소문자로 바꾼 뒤, `dictionary.txt`에 있는 단어가 포함되어 있는지 확인합니다.

예를 들어 복호화 결과가 아래와 같다면

```text
I love Mars
```

프로그램 내부에서는 아래처럼 소문자로 바꾸어 비교합니다.

```text
i love mars
```

따라서 `dictionary.txt`에 `mars`가 있으면 일치한다고 판단할 수 있습니다.

---

### 6.7 일치하는 단어를 찾으면 반복 중단

```python
return shift, decoded_text
```

사전 단어와 일치하는 복호화 결과를 발견하면, 더 이상 `0`부터 `25`까지 반복할 필요가 없습니다.

그래서 `return`을 사용하여 함수 실행을 즉시 종료합니다.

이 부분이 보너스 과제 조건인 “단어와 일치하는 키워드가 암호 속에서 발견될 경우 반복을 멈출 수 있게 작성”에 해당합니다.

---

### 6.8 최종 결과 저장

```python
with open(result_path, 'w', encoding='utf-8') as file:
    file.write(result)
```

자동으로 찾은 최종 복호화 결과를 `emergency_storage_key/result.txt` 파일에 저장합니다.

---

## 7. 실행 방법

VS Code 터미널에서 현재 위치가 `problem 2 - 2` 폴더인지 확인합니다.

터미널 위치 예시는 아래와 같습니다.

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

## 8. 실행 결과 예시

실행하면 아래처럼 복호화 결과가 출력됩니다.

```text
암호문: B ehox Ftkl

카이사르 암호 해독 결과

0: B ehox Ftkl
1: A dgnw Esjk
2: Z cfmv Drij
3: Y belu Cqhi
4: X adkt Bpgh
5: W zcjs Aofg
6: V ybir Znef
7: U xahq Ymdf
8: T wzgp Xlce
9: S vyfo Wkbd
10: R uxen Vjac
11: Q twdm Uizb
12: P svcl Thya
13: O rubk Sgxz
14: N qtaj Rfwy
15: M pszi Qevx
16: L oryh Pduw
17: K nqxg Octv
18: J mpwf Nbsu
19: I love Mars

사전에 있는 단어와 일치하는 키워드를 발견했습니다.
발견된 단어: mars
사용된 자리수: 19
해독 결과: I love Mars

최종 암호가 emergency_storage_key/result.txt 파일에 저장되었습니다.
최종 암호: I love Mars
```

---

## 9. 최종 결과

정상 실행되면 아래 위치에 `result.txt` 파일이 생성됩니다.

```text
problem 2 - 2
└── emergency_storage_key
    ├── password.txt
    ├── dictionary.txt
    └── result.txt
```

`result.txt` 안에는 다음 내용이 저장됩니다.

```text
I love Mars
```

---

## 10. 기본 과제 코드와 보너스 과제 코드의 차이

| 구분 | 기본 과제 | 보너스 과제 |
|---|---|---|
| 해독 방식 | 0~25까지 모두 출력 | 0~25까지 확인하면서 사전 단어와 비교 |
| 정답 선택 | 사람이 직접 자리수 입력 | 프로그램이 사전 단어를 기준으로 자동 판단 |
| 추가 파일 | 없음 | `dictionary.txt` 필요 |
| 반복 중단 | 직접 입력 전까지 중단되지 않음 | 일치 단어 발견 시 자동 중단 |
| 결과 저장 | 사용자가 입력한 자리수로 저장 | 자동으로 찾은 결과를 저장 |

---

## 11. 보너스 과제 수행 시 주의 사항

1. `dictionary.txt`는 반드시 `emergency_storage_key` 폴더 안에 있어야 합니다.
2. `dictionary.txt` 안에는 정답에 포함될 만한 단어를 한 줄씩 작성합니다.
3. 이번 정답은 `I love Mars`이므로 `mars`가 들어 있어야 자동으로 찾을 수 있습니다.
4. Python 파일은 `problem 2 - 2` 폴더 안에서 실행해야 합니다.
5. 바깥쪽 `password.txt`는 zip 파일 해제용이고, 코드가 읽어야 하는 파일은 `emergency_storage_key/password.txt`입니다.

---

## 12. 제출 전 확인 사항

제출 전에 아래 파일 구조를 확인합니다.

```text
problem 2 - 2
├── emergency_storage_key
│   ├── password.txt
│   ├── dictionary.txt
│   └── result.txt
├── door_hacking.py
├── emergency_storage_key.zip
└── password.txt
```

확인해야 할 내용은 다음과 같습니다.

- `door_hacking.py` 파일이 존재하는지 확인합니다.
- `emergency_storage_key/password.txt` 안에 `B ehox Ftkl`이 있는지 확인합니다.
- `emergency_storage_key/dictionary.txt` 안에 `mars`가 있는지 확인합니다.
- 프로그램 실행 후 `emergency_storage_key/result.txt` 파일이 생성되었는지 확인합니다.
- `result.txt` 안에 `I love Mars`가 저장되어 있는지 확인합니다.
- 실행 중 경고 메시지나 오류 메시지가 없는지 확인합니다.

---

## 13. 최종 정리

이번 보너스 과제에서 중요한 핵심은 다음과 같습니다.

1. 텍스트 사전 파일인 `dictionary.txt`를 직접 만듭니다.
2. Python 코드에서 `dictionary.txt`를 읽어 단어 목록을 만듭니다.
3. 카이사르 암호문 `B ehox Ftkl`을 0부터 25까지 복호화합니다.
4. 복호화 결과 안에 사전 단어가 포함되어 있는지 검사합니다.
5. `mars`가 발견되는 `19: I love Mars`에서 반복을 멈춥니다.
6. 최종 결과를 `emergency_storage_key/result.txt`에 저장합니다.

따라서 보너스 과제는 단순히 모든 결과를 출력하는 것을 넘어서, 텍스트 사전을 이용해 정답을 자동으로 판별하도록 개선한 프로그램입니다.
