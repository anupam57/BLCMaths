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