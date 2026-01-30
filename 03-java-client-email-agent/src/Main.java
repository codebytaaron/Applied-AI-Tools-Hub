import java.nio.file.*;
import java.nio.charset.StandardCharsets;

public class Main {
    public static void main(String[] args) throws Exception {
        String input = "";
        try { input = Files.readString(Paths.get("input.txt"), StandardCharsets.UTF_8); } catch (Exception e) {}
        input = input.trim();
        if (input.isEmpty()) {
            System.err.println("No input provided. Edit input.txt.");
            System.exit(1);
        }
        System.out.println("# Client Email Draft\n");
        System.out.println("Subject: Quick update + next steps\n");
        System.out.println("Hi [Name],\n");
        System.out.println("Here’s a clear update based on the notes below. I’ve included next steps and what I need from you.\n");
        System.out.println("## Next steps\n- \n\n## Notes\n```text\n" + input + "\n```");
        System.out.println("\nThanks,\n[Your Name]");
    }
}
