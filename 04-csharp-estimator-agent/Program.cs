using System;
using System.IO;

class Program {
    static void Main() {
        var input = File.Exists("input.txt") ? File.ReadAllText("input.txt") : "";
        input = input.Trim();
        if (input.Length == 0) {
            Console.Error.WriteLine("No input provided. Edit input.txt.");
            Environment.Exit(1);
        }
        Console.WriteLine("# Itemized Estimate\n");
        Console.WriteLine("## Scope\n- \n\n## Line Items\n| Item | Qty | Unit | Rate | Total |\n|---|---:|---|---:|---:|\n| Labor |  | hr |  |  |\n| Materials |  |  |  |  |\n");
        Console.WriteLine("## Assumptions\n- \n\n## Raw Notes\n```text\n" + input + "\n```");
    }
}
