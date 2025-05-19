from typing import TypeVar

from fastapi import HTTPException, status


T = TypeVar("T")


def or_404(result: T | None, message="Not found") -> T:
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=message
        )
    return result
