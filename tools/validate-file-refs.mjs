/**
 * File Reference Validator for bmad-builder
 *
 * Validates cross-file references in BMB source files (agents, workflows, steps).
 * Catches broken file paths, missing referenced files, and absolute path leaks.
 * Auto-detects own module code from module.yaml and skips external module refs.
 *
 * What it checks:
 *   - {project-root}/_bmad/bmb/ references → src/ files
 *   - Relative path references (./file.md, ../data/file.csv)
 *   - Frontmatter path variables (nextStepFile, stepTemplate, etc.)
 *   - CSV workflow-file column → source files
 *   - Absolute path leak detection (/Users/, /home/, C:\)
 *
 * What it skips:
 *   - External module refs ({project-root}/_bmad/core/, bmm/, etc.)
 *   - Relative refs resolving outside src/ (../../../../core/)
 *   - Install-generated files (config.yaml, docs/ KBs)
 *   - Template placeholders ([N], [name], [template])
 *   - Runtime variables ({output_folder}, {bmad_builder_output_folder}, etc.)
 *   - {{mustache}} template variables
 *   - Lines with <!-- validate-file-refs:ignore --> comment
 *   - Lines after <!-- validate-file-refs:ignore-next-line --> comment
 *   - Refs with EXAMPLE- or invalid- filename prefix in data/ directories
 *
 * Usage:
 *   node tools/validate-file-refs.mjs              # Warning mode (exit 0)
 *   node tools/validate-file-refs.mjs --strict      # Fail on issues (exit 1)
 *   node tools/validate-file-refs.mjs --verbose      # Show all checked refs
 *   node tools/validate-file-refs.mjs --include-external  # Show external refs as INFO
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import yaml from 'yaml';
import { parse as parseCsv } from 'csv-parse/sync';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// --- CLI Parsing ---

const flags = new Set(process.argv.slice(2).filter((a) => a.startsWith('--')));
const VERBOSE = flags.has('--verbose');
const STRICT = flags.has('--strict');
const INCLUDE_EXTERNAL = flags.has('--include-external');

const PROJECT_ROOT = path.resolve(__dirname, '..');
const SRC_DIR = path.join(PROJECT_ROOT, 'src');

// --- Constants ---

const SCAN_EXTENSIONS = new Set(['.yaml', '.yml', '.md', '.csv']);
const SKIP_DIRS = new Set(['node_modules', '_module-installer', '.git']);

// Install-generated paths that don't exist in the source tree
const INSTALL_ONLY_PATHS = ['docs/'];
const INSTALL_GENERATED_FILES = ['config.yaml'];

// Runtime variables that cannot be resolved statically
const UNRESOLVABLE_VARS = [
  '{output_folder}',
  '{value}',
  '{timestamp}',
  '{config_source}:',
  '{installed_path}',
  '{shared_path}',
  '{planning_artifacts}',
  '{research_topic}',
  '{user_name}',
  '{communication_language}',
  '{bmad_builder_output_folder}',
  '{new_workflow_name}',
  '{module_code}',
  '{workflow_name}',
  '{project_name}',
  '{datetime}',
  '{date}',
  '{count}',
  '{epic_number}',
  '{sidecar-folder}',
  '{targetWorkflowPath}',
  '{workflow_folder_path}',
  '{module_output_folder}',
];

// Frontmatter keys that contain file paths
const FRONTMATTER_PATH_KEYS = new Set([
  'nextStepFile',
  'thisStepFile',
  'nextStep',
  'continueStepFile',
  'skipToStepFile',
  'altStepFile',
  'workflowFile',
  'stepTemplate',
  'agentTemplate',
  'agentArch',
  'menuHandlingStandards',
  'outputFormatStandards',
  'frontmatterStandards',
  'brainstormContext',
  'workflowExamples',
  'templateFile',
  'outputFile',
  'workflowPlanFile',
  'validationReportFile',
  'advancedElicitationTask',
  'partyModeWorkflow',
]);

// Regex patterns
const PROJECT_ROOT_REF = /\{project-root\}\/_bmad\/([^\s'"<>})\]`]+)/g;
const RELATIVE_PATH_QUOTED = /['"](\.\.\/?[^'"]+\.(?:md|yaml|yml|xml|json|csv|txt))['"]/g;
const RELATIVE_PATH_DOT = /['"](\.\/[^'"]+\.(?:md|yaml|yml|xml|json|csv|txt))['"]/g;
const ABS_PATH_LEAK = /(?:\/Users\/|\/home\/|[A-Z]:\\)/;

// Inline suppression comments
const IGNORE_COMMENT = /<!--\s*validate-file-refs:ignore\s*-->/;
const IGNORE_NEXT_LINE_COMMENT = /<!--\s*validate-file-refs:ignore-next-line\s*-->/;

// Data directory example filename prefixes (auto-skipped)
const DATA_DIR_EXAMPLE_PREFIXES = ['EXAMPLE-', 'invalid-'];

// --- Helpers ---

function escapeAnnotation(str) {
  return str.replaceAll('%', '%25').replaceAll('\r', '%0D').replaceAll('\n', '%0A');
}

function stripCodeBlocks(content) {
  return content.replaceAll(/```[\s\S]*?```/g, (m) => m.replaceAll(/[^\n]/g, ''));
}

function offsetToLine(content, offset) {
  let line = 1;
  for (let i = 0; i < offset && i < content.length; i++) {
    if (content[i] === '\n') line++;
  }
  return line;
}

/**
 * Detect whether a reference contains [bracketed] template placeholders.
 * Matches [non-numeric] content like [N], [name], [template], [output].
 * Does NOT match [1], [2] (numbered list items).
 */
