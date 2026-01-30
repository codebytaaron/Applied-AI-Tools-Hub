package main

import (
    "bufio"
    "fmt"
    "os"
    "strings"
)

func readAll() string {
    b, _ := os.ReadFile("input.txt")
    if len(b) > 0 {
        return string(b)
    }
    // fallback stdin
    in := bufio.NewScanner(os.Stdin)
    var sb strings.Builder
    for in.Scan() {
        sb.WriteString(in.Text())
        sb.WriteString("\n")
    }
    return sb.String()
}

func main() {
    input := strings.TrimSpace(readAll())
    if input == "" {
        fmt.Println("No input provided. Edit input.txt or pipe stdin.")
        os.Exit(1)
    }
    fmt.Println("# Work Order")
    fmt.Println("")
    fmt.Println("## Summary")
    fmt.Println("- Convert the notes below into a clear job plan.")
    fmt.Println("")
    fmt.Println("## Raw Notes")
    fmt.Println("```")
    fmt.Println(input)
    fmt.Println("```")
    fmt.Println("")
    fmt.Println("## Checklist")
    fmt.Println("- [ ] Confirm site address and access")
    fmt.Println("- [ ] Tools and materials loaded")
    fmt.Println("- [ ] Safety briefing completed")
    fmt.Println("- [ ] Customer sign-off captured")
}
