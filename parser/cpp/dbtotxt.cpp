#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "util.h"
#include "uint128.h"
typedef uint128_t IPV6;
//using namespace std;

int offlen;
#define iplen 8

char *ipwrydata;

int main(){
	FILE *fp,*fp2;
	char *s1,*s2,*cp;
	IPV6 ip6,ip62;
	unsigned __int64 thisip,lastip;
	__int64 line=-1, i, indexstart, indexcount, offset, off2;
	int flen;

	fp2=fopen("out.txt","wt");

	fp=fopen("ipv6wry.db","rb");
	fseek(fp,0,2);
	flen=ftell(fp);
	fseek(fp,0,0);
	ipwrydata=(char*)malloc(flen+8);
	memset(ipwrydata + flen, 0, 8);
	fread(ipwrydata,1,flen,fp);
	fclose(fp);

	fprintf(fp2,"STARTIPV6\tENDIPV6\tCOUNTRY\tLOCAL\n");

	offlen=ipwrydata[6];
	indexcount=*(__int64*)&ipwrydata[8];
	indexstart=*(__int64*)&ipwrydata[16];
	thisip=lastip=0;
 	for(i=indexcount-1;i>=0;i--){
		thisip=*(__int64*)&ipwrydata[indexstart+i*(iplen+offlen)];
		ip6.hi=thisip;
		ip62.hi=lastip-1;

		offset=intn(&ipwrydata[indexstart+i*(iplen+offlen)+iplen],offlen);
redir:
		switch(ipwrydata[offset]){
			case 1:
				offset=intn(&ipwrydata[offset+1],offlen);
				goto redir;
			case 2:
				off2=intn(&ipwrydata[offset+1],offlen);
				offset+=offlen+1;
				break;
			default:
				off2=offset;
				cp=strchr(&ipwrydata[off2],0);
				offset=cp-ipwrydata+1;
				break;
		}
		s1=&ipwrydata[off2];
		switch(ipwrydata[offset]){
			case 1:
			case 2:
				off2=intn(&ipwrydata[offset+1],offlen);
				break;
			default:
				off2=offset;
				break;
		}
		s2=&ipwrydata[off2];

		fprintf(fp2,"%04X%04X%04X%04X\t%04X%04X%04X%04X\t%s\t%s\n",
			ip6.n()[7],ip6.n()[6],ip6.n()[5],ip6.n()[4],
			ip62.n()[7],ip62.n()[6],ip62.n()[5],ip62.n()[4],
			s1,s2);

		lastip=thisip;
	}
	
	fclose(fp2);

	free(ipwrydata);

	return 0;
}

