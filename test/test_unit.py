import json, os, subprocess, sys
import pytest
from xtrgen import xtrgen as tf

SCRIPT = tf.__file__
yaml = pytest.importorskip('yaml', reason='PyYAML not installed')


def test_load_config_json(tmp_path):
    p = tmp_path / 'c.json'
    p.write_text(json.dumps({'name': 'x', 'n': 2}), encoding='utf-8')
    assert tf.load_config(str(p)) == {'name': 'x', 'n': 2}


@pytest.mark.parametrize('ext', ['.yml', '.yaml', '.YML', '.Yaml'])
def test_load_config_yaml_extensions(tmp_path, ext):
    p = tmp_path / f'c{ext}'
    p.write_text('name: x\nn: 2\n', encoding='utf-8')
    assert tf.load_config(str(p)) == {'name': 'x', 'n': 2}


def test_load_template_file_and_string(tmp_path):
    p = tmp_path / 't.txt'
    p.write_text('hi {{name}}', encoding='utf-8')
    assert tf.load_template(str(p)) == 'hi {{name}}'
    assert tf.load_template('raw {{name}}') == 'raw {{name}}'


def test_fill_template():
    out = tf.fill_template({'name': 'x', 'n': 2}, '{{name}}-{{n}}-{{missing}}')
    assert out == 'x-2-{{missing}}'


def test_save_output_atomic(tmp_path):
    target = tmp_path / 'out.txt'
    target.write_text('old', encoding='utf-8')
    tf.save_output(str(target), 'new')
    assert target.read_text(encoding='utf-8') == 'new'
    assert os.listdir(tmp_path) == ['out.txt']  # no temp file left behind


def test_cli_stdout_and_dash(tmp_path):
    cfg = tmp_path / 'c.json'
    cfg.write_text('{"name": "x"}', encoding='utf-8')
    base = [sys.executable, SCRIPT, '--config', str(cfg), '--template', 'hi {{name}}']
    for extra in ([], ['--out', '-']):
        r = subprocess.run(base + extra, capture_output=True, text=True, check=True)
        assert r.stdout == 'hi x\n'


def test_cli_out_file(tmp_path):
    cfg = tmp_path / 'c.yaml'
    cfg.write_text('name: x\n', encoding='utf-8')
    out = tmp_path / 'o.txt'
    subprocess.run([sys.executable, SCRIPT, '--config', str(cfg),
                    '--template', 'hi {{name}}', '--out', str(out)], check=True)
    assert out.read_text(encoding='utf-8') == 'hi x'