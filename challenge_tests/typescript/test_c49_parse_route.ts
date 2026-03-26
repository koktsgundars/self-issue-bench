// Tests for c49_parse_route: matchRoute(pattern, url)
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';

const codeFile = process.env.CODE_FILE!;
const code = fs.readFileSync(codeFile, 'utf8');

const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'ts-test-'));
const tmpFile = path.join(tmpDir, 'code.ts');
fs.writeFileSync(tmpFile, code + '\nexport { matchRoute };');
const imported = require(tmpFile);
const matchRoute = imported.matchRoute;

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

test('exact match: /users matches /users', () => {
  const result = matchRoute('/users', '/users');
  assertEqual(result, { matched: true, params: {} });
});

test('named param: /users/:id matches /users/123', () => {
  const result = matchRoute('/users/:id', '/users/123');
  assertEqual(result, { matched: true, params: { id: '123' } });
});

test('multiple params: /users/:id/posts/:postId', () => {
  const result = matchRoute('/users/:id/posts/:postId', '/users/42/posts/7');
  assertEqual(result, { matched: true, params: { id: '42', postId: '7' } });
});

test('wildcard: /files/*', () => {
  const result = matchRoute('/files/*', '/files/a/b/c');
  assertEqual(result, { matched: true, params: { '*': 'a/b/c' } });
});

test('no match', () => {
  const result = matchRoute('/users/:id', '/posts/123');
  assertEqual(result, { matched: false, params: {} });
});

test('trailing slash ignored', () => {
  const result = matchRoute('/users/:id', '/users/123/');
  assertEqual(result, { matched: true, params: { id: '123' } });
});

test('pattern with no params', () => {
  const result = matchRoute('/about/us', '/about/us');
  assertEqual(result, { matched: true, params: {} });
});

fs.rmSync(tmpDir, { recursive: true, force: true });
console.log(`\n${passed} passed, ${failed} failed`);
if (failed > 0) process.exit(1);
