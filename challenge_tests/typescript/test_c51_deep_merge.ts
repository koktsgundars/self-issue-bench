// Tests for c51_deep_merge: deepMerge(...sources)
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';

const codeFile = process.env.CODE_FILE!;
const code = fs.readFileSync(codeFile, 'utf8');

const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'ts-test-'));
const tmpFile = path.join(tmpDir, 'code.ts');
fs.writeFileSync(tmpFile, code + '\nexport { deepMerge };');
const imported = require(tmpFile);
const deepMerge = imported.deepMerge;

let passed = 0;
let failed = 0;

function test(name: string, fn: () => void) {
  try { fn(); console.log(`PASS ${name}`); passed++; }
  catch (e: any) { console.log(`FAIL ${name}: ${e.message}`); failed++; }
}

function assertEqual(actual: any, expected: any) {
  if (JSON.stringify(actual) !== JSON.stringify(expected)) {
    throw new Error(`Expected ${JSON.stringify(expected)}, got ${JSON.stringify(actual)}`);
  }
}

test('basic merge: {a:1} + {b:2} -> {a:1,b:2}', () => {
  assertEqual(deepMerge({ a: 1 }, { b: 2 }), { a: 1, b: 2 });
});

test('override: {a:1} + {a:2} -> {a:2}', () => {
  assertEqual(deepMerge({ a: 1 }, { a: 2 }), { a: 2 });
});

test('deep merge: {a:{b:1}} + {a:{c:2}} -> {a:{b:1,c:2}}', () => {
  assertEqual(deepMerge({ a: { b: 1 } }, { a: { c: 2 } }), { a: { b: 1, c: 2 } });
});

test('arrays replaced: {a:[1]} + {a:[2]} -> {a:[2]}', () => {
  assertEqual(deepMerge({ a: [1] }, { a: [2] }), { a: [2] });
});

test('three sources', () => {
  assertEqual(deepMerge({ a: 1 }, { b: 2 }, { c: 3 }), { a: 1, b: 2, c: 3 });
});

test('null overrides object', () => {
  const result = deepMerge({ a: { b: 1 } }, { a: null } as any);
  assertEqual(result.a, null);
});

test('inputs not mutated', () => {
  const obj1 = { a: { b: 1 } };
  const obj2 = { a: { c: 2 } };
  deepMerge(obj1, obj2);
  assertEqual(obj1, { a: { b: 1 } });
  assertEqual(obj2, { a: { c: 2 } });
});

fs.rmSync(tmpDir, { recursive: true, force: true });
console.log(`\n${passed} passed, ${failed} failed`);
if (failed > 0) process.exit(1);
