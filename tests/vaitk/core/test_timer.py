import sys

from vaitk.core import CoreApplication, Timer


def test_instantiation():
    app = CoreApplication(sys.argv)
    try:
        timer = Timer()
        assert timer.interval is None
        assert not timer.single_shot
        assert not timer.is_running()
    finally:
        app.exit()


def test_single_shot_timer_runs_on_event_loop():
    app = CoreApplication(sys.argv)
    fired = []
    timer = Timer.single_shot_timer(1, lambda: (fired.append(True), app.exit()))
    try:
        assert timer.is_running()
        app.run()
        assert fired == [True]
        assert not timer.is_running()
    finally:
        app.exit()


def test_repeating_timer_can_be_stopped():
    app = CoreApplication(sys.argv)
    fired = []

    def on_timeout():
        fired.append(True)
        timer.stop()
        app.exit()

    timer = Timer(interval=1)
    timer.timeout.connect(on_timeout)
    timer.start()
    try:
        app.run()
        assert fired == [True]
        assert not timer.is_running()
    finally:
        app.exit()
