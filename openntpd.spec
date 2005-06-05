Summary:	FREE and easy to use implementation of the Network Time Protocol
Summary(pl):	Wolnodostêpna i ³atwa w u¿yciu implementacja protoko³u NTP
Name:		openntpd
Version:	3.7p1
Release:	0.1
License:	BSD
Group:		Daemons
Source0:	ftp://ftp.openbsd.org/pub/OpenBSD/OpenNTPD/%{name}-%{version}.tar.gz
# Source0-md5:	10ed8eefd760e5819efcf3277b118f47
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://www.openntpd.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	openssl-devel
BuildRequires:	sed >= 4.0
Requires(post,preun):   /sbin/chkconfig
Obsoletes:	ntp
Obsoletes:	ntp-client
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenNTPD is a FREE, easy to use implementation of the Network Time
Protocol. It provides the ability to sync the local clock to remote
NTP servers and can act as NTP server itself, redistributing the local
clock.

%description -l pl
OpenNTPD to wolnodostêpna, ³atwa w u¿yciu implementacja protoko³u NTP
(Network Time Protocol). Daje mo¿liwo¶æ synchronizacji lokalnego
zegara ze zdalnymi serwerami NTP i mo¿e dzia³aæ samemu jako serwer
NTP, rozpowszechniaj±c lokalny zegar.

%prep
%setup -q
sed -i -e 's#_ntp#nobody#g' ntpd.h

%build
%{__gettextize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%configure \
	--with-adjtimex
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{sysconfig,rc.d/init.d}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/ntpd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/ntpd

%post
/sbin/chkconfig --add ntpd
if [ -f /var/lock/subsys/ntpd ]; then
        /etc/rc.d/init.d/ntpd restart >&2
else
        echo "Run \"/etc/rc.d/init.d/ntpd start\" to start %{name} daemon."
fi

%preun
if [ "$1" = "0" ]; then
        if [ -f /var/lock/subsys/ntpd ]; then
                /etc/rc.d/init.d/ntpd stop >&2
        fi
        /sbin/chkconfig --del ntpd
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README ChangeLog
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man?/*
%attr(640,root,root) %config(noreplace) %verify(not size md5 mtime) %{_sysconfdir}/ntpd.conf
%attr(640,root,root) %config(noreplace) %verify(not size md5 mtime) /etc/sysconfig/ntpd
%attr(754,root,root) /etc/rc.d/init.d/ntpd
