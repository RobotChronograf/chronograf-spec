#!/usr/bin/env python3
"""
OPENRGD — Chronograf Builder v0.2.0
-----------------------------------

Struttura attesa:

    spec/chronograf/
      ├─ layers/
      │    ├─ time_kernel.rcg
      │    ├─ time_channels.rcg
      │    └─ time_topology.rcg
      ├─ manifest/
      │    └─ chronograf_manifest.rcg
      └─ tools/
           ├─ build_chronograf.py
           └─ validate_chronograf.py
           └─ utils.py  (strip_jsonc_comments)

Uso (da dentro spec/chronograf/tools):

    python build_chronograf.py all
    python build_chronograf.py integrity
    python build_chronograf.py bounds
    python build_chronograf.py contracts
"""

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any

from utils import strip_jsonc_comments


# ---------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------


def get_chronograf_root() -> Path:
    """
    spec/chronograf/tools/build_chronograf.py
    → chronograf_root = spec/chronograf
    """
    return Path(__file__).resolve().parents[1]


def get_dirs() -> Dict[str, Path]:
    root = get_chronograf_root()
    layers = root / "layers"
    manifest_dir = root / "manifest"

    if not layers.exists():
        raise FileNotFoundError(f"Layers dir not found: {layers}")
    if not manifest_dir.exists():
        raise FileNotFoundError(f"Manifest dir not found: {manifest_dir}")

    return {
        "root": root,
        "layers": layers,
        "manifest_dir": manifest_dir,
        "manifest_path": manifest_dir / "chronograf_manifest.rcg",
    }


