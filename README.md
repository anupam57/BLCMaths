# 🛠️ Automated Config & Workflow Generator

This repository automates two related tasks for each module in the project:

1. **Merge configs**  
   Combine a global `default-config.yml` with each module’s `config.yml` into a `final-config.yml`.

2. **Generate workflows**  
   Use a reusable `workflow_template.yml` and module-specific `final-config.yml` to create a GitHub Actions workflow file for each module (e.g., `ModuleA/ModuleA-workflow.yml`).

## 📂 Project Structure
```
.github/
  workflows/
    main.yml                  # Orchestrates config merge + workflow generation
  workflow-setup/
    default-config.yml         # Global default config
    push_template.yml          # Workflow template with placeholders
  scripts/
    merge_configs.py           # Merges configs into final-config.yml
    generate_workflow.py       # Generates workflows from final-config.yml
ModuleA/
  config.yml                   # Module-specific overrides
  final-config.yml             # (generated)
  ModuleA-workflow.yml         # (generated)
ModuleB/
  config.yml
  final-config.yml
  ModuleB-workflow.yml
```
## ⚙️ Config Merging

Each module has a `config.yml` with overrides. These are merged with the root `.github/workflow-setup/default-config.yml` to produce a `final-config.yml`.

### Example: `default-config.yml`

```yaml
clusters:
  - et
  - qt
  - dt
  - sb

placeholders:
  NOTIFY_ON_FAIL:
    value: false
```
Example: ModuleA/config.yml

```yaml
placeholders:
  MODULE_NAME:
    value: Generic-Module
```

Generated: ModuleA/final-config.yml

```yaml
clusters:
  - et
  - qt
  - dt
  - sb

placeholders:
  MODULE_NAME:
    value: Generic-Module
  NOTIFY_ON_FAIL:
    value: false
```

### 📝 Workflow Template
The file .github/workflow-setup/push_template.yml defines the skeleton workflow with placeholders:

```yaml
jobs:
  initialize:
    uses: ./.github/workflows/ci_cd_initialize.yml
    with:
      project-name: <PROJECT_NAME>
      module: <MODULE_NAME>

  # repeat for each cluster start
  promote-<cluster>:
    needs: [ initialize, promote-<previous-cluster> ]
    with:
      environment: <cluster>
  # repeat for each cluster end

```
-
### 🔄 Placeholder Replacement
Placeholders inside the template are replaced with values from each module’s final-config.yml.

<MODULE_NAME> → From module config

<NOTIFY_ON_FAIL> → From module config

<PROJECT_NAME> → Automatically replaced with module folder name (e.g., ModuleA)

💡 If PROJECT_NAME is explicitly defined in final-config.yml, it will override the folder name.

### 📊 Process Diagram
mermaid
``` yml
flowchart TD
    A[default-config.yml] --> C[merge_configs.py]
    B[ModuleX/config.yml] --> C
    C --> D[final-config.yml]

    D --> E[generate_workflow.py]
    T[push_template.yml] --> E
    E --> F[ModuleX-workflow.yml]
```

### 🚀 Workflow
The GitHub Actions workflow (.github/workflows/main.yml) runs automatically on pushes:

Merge configs → generates Module*/final-config.yml

Generate workflows → generates Module*/Module*-workflow.yml

Each module ends up with its own workflow YAML ready for GitHub Actions.

▶️ Running Locally
If you want to test outside of GitHub Actions:

bash
Copy code
# Merge configs
python .github/scripts/merge_configs.py

# Generate workflows
python .github/scripts/generate_workflow.py
✅ Benefits
No duplicated config — defaults live in one place

Each module has its own clean workflow file

Adding new placeholders doesn’t require changing scripts

Flexible: module-specific overrides + auto-injected values

pgsql
Copy code

