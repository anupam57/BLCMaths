import os
import yaml

ROOT = os.getcwd()
DEFAULT_CONFIG = os.path.join(ROOT, ".github/workflow-setup/default-config.yml")

def deep_merge(a, b):
    if isinstance(a, dict) and isinstance(b, dict):
        merged = dict(a)
        for k, v in b.items():
            merged[k] = deep_merge(merged.get(k), v)
        return merged
    elif isinstance(a, list) and isinstance(b, list):
        return b  # replace lists instead of merging
    else:
        return b if b is not None else a

with open(DEFAULT_CONFIG) as f:
    default_data = yaml.safe_load(f) or {}

for folder in os.listdir(ROOT):
    module_path = os.path.join(ROOT, folder)
    config_file = os.path.join(module_path, "config.yml")

    if os.path.isdir(module_path) and folder.startswith("Module") and os.path.exists(config_file):
        with open(config_file) as f:
            module_data = yaml.safe_load(f) or {}

        merged = deep_merge(default_data, module_data)
        final_path = os.path.join(module_path, "final-config.yml")
        with open(final_path, "w") as out:
            yaml.dump(merged, out, sort_keys=False)
        print(f"✅ Created {final_path}")
