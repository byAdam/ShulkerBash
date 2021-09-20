# Create Objectives
scoreboard objectives add input
scoreboard objectives add input_buf
scoreboard objectives add index
scoreboard objectives add tmp
scoreboard objectives add const

scoreboard players set n10 const 10
scoreboard players set n100 const 100
scoreboard players set n1000 const 1000
scoreboard players set n10000 const 10000
summon x
scoreboard players set @e[type=x] input 5
scoreboard players set @e[type=x] input = n10 const


scoreboard objectives add is_prime

# Init Variables
scoreboard players set @s index 1
scoreboard players set @s is_prime 1

## Input
summon writer 1 3 0
scoreboard players set @e[type=writer] input_ord 0

setblock 9 3 0 no

# Camera
function tools/build_keyboard
