// Tests for c52_retry_ts: retry(fn, options?)
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';

const codeFile = process.env.CODE_FILE!;
const code = fs.readFileSync(codeFile, 'utf8');

const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'ts-test-'));
const tmpFile = path.join(tmpDir, 'code.ts');
fs.writeFileSync(tmpFile, code + '\nexport { retry };');
const imported = require(tmpFile);
const retry = imported.retry;

let passed = 0;
let failed = 0;

function test(name: string, fn: () => Promise<void>) {
  fn().then(() => { console.log(`PASS ${name}`); passed++; })
    .catch((e: any) => { console.log(`FAIL ${name}: ${e.message}`); failed++; })
    .then(() => {
      // Check if all tests are done
      if (passed + failed === 6) {
        fs.rmSync(tmpDir, { recursive: true, force: true });
        console.log(`\n${passed} passed, ${failed} failed`);
        if (failed > 0) process.exit(1);
      }
    });
}

function assertEqual(actual: any, expected: any) {
  if (JSON.stringify(actual) !== JSON.stringify(expected)) {
    throw new Error(`Expected ${JSON.stringify(expected)}, got ${JSON.stringify(actual)}`);
  }
}

test('immediate success', async () => {
  const result = await retry(() => Promise.resolve(42), { retries: 3, delay: 1 });
  assertEqual(result, 42);
});

test('success after failures', async () => {
  let attempt = 0;
  const fn = () => {
    attempt++;
    if (attempt < 3) return Promise.reject(new Error('fail'));
    return Promise.resolve('ok');
  };
  const result = await retry(fn, { retries: 5, delay: 1, backoff: 1 });
  assertEqual(result, 'ok');
});

test('all retries exhausted rejects', async () => {
  const fn = () => Promise.reject(new Error('always fails'));
  try {
    await retry(fn, { retries: 2, delay: 1, backoff: 1 });
    throw new Error('Should have rejected');
  } catch (e: any) {
    if (e.message === 'Should have rejected') throw e;
    assertEqual(e.message, 'always fails');
  }
});

test('respects retry count', async () => {
  let attempts = 0;
  const fn = () => { attempts++; return Promise.reject(new Error('fail')); };
  try {
    await retry(fn, { retries: 2, delay: 1, backoff: 1 });
  } catch {}
  // 1 initial + 2 retries = 3 total attempts
  assertEqual(attempts, 3);
});

test('abort signal cancels', async () => {
  const controller = new AbortController();
  let attempts = 0;
  const fn = () => {
    attempts++;
    if (attempts === 1) {
      controller.abort();
    }
    return Promise.reject(new Error('fail'));
  };
  try {
    await retry(fn, { retries: 5, delay: 10, backoff: 1, signal: controller.signal });
    throw new Error('Should have rejected');
  } catch (e: any) {
    if (e.message === 'Should have rejected') throw e;
    // Should have been aborted early, not exhausted all retries
    if (attempts > 3) throw new Error(`Too many attempts: ${attempts}`);
  }
});

test('returns correct value', async () => {
  const result = await retry(() => Promise.resolve({ key: 'value' }), { retries: 1, delay: 1 });
  assertEqual(result, { key: 'value' });
});
