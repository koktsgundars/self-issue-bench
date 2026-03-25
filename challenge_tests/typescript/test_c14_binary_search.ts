// Tests for c14_binary_search: validateSchema(schema, data)
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';

const codeFile = process.env.CODE_FILE!;
const code = fs.readFileSync(codeFile, 'utf8');

// Write code to a temp .ts file and import it via tsx
const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'ts-test-'));
const tmpFile = path.join(tmpDir, 'code.ts');
fs.writeFileSync(tmpFile, code + '\nexport { validateSchema };');
const imported = require(tmpFile);
const validateSchema = imported.validateSchema as (schema: object, data: unknown) => { valid: boolean; errors: string[] };

let passed = 0;
let failed = 0;

function test(name: string, fn: () => void) {
  try {
    fn();
    console.log(`PASS ${name}`);
    passed++;
  } catch (e: any) {
    console.log(`FAIL ${name}: ${e.message}`);
    failed++;
  }
}

function assertEqual(actual: any, expected: any) {
  if (JSON.stringify(actual) !== JSON.stringify(expected)) {
    throw new Error(`Expected ${JSON.stringify(expected)}, got ${JSON.stringify(actual)}`);
  }
}

test('valid string type', () => {
  const result = validateSchema({ type: 'string' }, 'hello');
  assertEqual(result.valid, true);
  assertEqual(result.errors.length, 0);
});

test('invalid string type', () => {
  const result = validateSchema({ type: 'string' }, 42);
  assertEqual(result.valid, false);
  if (result.errors.length === 0) throw new Error('Expected errors');
});

test('valid number type', () => {
  const result = validateSchema({ type: 'number' }, 42);
  assertEqual(result.valid, true);
});

test('required fields present', () => {
  const schema = { type: 'object', required: ['name'], properties: { name: { type: 'string' } } };
  const result = validateSchema(schema, { name: 'Alice' });
  assertEqual(result.valid, true);
});

test('required fields missing', () => {
  const schema = { type: 'object', required: ['name'], properties: { name: { type: 'string' } } };
  const result = validateSchema(schema, {});
  assertEqual(result.valid, false);
});

test('nested object validation', () => {
  const schema = {
    type: 'object',
    properties: {
      address: {
        type: 'object',
        properties: { city: { type: 'string' } },
        required: ['city'],
      },
    },
  };
  const result = validateSchema(schema, { address: { city: 'NYC' } });
  assertEqual(result.valid, true);
});

test('array items validation', () => {
  const schema = { type: 'array', items: { type: 'number' } };
  const result = validateSchema(schema, [1, 2, 3]);
  assertEqual(result.valid, true);
});

test('array items invalid', () => {
  const schema = { type: 'array', items: { type: 'number' } };
  const result = validateSchema(schema, [1, 'two', 3]);
  assertEqual(result.valid, false);
});

test('enum valid', () => {
  const schema = { enum: ['a', 'b', 'c'] };
  const result = validateSchema(schema, 'b');
  assertEqual(result.valid, true);
});

test('enum invalid', () => {
  const schema = { enum: ['a', 'b', 'c'] };
  const result = validateSchema(schema, 'd');
  assertEqual(result.valid, false);
});

test('minimum valid', () => {
  const schema = { type: 'number', minimum: 0 };
  const result = validateSchema(schema, 5);
  assertEqual(result.valid, true);
});

test('minimum invalid', () => {
  const schema = { type: 'number', minimum: 10 };
  const result = validateSchema(schema, 5);
  assertEqual(result.valid, false);
});

test('null type', () => {
  const result = validateSchema({ type: 'null' }, null);
  assertEqual(result.valid, true);
});

console.log(`\n${passed} passed, ${failed} failed`);
if (failed > 0) process.exit(1);
