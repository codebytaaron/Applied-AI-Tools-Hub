local f = io.open("input.txt","r")
local input = f and f:read("*a") or ""
if f then f:close() end
input = input:gsub("^%s+",""):gsub("%s+$","")
if input == "" then
  io.stderr:write("No input provided. Edit input.txt.\n")
  os.exit(1)
end
print("# Menu Description Polish\n")
print("## Guidelines\n- Keep it short\n- Lead with the main ingredient\n- Mention sauces/texture\n")
print("## Raw Notes\n```text\n"..input.."\n```")
