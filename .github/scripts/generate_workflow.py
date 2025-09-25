import yaml
from pathlib import Path

TEMPLATE_FILE = ".github/workflow-setup/push_template.yml"
MODULE_PREFIX = "Module"
CONFIG_FILE = "final-config.yml"

# Load template
template = Path(TEMPLATE_FILE).read_text().splitlines()
start_idx = template.index("  # repeat for each cluster start") + 1
end_idx = template.index("  # repeat for each cluster end")
repeat_block = template[start_idx:end_idx]

for module_dir in Path(".").glob(f"{MODULE_PREFIX}*"):
    config_path = module_dir / CONFIG_FILE
    if not config_path.exists():
        print(f"⚠️ Skipping {module_dir}, no {CONFIG_FILE}")
        continue

    with open(config_path) as f:
        config = yaml.safe_load(f) or {}

    clusters = config.get("clusters", [])
    placeholders = config.get("placeholders", {})
    # unwrap placeholders: each key has {value: X}
    resolved_placeholders = {
        key: str(val.get("value", "")) for key, val in placeholders.items()
    }

    final_lines = []
    for line in template[:start_idx-1]:
        for key, value in resolved_placeholders.items():
            line = line.replace(f"{key}", value)
        final_lines.append(line)

    previous = None
    for cluster in clusters:
        for line in repeat_block:
            new_line = line.replace("<cluster>", cluster)
            if previous:
                new_line = new_line.replace("<previous-cluster>", previous)
            else:
                new_line = new_line.replace(", promote-<previous-cluster>", "")

            for key, value in resolved_placeholders.items():
                new_line = new_line.replace(f"{key}", value)

            final_lines.append(new_line)
        final_lines.append("")
        previous = cluster

    output_file = module_dir / f"{module_dir.name}-workflow.yml"
    output_file.write_text("\n".join(final_lines) + "\n")
    print(f"✅ Workflow generated: {output_file}")