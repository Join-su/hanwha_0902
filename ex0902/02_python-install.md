# 파이썬 설치 방법

## 설치 (python.org)
1. `python.org` 접속 → Downloads
2. Python 3.12.10 설치 파일 다운로드
3. 설치 실행 (Windows는 `Add python.exe to PATH` 체크)

## venv 만들기 / 활성화 / 비활성화
```bash
# 만들기
python -m venv venv

# 활성화 (Windows)
venv\Scripts\activate

# 활성화 (Mac/Linux)
source venv/bin/activate

# 비활성화
deactivate
```