function isBracketedPlaceholder(refStr) {
  return /\[[^\]]*[A-Za-z][^\]]*\]/.test(refStr);
}

/**
 * Check if a line should be ignored via inline suppression comments.
 * Supports <!-- validate-file-refs:ignore --> on the same line
 * and <!-- validate-file-refs:ignore-next-line --> on the previous line.
 */
function isLineIgnored(contentLines, lineNumber) {
  const idx = lineNumber - 1;
  if (idx < 0 || idx >= contentLines.length) return false;
  if (IGNORE_COMMENT.test(contentLines[idx])) return true;
  if (idx > 0 && IGNORE_NEXT_LINE_COMMENT.test(contentLines[idx - 1])) return true;
  return false;
}

/**
 * Check if a reference uses a documentation-example filename convention
 * inside a data/ directory. Files prefixed with EXAMPLE- or invalid-
 * are treated as illustrative and skipped.
 */
function isDataDirExample(filePath, refStr) {
  if (!filePath.includes('/data/')) return false;
  const basename = path.basename(refStr);
  return DATA_DIR_EXAMPLE_PREFIXES.some((prefix) => basename.startsWith(prefix));
}

/**
 * Check if a reference string is statically resolvable.
 */
function isResolvable(refStr) {
  if (refStr.includes('{{')) return false;
  if (isBracketedPlaceholder(refStr)) return false;
  for (const v of UNRESOLVABLE_VARS) {
    if (refStr.includes(v)) return false;
  }
  return true;
}

/**
 * Check if a cleaned path is install-generated (not in source tree).
 */
function isInstallGenerated(cleanedPath) {
  for (const prefix of INSTALL_ONLY_PATHS) {
    if (cleanedPath.startsWith(prefix)) return true;
  }
  const basename = path.basename(cleanedPath);
  for (const generated of INSTALL_GENERATED_FILES) {
    if (basename === generated) return true;
  }
  return false;
}

/**
 * Read module.yaml to detect the module's own code (e.g., "bmb").
 */
function detectModuleCode(srcDir) {
  const moduleYamlPath = path.join(srcDir, 'module.yaml');
  if (!fs.existsSync(moduleYamlPath)) return null;
  try {
    const content = fs.readFileSync(moduleYamlPath, 'utf-8');
    const data = yaml.parse(content);
    return data?.code || null;
  } catch {
    return null;
  }
}

/**
 * Check if a {project-root}/_bmad/ ref is external (different module).
 */
