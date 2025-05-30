import curses
import random
import time

# Define Cityscape (ASCII Art)
CITY_WIDTH = 70
CITY_HEIGHT = 12

# Characters for the city skyline (building parts)
CITY_BUILDINGS = ['|', '_', 'I', '#', '[]', '@', '[]', '=', ':']
FLOOR_HEIGHT = 2

# ANSI color codes for different parts
COLOR_HEAD = 3
COLOR_TRAIL = 2
COLOR_BUILDING = 1

def generate_city():
    """Generate a random city skyline using ASCII characters."""
    city = []
    for row in range(CITY_HEIGHT):
        buildings = []
        for col in range(CITY_WIDTH):
            building_height = random.randint(1, 5) * FLOOR_HEIGHT
            building = random.choice(CITY_BUILDINGS)
            buildings.append(building * building_height)
        city.append(''.join(buildings))
    return city

def print_city(stdscr, city, start_y):
    """Print the city skyline on the screen."""
    max_y, max_x = stdscr.getmaxyx()
    for i, row in enumerate(city):
        # Truncate row if it's too long for the screen
        stdscr.addstr(start_y + i, 0, row[:max_x - 1], curses.color_pair(COLOR_BUILDING))

def matrix_rain(stdscr, city):
    """Animate the matrix rain over the city."""
    max_y, max_x = stdscr.getmaxyx()
    city_start_y = max_y - CITY_HEIGHT
    columns = [random.randint(-20, 0) for _ in range(CITY_WIDTH)]
    trails = [0 for _ in range(CITY_WIDTH)]
    chars = '0123456789ABCDEF'

    while True:
        stdscr.clear()
        # Draw rain
        for x in range(CITY_WIDTH):
            col_y = columns[x]
            if 0 <= col_y < city_start_y:
                # Head
                stdscr.addstr(col_y, x, random.choice(chars), curses.color_pair(COLOR_HEAD))
            # Trail
            for t in range(1, 6):
                trail_y = col_y - t
                if 0 <= trail_y < city_start_y:
                    stdscr.addstr(trail_y, x, random.choice(chars), curses.color_pair(COLOR_TRAIL))
            # Move column down
            if random.random() > 0.975:
                columns[x] = random.randint(-20, 0)
            else:
                columns[x] += 1
            if columns[x] > city_start_y + 5:
                columns[x] = random.randint(-20, 0)
        # Draw city
        print_city(stdscr, city, city_start_y)
        stdscr.refresh()
        time.sleep(0.05)

def main(stdscr):
    """Initialize the curses environment and start animation."""
    # Setup colors
    curses.start_color()
    curses.init_pair(COLOR_BUILDING, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Building colors
    curses.init_pair(COLOR_TRAIL, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Trail color
    curses.init_pair(COLOR_HEAD, curses.COLOR_WHITE, curses.COLOR_GREEN)  # Head color

    # Hide the cursor
    curses.curs_set(0)

    # Generate the city once
    city = generate_city()

    # Run the matrix rain animation
    matrix_rain(stdscr, city)

# Run the curses application
curses.wrapper(main)
