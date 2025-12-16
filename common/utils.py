from typing import Any, Mapping


def dict_get(data: dict, path: str) -> Any:
    current = data
    for part in (segment for segment in path.split(".") if segment):
        if isinstance(current, Mapping):
            current = current.get(part)
        elif isinstance(current, list):
            try:
                index = int(part)
            except ValueError:
                return None
            if index < 0 or index >= len(current):
                return None
            current = current[index]
        else:
            return None

        if current is None:
            return None
    return current
