# async, Pydantic, FastAPI 한 번에 이해하기

async, Pydantic, FastAPI는 역할이 서로 다르지만, 웹 API를 만들 때 한 팀처럼 자주 함께 사용됩니다.

아주 쉽게 말하면:

- **FastAPI**: 손님 주문을 받는 식당
- **Pydantic**: 주문서가 제대로 작성됐는지 확인하는 직원
- **async**: 음식이 만들어지는 동안 다른 손님 주문도 받는 방식

---

## 1. FastAPI는 무엇인가요?

FastAPI는 Python으로 **웹 API 서버**를 만드는 도구입니다.

API는 쉽게 말해 컴퓨터끼리 대화하는 창구입니다.

예를 들어 손님이 이런 주문을 보냅니다.

```json
{
  "name": "사과",
  "count": 3
}
```

FastAPI는 이 요청을 받고, 우리가 만든 Python 함수를 실행해 줍니다.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "안녕하세요"}
```

이 코드는 다음과 같은 뜻입니다.

> 누군가 `/` 주소로 오면 "안녕하세요"라고 대답해 주세요.

---

## 2. Pydantic은 무엇인가요?

Pydantic은 들어온 데이터가 **약속한 모양인지 검사하는 도구**입니다.

어린이집 선생님이 준비물 목록을 검사한다고 생각하면 됩니다.

> 이름은 꼭 있어야 해요.
> 수량은 숫자여야 해요.
> 수량은 0보다 커야 해요.

Pydantic으로 규칙을 적습니다.

```python
from pydantic import BaseModel, Field

class Order(BaseModel):
    name: str
    count: int = Field(gt=0)
```

이 뜻은 다음과 같습니다.

- `name`: 문자열이어야 함
- `count`: 숫자여야 함
- `count`: 0보다 커야 함

정상적인 데이터:

```json
{
  "name": "사과",
  "count": 3
}
```

잘못된 데이터:

```json
{
  "name": "사과",
  "count": -2
}
```

`-2`는 0보다 크지 않으므로 Pydantic이 알려줍니다.

> "이 주문서는 잘못됐어요."

---

## 3. async는 무엇인가요?

async는 **기다리는 동안 다른 일을 할 수 있게 하는 Python 기능**입니다.

예를 들어 식당에서 음식이 완성되기까지 5분이 걸린다고 해보겠습니다.

**나쁜 웨이터**

1. 첫 번째 손님 주문 받기
2. 음식이 나올 때까지 가만히 기다리기
3. 음식 전달하기
4. 그다음 손님 주문 받기

**좋은 웨이터**

1. 첫 번째 손님 주문 받기
2. 음식이 나오는 동안 두 번째 손님 주문 받기
3. 또 기다리는 동안 세 번째 손님 주문 받기
4. 음식이 준비되면 전달하기

이런 식으로 **네트워크, 데이터베이스, 외부 API 응답을 기다리는 동안 다른 요청을 처리**하는 것이 async의 핵심입니다.

```python
import asyncio

async def make_food():
    await asyncio.sleep(3)
    return "음식 완성"
```

여기서:

- `async def`: 이 함수는 기다릴 수 있는 함수예요.
- `await`: 여기서 잠깐 기다리지만, 다른 일을 해도 돼요.

단, async가 붙었다고 무조건 빨라지는 것은 아닙니다.

- 데이터베이스 응답 기다리기 → async가 유용함
- 외부 API 응답 기다리기 → async가 유용함
- 아주 오래 걸리는 계산 → async만으로 해결되지 않음

---

## 4. 세 가지를 함께 사용하는 예제

사과 주문 API를 만들어 보겠습니다.

```python
import asyncio

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Order(BaseModel):
    name: str
    count: int = Field(gt=0)


class Receipt(BaseModel):
    message: str
    total_price: int


@app.post("/orders", response_model=Receipt)
async def create_order(order: Order) -> Receipt:
    # 음식점이나 데이터베이스에 주문을 전달한다고 가정
    await asyncio.sleep(1)

    total_price = order.count * 1000

    return Receipt(
        message=f"{order.name} {order.count}개 주문 완료",
        total_price=total_price,
    )
