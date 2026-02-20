from pydantic import BaseModel
from typing import Any
import jsonref

# model_json_schema 함수 호출 시, jsonref 를 사용하여 $defs, #ref를 제거하고 완전한 스키마를 리턴하는 모델.
class DerefModel(BaseModel):
    @classmethod
    def model_json_schema(cls, *args, **kwargs) -> dict[str, Any]:
        d: dict[str, Any] = jsonref.replace_refs(super().model_json_schema(*args, **kwargs), proxies=False) # type: ignore
        d.pop('$defs', None)
        return d
