name: Generate Workflow

on:
  pull_request:
    paths:
      - "clusters.yml"
      - "workflow_template.yml"
      - ".github/scripts/generate_workflow.py"

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.x"

      - name: Install dependencies
        run: pip install pyyaml

      - name: Run generator
        run: python .github/scripts/generate_workflow.py

      - name: Commit generated workflow
        uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: "chore: auto-generate workflow"
          file_pattern: ".github/workflows/generated.yml"