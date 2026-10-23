"""Read-only PHP indicators in a Git checkout. Never certifies deployed systems."""
import argparse
import json
from pathlib import Path
import re
import subprocess

PHP_SUFFIXES = {'.php', '.phtml', '.php3', '.php4', '.php5', '.phar'}
PATTERN = re.compile(r'\b(?:php(?:-fpm|-cgi)?|mod_php|frankenphp|composer)\b', re.I)


def inventory(root):
    root = Path(root).resolve()
    paths = subprocess.check_output(['git', 'ls-files', '-z'], cwd=root).decode().split('\0')
    paths = [p for p in paths if p]
    indicators, skipped = [], []
    for name in sorted(paths):
        path = root / name
        if path.is_symlink() or not path.is_file():
            skipped.append(name)
            continue
        if path.suffix.lower() in PHP_SUFFIXES or path.name.lower() in {'composer.json', 'composer.lock'}:
            indicators.append({'path': name, 'reason': 'PHP source or Composer manifest'})
        try:
            if path.stat().st_size > 1_000_000:
                skipped.append(name)
                continue
            content = path.read_text(encoding='utf-8')
        except (UnicodeError, OSError):
            skipped.append(name)
            continue
        # References are leads, not proof of a deployed runtime or an affected version.
        if PATTERN.search(content):
            indicators.append({'path': name, 'reason': 'PHP-related text reference; human assessment required'})
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
    dirty = bool(subprocess.check_output(['git', 'status', '--porcelain'], cwd=root))
    return {'repository': root.name, 'commit': commit, 'working_tree_dirty': dirty,
            'tracked_files': len(paths), 'indicators': indicators, 'skipped_files': skipped,
            'source_status': 'REVIEW_REQUIRED' if indicators else 'NO_INDICATOR_FOUND',
            'deployment_status': 'UNKNOWN',
            'limitations': 'Tracked working-tree files only; skips symlinks, unreadable/binary files and content over 1 MB. Untracked files, fetched dependencies, images, hosting and third-party services are not inspected. No vulnerability or patch-status determination.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('repository', type=Path)
    args = parser.parse_args()
    print(json.dumps(inventory(args.repository), indent=2))

if __name__ == '__main__':
    main()
