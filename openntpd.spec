Summary:	FREE and easy to use implementation of the Network Time Protocol
Summary(pl.UTF-8):	Wolnodostępna i łatwa w użyciu implementacja protokołu NTP
Name:		openntpd
Version:	6.0p1
Release:	1
License:	BSD
Group:		Daemons
Source0:	https://ftp.openbsd.org/pub/OpenBSD/OpenNTPD/%{name}-%{version}.tar.gz
# Source0-md5:	9388979cc2713551bfbdfb3864291abe
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.service
URL:		http://www.openntpd.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-tools
BuildRequires:	intltool
BuildRequires:	openssl-devel
BuildRequires:	rpmbuild(macros) >= 1.647
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun,postun):	systemd-units >= 38
Requires:	rc-scripts
Requires:	systemd-units >= 0.38
Provides:	ntpclient
Provides:	ntpdaemon
Obsoletes:	ntpclient
Obsoletes:	ntpdaemon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		privsepdir	/usr/share/empty

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
%configure \
	--with-privsep-path=%{privsepdir} \
	--with-privsep-user=nobody

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{sysconfig,rc.d/init.d} \
	$RPM_BUILD_ROOT%{systemdunitdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/ntpd
cp -a %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/ntpd

install %{SOURCE3} $RPM_BUILD_ROOT%{systemdunitdir}/ntpd.service

%post
/sbin/chkconfig --add ntpd
%service ntpd restart "OpenNTP Daemon"
%systemd_post ntpd.service

%preun
if [ "$1" = "0" ]; then
	%service ntpd stop
	/sbin/chkconfig --del ntpd
fi
%systemd_preun ntpd.service

%postun
%systemd_reload

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README ChangeLog
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ntpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/ntpd
%attr(754,root,root) /etc/rc.d/init.d/ntpd
%attr(755,root,root) %{_sbindir}/ntpctl
%attr(755,root,root) %{_sbindir}/ntpd
%{systemdunitdir}/ntpd.service
%{_mandir}/man5/ntpd.conf.5*
%{_mandir}/man8/ntpctl.8*
%{_mandir}/man8/ntpd.8*
