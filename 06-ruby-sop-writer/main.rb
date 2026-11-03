input = File.exist?("input.txt") ? File.read("input.txt").strip : ""
if input.empty?
  warn "No input provided. Edit input.txt."
  exit 1
end

puts "# SOP (Standard Operating Procedure)\n\n"
puts "## Purpose\n- \n\n## Steps\n1. \n2. \n\n## Quality Checks\n- \n\n## Raw Notes\n```text\n#{input}\n```"
