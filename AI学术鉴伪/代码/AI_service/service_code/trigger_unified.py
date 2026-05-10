from __future__ import annotations

from service_runtime.protocol import (
    load_request,
    print_error,
    print_ready,
    print_result,
    resolve_request_path,
    wait_for_request_file,
)
from service_runtime.router import dispatch_request


def main() -> int:
    request_path = resolve_request_path()
    print_ready()

    try:
        wait_for_request_file(request_path)
        request_data = load_request(request_path)
        result = dispatch_request(request_data, request_path=request_path)
        print_result(result)
        return 0
    except Exception as exc:
        request_id = None
        try:
            request_id = request_data.get("request_id")  # type: ignore[name-defined]
        except Exception:
            request_id = None
        print_error(exc, request_id=request_id)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

