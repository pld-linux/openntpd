# TODO
# - client/daemon package split like ntp.spec
Summary:	FREE and easy to use implementation of the Network Time Protocol
Summary(pl.UTF-8):	Wolnodostępna i łatwa w użyciu implementacja protokołu NTP
Name:		openntpd
Version:	3.9p1
Release:	6
License:	BSD
Group:		Daemons
Source0:	ftp://ftp.openbsd.org/pub/OpenBSD/OpenNTPD/%{name}-%{version}.tar.gz
# Source0-md5:	afc34175f38d08867c1403d9008600b3
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://www.openntpd.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	openssl-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
Provides:	ntpclient
Provides:	ntpdaemon
Obsoletes:	ntpclient
Obsoletes:	ntpdaemon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenNTPD is a FREE, easy to use implementation of the Network Time
Protocol.

It provides the ability to sync the local clock to remote NTP servers
and can act as NTP server itself, redistributing the local clock.

%description -l pl.UTF-8
OpenNTPD to wolnodostępna, łatwa w użyciu implementacja protokołu NTP
(Network Time Protocol).

Daje możliwość synchronizacji lokalnego zegara ze zdalnymi serwerami
NTP i może działać samemu jako serwer NTP, rozpowszechniając lokalny
zegar.

%prep
%setup -q

%build
cp -f /usr/share/automake/config.sub .
%{__gettextize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%configure \
	--with-adjtimex \
	--with-privsep-path=/usr/share/empty \
	--with-mantype=man \
	--with-privsep-user=nobody

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{sysconfig,rc.d/init.d}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/ntpd
cp -a %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/ntpd

%post
/sbin/chkconfig --add ntpd
%service ntpd restart "OpenNTP Daemon"

%preun
if [ "$1" = "0" ]; then
	%service ntpd stop
	/sbin/chkconfig --del ntpd
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README ChangeLog
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man?/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ntpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/ntpd
%attr(754,root,root) /etc/rc.d/init.d/ntpd
