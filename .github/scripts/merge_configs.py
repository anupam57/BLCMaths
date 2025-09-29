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

/*
Typescript

import { mergeYAML } from "yaml-merge";
import { parse, stringify } from "yaml";
import * as fs from "fs-extra";
import deepmerge from "deepmerge";
import path from "path";

interface SomeConfigType {
  // define types according to your YAML structure
  [key: string]: any;
}

/**
 * Merge multiple YAML configuration files into one, writing output.
 * 
 * @param inputPaths Paths of YAML config files to merge (in order).
 * @param outputPath Path to write merged YAML.
 */
async function mergeConfigs(inputPaths: string[], outputPath: string) {
  // Option A: Use yaml-merge if it fits
  try {
    const mergedYaml = await mergeYAML(inputPaths, {
      // some options if yaml-merge supports (if required)
    });
    await fs.outputFile(outputPath, mergedYaml);
    console.log(`Merged YAML written to ${outputPath}`);
    return;
  } catch (e) {
    console.warn("yaml-merge method failed; falling back to manual merge", e);
  }

  // Option B: Parse + deep merge + stringify
  const docs: SomeConfigType[] = [];
  for (const p of inputPaths) {
    const content = await fs.readFile(p, "utf8");
    const doc = parse(content) as SomeConfigType;
    docs.push(doc);
  }

  // Deep merge all docs in order
  const mergedObj = docs.reduce((acc, doc) => deepmerge(acc, doc), {} as SomeConfigType);

  // Convert back to YAML
  const mergedYaml = stringify(mergedObj);

  // Write to file
  await fs.outputFile(outputPath, mergedYaml);
  console.log(`Merged YAML written to ${outputPath}`);
}

// Example usage (can be adapted to CLI)
// Suppose in Python script they did something like merging “base.yml + override.yml”:
const inputs = [
  path.join(__dirname, "../configs/base.yml"),
  path.join(__dirname, "../configs/override.yml"),
];
const out = path.join(__dirname, "../configs/merged.yml");

mergeConfigs(inputs, out).catch(err => {
  console.error("Error during merge:", err);
  process.exit(1);
});

*/
