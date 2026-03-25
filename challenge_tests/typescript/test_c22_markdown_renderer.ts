// Tests for c22_markdown_renderer: renderMarkdown(input)
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';

const codeFile = process.env.CODE_FILE!;
const code = fs.readFileSync(codeFile, 'utf8');

// Write code to a temp .ts file and import it via tsx
const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'ts-test-'));
const tmpFile = path.join(tmpDir, 'code.ts');
fs.writeFileSync(tmpFile, code + '\nexport { renderMarkdown };');
const imported = require(tmpFile);
const renderMarkdown = imported.renderMarkdown as (input: string) => string;

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

function assertContains(actual: string, expected: string) {
  if (!actual.includes(expected)) {
    throw new Error(`Expected output to contain "${expected}", got "${actual}"`);
  }
}

test('h1 heading', () => {
  const result = renderMarkdown('# Hello');
  assertContains(result, '<h1>');
  assertContains(result, 'Hello');
  assertContains(result, '</h1>');
});

test('h2 heading', () => {
  const result = renderMarkdown('## Sub');
  assertContains(result, '<h2>');
});

test('bold text', () => {
  const result = renderMarkdown('**bold**');
  assertContains(result, '<strong>bold</strong>');
});

test('italic text', () => {
  const result = renderMarkdown('*italic*');
  assertContains(result, '<em>italic</em>');
});

test('inline code', () => {
  const result = renderMarkdown('`code`');
  assertContains(result, '<code>code</code>');
});

test('link', () => {
  const result = renderMarkdown('[text](http://example.com)');
  assertContains(result, '<a href="http://example.com">text</a>');
});

test('unordered list', () => {
  const result = renderMarkdown('- item1\n- item2');
  assertContains(result, '<ul>');
  assertContains(result, '<li>');
  assertContains(result, 'item1');
  assertContains(result, 'item2');
  assertContains(result, '</ul>');
});

test('paragraph', () => {
  const result = renderMarkdown('Hello world');
  assertContains(result, '<p>');
  assertContains(result, 'Hello world');
});

test('code block', () => {
  const result = renderMarkdown('```\nconst x = 1;\n```');
  assertContains(result, '<pre>');
  assertContains(result, '<code>');
  assertContains(result, 'const x = 1;');
});

test('code block no inline formatting', () => {
  const result = renderMarkdown('```\n**not bold**\n```');
  // Inside code blocks, ** should NOT become <strong>
  if (result.includes('<strong>')) {
    throw new Error('Code block should not process inline formatting');
  }
});

test('inline formatting in heading', () => {
  const result = renderMarkdown('# Hello **world**');
  assertContains(result, '<strong>world</strong>');
});

// Cleanup temp dir
fs.rmSync(tmpDir, { recursive: true, force: true });

console.log(`\n${passed} passed, ${failed} failed`);
if (failed > 0) process.exit(1);
