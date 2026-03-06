# 포커리그 그룹 배치 개선안

## 개요

각 회차가 끝난 후 승강 처리 → 다음 회차 그룹 재배치 시 사용하는 알고리즘.
**잔여 인원 분산 흡수 방식**으로 빈 그룹 생성 없이 균등 배치.

---

## 핵심 파라미터

| 파라미터 | 값 | 설명 |
|---|---|---|
| `max_size` | 22 | 그룹당 최대 허용 인원 |
| `min_size` | 8 (권장) | 그룹당 최소 인원 (이하면 n 축소) |
| 승격 비율 | 25% | `ceil(group_size × 0.25)` |
| 강등 비율 | 20% | `ceil(group_size × 0.20)` |

---

## 그룹 수 결정 로직

```python
import math

def calc_groups(total: int, max_size: int = 22, min_size: int = 8) -> int:
    n = math.ceil(total / max_size)
    # min_size 미달 시 그룹 수 축소
    while n > 1 and math.ceil(total / n) < min_size:
        n -= 1
    return n
```

---

## 인원 분배 로직 (잔여 분산 흡수)

```python
def distribute(total: int, n: int) -> list[int]:
    """
    총 인원을 n개 그룹에 균등 분배.
    나머지는 앞 그룹부터 1명씩 흡수.
    """
    base = total // n
    remainder = total % n
    sizes = []
    for i in range(n):
        sizes.append(base + (1 if i < remainder else 0))
    return sizes  # 예: total=50, n=3 → [17, 17, 16]
```

---

## 승강 슬롯 계산

```python
def calc_slots(group_size: int) -> dict:
    return {
        "promote": math.ceil(group_size * 0.25),   # 상위 리그 승격
        "relegate": math.ceil(group_size * 0.20),  # 하위 리그 강등
    }
```

**예시 (22명 그룹):**
- 승격: `ceil(22 × 0.25)` = 6명
- 강등: `ceil(22 × 0.20)` = 5명

---

## 전체 배치 예시

| 총 인원 | 그룹 수 (n) | 그룹 크기 |
|---|---|---|
| 100명 | 5 | [20, 20, 20, 20, 20] |
| 50명 | 3 | [17, 17, 16] |
| 65명 | 3 | [22, 22, 21] |
| 23명 | 2 | [12, 11] |
| 10명 | 1 | [10] |

---

## 배치 순서

1. 전체 참가자 점수순 정렬
2. `calc_groups(total)`으로 그룹 수 결정
3. `distribute(total, n)`으로 각 그룹 인원 수 확정
4. 상위 그룹부터 순서대로 배치 (1위 → A그룹, ...)
5. 각 그룹 내 `calc_slots()`으로 승강 슬롯 표시

---

## 이전 세션 논의 컨텍스트

- 2026-03-06 대화에서 설계
- 한게임포커 포커리그 시뮬레이션용
- 관련 파일: `C:\Users\NHN\Desktop\포커리그 시뮬레이션.xlsx`
