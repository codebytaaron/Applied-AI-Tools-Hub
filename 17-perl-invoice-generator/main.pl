use strict; use warnings;
my $input = "";
if (open my $fh, "<", "input.txt") { local $/; $input = <$fh>; close $fh; }
$input =~ s/^\s+|\s+$//g;
if ($input eq "") { die "No input provided. Edit input.txt.\n"; }

print "# Invoice (Markdown)\n\n";
print "## Bill To\n- \n\n## Line Items\n| Item | Qty | Rate | Total |\n|---|---:|---:|---:|\n| Labor |  |  |  |\n| Materials |  |  |  |\n\n";
print "## Notes\n```text\n$input\n```\n";