# ---------------------------------------------------------------------
# Low-level helpers
# ---------------------------------------------------------------------


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def load_jsonc(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    clean = strip_jsonc_comments(text)
    return json.loads(clean)


def dump_json_with_header(path: Path, data: Any) -> None:
    """
    Preserva il banner iniziale (commento prima del primo '{'),
    poi riscrive il JSON formattato sotto.
    """
    original = path.read_text(encoding="utf-8") if path.exists() else ""
    brace_idx = original.find("{")
    header = original[:brace_idx] if brace_idx != -1 else ""
    json_body = json.dumps(data, indent=2)
    path.write_text(f"{header}{json_body}\n", encoding="utf-8")


# ---------------------------------------------------------------------
# 1) INTEGRITY LEVEL
# ---------------------------------------------------------------------


def update_integrity(manifest: Dict[str, Any], dirs: Dict[str, Path]) -> None:
    layers = dirs["layers"]

    kernel_path = layers / "time_kernel.rcg"
    channels_path = layers / "time_channels.rcg"
    topology_path = layers / "time_topology.rcg"

    print("[INTEGRITY] Updating hashes and generated_at_iso8601_str")

    for p in (kernel_path, channels_path, topology_path):
        if not p.exists():
            raise FileNotFoundError(f"Missing required file: {p}")

    # timestamp
    now = datetime.now(timezone.utc).isoformat()
    meta = manifest.setdefault("meta_group", {})
    meta["generated_at_iso8601_str"] = now
    print(f"[INTEGRITY] generated_at_iso8601_str = {now}")

    # hashes (relative paths rispetto alla root di chronograf)
    sources = manifest.setdefault("sources_group", {})

    files = {
        "time_kernel_file":   ("layers/time_kernel.rcg",   kernel_path),
        "time_channels_file": ("layers/time_channels.rcg", channels_path),
        "time_topology_file": ("layers/time_topology.rcg", topology_path),
    }

    for key, (rel, path) in files.items():
        digest = sha256_file(path)
        entry = sources.setdefault(key, {})
        entry["relative_path_str"] = rel
        entry["expected_sha256_hex_str"] = digest
        print(f"[INTEGRITY] {key}: {rel} → {digest}")


# ---------------------------------------------------------------------
# 2) BOUNDS LEVEL
# ---------------------------------------------------------------------


def update_bounds(manifest: Dict[str, Any], dirs: Dict[str, Path]) -> None:
    layers = dirs["layers"]
    print("[BOUNDS] Updating loop/channel bounds")

    topology = load_jsonc(layers / "time_topology.rcg")
    channels = load_jsonc(layers / "time_channels.rcg")

    loops = topology.get("loops_list", [])
    freqs = [float(loop.get("target_frequency_hz_float", 0.0)) for loop in loops]

    if freqs:
        max_f = max(freqs)
        min_f = min(freqs)
    else:
        max_f = 0.0
        min_f = 0.0

    total_loops = len(loops)
    total_channels = len(channels.get("channels_list", []))

    bounds = manifest.setdefault("bounds_group", {})
    bounds["max_loop_frequency_hz_float"] = max_f
    bounds["min_loop_frequency_hz_float"] = min_f
    bounds["total_defined_loops_int"] = total_loops
    bounds["total_defined_channels_int"] = total_channels

    print(f"[BOUNDS] max_loop_frequency_hz_float  = {max_f}")
    print(f"[BOUNDS] min_loop_frequency_hz_float  = {min_f}")
    print(f"[BOUNDS] total_defined_loops_int      = {total_loops}")
    print(f"[BOUNDS] total_defined_channels_int   = {total_channels}")


# ---------------------------------------------------------------------
# 3) CONTRACTS LEVEL
# ---------------------------------------------------------------------


def update_contracts(manifest: Dict[str, Any], dirs: Dict[str, Path]) -> None:
    layers = dirs["layers"]
    print("[CONTRACTS] Updating time/uncertainty/barcode contracts")

    kernel = load_jsonc(layers / "time_kernel.rcg")

    time_atom = kernel.get("time_atom_encoding_group", {})
    unc_model = kernel.get("uncertainty_model_group", {})
    barcode_schema = kernel.get("temporal_barcode_schema_group", {})

    # runtime_time_contract_group
    rtc = manifest.setdefault("runtime_time_contract_group", {})
    rtc["time_atom_version_str"] = time_atom.get("version_str", "time_atom_v1")
    rtc["epoch_reference_enum_str"] = time_atom.get("epoch_reference_enum_str", "TAI")
    rtc["min_supported_tick_exp10_int"] = time_atom.get("min_supported_tick_exp10_int", -18)
    rtc["nominal_runtime_precision_exp10_int"] = time_atom.get(
        "recommended_runtime_tick_exp10_int", -9
    )
    rtc["supported_timescales_arr"] = [
        "UTC",
        "TAI",
        "GPS",
        "LOCAL_MONOTONIC",
        "SIM_TIME",
    ]
    rtc["default_display_timescale_enum_str"] = "UTC"
    rtc["default_cli_output_format_enum_str"] = "ISO8601_UTC_PLUS_ATOM"

    # uncertainty_contract_group
    uc = manifest.setdefault("uncertainty_contract_group", {})
    uc["uses_parametric_uncertainty_bool"] = unc_model.get(
        "must_carry_uncertainty_bool", True
    )
    uc["default_uncertainty_exp10_int"] = unc_model.get(
        "default_uncertainty_exp10_int", -6
    )
    uc["max_uncertainty_exp10_int"] = uc.get("max_uncertainty_exp10_int", 0)
    uc["supported_semantic_kinds_list"] = unc_model.get(
        "supported_semantic_kinds_list", []
    )
    uc["llm_friendly_schema_hint_str"] = "time_atom_obj.uncertainty_group"
    if "doc_str" not in uc:
        uc["doc_str"] = (
            "Uncertainty is not an afterthought: it is a first-class "
            "dimension of every Temporal Barcode."
        )

    # temporal_barcode_contract_group
    bc = manifest.setdefault("temporal_barcode_contract_group", {})
    bc["temporal_barcode_version_str"] = barcode_schema.get(
        "version_str", "temporal_barcode_v1"
    )
    bc["required_fields_list"] = barcode_schema.get("required_fields_list", [])
    bc["recommended_fields_list"] = barcode_schema.get("recommended_fields_list", [])
    bc["max_barcode_rate_hz_float"] = bc.get("max_barcode_rate_hz_float", 10000.0)
    bc["llm_streaming_hint_str"] = (
        "Temporal Barcodes SHOULD be emitted as newline-delimited JSON objects "
        "for efficient LLM streaming."
    )
    if "schema_layout_doc_str" not in bc:
        bc["schema_layout_doc_str"] = barcode_schema.get(
            "schema_layout_doc_str",
            "A Temporal Barcode is {time_atom_obj, channel_code_str, loop_id_str, "
            "primary_domain_enum_str, event_kind_enum_str, ...}.",
        )


# ---------------------------------------------------------------------
# Orchestratore
# ---------------------------------------------------------------------


def build_chronograf(command: str) -> None:
    dirs = get_dirs()
    manifest_path = dirs["manifest_path"]

    if not manifest_path.exists():
        raise FileNotFoundError(f"Manifest not found: {manifest_path}")

    manifest = load_jsonc(manifest_path)

    if command in ("integrity", "all"):
        update_integrity(manifest, dirs)
    if command in ("bounds", "all"):
        update_bounds(manifest, dirs)
    if command in ("contracts", "all"):
        update_contracts(manifest, dirs)

    dump_json_with_header(manifest_path, manifest)
    print(f"[OK] chronograf_manifest.rcg updated ({command})")


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(
        description="OpenRGD Chronograf Manifest Builder"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("all", help="Update integrity, bounds and contracts")
    sub.add_parser("integrity", help="Update hashes + generated_at only")
    sub.add_parser("bounds", help="Update loop/channel bounds only")
    sub.add_parser("contracts", help="Update time/uncertainty/barcode contracts only")

    args = parser.parse_args(argv)
    try:
        build_chronograf(args.command)
    except Exception as e:
        print(f"[ERROR] Build failed: {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
