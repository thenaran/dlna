install:
	@cd /lib;tar xvfp minidlna.tar
	@cd /lib/minidlna-1.1.3/;./configure;make;make install
	@rm /lib/minidlna.tar
	@apt-get install -y autoconf automake libtool
	@cd /lib/gmrender-resurrect; ./autogen.sh; ./configure; make && make install
	@apt-get remove -y autoconf automake libtool
