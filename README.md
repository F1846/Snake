Snake Game in Python -

Settings

 # Change background color every x foods eaten.
            if score % 20000 == 0:
                bg_color_index = (bg_color_index + 1) % len(BACKGROUND_COLORS)
            checkpoint = {
                "snake": list(snake),
                "snake_length": snake_length,
                "dx": dx, "dy": dy,
                "score": score,
                "speed": speed,


# Check food collision.
        if new_head == food_pos:
            snake_length += 4  # Grow by 4 segments.
            score += 1
            if score % 6 == 0:
                speed += 1  # Increase speed every 4 foods eaten.
            if score % 40 == 0:
                speed -= 3
               
            if score % 40 == 0:  
                      snake_length = snake_length // 2
            if score % 50 == 0:
                large_food = spawn_food(is_large=True)
                score += 15  # Add 15 points for the large food
                food_pos = spawn_food() 
            else:
                food_pos = spawn_food()  
