const std = @import("std");

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const alloc = gpa.allocator();

    const cwd = std.fs.cwd();
    var file = cwd.openFile("input.txt", .{}) catch {
        std.log.err("No input.txt found", .{});
        return;
    };
    defer file.close();

    const data = try file.readToEndAlloc(alloc, 1_000_000);
    defer alloc.free(data);

    const trimmed = std.mem.trim(u8, data, " \n\r\t");
    if (trimmed.len == 0) {
        std.log.err("No input provided. Edit input.txt.", .{});
        return;
    }

    const out = std.io.getStdOut().writer();
    try out.print("# Bid Submission Checklist\n\n", .{});
    try out.print("## Checklist\n- [ ] Scope confirmed\n- [ ] Exclusions listed\n- [ ] Schedule confirmed\n- [ ] Insurance/COI ready\n- [ ] Pricing reviewed\n\n", .{});
    try out.print("## Raw Notes\n```text\n{s}\n```\n", .{trimmed});
}