function isExternalRef(refStr, moduleCode) {
  if (!moduleCode) return false;
  const match = refStr.match(/\{project-root\}\/_bmad\/([^/]+)\//);
  if (!match) return false;
  const refModule = match[1];
  // .memory, _config are special framework paths, not external modules
  if (refModule.startsWith('_')) return false;
  return refModule !== moduleCode;
}

/**
 * Map {project-root}/_bmad/bmb/ paths to src/ paths.
 * Returns null for install-generated or external refs.
 */
function mapInstalledToSource(refPath, moduleCode) {
  const match = refPath.match(/\{project-root\}\/_bmad\/([^/]+)\/(.*)/);
  if (!match) return null;

  const refModule = match[1];
  const subPath = match[2];

  // External module — skip
  if (moduleCode && refModule !== moduleCode) return null;

  // Install-generated — skip
  if (isInstallGenerated(subPath)) return null;

  return path.join(SRC_DIR, subPath);
}

// --- File Discovery ---

function getSourceFiles(dir) {
  const files = [];
  function walk(currentDir) {
    const entries = fs.readdirSync(currentDir, { withFileTypes: true });
    for (const entry of entries) {
      if (SKIP_DIRS.has(entry.name)) continue;
      const fullPath = path.join(currentDir, entry.name);
      if (entry.isDirectory()) {
        walk(fullPath);
      } else if (entry.isFile() && SCAN_EXTENSIONS.has(path.extname(entry.name))) {
        files.push(fullPath);
      }
    }
  }
  walk(dir);
  return files;
}

// --- Reference Extraction ---

/**
 * Extract references from YAML files.
 */
function extractYamlRefs(filePath, content) {
  const refs = [];
  let doc;
  try {
    doc = yaml.parseDocument(content);
  } catch {
    return refs;
  }

  function checkValue(value, range, keyPath) {
    if (typeof value !== 'string') return;
    if (!isResolvable(value)) return;

    const line = range ? offsetToLine(content, range[0]) : undefined;

    // {project-root}/_bmad/ refs
    const prMatch = value.match(/\{project-root\}\/_bmad\/[^\s'"<>})\]`]+/);
    if (prMatch) {
      refs.push({ file: filePath, raw: prMatch[0], type: 'project-root', line, key: keyPath });
    }

    // Relative paths
    const relMatch = value.match(/^\.\.?\/[^\s'"<>})\]`]+\.(?:md|yaml|yml|xml|json|csv|txt)$/);
    if (relMatch) {
      refs.push({ file: filePath, raw: relMatch[0], type: 'relative', line, key: keyPath });
    }
  }

  function walkNode(node, keyPath) {
    if (!node) return;
    if (yaml.isMap(node)) {
      for (const item of node.items) {
        const key = item.key && item.key.value !== undefined ? item.key.value : '?';
        const childPath = keyPath ? `${keyPath}.${key}` : String(key);
        walkNode(item.value, childPath);
      }
    } else if (yaml.isSeq(node)) {
      for (const [i, item] of node.items.entries()) {
        walkNode(item, `${keyPath}[${i}]`);
      }
    } else if (yaml.isScalar(node)) {
      checkValue(node.value, node.range, keyPath);
    }
  }

  walkNode(doc.contents, '');
  return refs;
}

/**
 * Extract references from markdown files (frontmatter + body).
 */
function extractMarkdownRefs(filePath, content) {
  const refs = [];

  // Parse frontmatter
  const fmMatch = content.match(/^---\n([\s\S]*?)\n---/);
  if (fmMatch) {
    try {
      const fmData = yaml.parse(fmMatch[1]);
      if (fmData && typeof fmData === 'object') {
        for (const [key, value] of Object.entries(fmData)) {
          if (typeof value !== 'string') continue;
          if (!isResolvable(value)) continue;

          if (FRONTMATTER_PATH_KEYS.has(key)) {
            const line = offsetToLine(content, content.indexOf(`${key}:`));
            if (value.includes('{project-root}/_bmad/')) {
              refs.push({ file: filePath, raw: value, type: 'project-root', line, key });
            } else if (value.startsWith('./') || value.startsWith('../')) {
              refs.push({ file: filePath, raw: value, type: 'relative', line, key });
            }
          }
        }
      }
    } catch {
      // Unparseable frontmatter
    }
  }

  // Body references (after stripping code blocks)
  const stripped = stripCodeBlocks(content);

  // {project-root}/_bmad/ refs in body text
  PROJECT_ROOT_REF.lastIndex = 0;
  let match;
  while ((match = PROJECT_ROOT_REF.exec(stripped)) !== null) {
    const raw = `{project-root}/_bmad/${match[1]}`;
    if (!isResolvable(raw)) continue;
    // Skip if already captured from frontmatter
    if (refs.some((r) => r.raw === raw && r.file === filePath)) continue;
    refs.push({
      file: filePath,
      raw,
      type: 'project-root',
      line: offsetToLine(stripped, match.index),
    });
  }

  // Quoted relative paths in body
  for (const regex of [RELATIVE_PATH_QUOTED, RELATIVE_PATH_DOT]) {
    regex.lastIndex = 0;
    while ((match = regex.exec(stripped)) !== null) {
      const raw = match[1];
      if (!isResolvable(raw)) continue;
      if (refs.some((r) => r.raw === raw && r.file === filePath)) continue;
      refs.push({
        file: filePath,
        raw,
        type: 'relative',
        line: offsetToLine(stripped, match.index),
      });
    }
  }

  return refs;
}

/**
 * Extract workflow-file references from CSV files.
 */
function extractCsvRefs(filePath, content) {
  const refs = [];
  let records;
  try {
    records = parseCsv(content, {
      columns: true,
      skip_empty_lines: true,
      relax_column_count: true,
    });
  } catch {
    return refs;
  }

  const firstRecord = records[0];
  if (!firstRecord || !('workflow-file' in firstRecord)) return refs;

  for (const [i, record] of records.entries()) {
    const raw = record['workflow-file'];
    if (!raw || raw.trim() === '') continue;
    if (!isResolvable(raw)) continue;

    const line = i + 2; // header + 0-based index + 1
    // CSV uses bare _bmad/ prefix
    refs.push({ file: filePath, raw, type: 'project-root', line });
  }

  return refs;
}

/**
 * Detect absolute path leaks in file content.
 */
function checkAbsolutePathLeaks(filePath, content) {
  const leaks = [];
  let ignoredCount = 0;
  const stripped = stripCodeBlocks(content);
  const lines = stripped.split('\n');
  const originalLines = content.split('\n');

  for (const [i, line] of lines.entries()) {
    if (ABS_PATH_LEAK.test(line)) {
      if (isLineIgnored(originalLines, i + 1)) {
        ignoredCount++;
      } else {
        leaks.push({ file: filePath, line: i + 1, content: line.trim().slice(0, 100) });
      }
    }
  }
  return { leaks, ignoredCount };
}

// --- Reference Resolution ---

function resolveRef(ref, moduleCode) {
  if (ref.type === 'project-root') {
    // Handle bare _bmad/ prefix (from CSV)
    let refPath = ref.raw;
    if (!refPath.includes('{project-root}') && refPath.startsWith('_bmad/')) {
      refPath = `{project-root}/${refPath}`;
    }
    return mapInstalledToSource(refPath, moduleCode);
  }

  if (ref.type === 'relative') {
    const resolved = path.resolve(path.dirname(ref.file), ref.raw);
    // Skip if resolves outside src/
    if (!resolved.startsWith(SRC_DIR)) return null;
    return resolved;
  }

  return null;
}

// --- Exports for testing ---

export const _testing = {
  mapInstalledToSource,
  isResolvable,
  extractYamlRefs,
  extractMarkdownRefs,
  extractCsvRefs,
  checkAbsolutePathLeaks,
  detectModuleCode,
  isExternalRef,
  isBracketedPlaceholder,
  isInstallGenerated,
  isLineIgnored,
  isDataDirExample,
  resolveRef,
  getSourceFiles,
  stripCodeBlocks,
  offsetToLine,
  SRC_DIR,
  PROJECT_ROOT,
};

// --- Main ---

const _isMain = process.argv[1] && path.resolve(process.argv[1]) === path.resolve(__filename);
if (_isMain) {
  const moduleCode = detectModuleCode(SRC_DIR);
  console.log(`\nValidating file references in: ${path.relative(process.cwd(), SRC_DIR)}/`);
  console.log(`Mode: ${STRICT ? 'STRICT (exit 1 on issues)' : 'WARNING (exit 0)'}${VERBOSE ? ' + VERBOSE' : ''}`);
  console.log(`Module: ${moduleCode || '(unknown)'}\n`);

  const files = getSourceFiles(SRC_DIR);
  console.log(`Files to scan: ${files.length}\n`);

  let totalRefs = 0;
  let brokenRefs = 0;
  let totalLeaks = 0;
  let externalRefs = 0;
  let ignoredRefs = 0;
  let filesWithIssues = 0;
  const refsByType = { 'project-root': 0, relative: 0 };
  const allIssues = [];

  for (const filePath of files) {
    const relativePath = path.relative(PROJECT_ROOT, filePath);
    const content = fs.readFileSync(filePath, 'utf-8');
    const ext = path.extname(filePath);
    const contentLines = content.split('\n');

    // Extract references by file type
    let refs;
    if (ext === '.yaml' || ext === '.yml') {
      refs = extractYamlRefs(filePath, content);
    } else if (ext === '.csv') {
      refs = extractCsvRefs(filePath, content);
    } else {
      refs = extractMarkdownRefs(filePath, content);
    }

    // Filter inline-ignored and data-dir example refs
    refs = refs.filter((ref) => {
      if (ref.line && isLineIgnored(contentLines, ref.line)) {
        ignoredRefs++;
        return false;
      }
      if (isDataDirExample(filePath, ref.raw)) {
        ignoredRefs++;
        return false;
      }
      return true;
    });

    const broken = [];
    const external = [];

    for (const ref of refs) {
      totalRefs++;
      if (ref.type in refsByType) refsByType[ref.type]++;

      // Check for external module refs
      if (ref.type === 'project-root' && isExternalRef(ref.raw, moduleCode)) {
        externalRefs++;
        if (INCLUDE_EXTERNAL) {
          external.push({ ref, module: ref.raw.match(/\{project-root\}\/_bmad\/([^/]+)\//)?.[1] });
        }
        continue;
      }

      const resolved = resolveRef(ref, moduleCode);
      if (resolved === null) continue; // Skipped (install-generated, external, outside src)

      if (!fs.existsSync(resolved)) {
        broken.push({ ref, resolved: path.relative(PROJECT_ROOT, resolved) });
        brokenRefs++;
      }
    }

    // Absolute path leaks
    const { leaks, ignoredCount: leakIgnored } = checkAbsolutePathLeaks(filePath, content);
    totalLeaks += leaks.length;
    ignoredRefs += leakIgnored;

    const hasIssues = broken.length > 0 || leaks.length > 0;
    const hasInfo = external.length > 0;

    if (hasIssues) {
      filesWithIssues++;
      console.log(`\n${relativePath}`);

      for (const { ref, resolved } of broken) {
        const location = ref.line ? `line ${ref.line}` : ref.key ? `key: ${ref.key}` : '';
        console.log(`  [BROKEN] ${ref.raw}${location ? ` (${location})` : ''}`);
        console.log(`     Target not found: ${resolved}`);
        allIssues.push({ file: relativePath, line: ref.line || 1, ref: ref.raw, issue: 'broken ref' });
        if (process.env.GITHUB_ACTIONS) {
          const line = ref.line || 1;
          console.log(`::warning file=${relativePath},line=${line}::${escapeAnnotation(`Broken reference: ${ref.raw} → ${resolved}`)}`);
        }
      }

      for (const leak of leaks) {
        console.log(`  [ABS-PATH] Line ${leak.line}: ${leak.content}`);
        allIssues.push({ file: relativePath, line: leak.line, ref: leak.content, issue: 'abs-path' });
        if (process.env.GITHUB_ACTIONS) {
          console.log(`::warning file=${relativePath},line=${leak.line}::${escapeAnnotation(`Absolute path leak: ${leak.content}`)}`);
        }
      }
    } else if (VERBOSE && refs.length > 0) {
      console.log(`  [OK] ${relativePath} (${refs.length} refs)`);
    }

    if (hasInfo) {
      for (const { ref, module: mod } of external) {
        console.log(`  [INFO] External ref to ${mod}: ${ref.raw}`);
      }
    }
  }

  // Summary
  const totalIssues = brokenRefs + totalLeaks;
  console.log(`\n${'─'.repeat(60)}`);
  console.log(`\nSummary:`);
  console.log(`  Files scanned:        ${files.length}`);
  console.log(`  References checked:   ${totalRefs}`);
  console.log(`    project-root refs:  ${refsByType['project-root']}`);
  console.log(`    relative refs:      ${refsByType.relative}`);
  console.log(`  External (skipped):   ${externalRefs}`);
  if (ignoredRefs > 0) {
    console.log(`  Suppressed (ignored): ${ignoredRefs}`);
  }
  console.log(`  Broken references:    ${brokenRefs}`);
  console.log(`  Absolute path leaks:  ${totalLeaks}`);
  console.log(
    `  Total issues:         ${totalIssues} / ${totalRefs} refs (${totalRefs > 0 ? ((totalIssues / totalRefs) * 100).toFixed(1) : 0}%)`,
  );

  const hasIssues = totalIssues > 0;

  if (hasIssues) {
    console.log(`  Files affected:       ${filesWithIssues}`);
    if (STRICT) {
      console.log(`\n  [STRICT MODE] Exiting with failure.`);
    } else {
      console.log(`\n  Run with --strict to treat warnings as errors.`);
    }
  } else {
    console.log(`\n  All file references valid!`);
  }
  console.log('');

  // GHA step summary
  if (process.env.GITHUB_STEP_SUMMARY) {
    let summary = '## BMB File Reference Validation\n\n';
    if (allIssues.length > 0) {
      summary += '| File | Line | Reference | Issue |\n';
      summary += '|------|------|-----------|-------|\n';
      for (const iss of allIssues) {
        summary += `| ${iss.file} | ${iss.line} | ${iss.ref} | ${iss.issue} |\n`;
      }
      summary += '\n';
    }
    summary += `**${files.length} files scanned, ${totalRefs} references checked, ${brokenRefs + totalLeaks} issues found**\n`;
    fs.appendFileSync(process.env.GITHUB_STEP_SUMMARY, summary);
  }

  process.exit(hasIssues && STRICT ? 1 : 0);
}
