def loop
    # Copys input score
    scoreboard players operation @s prime_tmp = @s prime
    # Adds 1 to iterator
    scoreboard players add @s prime_calc 1
    # Gets prime_tmp % prime_calc
    scoreboard players operation @s prime_tmp %= @s prime_calc
    # Gets prime_calc squared
    scoreboard players operation @s prime_calc_square = @s prime_calc
    scoreboard players operation @s prime_calc_square *= @s prime_calc_square
    scoreboard players operation @s prime_calc_square -= @s prime

    # If it does not divide in evenly, run this loop again
    execute @s[scores={prime_tmp=!0,prime_calc_square=..0}] ~ ~ ~ function loop

# Creates objectives
scoreboard objectives add prime
scoreboard objectives add prime_tmp
scoreboard objectives add prime_calc
scoreboard objectives add prime_calc_square

## Waits for user input
say Enter your number:
scoreboard input ask
scoreboard input read @s prime
scoreboard players set @s prime_calc 1

# Begins prime loop if input is greater than 1
execute @s[scores={prime=2..}] ~ ~ ~ function loop

scoreboard players operation @s prime_calc -= @s prime
## If the number that divides in is the same as the input, prime_calc will be 0
execute @s[scores={prime=1}] ~ ~ ~ say Not Prime
execute @s[scores={prime=2..,prime_calc=0}] ~ ~ ~ say Prime
execute @s[scores={prime_calc=!0,prime_calc_square=1..}] ~ ~ ~ say Prime
execute @s[scores={prime_calc=!0,prime_calc_square=..0}] ~ ~ ~ say Not Prime