import threading

from pytest_tagging.utils import TagCounter


class TestTagCounter:
    def test_update(self):
        counter = TagCounter(threading.Lock())
        assert dict(counter.items()) == {}

        counter.update({"A", "B", "C"})
        assert dict(counter.items()) == {"A": 1, "B": 1, "C": 1}

        counter.update({"A"})
        assert dict(counter.items()) == {"A": 2, "B": 1, "C": 1}

    def test_empty_is_false(self):
        assert bool(TagCounter(threading.Lock())) is False

    def test_threadsafe_update(self):
        counter = TagCounter(threading.Lock())

        def update(counter):
            counter.update({"A", "B"})

        threads = [threading.Thread(target=update, args=(counter,)) for _ in range(5)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        assert dict(counter.items()) == {"A": 5, "B": 5}
