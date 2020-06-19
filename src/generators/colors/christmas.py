class ChristmasColorGenerator:
    def __init__(self, random_choice=True):
        self.colors = list()
        self.colors.append((255, 255, 255))
        self.colors.append((50, 50, 50))

        self.last_color = self.get_random_color()
        self.current_color = self.get_random_color()
        self.fade = 0
        self.random_choice = random_choice

    def get_color(self):
        if self.random_choice:
            return random.choice(self.colors)
        else:
            if self.fade >= 1:
                self.last_color = self.current_color
                self.current_color = self.get_random_color()
                self.fade = 0

            self.fade += 1 / (4 * constants.FRAMES_PER_SECOND)

            return self.mix_color(self.fade, self.last_color,
                                  self.current_color)

    def get_random_color(self):
        return random.choice(self.colors)

    def mix_color(self, fade, color1, color2):
        r = color1[0] * (1 - fade) + color2[0] * fade
        g = color1[1] * (1 - fade) + color2[1] * fade
        b = color1[2] * (1 - fade) + color2[2] * fade

        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))

        return (r, g, b)
