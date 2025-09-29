// .github/scripts/generate_workflow.ts
import * as fs from "fs";
import * as path from "path";
import * as yaml from "yaml";  // npm install yaml

const TEMPLATE_FILE = ".github/workflow-setup/push_template.yml";
const MODULE_PREFIX = "Module";
const CONFIG_FILE = "final-config.yml";

// Load template
const templateContent = fs.readFileSync(TEMPLATE_FILE, "utf8").split(/\r?\n/);
const startIdx = templateContent.indexOf("  # repeat for each cluster start") + 1;
const endIdx = templateContent.indexOf("  # repeat for each cluster end");
const repeatBlock = templateContent.slice(startIdx, endIdx);

const cwd = process.cwd();
const moduleDirs = fs.readdirSync(cwd).filter((d) => d.startsWith(MODULE_PREFIX));

for (const dir of moduleDirs) {
    const moduleDir = path.join(cwd, dir);
    const configPath = path.join(moduleDir, CONFIG_FILE);

    if (!fs.existsSync(configPath)) {
        console.log(`⚠️ Skipping ${dir}, no ${CONFIG_FILE}`);
        continue;
    }

    const config = yaml.parse(fs.readFileSync(configPath, "utf8")) || {};
    const clusters: string[] = config.clusters || [];
    const placeholders: Record<string, any> = config.placeholders || {};

    // Collect placeholders from final-config.yml
    const resolvedPlaceholders: Record<string, string> = {};
    for (const [key, val] of Object.entries(placeholders)) {
        resolvedPlaceholders[key] = String(val?.value ?? "");
    }

    // Hardcode PROJECT_NAME to module_dir name
    resolvedPlaceholders["PROJECT_NAME"] = dir;

    const finalLines: string[] = [];

    // Lines before repeat block
    for (let i = 0; i < startIdx - 1; i++) {
        let line = templateContent[i];
        for (const [key, value] of Object.entries(resolvedPlaceholders)) {
            line = line.replace(new RegExp(key, "g"), value);
        }
        finalLines.push(line);
    }

    // Repeat block per cluster
    let previous: string | null = null;
    for (const cluster of clusters) {
        for (const lineRaw of repeatBlock) {
            let newLine = lineRaw.replace(/<cluster>/g, cluster);

            if (previous) {
                newLine = newLine.replace(/<previous-cluster>/g, previous);
            } else {
                newLine = newLine.replace(/, promote-<previous-cluster>/g, "");
            }

            for (const [key, value] of Object.entries(resolvedPlaceholders)) {
                newLine = newLine.replace(new RegExp(key, "g"), value);
            }

            finalLines.push(newLine);
        }
        finalLines.push("");
        previous = cluster;
    }

    const outputFile = path.join(moduleDir, `${dir}-workflow.yml`);
    fs.writeFileSync(outputFile, finalLines.join("\n") + "\n", "utf8");
    console.log(`✅ Workflow generated: ${outputFile}`);
}