from flask import jsonify, request
from typing import Callable , Dict , Any

def produces(*types: str):
    def decorator(f):
        f._produce_type = list(types)
        return f
    return decorator

def consumes(*types: str):
    def decorator(f: Callable):
        f._consume_type = list(types)
        return f
    return decorator