import pytest

from conftest import StopInfiniteLoop
from game_objects import Poison
from settings import GRID_SIZE, START_SPEED


@pytest.mark.timeout(1, method='thread')
@pytest.mark.usefixtures('modified_clock')
def test_main_run_without_exceptions(_the_snake):
    try:
        _the_snake.main()
    except StopInfiniteLoop:
        pass
    except Exception as error:
        raise AssertionError(
            'При запуске функции `main` возникло исключение: '
            f'`{type(error).__name__}: {error}`\n\n'
            'Убедитесь, что функция работает корректно.'
        )


PAUSE_MARK = (1, 2, 3)


def run_frames(monkeypatch, the_snake, frames, on_keys):
    """Прогоняет `main` заданное число кадров.

    Вместо `handle_keys` на каждом кадре вызывается on_keys(snake, frame).
    Надпись паузы подменяется пикселем цвета PAUSE_MARK в углу экрана.
    """
    frame = 0

    class _Clock:
        def tick(self, *args):
            nonlocal frame
            frame += 1
            if frame > frames:
                raise StopInfiniteLoop

    def fake_keys(snake):
        on_keys(snake, frame)

    draw_calls = []

    def fake_draw_pause():
        draw_calls.append(frame)
        the_snake.screen.set_at((0, 0), PAUSE_MARK)

    monkeypatch.setattr(the_snake, 'clock', _Clock())
    monkeypatch.setattr(the_snake, 'handle_keys', fake_keys)
    monkeypatch.setattr(the_snake, 'draw_pause', fake_draw_pause)
    # Экран общий для всех тестов: убираем следы предыдущих.
    the_snake.screen.fill((0, 0, 0))
    with pytest.raises(StopInfiniteLoop):
        the_snake.main()
    return draw_calls


def test_snake_stands_still_on_pause(monkeypatch, _the_snake):
    seen = []

    def on_keys(snake, frame):
        snake.paused = True
        seen.append(list(snake.positions))

    draw_calls = run_frames(monkeypatch, _the_snake, 5, on_keys)
    assert all(positions == seen[0] for positions in seen)
    # Надпись рисуется один раз, а не на каждом кадре паузы.
    assert draw_calls == [1]


def test_unpause_resumes_and_removes_text(monkeypatch, _the_snake):
    seen = []

    def on_keys(snake, frame):
        # Кадры 1-2 на паузе, дальше игра идёт.
        snake.paused = frame <= 2
        seen.append(list(snake.positions))

    run_frames(monkeypatch, _the_snake, 4, on_keys)
    assert seen[0] == seen[2]
    assert seen[3] != seen[2]
    assert tuple(_the_snake.screen.get_at((0, 0)))[:3] != PAUSE_MARK


def game_over_frames(monkeypatch, the_snake, frames, on_keys):
    """Как `run_frames`, но дополнительно считает вызовы `draw_game_over`.

    Возвращает номера кадров, на которых рисовалась надпись проигрыша.
    """
    calls = []
    current = {'frame': 0}

    def keys(snake, frame):
        current['frame'] = frame
        on_keys(snake, frame)

    monkeypatch.setattr(
        the_snake, 'draw_game_over',
        lambda score, record: calls.append(current['frame'])
    )
    run_frames(monkeypatch, the_snake, frames, keys)
    return calls


def test_snake_stands_still_after_game_over(monkeypatch, _the_snake):
    seen = []

    def on_keys(snake, frame):
        snake.game_over = True
        seen.append(list(snake.positions))

    calls = game_over_frames(monkeypatch, _the_snake, 5, on_keys)
    assert all(positions == seen[0] for positions in seen)
    # Надпись рисуется один раз, а не на каждом кадре проигрыша.
    assert calls == [1]


def test_game_resets_after_game_over(monkeypatch, _the_snake):
    seen = []

    def on_keys(snake, frame):
        if frame == 1:
            snake.length = 5
            snake.speed = 10
            snake.game_over = True
        elif frame == 3:
            # Игрок нажал клавишу после задержки.
            snake.game_over = False
        seen.append((snake.length, snake.speed))

    game_over_frames(monkeypatch, _the_snake, 4, on_keys)
    assert seen[2] == (5, 10)
    assert seen[3] == (1, START_SPEED)


def test_game_is_not_reset_again_after_restart(monkeypatch, _the_snake):
    seen = []

    def on_keys(snake, frame):
        if frame == 1:
            snake.game_over = True
        elif frame == 2:
            snake.game_over = False
        elif frame == 4:
            # Змейка подросла уже в новой игре.
            snake.length = 3
        seen.append(snake.length)

    game_over_frames(monkeypatch, _the_snake, 6, on_keys)
    assert seen[4:] == [3, 3]


def test_second_game_over_shows_text_again(monkeypatch, _the_snake):
    def on_keys(snake, frame):
        if frame in (1, 4):
            snake.game_over = True
        elif frame in (2, 5):
            snake.game_over = False

    calls = game_over_frames(monkeypatch, _the_snake, 5, on_keys)
    assert calls == [1, 4]


def test_poison_death_does_not_crash_main(monkeypatch, _the_snake):
    poisons = []

    class RecordedPoison(Poison):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            poisons.append(self)

    states = []

    def on_keys(snake, frame):
        if frame == 1:
            # Отрава прямо перед головой змейки длиной 1.
            head_x, head_y = snake.get_head_position()
            poisons[0].positions = [(head_x + GRID_SIZE, head_y)]
        states.append(snake.game_over)

    monkeypatch.setattr(_the_snake, 'Poison', RecordedPoison)
    game_over_frames(monkeypatch, _the_snake, 3, on_keys)
    assert states == [False, True, True]
