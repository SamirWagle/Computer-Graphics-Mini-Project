# Import necessary modules
import sys  # System-specific parameters and functions
import random  # Generate random numbers
import time  # Time-related functions
import math  # Mathematical functions
import pygame  # Pygame library for graphics and game development

# Constants for the simulation
FPS = 60  # Frames per second, determines the speed of the simulation
WIDTH = 800  # Width of the simulation window
HEIGHT = 600  # Height of the simulation window
MAX_PARTICLES = 5000  # Maximum number of particles in the simulation
PARTICLE_GENERATION_RATE = 50  # Rate at which new particles are generated per frame

# Color definitions for various elements
COLOR_BLUE = (0, 0, 255, 50)  # Blue color with some transparency for particles
COLOR_CYAN = (0, 255, 255, 50)  # Cyan color with some transparency for particles
COLOR_SKY_BLUE = (135, 206, 235)  # Sky blue color for the background
COLOR_WHITE = (255, 255, 255)  # White color for the fountain structure
COLOR_GRAY = (169, 169, 169)  # Gray color for the lighter part of the base
COLOR_DARK_GRAY = (105, 105, 105)  # Dark gray color for the darker part of the base

class Particle:
    """Class representing a particle in the fountain"""

    def __init__(self):
        # Initializing particle's position and velocity
        self.x = 0  # X-coordinate of the particle
        self.y = 0  # Y-coordinate of the particle
        self.v_x = 0  # Velocity in the X-direction
        self.v_y = 0  # Velocity in the Y-direction
        self.color = COLOR_BLUE  # Color of the particle

    def update(self, dtime: float, gravity: float, wind: float) -> None:
        """Update particle's position and velocity based on gravity and wind"""
        self.x += self.v_x * dtime + wind * dtime  # Update X position with wind effect
        self.y += self.v_y * dtime  # Update Y position
        self.v_y += gravity * dtime  # Update Y velocity with gravity

    def set(self, x, y, v_x, v_y, color):
        """Set particle's initial position, velocity, and color"""
        self.x = x  # X-coordinate
        self.y = y  # Y-coordinate
        self.v_x = v_x  # Velocity in the X-direction
        self.v_y = v_y  # Velocity in the Y-direction
        self.color = color  # Color of the particle

    def draw(self, screen):
        """Draw particle on the screen"""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 2)  # Draw a small circle for the particle

class Fountain:
    """Class representing the fountain"""

    def __init__(self, max_particles: int, particles_per_frame: int, spread: float, gravity: float, wind: float):
        # Initialize fountain properties
        self.particles_per_frame = particles_per_frame  # Number of particles generated per frame
        self.max_particles = max_particles  # Maximum number of particles
        self.spread = spread  # Spread of particles
        self.gravity = gravity  # Gravity effect on particles
        self.wind = wind  # Wind effect on particles
        self.source_x = WIDTH // 2  # X-coordinate of the fountain source
        self.source_y = HEIGHT - 50  # Y-coordinate of the fountain source
        self.particles = []  # List to store particles

    def update(self, dtime) -> None:
        """Update all particles in the fountain"""
        new_particles = [self.init_particle(Particle()) for _ in range(self.particles_per_frame)]  # Generate new particles
        self.particles.extend(new_particles)  # Add new particles to the list

        for particle in self.particles:
            particle.update(dtime, self.gravity, self.wind)  # Update each particle's position and velocity
            # Reinitialize particle if it goes out of bounds
            if particle.y > HEIGHT - 10 or particle.x < 0 or particle.x > WIDTH:
                self.init_particle(particle)

    def render(self, screen) -> None:
        """Render all particles and the fountain structure on the screen"""
        screen.fill(COLOR_SKY_BLUE)  # Fill background with sky blue color
        
        # Draw the base of the fountain
        pygame.draw.rect(screen, COLOR_DARK_GRAY, (self.source_x - 50, self.source_y, 100, 20))  # Dark gray base
        pygame.draw.rect(screen, COLOR_GRAY, (self.source_x - 60, self.source_y + 20, 120, 20))  # Light gray base
        
        # Draw cylinder structure of the fountain
        pygame.draw.rect(screen, COLOR_WHITE, (self.source_x - 12, self.source_y - 200, 25, 200))  # White cylinder
        
        # Draw triangular structure on top of the fountain
        pygame.draw.polygon(screen, COLOR_WHITE, [(self.source_x - 12, self.source_y - 200), 
                                                  (self.source_x + 12, self.source_y - 200), 
                                                  (self.source_x, self.source_y - 230)])  # White triangle
        
        # Draw all particles
        for particle in self.particles:
            particle.draw(screen)
        
        pygame.display.flip()  # Update the full display Surface to the screen

    def init_particle(self, particle: Particle) -> Particle:
        """Initialize particle with a random position and velocity"""
        radius = random.random() * self.spread  # Random radius for the spread of particles
        direction = random.random() * math.pi * 2  # Random direction in radians
        v_x = radius * math.cos(direction)  # Velocity in the X-direction based on radius and direction
        v_y = -random.uniform(150, 200)  # Initial velocity in the Y-direction (upward)
        color = COLOR_BLUE if random.random() > 0.5 else COLOR_CYAN  # Randomly choose blue or cyan color
        particle.set(self.source_x, self.source_y - 230, v_x, v_y, color)  # Set particle's position, velocity, and color
        return particle

