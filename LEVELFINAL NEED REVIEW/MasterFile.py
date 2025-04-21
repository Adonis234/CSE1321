import pygame, sys, random
from pygame.locals import *
pygame.init()
pygame.mixer.init()

#setup screen
screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
pygame.display.set_caption("Boppi's Quest: The Flower Rescue")

#load images
boppi = pygame.image.load("BoppiFront2.png").convert_alpha()
arrow = pygame.image.load("ArrowNextLevel.png").convert_alpha()
flower_image = pygame.image.load("flowerPickUp.png").convert_alpha()
flower_image = pygame.transform.scale(flower_image, (25, 25))
gameover_image = pygame.image.load("GameOver.png").convert_alpha()
gameover_image = pygame.transform.scale(gameover_image, (500,500))

# Load sounds and music
jump = pygame.mixer.Sound('Jump.mp3')
flower_sound = pygame.mixer.Sound('pick up.mp3')
death = pygame.mixer.Sound("death.mp3")
waterfall_sound = pygame.mixer.Sound('waterfallsound.wav')
typing_sound = pygame.mixer.Sound("typingSound.mp3")
flower_sound.set_volume(0.5)
jump.set_volume(0.5)
death.set_volume(0.9)
waterfall_sound.set_volume(0.5)
typing_sound.set_volume(0.4)

introFlag =True
level1Flag = False
level2Flag = False
level3Flag = False
level4Flag = False
endgameFlag = False
deadFlag = False
running = True

