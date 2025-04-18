import pygame
import sys

pygame.init()

# Screen setup
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Boppi's Quest: The Flower Rescue")

# Fonts and colors
font = pygame.font.Font(None, 40)
title_font = pygame.font.Font(None, 60)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Story text
story_lines = [
    "There once was a man who lived in the forest. His name was Boppi.",
    "One day he comes home and finds his cottage has been ransacked!",
    "He searches through the mess, frantically looking…",
    "His shoulders sink. He clutches his heart…",
    "\"She’s gone…\"",
    "\"He took her… He took my flower.\"",
    "",
    "Boppi stands up and turns away from his cottage.",
    "Far in the distance, a castle lays on the horizon.",
    "Its black turrets pierce the sky.",
    "",
    "Boppi knows what he must do to get her back.",
    "With determination, he squares his shoulders and sets off on an adventure…"
]

instructions = [
    "🎮 HOW TO PLAY 🎮",
    "→ Use arrow keys to move",
    "↑ Jump to reach platforms",
    "🌸 Collect flowers on your way",
    "SPACE: Talk to characters or interact",
    "",
    "[Press SPACE to begin your journey...]"
]

# Timing and layout
clock = pygame.time.Clock()
char_delay = 25  # ms between characters
line_spacing = 50
max_lines_on_screen = 10
scroll_speed = 2  # px per frame
scroll_offset = 0

# Typing & control vars
typed_lines = []
current_line = ""
line_index = 0
char_index = 0
story_finished = False
showing_story = True
showing_instructions = False
time_since_last_char = 0

def draw_typing_story(partial_line):
    screen.fill(BLACK)

    # Create a surface tall enough to hold all lines
    all_lines = typed_lines + ([partial_line] if partial_line else [])
    surface_height = len(all_lines) * line_spacing + 100
    text_surface = pygame.Surface((WIDTH, surface_height), pygame.SRCALPHA)

    # Draw all lines to the surface
    for i, line in enumerate(all_lines):
        line_surf = font.render(line, True, WHITE)
        text_surface.blit(line_surf, (80, i * line_spacing))

    # Scroll logic
    visible_start = max(0, scroll_offset)
    screen.blit(text_surface, (0, -visible_start))

    if story_finished:
        prompt = font.render("[Press SPACE to continue...]", True, WHITE)
        screen.blit(prompt, (80, HEIGHT - 60))

def draw_instructions():
    screen.fill(BLACK)
    y = 120
    for line in instructions:
        if line.startswith("🎮"):
            text = title_font.render(line, True, WHITE)
        else:
            text = font.render(line, True, WHITE)
        screen.blit(text, (80, y))
        y += 60

def main():
    global line_index, char_index, current_line, time_since_last_char
    global story_finished, showing_story, showing_instructions, scroll_offset

    if story_lines:
        current_line = story_lines[line_index]

    while True:
        dt = clock.tick(60)
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if story_finished and showing_story and event.key == pygame.K_SPACE:
                    showing_story = False
                    showing_instructions = True
                elif showing_instructions and event.key == pygame.K_SPACE:
                    print("Start game here!")  # Placeholder for actual game start
                    return

        partial_line = ""

        if showing_story and not story_finished:
            time_since_last_char += dt
            if time_since_last_char >= char_delay:
                time_since_last_char = 0
                if char_index < len(current_line):
                    char_index += 1
                    partial_line = current_line[:char_index]
                else:
                    typed_lines.append(current_line)
                    char_index = 0
                    line_index += 1
                    if line_index < len(story_lines):
                        current_line = story_lines[line_index]
                    else:
                        story_finished = True
                    # Adjust scroll if line count exceeds visible area
                    if len(typed_lines) >= max_lines_on_screen:
                        scroll_offset += scroll_speed * (line_spacing // scroll_speed)

        if showing_story:
            if char_index > 0 and line_index <= len(story_lines):
                partial_line = current_line[:char_index]
            draw_typing_story(partial_line)
        elif showing_instructions:
            draw_instructions()

        pygame.display.update()

main()
