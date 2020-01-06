#!usr/bin/perl -w
#Script: 	bedgraph_to_wig.pl
#Update date:	2019/12/19
#Author:	Zhuofan Zhang
#Usage:		perl -w bedgraph_to_wig.pl <in.bdg> > <out.wig>

use strict;

@ARGV == 2 or die "Usage: perl -w bedgraph_to_wig.pl <step> <in.bdg> > <out.wig>";

my ($step, $bdg_file) = @ARGV;
open BDG, "<$bdg_file" or die "$!";

# WIG file header
print "track type=wiggle_0\n";

my $cur_chr = "chr0";
#my $cur_pos = 0;
#my $cur_val = 0;
# For processing the duplicate situation
my $cur_start = 0;
my $cur_end = 0;

while(<BDG>)
{
    chomp;
    # Skip the comment lines
    next if(/^track/);
    next if(/#/);

    my ($chr, $start, $end, $val) = split(/\t/);
    # Ignore duplicate position
    #next if ($start eq $cur_start or $end eq $cur_end);
    next if ($chr eq $cur_chr and $start < $cur_end);
    #if($cur_chr ne $chr)
    #{
    #	$cur_chr = $chr;
	#$cur_pos = 0;
    #}

    #while($cur_pos < $start)
    #{
    #    $cur_pos += $step;
    #}
    #
    #$cur_val = $val;
    #$cur_pos = $pos;
    my $pos = $start;
    print "variableStep chrom=$chr span=$step\n";	
    while($pos < $end)
    {
    	print "$pos\t$val\n";
        $pos += $step;
    }
    # $cur_start = $start;
    $cur_chr = $chr;
    $cur_end = $end;
}
