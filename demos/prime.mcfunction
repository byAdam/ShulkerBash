def loop
    # Adds 1 to index
    scoreboard players add @s index 1

    # Is input divisible by index?
    scoreboard players operation @s tmp = @s input
    scoreboard players operation @s tmp %= @s index
    scoreboard players set @s[scores={tmp=0}] is_prime 0

    # Is index greater than the input squared?
    scoreboard players operation @s tmp = @s index
    scoreboard players operation @s tmp *= @s index
    scoreboard players operation @s tmp -= @s input

    # If number still could be prime, loop again
    execute @s[scores={tmp=..-1,is_prime=1}] ~ ~ ~ function loop
    
# Create Objectives
scoreboard objectives add input
scoreboard objectives add index
scoreboard objectives add tmp

scoreboard objectives add is_prime

# Init Variables
scoreboard players set @s index 1
scoreboard players set @s is_prime 1

# Get Input
say Enter your number:
scoreboard input ask
scoreboard input read @s input

# If 0 or less, set is_prime to zero
scoreboard players set @s[scores={input=..0}] is_prime 0
# If 2 or greater,run loop
execute @s[scores={input=2..}] ~ ~ ~ function loop

# Display output 
execute @s[scores={is_prime=0}] ~ ~ ~ say Not Prime
execute @s[scores={is_prime=1}] ~ ~ ~ say Prime