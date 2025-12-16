from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import urlencode, urlparse, urlunparse

import scrapy

from common.utils import dict_get


def _field_name(path: str) -> str:
    parts = [segment for segment in path.split(".") if segment]
    return parts[-1] if parts else path


class CommonSpider(scrapy.Spider):
    name = "common"

    def __init__(self, name, **kwargs) -> None:
        super().__init__(**kwargs)
        self.name = name.strip()

    def start_requests(self):
        template_path = (
            Path(__file__).resolve().parent.parent
            / "templates"
            / f"{self.name}.json"
        )

        with template_path.open("r", encoding="utf-8") as fp:
            template = json.load(fp)

        yield self._build_request(template, first_page=True)

    def _build_request(
        self, template: Mapping[str, Any], first_page: bool = False
    ) -> scrapy.Request:
        request_template = template["request"]
        method = (request_template.get("method") or "GET").upper()
        url = request_template.get("url")
        if not isinstance(url, str) or not url:
            raise RuntimeError(f"Template {self.template_name} is missing request.url")

        payload = request_template.get("queryDict")
        body: bytes | None = None
        final_url = url

        if first_page:
            pagination = request_template.get("pagination")
            if pagination["mode"] == "offset":
                payload.pop(pagination["offset"], None)
            elif pagination["mode"] == "page":
                payload[pagination["page"]] = 1

        if isinstance(payload, Mapping) and payload:
            if method == "GET":
                final_url = self._build_query_url(url, payload)
            else:
                body = json.dumps(payload, separators=(",", ":")).encode("utf-8")

        return scrapy.Request(
            final_url,
            method=method,
            body=body,
            callback=self.parse_response,
            headers=request_template.get("headersDict"),
            meta={"proxy": self.proxy, "template": template},
        )

    def parse_response(self, response: scrapy.http.Response):
        payload = response.json()
        template = response.meta["template"]
        result = self._extract_result(payload, template["response"])

        if not result:
            return

        for item in result:
            yield item

        template["last_page_size"] = len(result)
        # Paginate to next page.
        yield self._get_next_page(template)

    def _get_next_page(self, template):
        request_template = template.get("request")
        pagination = request_template.get("pagination")
        payload_template = request_template.get("queryDict")
        payload = {**payload_template}

        if pagination["mode"] == "page":
            page_key = pagination["page"]
            current_page_raw = payload_template.get(page_key) or 1
            current_page = int(current_page_raw)
            payload[page_key] = (current_page + 1,)

        elif pagination["mode"] == "offset":
            offset_key = pagination["offset"]
            current_offset_raw = payload_template.get(offset_key) or 0

            next_offset = int(current_offset_raw)
            if pagination.get("limit"):
                limit_key = pagination["limit"]
                limit_raw = payload_template[limit_key]
                limit = int(limit_raw)
                next_offset += limit
            else:
                next_offset += template["last_page_size"]

            payload[offset_key] = next_offset
        else:
            raise Exception(f"Unknown pagination mode: {pagination['mode']}")

        next_template = {
            **template,
            "request": {
                **request_template,
                "queryDict": payload,
            },
        }

        return self._build_request(next_template)

    def _extract_result(
        self, payload: Any, response_template: Mapping[str, Any] | None
    ) -> Any:
        extract_rules = response_template.get("$extract")
        if not isinstance(extract_rules, Mapping):
            raise Exception(f"extract_rules must be a dict: {extract_rules}")

        list_path = extract_rules.get("$list")
        if not isinstance(list_path, str):
            raise Exception(f"list_path must be a str: {list_path}")

        includes = extract_rules.get("$include") or []
        items = dict_get(payload, list_path)
        if items is None:
            raise Exception(
                f"No items is found for: ${list_path} in payload: ${payload}"
            )

        result = []
        base_values = self._extract_base_values(payload, includes)
        item_paths = self._get_item_paths(includes)

        for entry in items:
            current_item = {**base_values, "data": entry}
            for path, name in item_paths:
                current_item[name] = dict_get(entry, path)

            result.append(current_item)

        return result

    def _extract_base_values(self, payload, includes: list):
        base_values: dict[str, Any] = {}
        for include in includes:
            if isinstance(include, str):
                value = dict_get(payload, include)
                base_values[_field_name(include)] = value

        return base_values

    def _get_item_paths(self, includes: Any) -> list[tuple[str, str]]:
        if not isinstance(includes, list):
            return []

        item_paths: list[tuple[str, str]] = []
        for include in includes:
            if not isinstance(include, Mapping):
                continue

            per_item = include.get("$item")
            if not isinstance(per_item, list):
                continue

            for path in per_item:
                if isinstance(path, str):
                    item_paths.append((path, _field_name(path)))

        return item_paths

    def _build_query_url(self, url: str, params: Mapping[str, Any]) -> str:
        parsed = urlparse(url)
        payload = {
            key: value if isinstance(value, str) else json.dumps(value)
            for key, value in params.items()
        }
        query = urlencode(payload, doseq=True)
        return urlunparse(parsed._replace(query=query))
