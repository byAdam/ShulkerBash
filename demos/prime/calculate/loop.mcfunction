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
execute @s[scores={tmp=..-1,is_prime=1}] ~ ~ ~ function calculate/loop