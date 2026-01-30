use std::fs;

fn main() {
    let input = fs::read_to_string("input.txt").unwrap_or_else(|_| "".to_string());
    if input.trim().is_empty() {
        eprintln!("No input provided. Edit input.txt.");
        std::process::exit(1);
    }
    println!("# Policy Draft (Outline)\n");
    println!("## Purpose\n- Define the goal and scope.\n");
    println!("## Rules\n- List clear rules and enforcement.\n");
    println!("## Exceptions\n- Define exceptions and approvals.\n");
    println!("## Raw Notes\n```text\n{}\n```", input.trim());
}
