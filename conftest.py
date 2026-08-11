from __future__ import annotations

import inspect
## test for co author ##
import httpx


def _patch_httpx_for_starlette_testclient() -> None:
    # httpx>=0.28 dropped the `app=` kwarg that older Starlette TestClient
    # versions still pass to httpx.Client(); drop it so those tests don't
    # crash with TypeError. Safe to delete once Starlette stops sending it.
    signature = inspect.signature(httpx.Client.__init__)
    if "app" in signature.parameters:
        return

    original_init = httpx.Client.__init__

    def patched_init(self, *args, app=None, **kwargs):  # noqa: ANN001
        return original_init(self, *args, **kwargs)

    httpx.Client.__init__ = patched_init  # type: ignore[assignment]


_patch_httpx_for_starlette_testclient()
