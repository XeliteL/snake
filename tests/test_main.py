import pytest

from conftest import StopInfiniteLoop


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

