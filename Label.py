import pygame

pygame.init()


class Label:
    def __init__(self, master, text, position, font=None, font_size=30, color=(0, 0, 0), background=None,
                 underline=False, bold=False, italic=False):
        """
        activebackground, activeforeground, anchor, background, bitmap, borderwidth, cursor, disabledforeground, font,
        foreground, highlightbackground, highlightcolor, highlightthickness, justify, padx, pady, relief,
        takefocus, wraplength
        :param master:
        :param text:
        :param position:
        :param font:
        :param font_size:
        :param color:
        :param background:
        """
        self.surface = master
        self.text = text
        self.position = position
        self.color = color
        self.background = background

        # Set the font, use default if not provided
        if font is None:
            self.font = pygame.font.Font(None, font_size)
        else:
            self.font = pygame.font.Font(font, font_size)

        if underline:
            font.set_underline(True)
        if bold:
            font.set_bold(True)
        if italic:
            font.set_italic(True)

        # Render the text
        self.render_text()

    def render_text(self):
        # Render the text surface with or without background color
        if self.background:
            self.text_surface = self.font.render(self.text, True, self.color, self.background)
        else:
            self.text_surface = self.font.render(self.text, True, self.color)
        # Get the rectangle of the text surface
        self.text_rect = self.text_surface.get_rect(topleft=self.position)

    def draw(self):
        # Draw the text surface onto the given surface
        self.surface.blit(self.text_surface, self.text_rect)
