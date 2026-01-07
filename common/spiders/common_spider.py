from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import urlencode, urlparse, urlunparse

import scrapy

from common.utils import dict_get, dict_merge
from common.settings import PROXY


class CommonSpider(scrapy.Spider):
    name = "common"

    def __init__(self, name, **kwargs) -> None:
        super().__init__(**kwargs)
        self.name = name.strip()
        self.template_folder = (
            Path(__file__).resolve().parent.parent.parent / "templates" / self.name
        )
        request_template_path = self.template_folder / "request.json"
        with request_template_path.open("r", encoding="utf-8") as fp:
            self.request_template = json.load(fp)

        extract_template_path = self.template_folder / "extract.json"
        with extract_template_path.open("r", encoding="utf-8") as fp:
            self.extract_template = json.load(fp)
            if not isinstance(self.extract_template, Mapping):
                raise Exception(
                    f"extract_template must be a dict: {self.extract_template}"
                )

    def start_requests(self):
        send_template = self.request_template["request"]
        pagination = send_template.get("pagination")
        payload = send_template.get("payload", {}).copy()

        if pagination["mode"] == "offset":
            payload.pop(pagination["offset"], None)
        elif pagination["mode"] == "page":
            payload[pagination["page"]] = 1

        for category in self.request_template["categories"]:
            request_template = dict_merge(send_template, category)
            yield self._build_request(request_template, payload)

    def _build_request(
        self, request_template: Mapping[str, Any], payload: Mapping[str, Any]
    ) -> scrapy.Request:
        method = (request_template.get("method") or "GET").upper()
        url = request_template.get("url")
        if not isinstance(url, str) or not url:
            raise RuntimeError(f"Template {self.template_name} is missing request.url")

        body: bytes | None = None
        final_url = url

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
            headers=request_template.get("headers"),
            meta={
                "proxy": PROXY,
                "payload": payload,
                "request_template": request_template,
            },
        )

    def parse_response(self, response: scrapy.http.Response):
        payload = response.json()

        result = self._extract_result(payload)

        if not result:
            return

        for item in result:
            yield item

        # Paginate to next page.
        yield self._get_next_page(
            response.meta["request_template"],
            response.meta["payload"],
            last_page_size=len(result),
        )

    def _get_next_page(
        self, request_template, payload, last_page_size: int | None = None
    ) -> scrapy.Request:
        pagination = request_template.get("pagination")

        if pagination["mode"] == "page":
            page_key = pagination["page"]
            current_page_raw = payload.get(page_key) or 1
            current_page = int(current_page_raw)
            payload[page_key] = (current_page + 1,)

        elif pagination["mode"] == "offset":
            offset_key = pagination["offset"]
            current_offset_raw = payload.get(offset_key) or 0

            next_offset = int(current_offset_raw)
            if pagination.get("limit"):
                limit_key = pagination["limit"]
                limit_raw = payload[limit_key]
                limit = int(limit_raw)
                next_offset += limit
            elif last_page_size:
                next_offset += last_page_size
            else:
                raise Exception(
                    "Cannot determine next offset without 'limit' in template or last_page_size"
                )

            payload[offset_key] = next_offset
        else:
            raise Exception(f"Unknown pagination mode: {pagination['mode']}")

        return self._build_request(request_template, payload)

    def _extract_result(self, payload: Any) -> Any:
        list_path = self.extract_template.get("$list")
        if not isinstance(list_path, str):
            raise Exception(f"list_path must be a str: {list_path}")

        includes = self.extract_template.get("$include") or []
        items = dict_get(payload, list_path)
        if items is None:
            raise Exception(
                f"No items is found for: ${list_path} in payload: ${payload}"
            )

        result = []
        base_values = self._extract_base_values(payload, includes)
        item_paths = self.extract_template.get("$item") or {}

        for entry in items:
            current_item = {**base_values, **entry}
            for path_name, path in item_paths.items():
                current_item[path_name] = dict_get(entry, path)

            result.append(current_item)

        return result

    def _extract_base_values(self, payload, includes: dict[str, str]) -> dict[str, Any]:
        base_values: dict[str, Any] = {}
        for name, path in (includes or {}).items():
            base_values[name] = dict_get(payload, path)

        return base_values

    def _build_query_url(self, url: str, params: Mapping[str, Any]) -> str:
        parsed = urlparse(url)
        payload = {
            key: value if isinstance(value, str) else json.dumps(value)
            for key, value in params.items()
        }
        query = urlencode(payload, doseq=True)
        return urlunparse(parsed._replace(query=query))
