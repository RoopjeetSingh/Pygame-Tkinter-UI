import pygame

pygame.init()


def draw_bordered_rect(surface, rect, color, border_color, corner_radius, border_thickness):
    rect_tmp = pygame.Rect(rect)

    if border_thickness:
        if corner_radius <= 0:
            pygame.draw.rect(surface, border_color, rect_tmp)
        else:
            pygame.draw.rect(surface, border_color, rect_tmp, border_radius=corner_radius)

        rect_tmp.inflate_ip(-2 * border_thickness, -2 * border_thickness)
        inner_radius = corner_radius - border_thickness + 1
    else:
        inner_radius = corner_radius

    if inner_radius <= 0:
        pygame.draw.rect(surface, color, rect_tmp)
    else:
        pygame.draw.rect(surface, color, rect_tmp, border_radius=inner_radius)


class InputBox:

    def __init__(self, x: int, y: int, w: int, h: int, color_inactive: tuple[int, int, int] = (128, 128, 128),
                 color_active: tuple[int, int, int] = (255, 255, 255),
                 color_hover: tuple[int, int, int] = (135, 206, 235), function=None,
                 font: pygame.font.Font = None, text: str = '',
                 font_color: tuple[int, int, int] = (0, 0, 0), active: bool = False, border_radius: int = 0,
                 remove_active=False, cursor_color=(0, 0, 0), function_every_user_press=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color_inactive
        self.color_active = color_active
        self.color_inactive = color_inactive
        self.color_hover = color_hover
        self.font = font or pygame.font.Font(None, h - 5)
        self.text = ""
        self.font_color = font_color
        self.given_text = text
        self.active = active
        self.function = function
        self.border_radius = border_radius
        self.remove_active = remove_active
        self.cursor_color = cursor_color
        self.function_every_user_press = function_every_user_press
        if self.active:
            self.txt_surface = self.font.render(self.text, True, self.font_color)
        else:
            self.txt_surface = self.font.render(self.given_text, True, (238, 234, 222))
            self.txt_surface.set_alpha(128)
        self.draw_cursor = 0
        self.drawn = False
        self.cursor_speed = 600

    def check_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and not self.remove_active:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.color = self.color_hover
        else:
            self.color = self.color_inactive
            # Change the current color of the input box.
        if self.active:
            self.color = self.color_active
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN and self.text:
                    if self.function:
                        self.function(self.text)
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if self.font.render(self.text + event.unicode, True,
                                        self.font_color).get_width() <= self.rect.w - 10 and event.key != pygame.K_RETURN:
                        if self.function_every_user_press:
                            self.function_every_user_press(event.unicode)
                        else:
                            self.text += event.unicode
                # Re-render the text.
        if self.active:
            self.txt_surface = self.font.render(self.text, True, self.font_color)

    def cursor(self, screen):
        if self.active:
            if (self.drawn and self.draw_cursor % self.cursor_speed != 0) or \
                    (not self.drawn and self.draw_cursor % self.cursor_speed == 0):
                pygame.draw.line(screen, self.cursor_color,
                                 (self.txt_surface.get_width() + self.rect.x + 5, self.rect.y + 7),
                                 (self.txt_surface.get_width() + self.rect.x + 5, self.rect.bottom - 7), width=2)
                self.drawn = True
            else:
                self.drawn = False
            self.draw_cursor += 1
            if self.draw_cursor == self.cursor_speed:
                self.draw_cursor = 0

    def update(self, screen):
        draw_bordered_rect(screen, self.rect, self.color, (0, 0, 0), self.border_radius, 2)
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        self.cursor(screen)
