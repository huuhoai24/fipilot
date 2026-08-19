from typing import Any, Dict, List, Tuple


class IndexedTextResolver:

    @staticmethod
    def linearize(layout_regions: List[dict]) -> Tuple[str, Dict[int, str]]:
        """
        Build linearized text VÀ trả về index_map cùng lúc (single source of truth).
        Không còn bước parse ngược lại từ string.
        """
        texts = [
            block["text"].strip()
            for region in layout_regions
            for block in region["contained_blocks"]
            if block["text"].strip()
        ]
        index_map = dict(enumerate(texts))
        linearized_text = " ".join(f"[{i}]: {t}" for i, t in index_map.items())
        return linearized_text, index_map

    @staticmethod
    def resolve(
        data: Any,
        index_map: Dict[int, str],
        key_name: str = "description_refer_index_range",
        new_key: str = "jobDescription",
    ) -> Any:
        """
        Duyệt đệ quy dict/list, thay key_name (range [start, end]) bằng text
        ghép từ index_map, gán vào new_key. Sửa in-place, trả lại data.
        """
        if isinstance(data, dict):
            if key_name in data:
                start, end = data.pop(key_name)
                data[new_key] = " ".join(
                    index_map[i] for i in range(start, end + 1) if i in index_map
                )
            for v in data.values():
                IndexedTextResolver.resolve(v, index_map, key_name, new_key)
        elif isinstance(data, list):
            for item in data:
                IndexedTextResolver.resolve(item, index_map, key_name, new_key)
        return data