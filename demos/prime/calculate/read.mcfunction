scoreboard players set @s input 0

function calculate/read_block
scoreboard players operation @s input_buf *= n10000 const
execute @s[scores={input_buf=0..}] ~ ~ ~ scoreboard players operation @s input += @s input_buf
execute @s ~ ~ ~ tp @s ~1 ~ ~

function calculate/read_block
scoreboard players operation @s input_buf *= n1000 const
execute @s[scores={input_buf=0..}] ~ ~ ~ scoreboard players operation @s input += @s input_buf
execute @s ~ ~ ~ tp @s ~1 ~ ~

function calculate/read_block
scoreboard players operation @s input_buf *= n100 const
execute @s[scores={input_buf=0..}] ~ ~ ~ scoreboard players operation @s input += @s input_buf
execute @s ~ ~ ~ tp @s ~1 ~ ~

function calculate/read_block
scoreboard players operation @s input_buf *= n10 const
execute @s[scores={input_buf=0..}] ~ ~ ~ scoreboard players operation @s input += @s input_buf
execute @s ~ ~ ~ tp @s ~1 ~ ~

function calculate/read_block
execute @s[scores={input_buf=0..}] ~ ~ ~ scoreboard players operation @s input += @s input_buf

