import yaml
from pathlib import Path

TEMPLATE_FILE = "workflow_template.yml"
MODULE_PREFIX = "Module"
MODULE_CONFIG = "final-config.yml"
WORKFLOW_DIR = Path(".github/workflows")
WORKFLOW_DIR.mkdir(parents=True, exist_ok=True)

# Load template
template = Path(TEMPLATE_FILE).read_text().splitlines()

# Extract the repeat block between markers
start_idx = template.index("  # repeat for each cluster start") + 1
end_idx = template.index("  # repeat for each cluster end")
repeat_block = template[start_idx:end_idx]

# Process each module
for module_dir in Path(".").glob(f"{MODULE_PREFIX}*"):
    config_file = module_dir / MODULE_CONFIG
    if not config_file.exists():
        print(f"⚠️ Skipping {module_dir}, no {MODULE_CONFIG}")
        continue

    with open(config_file) as f:
        config = yaml.safe_load(f) or {}

    clusters = config.get("clusters", [])
    if not clusters:
        print(f"⚠️ No clusters defined in {config_file}")
        continue

    print(f"🔄 Generating workflow for {module_dir.name} with clusters: {clusters}")

    # Start fresh content for this module
    final_lines = []
    for line in template[:start_idx-1]:
        final_lines.append(line)

    previous = None
    for cluster in clusters:
        for line in repeat_block:
            new_line = line.replace("<cluster>", cluster)

            if previous:
                new_line = new_line.replace("<previous-cluster>", previous)
            else:
                # First cluster: remove ", promote-<previous-cluster>"
                new_line = new_line.replace(", promote-<previous-cluster>", "")

            # Replace placeholders with values from module config
            for key, value in config.items():
                if key == "clusters":
                    continue
                placeholder = f"<{module_dir.name}.{key}>"
                if placeholder in new_line:
                    new_line = new_line.replace(placeholder, str(value))

            final_lines.append(new_line)

        final_lines.append("")  # spacing
        previous = cluster

    # Write this module's workflow file
    output_file = WORKFLOW_DIR / f"{module_dir.name}-workflow.yml"
    output = "\n".join(final_lines) + "\n"
    output_file.write_text(output)

    print(f"✅ Workflow generated at on hoon hoonnn {output_file}")