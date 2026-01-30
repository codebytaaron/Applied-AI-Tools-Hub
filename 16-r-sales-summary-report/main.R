input <- ""
if (file.exists("input.txt")) input <- trimws(paste(readLines("input.txt"), collapse="\n"))
if (nchar(input) == 0) { cat("No input provided. Edit input.txt.\n", file=stderr()); quit(status=1) }

cat("# Sales Summary Report\n\n")
cat("## Highlights\n- \n\n## Risks\n- \n\n## Next Actions\n- \n\n")
cat("## Raw Notes\n```text\n")
cat(input)
cat("\n```\n")
