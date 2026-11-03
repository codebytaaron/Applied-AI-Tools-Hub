import System.IO

main :: IO ()
main = do
  input <- readFile "input.txt"
  let t = dropWhile (`elem` " \n\r\t") input
  if null t
    then hPutStrLn stderr "No input provided. Edit input.txt."
    else do
      putStrLn "# KPI Dictionary\n"
      putStrLn "## KPIs\n- Revenue: definition, formula, source\n- Gross Margin: definition, formula, source\n- CAC: definition, formula, source\n"
      putStrLn "## Raw Notes\n```text"
      putStrLn input
      putStrLn "```"
