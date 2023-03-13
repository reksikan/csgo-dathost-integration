from typing import Optional, Any, Dict, Tuple

from src.clients.dathost_client import DathostClient


class FakeDathostClient(DathostClient):

    response_dict: Dict[Tuple[str, str], Dict[str, Any]]

    async def _make_http_dathost_request(
        self,
        method: str,
        path: str,
        params: Optional[dict[str, Any]] = None,
        data: Optional[dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        return self.response_dict.get((method, path), {})
