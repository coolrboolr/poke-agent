import time
from pathlib import Path
from src.array_utils import zeros, copy_array

from .conftest import load_image

from src.perception.screen_diff import ScreenDiffer
from src.perception.hud_parser import HUDParser
from src.perception.sprite_detector import SpriteDetector
from src.perception.runner import PerceptionRunner


def test_screen_diff_latency_and_change(tmp_path):
    frame = load_image('blank.png')
    differ = ScreenDiffer()
    start = time.perf_counter()
    assert differ.has_changed(frame) is False
    elapsed = (time.perf_counter() - start) * 1000
    assert elapsed < 5
    modified = copy_array(frame)
    modified[0][0][0] = 255
    assert differ.has_changed(modified) is True


def test_hud_parser(monkeypatch):
    frame = load_image('textbox.png')
    parser = HUDParser()
    monkeypatch.setattr('pytesseract.image_to_string', lambda img: 'Hello world')
    result = parser.parse(frame)
    assert result['dialogue_text'] == 'Hello world'
    assert result['player_hp'] == 0.0

    battle = load_image('battle.png')
    monkeypatch.setattr('pytesseract.image_to_string', lambda img: '')
    result = parser.parse(battle)
    assert result['player_hp'] > 0.9
    assert 0.45 < result['enemy_hp'] < 0.65


def test_sprite_detector_latency():
    frame = load_image('blank.png')
    det = SpriteDetector()
    start = time.perf_counter()
    boxes = det.detect(frame)
    elapsed = (time.perf_counter() - start) * 1000
    assert elapsed < 15
    assert isinstance(boxes, list)
    assert boxes and boxes[0]['name'] == 'player'


def test_perception_runner(tmp_path, monkeypatch, caplog):
    monkeypatch.chdir(tmp_path)
    runner = PerceptionRunner()
    monkeypatch.setattr('pytesseract.image_to_string', lambda img: '')
    caplog.set_level('INFO')
    blank = load_image('blank.png')
    state1 = runner.process_frame(blank)
    assert state1['changed'] is False
    battle = load_image('battle.png')
    state2 = runner.process_frame(battle)
    assert state2['changed'] is True
    log_files = list(Path('logs').glob('game_state_*.json'))
    assert log_files
    assert any('perception' in m for m in caplog.text.splitlines())

