Summary:	FREE and easy to use implementation of the Network Time Protocol
Summary(pl):	Wolnodostêpna i ³atwa w u¿yciu implementacja protoko³u NTP
Name:		openntpd
Version:	3.6p1
Release:	0.1
License:	BSD
Group:		Daemons
Source0:	ftp://ftp.openbsd.org/pub/OpenBSD/OpenNTPD/%{name}-%{version}.tar.gz
# Source0-md5:	ba69427e83a9a8080410261af116cdbe
URL:		http://www.openntpd.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	openssl-devel
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

%build
%{__gettextize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README ChangeLog
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man?/*
%attr(640,root,root) %config(noreplace) %verify(not size md5 mtime) %{_sysconfdir}/ntpd.conf
