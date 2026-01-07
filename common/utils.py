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


def dict_merge(base: Mapping[str, Any], override: Mapping[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in override.items():
        base_value = merged.get(key)
        if isinstance(base_value, Mapping) and isinstance(value, Mapping):
            merged[key] = dict_merge(base_value, value)
        else:
            merged[key] = value

    return merged


def field_name(path: str) -> str:
    parts = [segment for segment in path.split(".") if segment]
    return parts[-1] if parts else path
