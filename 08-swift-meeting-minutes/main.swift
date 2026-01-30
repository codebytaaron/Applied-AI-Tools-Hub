import Foundation

let url = URL(fileURLWithPath: "input.txt")
let input = (try? String(contentsOf: url, encoding: .utf8))?.trimmingCharacters(in: .whitespacesAndNewlines) ?? ""
if input.isEmpty {
    fputs("No input provided. Edit input.txt.\n", stderr)
    exit(1)
}

print("# Meeting Minutes\n")
print("## Decisions\n- \n\n## Action Items\n- Owner:  | Due:  | Task:\n\n## Notes\n```text\n\(input)\n```")
