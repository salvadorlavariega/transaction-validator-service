from dataclasses import dataclass
from typing import Optional

@dataclass
class ValidationContext:
    isValid: bool = True
    error_message: Optional[str] = None
    failed_rule: Optional[str] = None