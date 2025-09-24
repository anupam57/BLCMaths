import yaml
from pathlib import Path

INPUT_FILE = "clusters.yml"
TEMPLATE_FILE = "workflow_template.yml"
OUTPUT_FILE = "final-workflow.yml"

# Load clusters
with open(INPUT_FILE) as f:
    clusters = yaml.safe_load(f)["clusters"]

# Load template
template = Path(TEMPLATE_FILE).read_text().splitlines()

# Extract the repeat block between markers
start_idx = template.index("  # repeat for each cluster start") + 1
end_idx = template.index("  # repeat for each cluster end")

repeat_block = template[start_idx:end_idx]

# Begin final content
final_lines = []

for line in template[:start_idx-1]:
    final_lines.append(line)

# Expand for each cluster
previous = None
for cluster in clusters:
    for line in repeat_block:
        new_line = line
        new_line = new_line.replace("<cluster>", cluster)
        if previous:
            new_line = new_line.replace("<previous-cluster>", previous)
        else:
            # First cluster: remove ", promote-<previous-cluster>"
            new_line = new_line.replace(", promote-<previous-cluster>", "")
        final_lines.append(new_line)
    final_lines.append("")  # spacing
    previous = cluster

# Write result
output = "\n".join(final_lines) + "\n"
Path(OUTPUT_FILE).write_text(output)

print(f"✅ Workflow generated at {OUTPUT_FILE}")
