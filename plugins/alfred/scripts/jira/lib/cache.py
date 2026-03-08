"""프로젝트 메타데이터 JSON 캐시 관리"""

import json
import os
import tempfile
from datetime import datetime, timezone


_CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".cache")
_CACHE_FILE = os.path.join(_CACHE_DIR, "project_meta.json")
_DEFAULT_MAX_AGE_HOURS = 168  # 7일


def _read_cache() -> dict:
    if not os.path.exists(_CACHE_FILE):
        return {"_version": 1, "global": {}, "projects": {}}
    with open(_CACHE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_cache(data: dict) -> None:
    os.makedirs(_CACHE_DIR, exist_ok=True)
    # 원자적 쓰기: 임시 파일 → rename
    fd, tmp_path = tempfile.mkstemp(dir=_CACHE_DIR, suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, _CACHE_FILE)
    except Exception:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise


def _is_stale(fetched_at: str | None, max_age_hours: int = _DEFAULT_MAX_AGE_HOURS) -> bool:
    if not fetched_at:
        return True
    try:
        dt = datetime.fromisoformat(fetched_at)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        age = datetime.now(timezone.utc) - dt
        return age.total_seconds() > max_age_hours * 3600
    except (ValueError, TypeError):
        return True


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class MetaCache:
    """프로젝트 메타데이터 JSON 캐시"""

    def __init__(self):
        self._data = _read_cache()

    def get_project(self, project_key: str, max_age_hours: int = _DEFAULT_MAX_AGE_HOURS) -> dict | None:
        project = self._data.get("projects", {}).get(project_key)
        if project and not _is_stale(project.get("_fetched_at"), max_age_hours):
            return project
        return None

    def set_project(self, project_key: str, data: dict) -> None:
        data["_fetched_at"] = _now_iso()
        self._data.setdefault("projects", {})[project_key] = data
        _write_cache(self._data)

    def get_global(self, key: str, max_age_hours: int = _DEFAULT_MAX_AGE_HOURS) -> list | None:
        section = self._data.get("global", {}).get(key)
        if section and not _is_stale(section.get("_fetched_at"), max_age_hours):
            return section.get("items")
        return None

    def set_global(self, key: str, items: list) -> None:
        self._data.setdefault("global", {})[key] = {
            "_fetched_at": _now_iso(),
            "items": items,
        }
        _write_cache(self._data)

    def invalidate(self, project_key: str | None = None) -> None:
        if project_key:
            self._data.get("projects", {}).pop(project_key, None)
        else:
            self._data = {"_version": 1, "global": {}, "projects": {}}
        _write_cache(self._data)
