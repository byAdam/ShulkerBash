## Read
summon read 1 3 0
execute @e[type=read] ~ ~ ~ function calculate/read
scoreboard players operation @s input = @e[type=read] input 
kill @e[type=read]

# Init Variables
scoreboard players set @s index 1
scoreboard players set @s is_prime 1

function tools/build_keyboard

# If 0 or less, set is_prime to zero
scoreboard players set @s[scores={input=..0}] is_prime 0
# If 2 or greater,run loop
execute @s[scores={input=2..}] ~ ~ ~ function calculate/loop

# Display output 
execute @s[scores={is_prime=0}] ~ ~ ~ setblock 9 3 0 no
execute @s[scores={is_prime=1}] ~ ~ ~ setblock 9 3 0 yes