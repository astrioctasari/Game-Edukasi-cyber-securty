// One-time migration helper. The desktop app consumes only the generated JSON.
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const { isRegExp } = require("node:util").types;

const root = path.resolve(__dirname, "..", "..");
const referenceRoot = path.join(root, "reference-web");
const levelFiles = fs
  .readdirSync(path.join(referenceRoot, "js", "levels"))
  .filter((name) => name.startsWith("level-") && name.endsWith(".js"))
  .sort();
const sources = [
  fs.readFileSync(path.join(referenceRoot, "js", "utils.js"), "utf8"),
  fs.readFileSync(path.join(referenceRoot, "js", "data", "graphics.js"), "utf8"),
  fs.readFileSync(path.join(referenceRoot, "js", "data", "lessons.js"), "utf8"),
  ...levelFiles.map((name) => fs.readFileSync(path.join(referenceRoot, "js", "levels", name), "utf8")),
  fs.readFileSync(path.join(referenceRoot, "js", "levels", "index.js"), "utf8"),
  "globalThis.__exported = { levels: LV, lessons: ED, wallpaper: WALL };",
].join("\n");

const context = {};
vm.runInNewContext(sources, context);
const data = JSON.stringify(
  context.__exported,
  (_key, value) =>
    isRegExp(value) ? { $regex: value.source, $flags: value.flags } : value,
  2,
);
const output = path.join(__dirname, "..", "data", "game_data.json");
fs.mkdirSync(path.dirname(output), { recursive: true });
fs.writeFileSync(output, data + "\n", "utf8");
console.log(`Exported ${context.__exported.levels.length} levels to ${output}`);