def make_renderer():
    """Initialize Pygame and create the renderer (window)"""
    pygame.init()  # Initialize all imported Pygame modules
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)  # Set up the display window
    pygame.display.set_caption("Water Fountain Simulation")  # Set the window title
    return screen  # Return the screen object

def limit_frame_rate(fps: float, cur_time: int) -> bool:
    """Limit the frame rate of the simulation"""
    dtime = time.time() - cur_time  # Calculate elapsed time since last frame
    frame_duration = 1 / fps  # Duration of each frame
    if dtime < frame_duration:
        time.sleep(frame_duration - dtime)  # Sleep if current frame finished early to maintain consistent FPS
        return True
    return False

def handle_events() -> bool:
    """Handle user input and events"""
    for event in pygame.event.get():  # Iterate over the list of events
        if event.type == pygame.QUIT:  # If the quit event is triggered
            return False  # Exit the main loop
    return True  # Continue running

def prompt_user():
    """Prompt user for input to configure the simulation"""
    print("Welcome to the Water Fountain Simulation!")
    while True:
        print("\n1. Start simulation")
        print("2. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            # Prompt user for simulation parameters
            density = int(input("Enter particle density (1-10000): "))
            spread = float(input("Enter particle spread (1-20): "))
            gravity = float(input("Enter gravity (0-20): ")) * 10  # Scale gravity for realistic effect
            wind = float(input("Enter wind speed (0-10): "))  # Wind effect
            # Initialize the fountain with user parameters
            fountain = Fountain(MAX_PARTICLES, density // 100, spread, gravity, wind)
            screen = make_renderer()  # Create the Pygame renderer
            main_loop(screen, fountain)  # Start the main loop

        elif choice == "2":
            print("Exiting...")
            break  # Exit the program
        else:
            print("Invalid choice. Please try again.")

def main_loop(screen, fountain: Fountain) -> None:
    """Main animation loop"""
    running = True  # Flag to control the main loop
    cur_time = time.time()  # Get the current time

    while running:
        fountain.render(screen)  # Render the fountain
        fountain.update(1/FPS)  # Update the fountain with a time step
        cur_time = time.time()  # Update the current time
        
        if not handle_events():  # Handle user input and events
            break  # Exit the main loop if quit event is triggered

        limit_frame_rate(FPS, cur_time)  # Limit the frame rate

    pygame.quit()  # Quit Pygame

def display_instructions():
    """Display instructions for using the simulation"""
    print("\nInstructions:")
    print("1. Use the prompt to configure the simulation.")
    print("2. Enter the desired particle density, spread, gravity, and wind speed.")
    print("3. Watch the fountain simulation in the Pygame window.")
    print("4. Close the window to exit the simulation.")

def additional_features():
    """Add some extra features or variations to the fountain"""
    print("\nAdditional Features:")
    print("1. Change the background color")
    print("2. Modify the fountain's structure")
    change_background_color()

def change_background_color():
    """Change the background color of the simulation"""
    global COLOR_SKY_BLUE
    print("\nChange Background Color:")
    print("1. Sky Blue")
    print("2. Light Green")
    print("3. Light Yellow")
    print("4. Light Pink")

    choice = input("Enter your choice: ")

    if choice == "1":
        COLOR_SKY_BLUE = (135, 206, 235)
    elif choice == "2":
        COLOR_SKY_BLUE = (144, 238, 144)
    elif choice == "3":
        COLOR_SKY_BLUE = (255, 255, 224)
    elif choice == "4":
        COLOR_SKY_BLUE = (255, 182, 193)
    else:
        print("Invalid choice. Default color will be used.")

def modify_fountain_structure():
    """Modify the structure of the fountain"""
    global HEIGHT, WIDTH, FPS, MAX_PARTICLES, PARTICLE_GENERATION_RATE
    print("\nModify Fountain Structure:")
    HEIGHT = int(input("Enter new height of the simulation window: "))
    WIDTH = int(input("Enter new width of the simulation window: "))
    FPS = int(input("Enter new frame rate (FPS): "))
    MAX_PARTICLES = int(input("Enter new maximum number of particles: "))
    PARTICLE_GENERATION_RATE = int(input("Enter new particle generation rate per frame: "))

def main():
    """Main function to run the simulation"""
    display_instructions()
    additional_features()
    prompt_user()

if __name__ == "__main__":
    main()
