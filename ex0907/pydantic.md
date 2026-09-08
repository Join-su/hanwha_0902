# Pydantic: 데이터가 들어오기 전에 한 번 확인하는 도구

> 이 노트는 수업에서 다룬 FastAPI 서비스 흐름과 Pydantic 공식 문서를 바탕으로 정리했습니다.[1][2]

## 1. Pydantic은 왜 사용할까?

웹 서비스에서는 화면, API, 데이터베이스처럼 여러 곳에서 데이터가 들어옵니다. 예를 들어 회원가입 요청에 `나이`가 숫자인지, 이메일이 비어 있지 않은지, 날짜 형식이 맞는지 확인해야 합니다.

Pydantic은 Python의 **타입 힌트**를 이용해 이 확인 작업을 도와주는 라이브러리입니다. 우리가 모델에 `id: int`, `name: str`처럼 작성하면 Pydantic이 데이터를 받아서 형식과 조건을 검사하고, 통과한 데이터를 모델 객체로 만들어 줍니다.[2][3]

수업에서 본 서비스 흐름으로 보면 다음 위치에 들어갑니다.[1]

```text
Streamlit 화면
   ↓ HTTP / JSON 요청
FastAPI API
   ↓
Pydantic 검증  ← 요청 데이터가 이 단계에서 확인됨
   ↓
비즈니스 로직 / 외부 AI API / DB
```

핵심은 **검증되지 않은 데이터를 바로 DB나 AI API로 보내지 않는 것**입니다. 먼저 Pydantic으로 형식을 맞춘 뒤 다음 작업을 진행하면 오류를 초기에 찾기 쉬워집니다.

---

## 2. 가장 기본: `BaseModel`

Pydantic에서는 보통 `BaseModel`을 상속해 데이터의 모양을 만듭니다.

```python
from datetime import datetime
from pydantic import BaseModel, PositiveInt


class User(BaseModel):
    id: int
    name: str = "John Doe"          # 값이 없으면 기본값 사용
    signup_ts: datetime | None       # 날짜 또는 None
    tastes: dict[str, PositiveInt]   # 값은 0보다 큰 정수여야 함


external_data = {
    "id": 123,
    "signup_ts": "2019-06-01 12:22",
    "tastes": {
        "wine": 9,
        "cheese": 7,
        "cabbage": "1",
    },
}

user = User(**external_data)

print(user.id)            # 123
print(user.name)          # John Doe
print(user.model_dump())  # 모델을 dict 형태로 꺼냄
```

여기서 볼 점은 `signup_ts`에 문자열이 들어왔지만 `datetime`으로 처리되고, `cabbage`의 문자열 `"1"`도 정수로 변환될 수 있다는 점입니다. 기본 설정에서는 가능한 경우 타입에 맞게 변환한 **결과 데이터**를 만들어 줍니다. 그래서 Pydantic의 검증은 “입력값을 그대로 통과시키는가”보다 “최종 결과가 선언한 타입과 조건을 만족하는가”에 가깝습니다.[1][3]

> `PositiveInt`는 0보다 큰 정수만 허용하는 타입입니다. 점수, 수량, 주문 개수처럼 음수가 되면 안 되는 값에 사용할 수 있습니다.[1]

---

## 3. 데이터가 잘못되면: `ValidationError`

형식이 맞지 않거나 필수 값이 빠지면 Pydantic은 `ValidationError`를 발생시킵니다. 한 번에 여러 오류를 알려주므로, 어디를 고쳐야 하는지 확인하기 좋습니다.[3]

```python
from pydantic import BaseModel, PositiveInt, ValidationError


class User(BaseModel):
    id: int
    name: str = "John Doe"
    signup_ts: str | None
    tastes: dict[str, PositiveInt]


bad_data = {
    "id": "not an int",
    "tastes": {},
}

try:
    User(**bad_data)
except ValidationError as e:
    print(e.errors())
```

