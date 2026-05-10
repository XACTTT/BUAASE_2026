#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import json
import os
import pickle
import subprocess
import sys
from pathlib import Path
from typing import Any

import cv2
import numpy as np


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run trigger_unified.py and fully decode its response")
    parser.add_argument(
        "--request-file",
        default=None,
        help="Optional request.json path. Defaults to service_code/requests/request.json",
    )
    parser.add_argument(
        "--python",
        default=sys.executable,
        help="Python executable used to start trigger_unified.py",
    )
    parser.add_argument(
        "--print-full-json",
        action="store_true",
        help="Print the full decoded outer JSON result",
    )
    parser.add_argument(
        "--save-image-outputs",
        default=None,
        help="Optional directory used to save decoded image masks/previews from the image pipeline",
    )
    return parser.parse_args()


def read_until_result(proc: subprocess.Popen[str]) -> str:
    marker_seen = False

    assert proc.stdout is not None
    for raw_line in proc.stdout:
        line = raw_line.rstrip("\n")
        print(line)
        if marker_seen:
            return line
        if line.strip() == "ai service result":
            marker_seen = True

    raise RuntimeError("trigger_unified.py exited without emitting a result payload")


def to_jsonable(obj: Any) -> Any:
    if isinstance(obj, np.ndarray):
        return {
            "type": "ndarray",
            "shape": list(obj.shape),
            "dtype": str(obj.dtype),
            "min": float(np.min(obj)) if obj.size else None,
            "max": float(np.max(obj)) if obj.size else None,
        }
    if isinstance(obj, (np.floating, np.integer)):
        return obj.item()
    if isinstance(obj, dict):
        return {str(k): to_jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [to_jsonable(v) for v in obj]
    return obj


def save_array_image(path: Path, arr: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if arr.ndim == 2:
        img = arr
    elif arr.ndim == 3 and arr.shape[0] in (1, 3):
        img = np.transpose(arr, (1, 2, 0))
    else:
        img = arr

    if img.dtype != np.uint8:
        scaled = img
        if np.issubdtype(img.dtype, np.floating):
            scaled = np.clip(img, 0.0, 1.0) * 255.0 if float(np.max(img)) <= 1.0 else np.clip(img, 0.0, 255.0)
        img = scaled.astype(np.uint8)

    if img.ndim == 3 and img.shape[2] == 3:
        cv2.imwrite(str(path), cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    else:
        cv2.imwrite(str(path), img)


def decode_image_transport(result: dict[str, Any], save_dir: Path | None) -> Any:
    transport = result.get("transport")
    if not isinstance(transport, dict):
        return None
    if transport.get("format") != "pickle_base64":
        return None

    encoded = transport.get("data")
    if not isinstance(encoded, str):
        return None

    raw = pickle.loads(base64.b64decode(encoded))
    decoded_summary = []

    if isinstance(raw, list):
        for method_item in raw:
            if not isinstance(method_item, tuple) or len(method_item) != 2:
                decoded_summary.append(to_jsonable(method_item))
                continue

            method_name, method_results = method_item
            method_entry: dict[str, Any] = {"method": method_name, "items": []}

            if isinstance(method_results, list):
                for idx, sample_item in enumerate(method_results):
                    if isinstance(sample_item, tuple) and len(sample_item) == 2:
                        image_ref, payload = sample_item
                        item_entry = {"image": image_ref, "payload": to_jsonable(payload)}
                        if save_dir is not None and isinstance(payload, np.ndarray):
                            out_path = save_dir / method_name / f"{idx:03d}.png"
                            save_array_image(out_path, payload)
                            item_entry["saved_to"] = str(out_path)
                        elif save_dir is not None and isinstance(payload, tuple):
                            tuple_saved = []
                            for part_idx, part in enumerate(payload):
                                if isinstance(part, np.ndarray):
                                    out_path = save_dir / method_name / f"{idx:03d}_{part_idx}.png"
                                    save_array_image(out_path, part)
                                    tuple_saved.append(str(out_path))
                            if tuple_saved:
                                item_entry["saved_arrays"] = tuple_saved
                        method_entry["items"].append(item_entry)
                    else:
                        method_entry["items"].append(to_jsonable(sample_item))
            else:
                method_entry["items"].append(to_jsonable(method_results))

            decoded_summary.append(method_entry)

    return decoded_summary


def print_pipeline_details(decoded: dict[str, Any], save_dir: Path | None) -> None:
    print("\n=== Decoded Summary ===")
    print(f"success: {decoded.get('success')}")
    print(f"pipeline: {decoded.get('pipeline')}")
    print(f"request_id: {decoded.get('request_id')}")

    if not decoded.get("success", False):
        print("error:", json.dumps(decoded.get("error"), ensure_ascii=False, indent=2))
        return

    result = decoded.get("result", {})
    if not isinstance(result, dict):
        print("result:", to_jsonable(result))
        return

    summary = result.get("summary")
    if summary is not None:
        print("summary:", json.dumps(to_jsonable(summary), ensure_ascii=False, indent=2))

    pipeline = decoded.get("pipeline")
    if pipeline == "image":
        decoded_transport = decode_image_transport(result, save_dir)
        if decoded_transport is not None:
            print("\n=== Image Transport Decoded ===")
            print(json.dumps(to_jsonable(decoded_transport), ensure_ascii=False, indent=2))
        else:
            print("transport:", json.dumps(to_jsonable(result.get("transport")), ensure_ascii=False, indent=2))
    elif pipeline == "bert_text":
        print("\n=== Bert Text Result ===")
        print(json.dumps(to_jsonable(result), ensure_ascii=False, indent=2))
    elif pipeline == "structured":
        print("\n=== Structured Result ===")
        print(json.dumps(to_jsonable(result), ensure_ascii=False, indent=2))
    else:
        print("\n=== Result ===")
        print(json.dumps(to_jsonable(result), ensure_ascii=False, indent=2))


def main() -> int:
    cli_args = parse_args()
    service_code_root = Path(__file__).resolve().parent
    trigger_path = service_code_root / "trigger_unified.py"
    request_file = Path(cli_args.request_file).resolve() if cli_args.request_file else service_code_root / "requests" / "request.json"
    save_dir = Path(cli_args.save_image_outputs).resolve() if cli_args.save_image_outputs else None

    env = os.environ.copy()
    env["UNIFIED_AI_REQUEST_FILE"] = str(request_file)

    proc = subprocess.Popen(
        [cli_args.python, str(trigger_path)],
        cwd=str(service_code_root),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    try:
        encoded_payload = read_until_result(proc)
        proc.wait(timeout=5)
    finally:
        if proc.poll() is None:
            proc.kill()

    decoded = json.loads(base64.b64decode(encoded_payload).decode("utf-8"))
    print_pipeline_details(decoded, save_dir)

    if cli_args.print_full_json:
        print("\n=== Full Outer JSON ===")
        print(json.dumps(decoded, ensure_ascii=False, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
