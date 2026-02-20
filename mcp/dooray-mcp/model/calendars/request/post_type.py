from enum import Enum

class PostType(str, Enum):
    to_me='toMe'
    to_cc_me='toCcMe'
    from_to_cc_me='fromToCcMe'
