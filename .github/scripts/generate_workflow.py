import yaml
from pathlib import Path

DEFAULT_FILE = "default-config.yml"
MODULE_PREFIX = "Module"
CONFIG_NAME = "config.yml"
OUTPUT_NAME = "final-config.yml"

def deep_merge(a, b):
    if isinstance(a, dict) and isinstance(b, dict):
        merged = dict(a)
        for k, v in b.items():
            merged[k] = deep_merge(merged.get(k), v)
        return merged
    elif isinstance(a, list) and isinstance(b, list):
        # Replace arrays completely (not append)
        return b
    else:
        return b if b is not None else a

# Load default config
with open(DEFAULT_FILE) as f:
    default_config = yaml.safe_load(f) or {}

# Loop over all module folders
for module_dir in Path(".").glob(f"{MODULE_PREFIX}*"):
    config_file = module_dir / CONFIG_NAME
    if not config_file.exists():
        print(f"⚠️ Skipping {module_dir}, no {CONFIG_NAME}")
        continue

    with open(config_file) as f:
        module_config = yaml.safe_load(f) or {}

    merged = deep_merge(default_config, module_config)

    output_file = module_dir / OUTPUT_NAME
    with open(output_file, "w") as out:
        yaml.dump(merged, out, sort_keys=False)

    print(f"✅ Generated {output_file}")