위 코드에서는 `id`가 정수로 바뀔 수 없는 문자열이고, `signup_ts`도 제공되지 않았기 때문에 오류가 나옵니다.

FastAPI에서는 이런 검증 오류를 활용해 API 요청이 잘못되었을 때 클라이언트에게 어떤 필드가 문제인지 알려줄 수 있습니다. 즉, 서버 코드가 깊이 실행된 뒤 실패하기보다 **입구에서 요청을 걸러 주는 역할**을 합니다.[1][3]

---

## 4. 조건을 더 붙이기: `Annotated`와 `Field`

타입만으로 부족할 때는 값의 조건도 적을 수 있습니다. 예를 들어 과일 색은 정해진 값 중 하나여야 하고, 무게는 0보다 커야 할 수 있습니다.

```python
from typing import Annotated, Literal
from pydantic import BaseModel, Field


class Fruit(BaseModel):
    name: str
    color: Literal["red", "green"]
    weight: Annotated[float, Field(gt=0)]


apple = Fruit(name="Apple", color="red", weight=4.2)
print(apple)
```

- `Literal["red", "green"]`: 색은 `red` 또는 `green`만 허용합니다.
- `Field(gt=0)`: `weight`는 0보다 커야 합니다. `gt`는 **greater than**의 약자입니다.
- `Annotated[...]`: 원래 타입에 추가 조건을 붙일 때 사용합니다.

수업 예제의 `Annotated[float, Gt(0)]`도 같은 목적입니다. 교육 초반에는 `Field(gt=0)`처럼 Pydantic 안에서 바로 읽히는 방식부터 사용해도 충분합니다.[1][2]

---

## 5. 조금 더 복잡한 규칙: validator

가끔은 타입과 간단한 조건만으로 부족합니다. 예를 들면 “비밀번호 확인 값이 비밀번호와 같아야 한다”, “닉네임 앞뒤 공백을 지운다” 같은 규칙입니다.

이럴 때 validator를 사용합니다. 필드 하나에 적용하는 `@field_validator`와 여러 필드를 함께 확인하는 `@model_validator`가 있습니다.[4]

```python
from typing_extensions import Self
from pydantic import BaseModel, model_validator


class SignupRequest(BaseModel):
    password: str
    password_repeat: str

    @model_validator(mode="after")
    def passwords_match(self) -> Self:
        if self.password != self.password_repeat:
            raise ValueError("비밀번호가 서로 다릅니다.")
        return self
```

처음에는 validator를 많이 쓰기보다 다음 순서로 생각하면 좋습니다.

1. 먼저 타입 힌트로 해결할 수 있는지 확인한다.
2. `Field`나 `PositiveInt` 같은 조건 타입으로 해결할 수 있는지 본다.
3. 여러 값의 관계처럼 정말 필요한 경우에만 validator를 추가한다.

validator는 검증한 뒤에는 **검증된 값을 반환**해야 합니다. 그리고 `before`, `after`, `plain`, `wrap`처럼 실행 위치가 나뉘지만, 초반에는 보통 `after` 규칙부터 익히면 됩니다.[4]

---

## 6. 실습에서 기억할 포인트

- Pydantic은 FastAPI에서 요청·응답 데이터의 형식을 정리할 때 특히 자주 사용합니다.[1]
- `BaseModel`은 “이 데이터에 어떤 필드가 있어야 하는지”를 선언하는 시작점입니다.[3]
- 기본값을 주고 싶으면 `name: str = "기본값"`처럼 작성합니다.
- 선택 가능한 값은 `str | None`처럼 표시할 수 있습니다.
- 검증된 모델을 딕셔너리로 바꾸려면 `model_dump()`를 사용합니다.[1][3]
- 오류 내용을 볼 때는 `ValidationError`의 `errors()`가 유용합니다.[1][3]
- 타입 변환을 원하지 않는 상황에서는 strict 모드도 사용할 수 있지만, 처음에는 어떤 값이 자동 변환되는지 먼저 이해하는 것이 좋습니다.[2]

