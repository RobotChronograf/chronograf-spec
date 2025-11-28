#!/usr/bin/env python3
"""
OPENRGD — Chronograf Validator v0.2.0
-------------------------------------

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
           ├─ validate_chronograf.py
           └─ utils.py  (strip_jsonc_comments)

Uso (da dentro spec/chronograf/tools):

    python validate_chronograf.py

Cosa controlla:

  1. INTEGRITY
     - Ricalcola SHA-256 dei files in layers/ indicati in sources_group
     - Li confronta con expected_sha256_hex_str nel manifest

  2. BOUNDS
     - Rilegge time_topology.rcg e time_channels.rcg
     - Ricava max/min frequency, numero di loops, numero di canali
     - Confronta con bounds_group nel manifest

  3. CONTRACTS (sanity, non blocca il mondo ma è utile)
     - Verifica che:
         * time_atom_version_str combaci col kernel
         * epoch_reference_enum_str coincida
         * min_supported_tick_exp10_int coincida
         * nominal_runtime_precision_exp10_int ≈ recommended_runtime_tick_exp10_int
         * uncertainty default_exp10 e semantic kinds combacino
         * temporal_barcode_version + required/recommended fields combacino
"""

import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

from utils import strip_jsonc_comments


# ---------------------------------------------------------------------
# Path & IO helpers
# ---------------------------------------------------------------------


def get_chronograf_root() -> Path:
    """spec/chronograf/tools/validate_chronograf.py → spec/chronograf."""
    return Path(__file__).resolve().parents[1]


def get_dirs() -> Dict[str, Path]:
    root = get_chronograf_root()
    layers = root / "layers"
    manifest_dir = root / "manifest"

    if not layers.exists():
        raise FileNotFoundError(f"[ERROR] Layers dir not found: {layers}")
    if not manifest_dir.exists():
        raise FileNotFoundError(f"[ERROR] Manifest dir not found: {manifest_dir}")

    return {
        "root": root,
        "layers": layers,
        "manifest_dir": manifest_dir,
        "manifest_path": manifest_dir / "chronograf_manifest.rcg",
    }


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


# ---------------------------------------------------------------------
# 1) INTEGRITY CHECK
# ---------------------------------------------------------------------


def validate_sources(manifest: Dict[str, Any], dirs: Dict[str, Path]) -> bool:
    """
    Controlla che gli SHA256 dei files in layers/ coincidano con quelli
    dichiarati in sources_group.
    """
    print("\n=== [1] SOURCE INTEGRITY CHECK ===")
    ok = True

    sources = manifest.get("sources_group", {})
    if not sources:
        print("  [FAIL] sources_group mancante nel manifest.")
        return False

    root = dirs["root"]

    for logical_name, entry in sources.items():
        rel = entry.get("relative_path_str")
        expected = entry.get("expected_sha256_hex_str")

        print(f"\n[CHECK] {logical_name}")
        if not rel or not expected:
            print("  [FAIL] relative_path_str o expected_sha256_hex_str mancanti.")
            ok = False
            continue

        file_path = root / rel
        if not file_path.exists():
            print(f"  [FAIL] File not found: {file_path}")
            ok = False
            continue

        actual = sha256_file(file_path)
        if actual.lower() == expected.lower():
            print(f"  [OK] Hash match for {rel}")
        else:
            print(f"  [FAIL] Hash mismatch for {rel}")
            print(f"       expected: {expected}")
            print(f"       actual  : {actual}")
            ok = False

    return ok


# ---------------------------------------------------------------------
# 2) BOUNDS CHECK
# ---------------------------------------------------------------------


def validate_bounds(manifest: Dict[str, Any], dirs: Dict[str, Path]) -> bool:
    """
    Rigenera bounds da topology+channels e li confronta con il manifest.
    """
    print("\n=== [2] BOUNDS CHECK ===")
    ok = True

    layers = dirs["layers"]

    topology = load_jsonc(layers / "time_topology.rcg")
    channels = load_jsonc(layers / "time_channels.rcg")
    loops = topology.get("loops_list", [])
    freqs: List[float] = [float(l.get("target_frequency_hz_float", 0.0)) for l in loops]

    if freqs:
        max_f = max(freqs)
        min_f = min(freqs)
    else:
        max_f = 0.0
        min_f = 0.0

    total_loops = len(loops)
    total_channels = len(channels.get("channels_list", []))

    bounds = manifest.get("bounds_group", {})
    if not bounds:
        print("  [FAIL] bounds_group mancante nel manifest.")
        return False

    def check_field(name: str, expected_val, actual_val):
        nonlocal ok
        if expected_val == actual_val:
            print(f"  [OK] {name}: {actual_val}")
        else:
            print(f"  [FAIL] {name} mismatch")
            print(f"       manifest: {expected_val}")
            print(f"       computed: {actual_val}")
            ok = False

    check_field("max_loop_frequency_hz_float",
                float(bounds.get("max_loop_frequency_hz_float", 0.0)),
                max_f)
    check_field("min_loop_frequency_hz_float",
                float(bounds.get("min_loop_frequency_hz_float", 0.0)),
                min_f)
    check_field("total_defined_loops_int",
                int(bounds.get("total_defined_loops_int", 0)),
                total_loops)
    check_field("total_defined_channels_int",
                int(bounds.get("total_defined_channels_int", 0)),
                total_channels)

    return ok


