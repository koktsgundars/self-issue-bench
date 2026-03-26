// Tests for c48_result_type: Ok, Err, Result
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';

const codeFile = process.env.CODE_FILE!;
const code = fs.readFileSync(codeFile, 'utf8');

const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'ts-test-'));
const tmpFile = path.join(tmpDir, 'code.ts');
fs.writeFileSync(tmpFile, code + '\nexport { Ok, Err };');
const imported = require(tmpFile);
const Ok = imported.Ok;
const Err = imported.Err;

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

test('Ok.isOk/isErr', () => {
  const ok = new Ok(42);
  assertEqual(ok.isOk(), true);
  assertEqual(ok.isErr(), false);
});

test('Err.isOk/isErr', () => {
  const err = new Err('bad');
  assertEqual(err.isOk(), false);
  assertEqual(err.isErr(), true);
});

test('Ok.unwrap returns value', () => {
  const ok = new Ok(42);
  assertEqual(ok.unwrap(), 42);
});

test('Err.unwrap throws', () => {
  const err = new Err('bad');
  let threw = false;
  try { err.unwrap(); } catch { threw = true; }
  if (!threw) throw new Error('Expected Err.unwrap to throw');
});

test('Ok.unwrapOr returns value', () => {
  const ok = new Ok(42);
  assertEqual(ok.unwrapOr(0), 42);
});

test('Err.unwrapOr returns fallback', () => {
  const err = new Err('bad');
  assertEqual(err.unwrapOr(99), 99);
});

test('Ok.map transforms', () => {
  const ok = new Ok(5);
  const mapped = ok.map((x: number) => x * 2);
  assertEqual(mapped.isOk(), true);
  assertEqual(mapped.unwrap(), 10);
});

test('Err.map returns self', () => {
  const err = new Err('bad');
  const mapped = err.map((x: number) => x * 2);
  assertEqual(mapped.isErr(), true);
  let threw = false;
  try { mapped.unwrap(); } catch { threw = true; }
  if (!threw) throw new Error('Expected mapped Err.unwrap to throw');
});

fs.rmSync(tmpDir, { recursive: true, force: true });
console.log(`\n${passed} passed, ${failed} failed`);
if (failed > 0) process.exit(1);
