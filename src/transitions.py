class FadeTransition:
    def __init__(self):
        self.progress = 1

    def reset(self):
        self.progress = 0

    def process(self, from_routine, to_routine):
        self.progress += 0.006
        self.progress = max(0, min(1, self.progress))

        if self.progress == 1:
            return to_routine.get_frame()

        return from_routine.get_frame() * (1 - self.progress) + \
            to_routine.get_frame() * self.progress
