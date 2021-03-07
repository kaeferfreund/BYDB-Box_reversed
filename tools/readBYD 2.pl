#!/usr/bin/perl
#
# readBYD.pl
#
# This program reads some current values from a BYD HVS/HVM Premium Battery Box.
# There is NO WARRANTY
#
#
# If you find this program useful send me some greetings to forenandi73@kabelmail.de
#
# redirect STDERR to nul (Windows) or /dev/null (UNIX) if you are not interested in the debugging output

use strict;
use IO::Socket;
use Digest::CRC;

# connect to BYD HVS/HVM Premium device, adjust PeerAddr to match your IP
my $sock = IO::Socket::INET->new(PeerAddr => '192.168.23.244', PeerPort => '8080', Proto => 'tcp') or die;

# commands to be sent to BYD
my $tobyd1="\x01\x03\x00\x00\x00\x13\x04\x07";
my $tobyd2="\x01\x03\x05\x00\x00\x19\x84\xcc";

# unbuffer output on socket, stdout, stderr
my $old=select($sock); $|=1; 
select(STDOUT);$|=1;
select(STDERR);$|=1;
select($old);

# always read one byte from stream
$/=\1;

# create empty hash for results
my %rh=();

# send first command to BYD
print $sock $tobyd1;
print STDERR "Data1 sent!\n";

# read 3 bytes
my $b11=<$sock>;	# 0x01
my $b12=<$sock>; 	# 0x03
my $b13=<$sock>; 	# length of data

my $dl1=ord($b13);	# data length
printf STDERR "data length=%d\n",$dl1;

# read payload
my $pl1=$b13;	
for (my $i=0;$i<$dl1;$i++)
{
	$pl1.=<$sock>;
}

# read checksum bytes
my $c11=<$sock>;	# checksum LSB
my $c12=<$sock>;	# checksum MSB

# get overall checksum from data
my $crc1=ord($c12)*256 + ord($c11);

# calculate checksum from actual data
my $ctx1 = Digest::CRC->new(width=>16, init=>0x0284, xorout=>0x0000, refout=>1, poly=>0x8005, refin=>1, cont=>0);
$ctx1->add($pl1);
my $digest1=$ctx1->digest;

printf STDERR "Payload length: %d, Checksum=%04X, Digest=%04X\n",length($pl1),$crc1,$digest1;

if ($b11 ne "\x01" || $b12 ne "\x03" || $crc1 != $digest1)
{
	die "illegal/unexpected data received";
}

# print received bytes
my $num1=0;
for (my $i=0;$i<length($pl1);$i++)
{
	my $c=substr($pl1,$i,1);
	$num1++;
	my $o=ord($c);
	$c=".";
	if ($o > 31 && $o < 127) { $c=chr($o); }

	printf STDERR "%03d: %03d %02X %s\n",$num1,$o,$o,$c;
}

# extract the values from the payload
&getvals1(\%rh,$pl1);

# send second command
print $sock $tobyd2;
print STDERR "Data2 sent!\n";

# read 3 bytes from response
my $b21=<$sock>;	#0x01
my $b22=<$sock>; 	#0x03
my $b23=<$sock>; 	# length of data

my $dl2=ord($b23);	# data length
printf STDERR "data length=%d\n",$dl2;

# read the payload
my $pl2=$b23;		# payload
for (my $i=0;$i<$dl2;$i++)
{
	$pl2.=<$sock>;
}

# read checksum bytes
my $c21=<$sock>;	# checksum LSB
my $c22=<$sock>;	# checksum MSB

# get overall checksum from data
my $crc2=ord($c22)*256 + ord($c21);

# calculate checksum from actual payload
my $ctx2 = Digest::CRC->new(width=>16, init=>0x0284, xorout=>0x0000, refout=>1, poly=>0x8005, refin=>1, cont=>0);
$ctx2->add($pl2);
my $digest2=$ctx2->digest;

printf STDERR "Payload length: %d, Checksum=%04X, Digest=%04X\n",length($pl2),$crc2,$digest2;

if ($b21 ne "\x01" || $b22 ne "\x03" || $crc2 != $digest2)
{
	die "illegal/unexpected data received";
}

# print payload bytes
my $num2=0;
for (my $i=0;$i<length($pl2);$i++)
{
	my $c=substr($pl2,$i,1);
	$num2++;
	my $o=ord($c);
	$c=".";
	if ($o > 31 && $o < 127) { $c=chr($o); }

	printf STDERR "%03d: %03d %02X %s\n",$num2,$o,$o,$c;
}

# extract the values from the payload
&getvals2(\%rh,$pl2);

# finally print the accumulated results
foreach my $k (sort keys %rh)
{
	printf STDOUT "%s = %s\n",$k,$rh{$k};
}

$sock->close();
print STDERR "End.\n";
exit(0);

sub getvals1
{
	my $h=shift @_;
	my $pl=shift @_;

	$$h{SerialNo}=substr($pl,1,19);
	$$h{"BMU-A"}=getvers(substr($pl,25,2));
	$$h{"BMU-B"}=getvers(substr($pl,27,2));
	$$h{BMS}=getvers(substr($pl,29,2));
}

sub getvals2
{
	my $h=shift @_;
	my $pl=shift @_;

	$$h{SoC}=getshort(substr($pl,1,2));
	$$h{CellVhigh}=getshort(substr($pl,3,2))/100;
	$$h{CellVlow}=getshort(substr($pl,5,2))/100;
	$$h{SoH}=getshort(substr($pl,7,2));
	$$h{Vbatt}=getshort(substr($pl,11,2))/100;
	$$h{CellTempHigh}=getshort(substr($pl,13,2));
	$$h{CellTempLow}=getshort(substr($pl,15,2));
	$$h{Vout}=getshort(substr($pl,33,2))/100;

	my $currval=getshort(substr($pl,9,2));
	
	if ($currval < 32768)
	{
		$$h{Current}=$currval/10;
	}
	else
	{
		$$h{Current}=($currval-2**16)/10;
	}
}

sub getshort
{
	my $v=shift @_;
	return(
		ord(substr($v,0,1))*256 + ord(substr($v,1,1))
	);
}

sub getvers
{
	my $v=shift @_;
	return(
		ord(substr($v,0,1)) . "." .  ord(substr($v,1,1))
	);
}

