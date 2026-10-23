import os
import subprocess
from repoguard.php_inventory import inventory


def repo(tmp_path):
    subprocess.run(['git', 'init', '-q', str(tmp_path)], check=True)
    subprocess.run(['git','-C',str(tmp_path),'-c','user.name=Lab','-c','user.email=lab@example.invalid','commit','--allow-empty','-qm','fixture'],check=True)
    return tmp_path


def add(root, name, content):
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    subprocess.run(['git','-C',str(root),'add',name],check=True)


def test_no_indicator_does_not_clear_deployment(tmp_path):
    root=repo(tmp_path)
    add(root,'app.js','console.log("hello")')
    result=inventory(root)
    assert result['source_status']=='NO_INDICATOR_FOUND'
    assert result['deployment_status']=='UNKNOWN'
    assert result['working_tree_dirty'] is True


def test_php_source_and_manifest_are_detected(tmp_path):
    root=repo(tmp_path)
    add(root,'index.PHP','')
    add(root,'composer.json','{}')
    result=inventory(root)
    assert result['source_status']=='REVIEW_REQUIRED'
    assert {i['path'] for i in result['indicators']}=={'composer.json','index.PHP'}


def test_docker_reference_requires_review(tmp_path):
    root=repo(tmp_path)
    add(root,'Dockerfile','FROM php:8.4-fpm')
    assert inventory(root)['source_status']=='REVIEW_REQUIRED'


def test_untracked_file_outside_scope(tmp_path):
    root=repo(tmp_path)
    (root/'private.php').write_text('<?php')
    assert inventory(root)['tracked_files']==0


def test_symlink_is_not_followed(tmp_path):
    root=repo(tmp_path)
    (root/'target.txt').write_text('php')
    (root/'link.txt').symlink_to(root/'target.txt')
    subprocess.run(['git','-C',str(root),'add','link.txt'],check=True)
    assert inventory(root)['skipped_files']==['link.txt']


def test_non_utf8_tracked_filename_cannot_crash_inventory(tmp_path):
    root = repo(tmp_path)
    raw_name = b'legacy-\xff.php'
    raw_root = os.fsencode(root)
    with open(raw_root + b'/' + raw_name, 'wb') as handle:
        handle.write(b'<?php echo "fixture";')
    subprocess.run([b'git', b'-C', raw_root, b'add', raw_name], check=True)

    result = inventory(root)

    assert result['source_status'] == 'REVIEW_REQUIRED'
    assert any(os.fsencode(item['path']) == raw_name for item in result['indicators'])