```

---

## 5. 요청이 들어오면 무슨 일이 생길까요?

손님이 다음 주문을 보냅니다.

```json
{
  "name": "사과",
  "count": 3
}
```

### 1단계: FastAPI가 주문을 받습니다

```python
@app.post("/orders")
```

이 부분은 이렇게 말하는 것입니다.

> `/orders` 주소로 POST 주문이 오면 이 함수를 실행하세요.

### 2단계: Pydantic이 주문서를 검사합니다

```python
order: Order
```

FastAPI는 `Order`라는 Pydantic 모델을 보고 데이터를 검사합니다.

검사 내용:

- `name`이 있는가?
- `name`은 글자인가?
- `count`가 있는가?
- `count`는 숫자인가?
- `count`가 0보다 큰가?

정상이라면 Python 객체로 바꿔 줍니다.

```python
order.name   # "사과"
order.count  # 3
```

### 3단계: async 함수가 실행됩니다

```python
async def create_order(...)
```

이 함수는 주문 처리 중에 기다려야 하는 일이 있어도, 서버가 다른 손님을 받을 수 있게 합니다.

```python
await asyncio.sleep(1)
```

실제 프로그램에서는 이 자리에 다음과 같은 코드가 들어갈 수 있습니다.

```python
await database.save(order)
```

또는:

```python
result = await payment_api.pay()
```

### 4단계: 계산하고 응답합니다

```python
total_price = order.count * 1000
```

사과 3개이므로 가격은 3,000원입니다.

응답:

```json
{
  "message": "사과 3개 주문 완료",
  "total_price": 3000
}
```

### 5단계: Pydantic이 응답도 확인합니다

```python
response_model=Receipt
```

이 부분은 말하자면:

> 손님에게 보여줄 영수증도 정해진 모양으로 만들어 주세요.

응답에 다음 두 값이 있는지 확인합니다.

- `message`: 문자열
- `total_price`: 숫자

즉, Pydantic은 **들어오는 데이터뿐 아니라 나가는 데이터도 정리**할 수 있습니다.

---

## 6. 세 가지의 관계

전체 흐름은 이렇게 볼 수 있습니다.

```text
손님
  ↓
주문 데이터(JSON)
  ↓
FastAPI
  ↓
Pydantic이 주문서 검사
  ↓
async 함수가 기다리는 동안 다른 손님 처리
  ↓
Pydantic이 영수증 모양 검사
  ↓
JSON 응답
```

역할을 다시 정리하면:

```text
FastAPI  = 웹 요청을 받고 함수를 연결하는 담당
Pydantic = 데이터 모양과 값이 맞는지 검사하는 담당
async    = 기다리는 동안 다른 일을 처리하는 담당
```

---

## 7. 잘못된 주문은 어떻게 될까요?

이런 요청을 보내면:

```json
{
  "name": "사과",
  "count": -2
}
```

`count`는 0보다 커야 하는데 `-2`이므로 FastAPI와 Pydantic이 자동으로 오류를 돌려줍니다.

대략 이런 형태입니다. (HTTP 상태 코드 `422 Unprocessable Entity`)

```json
{
  "detail": [
    {
      "type": "greater_than",
      "loc": ["body", "count"],
      "msg": "Input should be greater than 0",
      "input": -2,
      "ctx": { "gt": 0 }
    }
  ]
}
```

읽어보면 이런 뜻입니다.

> 요청 본문(body)의 `count` 값이 잘못됐어요. 0보다 큰 값이어야 하는데 `-2`가 들어왔어요.

중요한 점은, 우리가 오류 처리 코드를 따로 쓰지 않아도 **모델만 잘 정의해 두면 검증과 오류 응답이 자동으로 처리된다**는 것입니다.

---

## 8. 한 줄 정리

| 이름 | 한 마디로 | 언제 필요한가 |
| --- | --- | --- |
| FastAPI | 요청을 받아 함수로 연결하는 웹 프레임워크 | 웹 API 서버를 만들 때 |
| Pydantic | 데이터의 모양과 값을 검사하는 도구 | 입력·출력 데이터를 믿을 수 있게 만들 때 |
| async | 기다리는 동안 다른 일을 하는 방식 | DB·외부 API 응답을 기다릴 때 |

세 가지는 경쟁 관계가 아니라, **요청 받기(FastAPI) → 데이터 검증(Pydantic) → 효율적인 대기(async)** 로 이어지는 한 팀입니다.
