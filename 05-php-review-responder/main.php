<?php
        $input = file_exists("input.txt") ? trim(file_get_contents("input.txt")) : "";
        if ($input === "") { fwrite(STDERR, "No input provided. Edit input.txt.\n"); exit(1); }
        echo "# Review Response Draft\n\n";
        echo "## 5-star response\n- Thank them, mention something specific, invite back.\n\n";
        echo "## 1-star response\n- Apologize, take accountability, offer to fix offline.\n\n";
        echo "## Raw Notes\n```text\n$input\n```\n";
        ?>
