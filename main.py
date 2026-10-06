import pygame

# Initialize Pygame
(numpass, numfail) = pygame.init()
is_initialized = (numpass > 0 and numfail == 0)

def main():
    # Print the initialization results
    if is_initialized:
        print(f"Pygame initialized with {numpass} successful and {numfail} failed modules.")
    else:
        print(f"Pygame failed to initialize properly. {numpass} successful and {numfail} failed modules.")

    # Initialize the game window
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("My Game")

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    # Quit Pygame
    pygame.quit()


if __name__ == "__main__":
    main()
