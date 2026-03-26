// Tests for c45_binary_heap: BinaryHeap<T>
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';

const codeFile = process.env.CODE_FILE!;
const code = fs.readFileSync(codeFile, 'utf8');

const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'ts-test-'));
const tmpFile = path.join(tmpDir, 'code.ts');
fs.writeFileSync(tmpFile, code + '\nexport { BinaryHeap };');
const imported = require(tmpFile);
const BinaryHeap = imported.BinaryHeap;

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

test('min heap with number comparator', () => {
  const heap = new BinaryHeap((a: number, b: number) => a - b);
  heap.push(5);
  heap.push(3);
  heap.push(7);
  assertEqual(heap.peek(), 3);
});

test('max heap with reversed comparator', () => {
  const heap = new BinaryHeap((a: number, b: number) => b - a);
  heap.push(5);
  heap.push(3);
  heap.push(7);
  assertEqual(heap.peek(), 7);
});

test('pop returns in order', () => {
  const heap = new BinaryHeap((a: number, b: number) => a - b);
  heap.push(5);
  heap.push(1);
  heap.push(3);
  heap.push(2);
  heap.push(4);
  const result: number[] = [];
  while (heap.size > 0) {
    result.push(heap.pop());
  }
  assertEqual(result, [1, 2, 3, 4, 5]);
});

test('pop empty throws', () => {
  const heap = new BinaryHeap((a: number, b: number) => a - b);
  let threw = false;
  try { heap.pop(); } catch { threw = true; }
  if (!threw) throw new Error('Expected pop on empty heap to throw');
});

test('peek empty throws', () => {
  const heap = new BinaryHeap((a: number, b: number) => a - b);
  let threw = false;
  try { heap.peek(); } catch { threw = true; }
  if (!threw) throw new Error('Expected peek on empty heap to throw');
});

test('size tracks correctly', () => {
  const heap = new BinaryHeap((a: number, b: number) => a - b);
  assertEqual(heap.size, 0);
  heap.push(1);
  assertEqual(heap.size, 1);
  heap.push(2);
  assertEqual(heap.size, 2);
  heap.pop();
  assertEqual(heap.size, 1);
});

test('custom object comparator', () => {
  const heap = new BinaryHeap((a: { priority: number }, b: { priority: number }) => a.priority - b.priority);
  heap.push({ priority: 10 });
  heap.push({ priority: 1 });
  heap.push({ priority: 5 });
  assertEqual(heap.pop().priority, 1);
  assertEqual(heap.pop().priority, 5);
  assertEqual(heap.pop().priority, 10);
});

fs.rmSync(tmpDir, { recursive: true, force: true });
console.log(`\n${passed} passed, ${failed} failed`);
if (failed > 0) process.exit(1);