# ---------------------------------------------------------------------
# 3) CONTRACTS CHECK (sanity)
# ---------------------------------------------------------------------


def validate_contracts(manifest: Dict[str, Any], dirs: Dict[str, Path]) -> bool:
    """
    Controlla che i contratti di alto livello nel manifest siano coerenti
    con il kernel (Time Atom / Uncertainty / Temporal Barcode).
    Non è tanto un check di sicurezza, quanto di non-divergenza.
    """
    print("\n=== [3] CONTRACTS CHECK ===")
    ok = True

    layers = dirs["layers"]
    kernel = load_jsonc(layers / "time_kernel.rcg")

    time_atom = kernel.get("time_atom_encoding_group", {})
    unc_model = kernel.get("uncertainty_model_group", {})
    barcode_schema = kernel.get("temporal_barcode_schema_group", {})

    rtc = manifest.get("runtime_time_contract_group", {})
    uc = manifest.get("uncertainty_contract_group", {})
    bc = manifest.get("temporal_barcode_contract_group", {})

    # helper
    def check(label: str, manifest_val, kernel_val):
        nonlocal ok
        if manifest_val == kernel_val:
            print(f"  [OK] {label}")
        else:
            print(f"  [WARN] {label} diverge")
            print(f"         manifest: {manifest_val}")
            print(f"         kernel  : {kernel_val}")
            ok = False

    # --- Time Atom ---------------------------------------------------
    print("\n  -- Time Atom --")
    check("time_atom_version_str",
          rtc.get("time_atom_version_str"),
          time_atom.get("version_str"))

    check("epoch_reference_enum_str",
          rtc.get("epoch_reference_enum_str"),
          time_atom.get("epoch_reference_enum_str"))

    check("min_supported_tick_exp10_int",
          rtc.get("min_supported_tick_exp10_int"),
          time_atom.get("min_supported_tick_exp10_int"))

    check("nominal_runtime_precision_exp10_int",
          rtc.get("nominal_runtime_precision_exp10_int"),
          time_atom.get("recommended_runtime_tick_exp10_int"))

    # --- Uncertainty -------------------------------------------------
    print("\n  -- Uncertainty --")
    check("uses_parametric_uncertainty_bool",
          uc.get("uses_parametric_uncertainty_bool"),
          unc_model.get("must_carry_uncertainty_bool"))

    check("default_uncertainty_exp10_int",
          uc.get("default_uncertainty_exp10_int"),
          unc_model.get("default_uncertainty_exp10_int"))

    check("supported_semantic_kinds_list",
          uc.get("supported_semantic_kinds_list"),
          unc_model.get("supported_semantic_kinds_list"))

    # --- Temporal Barcode --------------------------------------------
    print("\n  -- Temporal Barcode --")
    check("temporal_barcode_version_str",
          bc.get("temporal_barcode_version_str"),
          barcode_schema.get("version_str"))

    check("required_fields_list",
          bc.get("required_fields_list"),
          barcode_schema.get("required_fields_list"))

    check("recommended_fields_list",
          bc.get("recommended_fields_list"),
          barcode_schema.get("recommended_fields_list"))

    return ok


# ---------------------------------------------------------------------
# Orchestratore
# ---------------------------------------------------------------------


def validate_chronograf() -> bool:
    dirs = get_dirs()
    manifest_path = dirs["manifest_path"]

    if not manifest_path.exists():
        print(f"[ERROR] Manifest not found: {manifest_path}")
        return False

    manifest = load_jsonc(manifest_path)

    ok_sources = validate_sources(manifest, dirs)
    ok_bounds = validate_bounds(manifest, dirs)
    ok_contracts = validate_contracts(manifest, dirs)

    all_ok = ok_sources and ok_bounds and ok_contracts

    print("\n=== SUMMARY ===")
    print(f"  Sources   : {'OK' if ok_sources else 'FAIL'}")
    print(f"  Bounds    : {'OK' if ok_bounds else 'FAIL'}")
    print(f"  Contracts : {'OK' if ok_contracts else 'WARN/FAIL'}")
    print(f"\nResult: {'✅ Chronograf manifest is VALID' if all_ok else '⚠️ Chronograf manifest has issues'}")

    return all_ok


def main() -> None:
    try:
        ok = validate_chronograf()
    except Exception as e:
        print(f"[ERROR] Validation failed with exception: {e}")
        sys.exit(1)

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