while running:
   while introFlag:

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
         "↑ Jump with SPACE to reach platforms",
         "🌸 Collect flowers on your way",
         "SPACE: Talk to characters or interact",
         "",
         "[Press SPACE to begin your journey...]"
      ]

      # Timing and layout
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
         text_surface = pygame.Surface((1280, surface_height), pygame.SRCALPHA)

         # Draw all lines to the surface
         for i, line in enumerate(all_lines):
            line_surf = font.render(line, True, WHITE)
            text_surface.blit(line_surf, (80, i * line_spacing))
            typing_sound.play()

         # Scroll logic
         visible_start = max(0, scroll_offset)
         screen.blit(text_surface, (0, -visible_start))

         if story_finished:
            prompt = font.render("[Press SPACE to continue...]", True, WHITE)
            screen.blit(prompt, (80, 720 - 60))
            typing_sound.stop()


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
         global line_index, char_index, current_line, time_since_last_char, introFlag, level1Flag
         global story_finished, showing_story, showing_instructions, scroll_offset

         if story_lines:
            current_line = story_lines[line_index]

         while running and introFlag:
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
                     introFlag = False
                     level1Flag = True # Placeholder for actual game start
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

   while level1Flag:
      pygame.mixer.music.load('backgound.mp3')
      pygame.mixer.music.play(-1)
      # Setup initial position
      boppiRect = pygame.Rect(0, 0, 45, 68)

      # Background
      level1Background = pygame.image.load("backgroundLevel1.png")

      # Platforms
      platRects = [
         pygame.Rect(-2, 150, 102, 10),
         pygame.Rect(198, 250, 102, 10),
         pygame.Rect(58, 350, 102, 10),
         pygame.Rect(198, 550, 102, 10),
         pygame.Rect(98, 70, 102, 10),
         pygame.Rect(348, 200, 102, 10),
         pygame.Rect(538, 300, 102, 10),
         pygame.Rect(800, 220, 102, 10),
         pygame.Rect(990, 120, 102, 10),
         pygame.Rect(698, 400, 102, 10),
         pygame.Rect(443, 500, 102, 10),
         pygame.Rect(648, 600, 102, 10),
         pygame.Rect(978, 600, 102, 10),
         pygame.Rect(1178, 350, 102, 10),
         pygame.Rect(38, 650, 42, 10),
      ]

      flowerRect_list = [
         pygame.Rect(105, 325, 10, 10),
         pygame.Rect(55, 625, 10, 10),
         pygame.Rect(145, 45, 10, 10),
         pygame.Rect(1040, 85, 10, 10),
         pygame.Rect(600, 45, 10, 10),
         pygame.Rect(855, 495, 10, 10),
      ]

      # Exit Arrow
      arrowRect = pygame.Rect(1222.5, 315, 30, 15)

      # Flowers
      flower_locations = [
         (95, 315),
         (45, 615),
         (135, 35),
         (1030, 75),
         (590, 35),
         (845, 485)
      ]

      # Ground
      ground = pygame.Rect(0, 720, 1280, 10)

      # Fonts and text
      font = pygame.font.SysFont("Arial", 36, bold=True)
      lives = 6
      flowers = 6
      showMessage = False
      messageTimer = 0

      cannotContinueText = font.render("Cannot continue. Collect all of the flowers!", True, (255, 255, 255))

      # Movement vars
      velocity_x = 0
      velocity_y = 0
      on_plat = False
      SPEED = 8
      JUMP_FORCE = -15
      GRAVITY = 1

      # Start boppi on first platform
      boppiRect.y = platRects[0].top - boppiRect.height

      running = True

      while running and level1Flag:
         num2 = 0
         clock.tick(60)
         for event in pygame.event.get():
            if event.type == QUIT:
               pygame.quit()
               sys.exit()

         # Input
         keys = pygame.key.get_pressed()
         velocity_x = 0
         if keys[K_a] or keys[K_LEFT]:
            velocity_x = -SPEED
         if keys[K_d] or keys[K_RIGHT]:
            velocity_x = SPEED
         if (keys[K_SPACE] or keys[K_UP]) and on_plat:
            velocity_y = JUMP_FORCE
            on_plat = False
            jump.play()

         # Apply gravity
         velocity_y += GRAVITY
         if velocity_y > 20:
            velocity_y = 20

         # Horizontal movement
         boppiRect.x += velocity_x
         for plat in platRects:
            if boppiRect.colliderect(plat):
               if velocity_x > 0:
                  boppiRect.right = plat.left
               elif velocity_x < 0:
                  boppiRect.left = plat.right

         # Keep inside screen
         if boppiRect.left < 0:
            boppiRect.left = 0
         if boppiRect.right > 1280:
            boppiRect.right = 1280

         # Prevent going off-screen vertically
         if boppiRect.top < -80:
            boppiRect.top = -80
         if boppiRect.bottom > ground.top:
            boppiRect.bottom = ground.top
            velocity_y = 0
            on_plat = True

         # Vertical movement
         boppiRect.y += velocity_y
         on_plat = False
         for plat in platRects:
            if boppiRect.colliderect(plat):
               if velocity_y > 0:
                  boppiRect.bottom = plat.top
                  velocity_y = 0
                  on_plat = True
               elif velocity_y < 0:
                  boppiRect.top = plat.bottom
                  velocity_y = 0

         # Ground collision
         if boppiRect.bottom >= ground.top:
            boppiRect.bottom = ground.top
            velocity_y = 0
            on_plat = True
            lives -= 1
            boppiRect = pygame.Rect(0, 0, 45, 68)
            screen.blit(boppi, (0, 47))
            pygame.display.flip()

         # Check to see if flowers picked up
         for flower in flowerRect_list[:]:
            if boppiRect.colliderect(flower):
               flowers -= 1
               flower_sound.play()
               index = flowerRect_list.index(flower)
               del flower_locations[index]
               flowerRect_list.remove(flower)

         # if player tries to exit screen, check flowers
         if boppiRect.colliderect(arrowRect):
            if flowers == 0:
               level1Flag = False
               pygame.mixer.music.stop()
               level2Flag = True
            else:
               showMessage = True
               messageTimer = pygame.time.get_ticks()

         # Remove message after 2 seconds
         if showMessage and pygame.time.get_ticks() - messageTimer > 2000:
            showMessage = False

         # If player dies
         if lives == 0:
            level1Flag = False
            pygame.mixer.music.stop()
            deadFlag = True
            flowerRect_list = [
               pygame.Rect(105, 325, 10, 10),
               pygame.Rect(55, 625, 10, 10),
               pygame.Rect(145, 45, 10, 10),
               pygame.Rect(1040, 85, 10, 10),
               pygame.Rect(600, 45, 10, 10),
               pygame.Rect(855, 495, 10, 10),
            ]
            flower_locations = [
               (95, 315),
               (45, 615),
               (135, 35),
               (1030, 75),
               (590, 35),
               (845, 485)
            ]

         # Draw everything
         screen.blit(level1Background, (0, 0))

         # Draw platforms
         for plat in platRects:
            pygame.draw.rect(screen, (0, 51, 0), plat)

         # Draw flowers
         for location in flower_locations:
            screen.blit(flower_image, location)

         screen.blit(arrow, (1222.5, 315))

         # Draw ground
         pygame.draw.rect(screen, (0, 0, 0), ground)

         # Draw Boppi
         screen.blit(boppi, boppiRect.topleft)

         # Draw UI Panel (bottom right)
         hud_width = 150
         hud_height = 70
         hud_x = screen.get_width() - hud_width - 20
         hud_y = screen.get_height() - hud_height - 20
         pygame.draw.rect(screen, (255, 255, 255), (hud_x, hud_y, hud_width, hud_height), border_radius=10)
         pygame.draw.rect(screen, (0, 0, 0), (hud_x, hud_y, hud_width, hud_height), 2, border_radius=10)

         # Fonts
         title_font = pygame.font.Font(None, 34)
         value_font = pygame.font.Font(None, 34)

         # Render Lives text
         lives_text = title_font.render(f"Lives:", True, (255, 102, 255))
         lives_value = value_font.render(str(lives), True, (255, 102, 255))

         # Render Flowers text
         flowers_text = title_font.render(f"Flowers:", True, (255, 102, 255))
         flowers_value = value_font.render(str(flowers), True, (255, 102, 255))

         # Blit Lives
         screen.blit(lives_text, (hud_x + 10, hud_y + 10))
         screen.blit(lives_value, (hud_x + 120, hud_y + 10))

         # Blit Flowers
         screen.blit(flowers_text, (hud_x + 10, hud_y + 35))
         screen.blit(flowers_value, (hud_x + 120, hud_y + 35))

         # Show warning message
         if showMessage:
            screen.blit(cannotContinueText, (350, 350))

         pygame.display.flip()

   while level2Flag:
      pygame.mixer.music.load('level3sound.mp3')
      pygame.mixer.music.play(-1)
      waterfall_sound.play(-1)

      boppiRect = pygame.Rect(0, 0, 45, 68)
      level2Background = pygame.image.load("BackgroundLevel2.png").convert_alpha()
      level2Background = pygame.transform.scale(level2Background, (1280, 720))

     # Waterfall platforms (in center)
      waterfall_platRects = [
         pygame.Rect(450, 60, 100, 10),
         pygame.Rect(590, 180, 100, 10),
         pygame.Rect(730, 60, 100, 10),
         pygame.Rect(450, 300, 100, 10),
         pygame.Rect(590, 420, 100, 10),
         pygame.Rect(730, 300, 100, 10),
         pygame.Rect(450, 540, 100, 10),
         pygame.Rect(590, 660, 100, 10),
         pygame.Rect(730, 540, 100, 10),
      ]

      #  left side
      left_platRects = [
         pygame.Rect(0, 330, 100, 10),  # starting platform
         pygame.Rect(150, 230, 100, 10),
         pygame.Rect(270, 140, 100, 10),
         pygame.Rect(20, 120, 100, 10),
         pygame.Rect(80, 510, 100, 10),
         pygame.Rect(270, 420, 100, 10),
         pygame.Rect(270, 600, 100, 10),
      ]

      # on right side
      right_platRects = [
         pygame.Rect(1100, 120, 100, 10),
         pygame.Rect(900, 220, 100, 10),
         pygame.Rect(1180, 350, 100, 10),  # arrow platform
         pygame.Rect(900, 550, 100, 10),
         pygame.Rect(1020, 450, 100, 10),
         pygame.Rect(1150, 650, 100, 10),
      ]

      all_platRects = left_platRects + waterfall_platRects + right_platRects

      original_waterfall_positions = [rect.y for rect in waterfall_platRects]

      # Exit Arrow
      arrowRect = pygame.Rect(1220, 315, 30, 15)

      # Flowers
      flowerRect_list = [
         pygame.Rect(181, 35, 10, 10),  # Left side
         pygame.Rect(491, 35, 10, 10),  # Waterfall
         pygame.Rect(1136, 65, 10, 10),  # Right side
         pygame.Rect(626, 540, 10, 10),  # Waterfall
         pygame.Rect(116, 475, 10, 10),  # Left side
         pygame.Rect(1186, 610, 10, 10),  # Right side
      ]

      # Ground
      ground = pygame.Rect(0, 720, 1280, 10)

      # Fonts and text
      font = pygame.font.SysFont("Arial", 36, bold=True)
      flowers = 6
      mistWarningText = font.render("Cannot continue. Collect all of the flowers!", True, (255, 255, 255))

      # Movement vars
      velocity_x = 0
      velocity_y = 0
      on_plat = False
      SPEED = 8
      JUMP_FORCE = -15
      GRAVITY = 1
      WATERFALL_SPEED = 1 # How fast waterfall
      MIST_FORCE = -5

      # starting point
      boppiRect.midbottom = left_platRects[0].midtop

      show_warning = False
      warning_timer = 0
      show_mist_warning = False
      mist_timer = 0

      while running and level2Flag:
         clock.tick(60)
         for event in pygame.event.get():
            if event.type == QUIT:
               pygame.quit()
               sys.exit()

         # Input
         keys = pygame.key.get_pressed()
         velocity_x = 0
         if keys[K_a] or keys[K_LEFT]:
            velocity_x = -SPEED
         if keys[K_d] or keys[K_RIGHT]:
            velocity_x = SPEED
         if (keys[K_SPACE] or keys[K_UP]) and on_plat:
            velocity_y = JUMP_FORCE
            jump.play()
            on_plat = False

         # Apply gravity
         velocity_y += GRAVITY
         if velocity_y > 20:
            velocity_y = 20

         # Downwards only
         for plat in waterfall_platRects:
            plat.y += WATERFALL_SPEED
            # Reset platform to top when it goes off screen
            if plat.top > 720:
               plat.y = -0.001

         # Flower movement - only waterfall flowers move
         for i, flower in enumerate(flowerRect_list):
            # Check if flower is in waterfall area (x between 400-880)
            if 400 <= flower.x <= 880:
               for plat in waterfall_platRects:
                  if abs(flower.x - plat.centerx) < 60:  # Rough association
                     flower.y = plat.y - 35  # Keep above platform
                     break

         # Horizontal movement
         boppiRect.x += velocity_x
         for plat in all_platRects:
            if boppiRect.colliderect(plat):
               if velocity_x > 0:
                  boppiRect.right = plat.left
               elif velocity_x < 0:
                  boppiRect.left = plat.right

         # Keep inside screen horizontally
         if boppiRect.left < 0:
            boppiRect.left = 0
         if boppiRect.right > 1280:
            boppiRect.right = 1280

         if boppiRect.top < -80:
            boppiRect.top = -80
            velocity_y = 0

         # Vertical movement
         boppiRect.y += velocity_y
         on_plat = False
         for plat in all_platRects:
            if boppiRect.colliderect(plat):
               if velocity_y > 0:
                  boppiRect.bottom = plat.top
                  velocity_y = 0
                  on_plat = True
               elif velocity_y < 0:
                  boppiRect.top = plat.bottom
                  velocity_y = 0

         # Check if player falls below screen (waterfall bottom)
         if boppiRect.top > 720:
            lives -= 1
            if lives <= 0:  # if player dies
               level2Flag = False
               pygame.mixer.music.stop()
               waterfall_sound.stop()
               deadFlag = True
               flowerRect_list = [
                  pygame.Rect(181, 35, 10, 10),
                  pygame.Rect(491, 35, 10, 10),
                  pygame.Rect(1136, 65, 10, 10),
                  pygame.Rect(626, 540, 10, 10),
                  pygame.Rect(116, 475, 10, 10),
                  pygame.Rect(1186, 610, 10, 10),
               ]

            # Reset position to starting platform
            boppiRect.midbottom = left_platRects[0].midtop
            # Reset waterfall platforms to original positions
            for i, plat in enumerate(waterfall_platRects):
               plat.y = original_waterfall_positions[i]
            warning_timer = 180  # 3 seconds at 60fps

         # Flower collection
         for flower in flowerRect_list[:]:  # Make a copy for iteration
            if boppiRect.colliderect(flower):
               flower_sound.play()
               flowers -= 1
               flowerRect_list.remove(flower)
               pygame.display.flip()

         if boppiRect.colliderect(arrowRect):
            if flowers == 0:
               level2Flag = False
               pygame.mixer.music.stop()
               waterfall_sound.stop()
               level3Flag = True
            else:
               # Apply mist force (push player up)
               velocity_y = MIST_FORCE
               # Show mist warning
               show_mist_warning = True
               mist_timer = 120  # 2 seconds

         # Warning message timers
         if show_warning:
            warning_timer -= 1
            if warning_timer <= 0:
               show_warning = False

         if show_mist_warning:
            mist_timer -= 1
            if mist_timer <= 0:
               show_mist_warning = False

         screen.blit(level2Background, (0, 0))

         for plat in left_platRects:
            pygame.draw.rect(screen, (0, 51, 0), plat)

         #  waterfall platforms (blue)
         for plat in waterfall_platRects:
            pygame.draw.rect(screen, (0, 100, 200), plat)

         #  right platforms (green)
         for plat in right_platRects:
            pygame.draw.rect(screen, (0, 51, 0), plat)

         #  flowers
         for flower in flowerRect_list:
            screen.blit(flower_image, flower.topleft)

         # arrow
         screen.blit(arrow, arrowRect.topleft)

         #  Boppi
         screen.blit(boppi, boppiRect.topleft)

         # Draw UI Panel (bottom right)
         hud_width = 150
         hud_height = 70
         hud_x = screen.get_width() - hud_width - 150
         hud_y = screen.get_height() - hud_height - 20
         pygame.draw.rect(screen, (255, 255, 255), (hud_x, hud_y, hud_width, hud_height), border_radius=10)
         pygame.draw.rect(screen, (0, 0, 0), (hud_x, hud_y, hud_width, hud_height), 2, border_radius=10)

         # Fonts
         title_font = pygame.font.Font(None, 34)
         value_font = pygame.font.Font(None, 34)

         # Render Lives text
         lives_text = title_font.render(f"Lives:", True, (255, 102, 255))
         lives_value = value_font.render(str(lives), True, (255, 102, 255))

         # Render Flowers text
         flowers_text = title_font.render(f"Flowers:", True, (255, 102, 255))
         flowers_value = value_font.render(str(flowers), True, (255, 102, 255))

         # Blit Lives
         screen.blit(lives_text, (hud_x + 10, hud_y + 10))
         screen.blit(lives_value, (hud_x + 120, hud_y + 10))

         # Blit Flowers
         screen.blit(flowers_text, (hud_x + 10, hud_y + 35))
         screen.blit(flowers_value, (hud_x + 120, hud_y + 35))

         # Show warnings if needed
         if show_mist_warning:
            screen.blit(mistWarningText, (350, 350))

         pygame.display.flip()

   while level3Flag:
      pygame.mixer.music.load('level2sound.mp3')
      pygame.mixer.music.play(-1)

      # Sets up rock class
      class Rock:
         def __init__(self):
            self.speed = 5
            self.sprite = pygame.image.load("rock.png").convert_alpha()
            self.rect = self.sprite.get_rect()
            self.rect.topleft = (random.randint(0, 1280 - self.rect.width), 0)
            # self.spawnSound = INSERT PATH TO ROCK SOUND

         def fall(self):
            self.rect = self.rect.move(0, self.speed)

         def draw(self, target):
            target.blit(self.sprite, self.rect)

      # Setup initial position
      boppiRect = pygame.Rect(0, 0, 45, 68)

      # Background
      level3Background = pygame.image.load("backgroundLevel3.png").convert()

      # Platforms
      platRects = [
         pygame.Rect(-2, 150, 102, 10),
         pygame.Rect(100, 400, 102, 10),
         pygame.Rect(620, 90, 102, 10),
         pygame.Rect(300, 80, 102, 10),
         pygame.Rect(150, 600, 102, 10),
         pygame.Rect(250, 200, 102, 10),
         pygame.Rect(457, 300, 102, 10),
         pygame.Rect(800, 220, 102, 10),
         pygame.Rect(990, 120, 40, 10),
         pygame.Rect(840, 300, 102, 10),
         pygame.Rect(670, 400, 102, 10),
         pygame.Rect(410, 500, 102, 10),
         pygame.Rect(648, 600, 102, 10),
         pygame.Rect(978, 600, 102, 10),
         pygame.Rect(1178, 350, 102, 10),
         pygame.Rect(1208, 500, 72, 10),
         pygame.Rect(70, 380, 30, 10),
      ]

      # Exit Arrow
      arrowRect = pygame.Rect(1222.5, 315, 30, 15)

      # Flowers
      flowerRect_list = [
         pygame.Rect(665, 60, 10, 10),
         pygame.Rect(80, 360, 10, 10),
         pygame.Rect(1005, 100, 10, 10),
         pygame.Rect(870, 260, 10, 10),
         pygame.Rect(195, 570, 10, 10),
         pygame.Rect(1240, 370, 10, 10),]

      flower_locations = [
         (665, 60),
         (80, 360),
         (1005, 100),
         (870, 260),
         (195, 570),
         (1240, 370)]

      # Rocks
      rockTimer = 0
      rockList = []

      # Ground
      ground = pygame.Rect(0, 720, 1280, 10)

      # Fonts and text
      font = pygame.font.SysFont("Arial", 36, bold=True)
      flowers = 6
      cannotContinueText = font.render("Cannot continue. Collect all of the flowers!", True, (255, 255, 255))
      showMessage = False
      messageTimer = 0

      # Movement vars
      velocity_x = 0
      velocity_y = 0
      on_plat = False
      SPEED = 8
      JUMP_FORCE = -15
      GRAVITY = 1

      # Start boppi on first platform
      boppiRect.y = platRects[0].top - boppiRect.height

      while running and level3Flag:
         num2 = 0  # used for the flowers
         rockTimer += 1
         clock.tick(60)
         for event in pygame.event.get():
            if event.type == QUIT:
               pygame.quit()
               sys.exit()

         # Input
         keys = pygame.key.get_pressed()
         velocity_x = 0
         if keys[K_a] or keys[K_LEFT]:
            velocity_x = -SPEED
         if keys[K_d] or keys[K_RIGHT]:
            velocity_x = SPEED
         if (keys[K_SPACE] or keys[K_UP]) and on_plat:
            velocity_y = JUMP_FORCE
            jump.play()
            on_plat = False

         # Apply gravity
         velocity_y += GRAVITY
         if velocity_y > 20:
            velocity_y = 20

         # Horizontal movement
         boppiRect.x += velocity_x
         for plat in platRects:
            if boppiRect.colliderect(plat):
               if velocity_x > 0:
                  boppiRect.right = plat.left
               elif velocity_x < 0:
                  boppiRect.left = plat.right

            # keeping inside:
            if boppiRect.left < 0:
               boppiRect.left = 0
         if boppiRect.right > 1280:
            boppiRect.right = 1280

         # Prevent going off-screen vertically
         if boppiRect.top < -80:
            boppiRect.top = -80
         if boppiRect.bottom > ground.top:
            boppiRect.bottom = ground.top
            velocity_y = 0
            on_plat = True

         # Vertical movement
         boppiRect.y += velocity_y
         on_plat = False
         for plat in platRects:
            if boppiRect.colliderect(plat):
               if velocity_y > 0:
                  boppiRect.bottom = plat.top
                  velocity_y = 0
                  on_plat = True
               elif velocity_y < 0:
                  boppiRect.top = plat.bottom
                  velocity_y = 0

         # Ground collision
         if boppiRect.bottom >= ground.top:
            boppiRect.bottom = ground.top
            velocity_y = 0
            on_plat = True
            lives -= 1
            boppiRect = pygame.Rect(0, 0, 45, 68)
            screen.blit(boppi, (0, 47))
            pygame.display.flip()

         # Top screen limit
         if boppiRect.top < -50:
            boppiRect.top = -50

         # Check to see if flowers picked up
         for flower in flowerRect_list:
            if boppiRect.colliderect(flower):
               flowers = flowers - 1
               flower_sound.play()
               del flowerRect_list[num2]
               del flower_locations[num2]
               pygame.display.flip()
            num2 = num2 + 1

         # if player tries to exit screen, check flowers
         if boppiRect.colliderect(arrowRect):
            if flowers == 0:
               level3Flag = False
               pygame.mixer.music.stop()
               level4Flag = True
            elif flowers != 0:
               showMessage = True
               messageTimer = pygame.time.get_ticks()

         # Remove message after 2 seconds
         if showMessage and pygame.time.get_ticks() - messageTimer > 2000:
            showMessage = False

         # If player dies
         if lives == 0:
            level3Flag = False
            pygame.mixer.music.stop()
            deadFlag = True

         # Draw everything
         screen.blit(level3Background, (0, 0))

         # Draw platforms
         for plat in platRects:
            pygame.draw.rect(screen, (55,32,66), plat)

         # Draw flowers
         for location in flower_locations:
            screen.blit(flower_image, location)

         screen.blit(arrow, (1222.5, 315))

         # Draw ground
         pygame.draw.rect(screen, (0, 0, 0), ground)

         # Draw Boppi
         screen.blit(boppi, boppiRect.topleft)

         # Draw UI Panel (bottom right)
         hud_width = 150
         hud_height = 70
         hud_x = screen.get_width() - hud_width - 20
         hud_y = screen.get_height() - hud_height - 20
         pygame.draw.rect(screen, (255, 255, 255), (hud_x, hud_y, hud_width, hud_height), border_radius=10)
         pygame.draw.rect(screen, (0, 0, 0), (hud_x, hud_y, hud_width, hud_height), 2, border_radius=10)

         # Fonts
         title_font = pygame.font.Font(None, 34)
         value_font = pygame.font.Font(None, 34)

         # Render Lives text
         lives_text = title_font.render(f"Lives:", True, (255, 102, 255))
         lives_value = value_font.render(str(lives), True, (255, 102, 255))

         # Render Flowers text
         flowers_text = title_font.render(f"Flowers:", True, (255, 102, 255))
         flowers_value = value_font.render(str(flowers), True, (255, 102, 255))

         # Blit Lives
         screen.blit(lives_text, (hud_x + 10, hud_y + 10))
         screen.blit(lives_value, (hud_x + 120, hud_y + 10))

         # Blit Flowers
         screen.blit(flowers_text, (hud_x + 10, hud_y + 35))
         screen.blit(flowers_value, (hud_x + 120, hud_y + 35))

         # Show warning message
         if showMessage:
            screen.blit(cannotContinueText, (350, 350))

         # causing rocks to spawn
         if rockTimer % 90 == 0:
            newRock = Rock()
            rockList.append(newRock)
            # newRock.spawnSound.play()

         for i in rockList:
            Rock.draw(i, screen)
            Rock.fall(i)
            if i.rect.midbottom == 800 - i.rect.height:
               rockList.remove(i)
            if pygame.Rect.colliderect(i.rect, boppiRect):
               lives -= 1
               boppiRect = pygame.Rect(0, 0, 45, 68)
               screen.blit(boppi, (0, 47))
               rockList.remove(i)

         pygame.display.flip()

   while level4Flag:
      running = True
      screen.fill((0, 0, 0))
      font = pygame.font.SysFont("Arial", 36, bold=True)
      text = font.render("INSERT LEVEL 4 HERE", True, (255, 255, 255))
      screen.blit(text, (350, 350))
      pygame.display.flip()
      while running and level4Flag:
         for event in pygame.event.get():
            if event.type == QUIT:
               pygame.quit()
               sys.exit()

   while deadFlag:
      running = True
      death.play()
      lives = 6
      dead_background = pygame.Surface((1280,720))
      dead_background.fill((0, 0, 0))
      dead_background.set_alpha(200)
      screen.blit(dead_background,(0,0))
      font = pygame.font.SysFont("Arial", 36, bold=True)
      screen.blit(gameover_image,(390,110))
      gameover_text1 = font.render("Press R to Retry", True, (255, 255, 255))
      gameover_text2 = font.render("Boppi didn't get his flower back.", True, (255,255,255))
      screen.blit(gameover_text1, (520, 500))
      screen.blit(gameover_text2, (420,550))
      pygame.display.flip()
      while running and deadFlag:
         for event in pygame.event.get():
            if event.type == QUIT:
               pygame.quit()
               sys.exit()
         keys = pygame.key.get_pressed()
         if keys[K_r]:
            level1Flag = True
            deadFlag = False