import java.io.File

fun main() {
    val input = if (File("input.txt").exists()) File("input.txt").readText().trim() else ""
    if (input.isEmpty()) {
        System.err.println("No input provided. Edit input.txt.")
        return
    }
    println("# Intake Questionnaire\n")
    println("## Questions")
    println("- What is the address / site access?")
    println("- What is the problem and when did it start?")
    println("- Any photos or model numbers?")
    println("- Preferred timing and constraints?")
    println("\n## Raw Notes\n```text\n$input\n```")
}
