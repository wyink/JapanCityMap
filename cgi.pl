#!/usr/bin/perl
#????????????
#??????????h??????,??????????????????????????B
use strict;
use encoding qw(shiftjis);#sourceCode(thisFile) ->shiftjis
binmode(STDOUT,":utf8");

my ($g_infile,$g_outfile,$g_str)=('','','');
my %g_hash=();

#__main__

#?z????????f?[?^???????
$g_infile ="corona_patient.csv";
%g_hash = cases_data_Read($g_infile); #$hash{city}=count

#???n?}???????
$g_infile = "changedOsaka3.svg";
$g_str = read_original_map($g_infile,\&Osaka,%g_hash); #$g_str = show.html(changed);

#???n?}?????????
$g_outfile = "cgi2.html";
print_out_map($g_outfile,$g_str);

exit;


sub cases_data_Read {
	my $infile = shift;
	my %tmp=();

	open my $IN,"<:utf8",$infile or die "No csv file found.";
		while(my $l=<$IN>){
			chomp $l;
			if($.<=3){next;}#skip header
			@_ =split/\,/,$l;
			$tmp{$_[4]}++; #city++
		}	
	close $IN;

	return %tmp;
}

sub read_original_map {
	my ($infile,$cb,%hash) = @_;
	my @cl=('#EBFFEB','#DDFFFF','#C9FCFF','#B5F9FF','#A1F2FF','#8CE6FF','#75DBFF','#65C6FF','#52B0FF','#4199FF','#3E7AFF','#305AFF','#2941F6','#2B2CE7','#2A0BD9');
	my ($check,$city,$bcc,$str,$acc) =('','','','','');

	open my $IN,"<:utf8",$infile or die "No csv file found.";
		while(my $l=<$IN>){
			if($l=~/^<path class="cwtv (\d+) (.+?|.+??)" style="fill-rule:evenodd;fill:(.+?)\;fill-opacity/){
				($check,$city,$bcc)=($1,$2,$3);
				if($city=~/??$/){
					if($cb){
						$city=$cb->($city,$check);
					}else{
						#default;
					}
				}
				if(exists $hash{$city}){
					if($hash{$city}<10){
						$acc = $cl[0];
					}elsif($hash{$city}>=150){
						$acc= $cl[14];
					}else{
						$acc = $cl[int($hash{$city}/10)];
					}
					$l=~s/${bcc}/${acc}/;
					$str .= $l;
				}else{#?z????????
					$str.=$l;
				}
			}else{
				$str .= $l
			}
		}
	close $IN;
	return $str;
}

sub print_out_map {
	my ($outfile,$str) = @_ ;
	open my $OUT,">:utf8",$outfile or die "Error writing outputfile";
	print $OUT "$str";
	$str="";
	close $OUT;
}

sub Osaka {
	my ($city,$check) = @_ ;
	my %SakaiCity= ('???'=>'','?k??'=>'27146','????'=>'','???'=>'','????'=>'','????'=>'27144','??????'=>'');

	if(exists $SakaiCity{$city}){
		if($city eq '?k??' && $SakaiCity{$city} != $check){
			$city="???s"
		}elsif($city eq '????' && $SakaiCity{$city} != $check){
			$city="???s"
		}else{
			$city = "??s";
		}
	}else{
		$city="???s"
	}
	return $city;
}

