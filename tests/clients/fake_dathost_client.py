from typing import Any, Dict, Optional, Tuple

from src.clients.dathost_client import DathostClient


class FakeDathostClient(DathostClient):

    response_dict: Dict[Tuple[str, str], Dict[str, Any]] = {}

    async def _make_http_dathost_request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        awaited_result_code: Tuple[int] = (200, 201),
    ) -> Dict[str, Any]:
        return self.response_dict.get((method, path), {})
