import { readFileSync, writeFileSync, mkdtempSync, rmSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { tmpdir } from "node:os";
import { join } from "node:path";
const temp = mkdtempSync(join(tmpdir(), "bottifact-model-"));
try {
  execFileSync(process.execPath, [
    "node_modules/typescript/bin/tsc",
    "--ignoreConfig",
    "--target",
    "ES2022",
    "--module",
    "ES2022",
    "--skipLibCheck",
    "--outDir",
    temp,
    "packages/core/src/table-model.ts",
  ]);
  const js = readFileSync(join(temp, "table-model.js"), "utf8").replace(
    /^export /gm,
    "",
  );
  writeFileSync(
    "packages/core/components/table-model.js",
    "/* Generated from core/src/table-model.ts; run node scripts/build_table_model.mjs. */\n(()=>{\n" +
      js +
      "\nglobalThis.BottifactTableModel=TableModel;\n})();\n",
  );
} finally {
  rmSync(temp, { recursive: true, force: true });
}
