Summary:	FREE and easy to use implementation of the Network Time Protocol
Summary(pl):	Wolnodost�pna i �atwa w u�yciu implementacja protoko�u NTP
Name:		openntpd
Version:	3.6p1
Release:	0.1
License:	BSD
Group:		Daemons
Source0:	ftp://ftp.openbsd.org/pub/OpenBSD/OpenNTPD/%{name}-%{version}.tar.gz
# Source0-md5:	ba69427e83a9a8080410261af116cdbe
Source1:	%{name}.init
Source2:	%{name}.sysconfig
# http://www.zipworld.com.au/~dtucker/openntpd/patches/
Patch0:		%{name}-3.6p1-linux-adjtimex4.patch
Patch1:		%{name}-cvs20041125.patch
URL:		http://www.openntpd.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	openssl-devel
Obsoletes:	ntp
Obsoletes:	ntp-client
Requires(post,preun):   /sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenNTPD is a FREE, easy to use implementation of the Network Time
Protocol. It provides the ability to sync the local clock to remote
NTP servers and can act as NTP server itself, redistributing the local
clock.

%description -l pl
OpenNTPD to wolnodost�pna, �atwa w u�yciu implementacja protoko�u NTP
(Network Time Protocol). Daje mo�liwo�� synchronizacji lokalnego
zegara ze zdalnymi serwerami NTP i mo�e dzia�a� samemu jako serwer
NTP, rozpowszechniaj�c lokalny zegar.

%prep
%setup -q
%patch0 -p0
%patch1 -p1
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
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{sysconfig,rc.d/init.d}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/ntpd
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/ntpd

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
