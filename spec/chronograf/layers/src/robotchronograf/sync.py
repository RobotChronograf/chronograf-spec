import os, json, hashlib
from datetime import datetime, timezone
from .utils import strip_jsonc_comments

def sha256_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def sync_chronograf(spec_dir):
    print(f"[RGC] Synchronizing Chronograf from {spec_dir}")

    files = {
        "time_kernel_rcg_sha256_hex_str": "time_kernel.rcg",
        "time_channels_rcg_sha256_hex_str": "time_channels.rcg",
        "time_topology_rcg_sha256_hex_str": "time_topology.rcg",
    }

    manifest_path = os.path.join(spec_dir, "chronograf_manifest.rcg")

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.loads(strip_jsonc_comments(f.read()))

    for key, filename in files.items():
        path = os.path.join(spec_dir, filename)
        digest = sha256_file(path)
        print(f"[RGC] {filename} → {digest}")
        manifest["sources_group"][key] = digest

    manifest["maintenance_group"]["generated_at_iso8601_str"] = datetime.now(timezone.utc).isoformat()

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print("[RGC] ✓ Manifest updated")
