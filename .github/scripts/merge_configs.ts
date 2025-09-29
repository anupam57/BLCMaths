// .github/scripts/merge_configs.ts
import * as fs from "fs";
import * as path from "path";
import * as yaml from "yaml";
import deepmerge from "deepmerge";

const DEFAULT_CONFIG = ".github/workflow-setup/default-config.yml";
const CONFIG_FILE = "config.yml";
const FINAL_CONFIG_FILE = "final-config.yml";
const MODULE_PREFIX = "Module";

// Helper: merge two YAML files
function mergeYamlFiles(baseFile: string, overrideFile: string): any {
    const baseYaml = fs.existsSync(baseFile) ? fs.readFileSync(baseFile, "utf8") : "";
    const overrideYaml = fs.existsSync(overrideFile) ? fs.readFileSync(overrideFile, "utf8") : "";

    const baseConfig = baseYaml ? yaml.parse(baseYaml) || {} : {};
    const overrideConfig = overrideYaml ? yaml.parse(overrideYaml) || {} : {};

    return deepmerge(baseConfig, overrideConfig);
}

function main() {
    const cwd = process.cwd();
    const moduleDirs = fs.readdirSync(cwd).filter((d) => d.startsWith(MODULE_PREFIX));

    for (const dir of moduleDirs) {
        const moduleDir = path.join(cwd, dir);
        const configPath = path.join(moduleDir, CONFIG_FILE);

        if (!fs.existsSync(configPath)) {
            console.log(`⚠️ Skipping ${dir}, no ${CONFIG_FILE}`);
            continue;
        }

        const finalConfig = mergeYamlFiles(DEFAULT_CONFIG, configPath);

        const outPath = path.join(moduleDir, FINAL_CONFIG_FILE);
        fs.writeFileSync(outPath, yaml.stringify(finalConfig), "utf8");
        console.log(`✅ Final config written: ${outPath}`);
    }
}

main();