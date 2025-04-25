from dataclasses import dataclass, field
from typing import List, Literal

# Constants
VALID_RETURNS = {"FILE", "JSON", "TEXT", "HTML"}
VALID_ACCEPTS = {
    "application/json",
    "application/xml",
    "application/x-www-form-urlencoded",
    "multipart/form-data",
    "text/plain"
}

# Literal types
AcceptType = Literal[
    "application/json",
    "application/xml",
    "application/x-www-form-urlencoded",
    "multipart/form-data",
    "text/plain"
]

ProduceTypeLiteral = Literal["FILE", "JSON", "TEXT", "HTML"]

@dataclass(frozen=True)
class ProduceType:
    value: ProduceTypeLiteral

    def __str__(self) -> str:
        return self.value
    
@dataclass(frozen=True)
class ConsumeType:
    value: AcceptType

    def __str__(self) -> str:
        return self.value
    
@dataclass
class Link:
    path     : str
    methods  : List[str] = field(default_factory=list)
    produces : List[ProduceType] = field(default_factory=list)
    consumes : List[ConsumeType] = field(default_factory=list)

    def __post_init__(self):
        invalid_produces = [r for r in self.produces if str(r) not in VALID_RETURNS]
        if invalid_produces:
            raise ValueError(f"Invalid produces value(s): {invalid_produces}. Must be one or more of {VALID_RETURNS}")

        invalid_consumes = [c for c in self.consumes if str(c) not in VALID_ACCEPTS]
        if invalid_consumes:
            raise ValueError(f"Invalid consumes value(s): {invalid_consumes}. Must be one or more of {VALID_ACCEPTS}")


    def as_dict(self):
        return {
            "path"     : self.path,
            "methods"  : self.methods,
            "produces" : [str(r) for r in self.produces],
            "consumes" : [str(c) for c in self.consumes]
        }
