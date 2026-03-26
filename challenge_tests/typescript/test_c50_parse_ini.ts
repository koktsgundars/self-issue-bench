// Tests for c50_parse_ini: parseINI(text)
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';

const codeFile = process.env.CODE_FILE!;
const code = fs.readFileSync(codeFile, 'utf8');

const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'ts-test-'));
const tmpFile = path.join(tmpDir, 'code.ts');
fs.writeFileSync(tmpFile, code + '\nexport { parseINI };');
const imported = require(tmpFile);
const parseINI = imported.parseINI;

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

test('basic section with key-value', () => {
  const input = '[server]\nhost = localhost\nport = 8080';
  const result = parseINI(input);
  assertEqual(result['server']['host'], 'localhost');
  assertEqual(result['server']['port'], '8080');
});

test('multiple sections', () => {
  const input = '[a]\nx = 1\n[b]\ny = 2';
  const result = parseINI(input);
  assertEqual(result['a']['x'], '1');
  assertEqual(result['b']['y'], '2');
});

test('comments ignored', () => {
  const input = '; this is a comment\n# another comment\n[sec]\nkey = val';
  const result = parseINI(input);
  assertEqual(result['sec']['key'], 'val');
  if (Object.keys(result).length !== 1) throw new Error('Should only have one section');
});

test('keys before section go under empty string', () => {
  const input = 'name = global\n[sec]\nkey = val';
  const result = parseINI(input);
  assertEqual(result['']['name'], 'global');
  assertEqual(result['sec']['key'], 'val');
});

test('whitespace trimming', () => {
  const input = '[sec]\n  key  =  value  ';
  const result = parseINI(input);
  assertEqual(result['sec']['key'], 'value');
});

test('quoted values', () => {
  const input = '[sec]\nname = "hello world"';
  const result = parseINI(input);
  assertEqual(result['sec']['name'], 'hello world');
});

test('empty input returns empty object', () => {
  const result = parseINI('');
  assertEqual(result, {});
});

fs.rmSync(tmpDir, { recursive: true, force: true });
console.log(`\n${passed} passed, ${failed} failed`);
if (failed > 0) process.exit(1);
