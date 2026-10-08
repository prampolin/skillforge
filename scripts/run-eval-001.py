#!/usr/bin/env python3
"""Prepare or run the paired EVAL-001 experiment using only installed tools."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import time
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_logged(command, cwd, env, prefix, timeout=1800):
    started = time.monotonic()
    with prefix.with_suffix('.stdout.log').open('w') as out, prefix.with_suffix('.stderr.log').open('w') as err:
        try:
            result = subprocess.run(command, cwd=cwd, env=env, stdout=out, stderr=err, timeout=timeout, check=False)
            code = result.returncode
        except subprocess.TimeoutExpired:
            code = 124
    return {'exit_code': code, 'elapsed_seconds': round(time.monotonic() - started, 3)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--prepare', action='store_true', help='Create fixtures and audit only; no model calls')
    mode.add_argument('--run', action='store_true', help='Execute both model calls (may incur usage)')
    parser.add_argument('--model', required=True)
    parser.add_argument('--effort', choices=['low', 'medium', 'high'], default='low')
    parser.add_argument('--order', choices=['baseline-first', 'skill-first'], default='baseline-first')
    args = parser.parse_args()
    codex = shutil.which('codex')
    if not codex or not shutil.which('node'):
        parser.error('Installed codex and node executables are required; nothing will be installed.')
    if not (ROOT / 'node_modules').is_dir():
        parser.error('Existing node_modules is required; dependencies will not be installed.')
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    results = Path(tempfile.mkdtemp(prefix=stamp + '-', dir=ROOT / 'evals/results/EVAL-001'))
    temp = Path(tempfile.mkdtemp(prefix='skillforge-eval-001-')).resolve()
    source_codex = Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex')))
    # Inventory paths/hashes only: config and credential contents may contain secrets.
    candidates = [source_codex / name for name in ('config.toml', 'AGENTS.md', 'AGENTS.override.md', 'managed_config.toml', 'requirements.toml')]
    for parent in {Path.home(), *ROOT.parents, temp.parent, *temp.parents}:
        candidates += [parent / name for name in ('AGENTS.md', 'AGENTS.override.md', '.codex/config.toml')]
    system_files = [Path('/etc/codex') / name for name in ('config.toml', 'managed_config.toml', 'requirements.toml')]
    candidates += system_files
    skill_roots = [Path.home() / '.agents/skills', source_codex / 'skills', Path('/etc/codex/skills')]
    audit = {'instruction_files': [{'path': str(p), 'sha256': digest(p)} for p in sorted(set(candidates)) if p.is_file()],
             'global_skill_files': sorted(str(p) for base in skill_roots if base.exists() for p in base.rglob('SKILL.md')),
             'controls': ['fresh Codex state', 'ignore user config and rules', 'project_doc_max_bytes=0',
                          'skip_host_skill_discovery=true', 'allowlisted environment', 'no shared daemon',
                          'workspace-write; never approve', 'no network for child shell commands'],
             'limitations': 'Not a filesystem read jail. Review traces for out-of-workspace reads. Managed server instructions cannot be audited locally.'}
    write_json(results / 'isolation-audit.json', audit)
    if any(p.exists() for p in system_files + [source_codex / 'managed_config.toml', source_codex / 'requirements.toml']):
        raise SystemExit(f'System/managed configuration needs review; stopped. Audit: {results}')
    # Keep HOME unchanged. Fresh application state is scoped to the child process.
    clean_env = {key: os.environ[key] for key in ('PATH', 'HOME', 'USER', 'LOGNAME', 'TMPDIR', 'LANG', 'LC_ALL') if key in os.environ}
    version = subprocess.run([codex, '--version'], text=True, capture_output=True, check=True).stdout.strip()
    (results / 'codex-version.txt').write_text(version + '\n')
    if version != 'codex-cli 0.161.0':
        raise SystemExit('This protocol is pinned to codex-cli 0.161.0. Review isolation flags before changing the pin.')
    dataset = (ROOT / 'evals/datasets/EVAL-001.md').read_text()
    prompt = dataset.split('<!-- PROMPT_START -->', 1)[1].split('<!-- PROMPT_END -->', 1)[0].strip() + '\n'
    (results / 'prompt.txt').write_text(prompt)
    skill_dir = ROOT / 'skills/nextjs-component'
    skill_files = [skill_dir / 'SKILL.md', *sorted((skill_dir / 'references').glob('*.md'))]
    guidance = '\n\n'.join(f'# {p.relative_to(skill_dir)}\n{p.read_text()}' for p in skill_files)
    (results / 'skill-instructions.txt').write_text(guidance)
    fixture = temp / 'fixture'
    fixture.mkdir()
    # Allowlist excludes repository instructions, skills, secrets, generated output and Git history.
    for name in ('app', 'src', 'components', 'lib', 'hooks', 'public', 'package.json', 'package-lock.json',
                 'tsconfig.json', 'next-env.d.ts', 'eslint.config.mjs', 'next.config.ts', 'next.config.mjs',
                 'next.config.js', 'postcss.config.mjs', 'components.json'):
        source = ROOT / name
        if source.is_dir():
            shutil.copytree(source, fixture / name, ignore=shutil.ignore_patterns('AGENTS.md', 'AGENTS.override.md', '.agents', '.codex', '.env*', 'SKILL.md'))
        elif source.is_file():
            shutil.copy2(source, fixture / name)
    initial_hashes = {str(p.relative_to(fixture)): digest(p) for p in fixture.rglob('*') if p.is_file()}
    write_json(results / 'fixture-sha256.json', initial_hashes)
    manifest = {'status': 'prepared', 'model': args.model, 'reasoning_effort': args.effort, 'order': args.order,
                'codex_version': version, 'temporary_root': str(temp), 'prompt_sha256': digest(results / 'prompt.txt'),
                'skill_sha256': {str(p.relative_to(skill_dir)): digest(p) for p in skill_files},
                'dependency_lock_sha256': digest(ROOT / 'package-lock.json'), 'arms': {}}
    write_json(results / 'manifest.json', manifest)
    for arm in ('baseline', 'with-skill'):
        work = temp / arm / 'workspace'
        shutil.copytree(fixture, work)
        # Independent physical copies prevent a generated command from mutating the real project.
        shutil.copytree(ROOT / 'node_modules', work / 'node_modules', symlinks=True)
        external_links = [str(p) for p in (work / 'node_modules').rglob('*')
                          if p.is_symlink() and not p.resolve().is_relative_to(work)]
        if external_links:
            raise SystemExit('Dependencies contain external symlinks; cannot safely isolate: ' + repr(external_links[:5]))
        state = temp / arm / 'codex-state'
        state.mkdir()
        env = dict(clean_env, CODEX_HOME=str(state))
        command = [codex, '--no-daemon', '-a', 'never', 'exec', '--ignore-user-config', '--ignore-rules',
                   '--ephemeral', '--skip-git-repo-check', '--sandbox', 'workspace-write', '--model', args.model,
                   '--color', 'never', '--json', '-C', str(work),
                   '-c', 'project_doc_max_bytes=0', '-c', 'project_doc_fallback_filenames=[]',
                   '-c', 'features.skip_host_skill_discovery=true', '-c', 'features.apps=false',
                   '-c', 'features.remote_plugin=false', '-c', 'features.shell_snapshot=false',
                   '-c', 'web_search="disabled"', '-c', 'sandbox_workspace_write.network_access=false',
                   '-c', 'shell_environment_policy.inherit="none"',
                   '-c', 'model_reasoning_effort=' + json.dumps(args.effort),
                   '-c', 'developer_instructions=' + json.dumps(guidance if arm == 'with-skill' else ''),
                   '-o', str(work / 'eval-final.txt'), '-']
        arm_dir = results / arm
        arm_dir.mkdir()
        write_json(arm_dir / 'command.json', command)
        manifest['arms'][arm] = {'status': 'not_run', 'workspace': str(work), 'usage': None}
    write_json(results / 'manifest.json', manifest)
    if args.prepare:
        print(f'Prepared only; no benchmark executed. Results: {results}\nTemporary files: {temp}')
        return
    # Require explicit API-key authentication; do not copy personal ChatGPT credentials or config.
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        raise SystemExit(f'OPENAI_API_KEY is required to run with clean state. Prepared artifacts: {results}')
    order = ('baseline', 'with-skill') if args.order == 'baseline-first' else ('with-skill', 'baseline')
    manifest['status'] = 'running'
    write_json(results / 'manifest.json', manifest)
    for arm in order:
        arm_dir = results / arm
        work = Path(manifest['arms'][arm]['workspace'])
        env = dict(clean_env, CODEX_HOME=str(temp / arm / 'codex-state'), CODEX_API_KEY=api_key)
        command = json.loads((arm_dir / 'command.json').read_text())
        started = time.monotonic()
        with (results / 'prompt.txt').open() as stdin, (arm_dir / 'events.jsonl').open('w') as stdout, (arm_dir / 'stderr.log').open('w') as stderr:
            try:
                process = subprocess.run(command, cwd=work, env=env, stdin=stdin, stdout=stdout, stderr=stderr, timeout=1800, check=False)
                code = process.returncode
            except subprocess.TimeoutExpired:
                code = 124
        usage = []
        completed = False
        malformed = 0
        for line in (arm_dir / 'events.jsonl').read_text().splitlines():
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                malformed += 1
                continue
            if event.get('type') == 'turn.completed':
                completed = True
                if isinstance(event.get('usage'), dict):
                    usage.append(event['usage'])
        info = {'status': 'completed' if code == 0 and completed else 'failed', 'exit_code': code,
                'elapsed_seconds': round(time.monotonic() - started, 3), 'workspace': str(work),
                'usage': usage or None, 'malformed_event_lines': malformed, 'manual_rubric': 'pending'}
        # Check generated code using pristine configuration, not any model-modified configuration.
        final_hashes = {str(p.relative_to(work)): digest(p) for p in work.rglob('*')
                        if p.is_file() and 'node_modules' not in p.parts and '.git' not in p.parts}
        changed = sorted(p for p in initial_hashes if final_hashes.get(p) != initial_hashes[p])
        added = sorted(set(final_hashes) - set(initial_hashes))
        info['changed_existing_files'] = changed
        info['added_files'] = added
        info['required_outputs_present'] = all((work / p).is_file() for p in ('components/user-card.tsx', 'app/user-card-demo/page.tsx'))
        artifacts = arm_dir / 'artifacts'
        artifacts.mkdir()
        for name in added + changed:
            source = work / name
            if source.is_file() and not source.is_symlink():
                target = artifacts / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
        for name in ('tsconfig.json', 'eslint.config.mjs'):
            if (fixture / name).exists():
                shutil.copy2(fixture / name, work / name)
        checks = {}
        for name, executable, config, flags in (
            ('typescript', 'tsc', 'tsconfig.json', ['--noEmit', '--incremental', 'false']),
            ('eslint', 'eslint', 'eslint.config.mjs', ['.', '--max-warnings=0'])):
            binary = ROOT / 'node_modules/.bin' / executable
            if (work / config).exists() and binary.exists():
                checks[name] = run_logged([str(binary), *flags], work, clean_env, arm_dir / name)
            else:
                checks[name] = {'status': 'not_configured_or_unavailable'}
        info['checks'] = checks
        if changed or not info['required_outputs_present'] or any(c.get('exit_code', 0) != 0 for c in checks.values()):
            info['status'] = 'failed'
        manifest['arms'][arm] = info
        write_json(arm_dir / 'summary.json', info)
        write_json(results / 'manifest.json', manifest)
    manifest['status'] = 'completed_pending_manual_review' if all(v['status'] == 'completed' for v in manifest['arms'].values()) else 'failed'
    write_json(results / 'manifest.json', manifest)
    print(f"{manifest['status']}: {results}\nTemporary files retained: {temp}")
    if manifest['status'] == 'failed':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
