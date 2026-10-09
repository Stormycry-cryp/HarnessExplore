"""Exercise bootstrap contracts with real local Git and stubbed network/install commands."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
REAL_GIT = shutil.which('git')
SCRIPT = REPO / 'harness-explore/scripts/bootstrap_codex.sh'
MANIFEST = REPO / 'harness-explore/references/codex-source-files.txt'
OFFICIAL = 'https://github.com/openai/codex.git'


class BootstrapTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='bootstrap-tests-', dir=REPO.parent)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.upstream = self.root / 'upstream'
        self.upstream.mkdir()
        self.git('init', '-b', 'main', str(self.upstream))
        for source in MANIFEST.read_text().splitlines():
            if not source or source.startswith('#'):
                continue
            path = self.upstream / source
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('fixture: ' + source + '\n')
        self.git('-C', str(self.upstream), 'add', '.')
        self.commit('first')
        self.first = self.git('-C', str(self.upstream), 'rev-parse', 'HEAD').stdout.strip()
        self.git('-C', str(self.upstream), 'tag', 'v1')
        (self.upstream / 'README.md').write_text('second snapshot\n')
        self.git('-C', str(self.upstream), 'add', '.')
        self.commit('second')
        self.second = self.git('-C', str(self.upstream), 'rev-parse', 'HEAD').stdout.strip()
        self.cache = self.root / 'cache'
        self.source = self.cache / 'openai-codex'
        self.evidence = self.cache / 'bootstrap-evidence.txt'
        self.log = self.root / 'calls.jsonl'
        package = self.root / 'package'
        (package / 'scripts').mkdir(parents=True)
        (package / 'references').mkdir()
        self.script = package / 'scripts/bootstrap_codex.sh'
        self.manifest = package / 'references/codex-source-files.txt'
        shutil.copy(SCRIPT, self.script)
        shutil.copy(MANIFEST, self.manifest)
        self.bin = self.root / 'bin'
        self.bin.mkdir()
        self.env = os.environ.copy()
        self.env.pop('HARNESS_EXPLORE_SOURCE_REF', None)
        self.env.update(PATH=str(self.bin) + os.pathsep + os.environ['PATH'],
                        HARNESS_EXPLORE_CACHE=str(self.cache), REAL_GIT=REAL_GIT,
                        FIXTURE=str(self.upstream), CALL_LOG=str(self.log))
        self.stub('git', '''
a = sys.argv[1:]
if os.environ.get('REQUIRE_NO_LAZY_FETCH') == '1' and os.environ.get('GIT_NO_LAZY_FETCH') != '1':
    sys.exit(91)
if 'fetch' in a and os.environ.get('FAIL_FETCH') == '1':
    sys.exit(92)
if 'clone' in a:
    a = [os.environ['FIXTURE'] if x == 'https://github.com/openai/codex.git' else x for x in a]
    result = subprocess.run([os.environ['REAL_GIT']] + a)
    if result.returncode == 0:
        subprocess.run([os.environ['REAL_GIT'], '-C', a[-1], 'remote', 'set-url', 'origin', 'https://github.com/openai/codex.git'], check=True)
    sys.exit(result.returncode)
if 'fetch' in a:
    a[a.index('origin')] = os.environ['FIXTURE']
sys.exit(subprocess.run([os.environ['REAL_GIT']] + a).returncode)
''')
        self.stub('curl', '''
if os.environ.get('FAIL_MANUAL') == '1': sys.exit(22)
Path(sys.argv[sys.argv.index('-o') + 1]).write_text('fresh official manual fixture\\n')
''')
        self.stub('codex', '''
if os.environ.get('DISABLE_GLOBAL') == '1': sys.exit(1)
print('codex-cli fixture-global')
''')
        self.stub('npm', '''
root = Path(sys.argv[sys.argv.index('--prefix') + 1])
cli = root / 'node_modules/.bin/codex'
cli.parent.mkdir(parents=True, exist_ok=True)
cli.write_text('#!/bin/sh\\necho codex-cli fixture-isolated\\n')
cli.chmod(0o755)
''')

    def git(self, *args):
        return subprocess.run([REAL_GIT, *args], text=True, capture_output=True, check=True)

    def commit(self, message):
        self.git('-C', str(self.upstream), '-c', 'user.name=Fixture',
                 '-c', 'user.email=fixture@example.invalid', 'commit', '-m', message)

    def stub(self, name, body):
        path = self.bin / name
        path.write_text('#!' + shutil.which('python3') + '\n' +
                        'import json, os, subprocess, sys\nfrom pathlib import Path\n' +
                        "with open(os.environ['CALL_LOG'], 'a') as f: f.write(json.dumps([Path(sys.argv[0]).name] + sys.argv[1:]) + '\\n')\n" + body)
        path.chmod(0o755)

    def run_bootstrap(self, *args, success=True):
        p = subprocess.run(['bash', str(self.script), *args], env=self.env,
                           text=True, capture_output=True)
        if success:
            self.assertEqual(p.returncode, 0, p.stderr + p.stdout)
        else:
            self.assertNotEqual(p.returncode, 0, p.stdout)
        return p

    def fields(self):
        return dict(line.split('=', 1) for line in self.evidence.read_text().splitlines())

    def calls(self):
        return [json.loads(line) for line in self.log.read_text().splitlines()]

    def test_online_records_verified_snapshot_and_manual(self):
        self.run_bootstrap()
        f = self.fields()
        self.assertEqual(f['source_commit'], self.second)
        self.assertEqual(f['source_ref'], 'main')
        self.assertEqual(f['source_state'], 'fetched_verified')
        self.assertEqual(f['manual_status'], 'downloaded')
        self.assertEqual(f['codex_version'], 'codex-cli fixture-global')
        for key in ('checked_at_utc', 'source_acquired_at_utc', 'manual_acquired_at_utc'):
            self.assertRegex(f[key], r'^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$')
        self.assertEqual(self.git('-C', str(self.source), 'remote', 'get-url', 'origin').stdout.strip(), OFFICIAL)
        self.assertEqual(self.git('-C', str(self.source), 'config', '--get', 'core.sparseCheckout').stdout.strip(), 'true')

    def test_offline_has_no_network_or_install_and_preserves_acquisition(self):
        self.env['HARNESS_EXPLORE_SOURCE_REF'] = 'v1'
        self.run_bootstrap()
        before = self.fields()
        self.env.pop('HARNESS_EXPLORE_SOURCE_REF')
        self.log.write_text('')
        self.env['REQUIRE_NO_LAZY_FETCH'] = '1'
        self.run_bootstrap('--offline')
        after = self.fields()
        self.assertEqual(after['mode'], 'offline')
        self.assertEqual(after['source_ref'], 'v1')
        self.assertEqual(after['source_commit'], self.first)
        self.assertEqual(after['source_acquired_at_utc'], before['source_acquired_at_utc'])
        self.assertEqual(after['manual_status'], 'cached_stale')
        self.assertEqual(after['manual_attempted_at_utc'], 'not_attempted')
        for call in self.calls():
            self.assertNotIn(call[0], ('curl', 'npm'))
            self.assertFalse(call[0] == 'git' and any(a in call for a in ('fetch', 'clone')))

    def test_true_partial_clone_supports_offline_status(self):
        # file:// honors blob filters; a plain local path silently ignores them.
        self.git('-C', str(self.upstream), 'config', 'uploadpack.allowFilter', 'true')
        (self.upstream / '.gitignore').write_text('node_modules/\n')
        excluded = self.upstream / 'not-selected.txt'
        excluded.write_text('This blob must remain outside the sparse download.\n')
        self.git('-C', str(self.upstream), 'add', '.gitignore', excluded.name)
        self.commit('partial-clone fixture')
        commit = self.git('-C', str(self.upstream), 'rev-parse', 'HEAD').stdout.strip()
        ignored_blob = self.git('-C', str(self.upstream), 'rev-parse', 'HEAD:.gitignore').stdout.strip()
        excluded_blob = self.git('-C', str(self.upstream), 'rev-parse', 'HEAD:not-selected.txt').stdout.strip()
        self.env['FIXTURE_URL'] = self.upstream.as_uri()
        self.stub('git', '''a = sys.argv[1:]
if os.environ.get('REQUIRE_NO_LAZY_FETCH') == '1' and os.environ.get('GIT_NO_LAZY_FETCH') != '1':
    sys.exit(91)
# Pass a process-local URL rewrite to online Git and its lazy-fetch children.
# Keep remote get-url unmodified so bootstrap verifies the actual official origin.
if os.environ.get('GIT_NO_LAZY_FETCH') != '1' and not ('remote' in a and 'get-url' in a):
    a = ['-c', 'url.' + os.environ['FIXTURE_URL'] + '.insteadOf=https://github.com/openai/codex.git'] + a
sys.exit(subprocess.run([os.environ['REAL_GIT']] + a).returncode)
''')
        online = self.run_bootstrap('--skip-cli')
        self.assertNotIn('filtering not recognized', online.stderr)
        self.assertNotIn('--filter is ignored', online.stderr)
        self.assertEqual(self.git('-C', str(self.source), 'config', '--get', 'remote.origin.promisor').stdout.strip(), 'true')
        self.assertEqual(self.git('-C', str(self.source), 'config', '--get', 'remote.origin.partialclonefilter').stdout.strip(), 'blob:none')
        self.assertEqual((self.source / '.gitignore').read_text(), 'node_modules/\n')
        no_fetch_env = os.environ.copy()
        no_fetch_env['GIT_NO_LAZY_FETCH'] = '1'
        blobs = subprocess.run([REAL_GIT, '-C', str(self.source), 'rev-list', '--objects', '--all', '--missing=print'],
                               env=no_fetch_env, text=True, capture_output=True, check=True)
        self.assertIn('?' + excluded_blob, blobs.stdout, 'fixture must contain an undownloaded blob')
        self.assertNotIn('?' + ignored_blob, blobs.stdout, '.gitignore must be downloaded online')
        self.log.write_text('')
        self.env['REQUIRE_NO_LAZY_FETCH'] = '1'
        # Any accidental offline transport is blocked, even if a child bypasses the stub.
        self.env.update(GIT_CONFIG_COUNT='1', GIT_CONFIG_KEY_0='protocol.allow',
                        GIT_CONFIG_VALUE_0='never', GIT_TRACE=str(self.root / 'offline-git.trace'))
        offline = self.run_bootstrap('--offline', '--skip-cli')
        self.assertNotIn('lazy fetching disabled', offline.stderr)
        self.assertNotIn('could not fetch', offline.stderr)
        self.assertEqual(self.fields()['source_commit'], commit)
        self.assertEqual(self.fields()['source_state'], 'cached_verified')
        for call in self.calls():
            self.assertNotIn(call[0], ('curl', 'npm'))
            self.assertFalse(call[0] == 'git' and any(a in call for a in ('fetch', 'clone')))
        trace = (self.root / 'offline-git.trace').read_text()
        self.assertNotIn('remote-https', trace)
        self.assertNotIn('upload-pack', trace)
        self.assertNotIn(' fetch ', trace)

    def test_commit_and_tag_pin_actual_sha(self):
        for ref in (self.first, 'v1'):
            self.env['HARNESS_EXPLORE_SOURCE_REF'] = ref
            self.run_bootstrap('--skip-cli')
            self.assertEqual(self.fields()['source_commit'], self.first)
            self.assertEqual(self.fields()['source_ref'], ref)
            self.run_bootstrap('--offline', '--skip-cli')

    def test_offline_ref_mismatch_preserves_evidence(self):
        self.run_bootstrap('--skip-cli')
        evidence = self.evidence.read_bytes()
        self.env['HARNESS_EXPLORE_SOURCE_REF'] = 'v1'
        p = self.run_bootstrap('--offline', '--skip-cli', success=False)
        self.assertIn('does not verify requested ref', p.stderr)
        self.assertEqual(self.evidence.read_bytes(), evidence)

    def test_missing_paths_are_reported_together_and_previous_cache_survives(self):
        self.run_bootstrap('--skip-cli')
        evidence = self.evidence.read_bytes()
        with self.manifest.open('a') as f:
            f.write('missing/one.rs\nmissing/two.rs\n')
        p = self.run_bootstrap('--skip-cli', success=False)
        self.assertIn('missing/one.rs', p.stderr)
        self.assertIn('missing/two.rs', p.stderr)
        self.assertIn('ls-tree', p.stderr)
        self.assertIn('gh api', p.stderr)
        self.assertEqual(self.git('-C', str(self.source), 'rev-parse', 'HEAD').stdout.strip(), self.second)
        self.assertEqual(self.evidence.read_bytes(), evidence)

    def test_stale_manual_is_not_reported_as_downloaded(self):
        self.run_bootstrap('--skip-cli')
        old = self.fields()
        manual = (self.cache / 'codex-manual.md').read_bytes()
        self.env['FAIL_MANUAL'] = '1'
        p = self.run_bootstrap('--skip-cli')
        self.assertEqual(self.fields()['manual_status'], 'cached_stale')
        self.assertEqual(self.fields()['manual_acquired_at_utc'], old['manual_acquired_at_utc'])
        self.assertEqual((self.cache / 'codex-manual.md').read_bytes(), manual)
        self.assertIn('download failed', p.stderr)

    def test_fetch_failure_keeps_previous_snapshot_and_evidence(self):
        self.run_bootstrap('--skip-cli')
        evidence = self.evidence.read_bytes()
        self.env['FAIL_FETCH'] = '1'
        self.run_bootstrap('--skip-cli', success=False)
        self.assertEqual(self.evidence.read_bytes(), evidence)
        self.assertEqual(self.git('-C', str(self.source), 'rev-parse', 'HEAD').stdout.strip(), self.second)

    def test_manual_failure_without_cache_is_unavailable(self):
        self.env['FAIL_MANUAL'] = '1'
        self.run_bootstrap('--skip-cli')
        self.assertEqual(self.fields()['manual_status'], 'unavailable')
        self.assertEqual(self.fields()['manual_path'], 'unavailable')
        self.assertFalse((self.cache / 'codex-manual.md').exists())

    def test_legacy_manual_acquisition_is_unknown(self):
        self.cache.mkdir()
        (self.cache / 'codex-manual.md').write_text('old unrecorded manual\n')
        self.env['FAIL_MANUAL'] = '1'
        self.run_bootstrap('--skip-cli')
        self.assertEqual(self.fields()['manual_status'], 'cached_stale')
        self.assertEqual(self.fields()['manual_acquired_at_utc'], 'unknown')

    def test_dirty_checkout_is_never_overwritten(self):
        self.run_bootstrap('--skip-cli')
        readme = self.source / 'README.md'
        readme.write_text('user edit\n')
        evidence = self.evidence.read_bytes()
        for args in (('--skip-cli',), ('--offline', '--skip-cli')):
            self.log.write_text('')
            p = self.run_bootstrap(*args, success=False)
            self.assertIn('Refusing dirty source checkout', p.stderr)
            self.assertEqual(readme.read_text(), 'user edit\n')
            self.assertEqual(self.evidence.read_bytes(), evidence)
            self.assertFalse(any('fetch' in c or 'clone' in c for c in self.calls()))

    def test_untracked_files_make_checkout_dirty(self):
        self.run_bootstrap('--skip-cli')
        (self.source / 'personal-notes.txt').write_text('keep me\n')
        self.assertIn('dirty source checkout', self.run_bootstrap('--skip-cli', success=False).stderr)

    def test_ignored_user_files_are_preserved(self):
        self.run_bootstrap('--skip-cli')
        (self.source / '.git/info/exclude').write_text('personal-notes.txt\n')
        personal = self.source / 'personal-notes.txt'
        personal.write_text('keep ignored content\n')
        self.assertIn('dirty source checkout', self.run_bootstrap('--skip-cli', success=False).stderr)
        self.assertEqual(personal.read_text(), 'keep ignored content\n')

    def test_source_symlink_and_nonofficial_origin_are_rejected(self):
        self.cache.mkdir()
        self.source.symlink_to(self.upstream, target_is_directory=True)
        self.assertIn('source symlink', self.run_bootstrap('--skip-cli', success=False).stderr)
        self.source.unlink()
        self.run_bootstrap('--skip-cli')
        self.git('-C', str(self.source), 'remote', 'set-url', 'origin', 'https://example.invalid/codex.git')
        self.assertIn('non-official', self.run_bootstrap('--offline', '--skip-cli', success=False).stderr)

    def test_skip_cli_never_invokes_codex_or_npm(self):
        self.run_bootstrap('--skip-cli')
        self.assertEqual(self.fields()['cli_status'], 'skipped')
        self.assertEqual(self.fields()['codex_version'], 'unavailable')
        self.assertFalse(any(c[0] in ('codex', 'npm') for c in self.calls()))

    def test_cli_install_is_isolated_and_offline_reuses_it(self):
        self.env['DISABLE_GLOBAL'] = '1'
        self.run_bootstrap()
        self.assertEqual(self.fields()['cli_status'], 'isolated_installed')
        self.assertEqual(self.fields()['codex_version'], 'codex-cli fixture-isolated')
        npm_calls = [c for c in self.calls() if c[0] == 'npm']
        self.assertEqual(len(npm_calls), 1)
        self.assertIn(str(self.cache / 'codex-cli'), npm_calls[0])
        self.assertNotIn('-g', npm_calls[0])
        self.log.write_text('')
        self.run_bootstrap('--offline')
        self.assertEqual(self.fields()['cli_status'], 'isolated_cached')
        self.assertFalse(any(c[0] == 'npm' for c in self.calls()))

    def test_offline_missing_cache_or_cli_fails_without_install(self):
        self.assertIn('existing official source cache', self.run_bootstrap('--offline', '--skip-cli', success=False).stderr)
        self.run_bootstrap('--skip-cli')
        self.env['DISABLE_GLOBAL'] = '1'
        self.log.write_text('')
        self.assertIn('no working Codex CLI', self.run_bootstrap('--offline', success=False).stderr)
        self.assertFalse(any(c[0] in ('npm', 'curl') for c in self.calls()))


if __name__ == '__main__':
    unittest.main()
