
%bcond_with	capifax	# capifax has some error and won't build right now

Summary:	CAPI 2.0 libraries and configuration tools
Summary(de):	CAPI 2.0 Werkzeuge für verschiedene ISDN Karten
Summary(pl):	Biblioteki i narzêdzia konfiguracyjne CAPI 2.0
Name:		capi4k-utils
Version:	2005.07.18
Release:	1
License:	GPL
Group:		Applications/Communications
Source0:	ftp://ftp.in-berlin.de/pub/capi4linux/%{name}-2005-07-18.tar.gz
# Source0-md5:	c745759b6b3d64e19763727176648cdf
Source1:	ftp://ftp.in-berlin.de/pub/capi4linux/CHANGES
# Source1-md5:	03739a0170eba14f03f7dc7ccc58bba8
Source10:	capi.conf
Source11:	capi.init
Patch0:		%{name}-make.patch
Patch1:		%{name}-amd64.patch
URL:		ftp://ftp.in-berlin.de/pub/capi4linux/
BuildRequires:	libtool
BuildRequires:	ppp-plugin-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post):	/sbin/ldconfig
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		ppp_ver		%(awk -F'"' '/VERSION/ { print $2 }' /usr/include/pppd/patchlevel.h 2>/dev/null || echo ERROR)

%description
These are the necessary tools to operate various CAPI 2.0 compatible
ISDN adapters.

In order to use the tools you need to install the appropriate driver
for the adapter. Native driver packages for some adapters are provided
with the kernel.

%description -l de
Dies sind die notwendigen Grundprogramme um verschiedene CAPI 2.0
fähige Geräte und ISDN Karten einzurichten. Für einige Karten müssen
Sie zusätzlich entsprechende Treiber installieren.

%description -l pl
W tym pakiecie zawarte s± biblioteki wspó³dzielone libcapi20 oraz
narzêdzia s³u¿±ce do ³adowania i konfiguracji sterowników CAPI.

Aby skorzystaæ z tych narzêdzi potrzebny jest jeszcze odpowiedni
sterownik do karty ISDN. Kilka takich sterowników znajduje siê ju¿ w
j±drze.

%package devel
Summary:	Header files for capi development
Summary(de):	Kopfdateien zur Entwicklung von CAPI Programmen
Summary(pl):	Pliki nag³ówkowe capi
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the header files required to develop capi
applications.

%description devel -l pl
Ten pakiet zawiera pliki nag³ówkowe potrzebne do budowania programów
korzystaj±cych ze sterowników w standardzie CAPI poprzez bibliotekê
libcapi.

%description devel -l de
Dieses Paket stellt die Dateien bereit um CAPI Programme zu entwickeln
oder neu zu Übersetzen.

%package static
Summary:	Static capi libraries
Summary(pl):	Statyczne biblioteki capi
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static versions of capi libraries.

%description static -l pl
Statyczne wersje bibliotek capi.

%if %{with capifax}
%package capifax
Summary:	CAPI 2.0 fax tool
Summary(de):	CAPI 2.0 Fax Programm
Summary(pl):	Proste narzêdzia do faksowania wykorzystuj±cy mo¿liwo¶ci CAPI 2.0
Group:		Applications/Communications
Requires:	%{name} = %{version}-%{release}

%description capifax
Native tools for sending and receiving fax with CAPI 2.0.

HINT: If you intend to use other CAPI 2.0 compliant fax software you
      do not need to install this package.

%description capifax -l de
Basis Programm zum Senden und Empfangen von Fax mittels CAPI 2.0.

HINWEIS: Falls Sie andere CAPI 2.0 fähige Faxprogramme einsetzen
         wollen brauchen Sie dieses Paket nicht installieren.

%description capifax -l pl
Podstawowe programy do wysy³ania i odbierania faksów przez CAPI 2.0.

PORADA: Je¶li zamierzasz korzystaæ z innego pakietu do obs³ugi faksów
        (np. capisuite lub hylafax) to nie potrzebujesz tego pakietu.

%endif

%package remotecapi
Summary:	CAPI 2.0 remote tool
Summary(de):	CAPI 2.0 Fernsteuerungsprogramm
Summary(pl):	Program udostêpniaj±cy interface CAPI 2.0 przez sieæ
Group:		Applications/Communications
Requires:	%{name} = %{version}-%{release}

%description remotecapi
Native tool for remote control (login) with CAPI 2.0.

ATTENTION: This is extreme BETA.
           Avoid to install this package.

%description remotecapi -l de
Basis Programm zu Fernsteuerung (Login) mittels CAPI 2.0.

ACHTUNG: Dieses Programm ist BETA Testsoftware.
         Vermeiden Sie dieses Paket zu installieren.

%description remotecapi -l pl
Program udostêpniaj±cy interface CAPI 2.0 przez sieæ

UWAGA: To jest na razie BETA. Tylko do testów.

%package -n ppp-plugin-capi
Summary:	capiplugin for pppd-%{ppp_ver}
Summary(pl):	Wtyczka capi dla pppd w wersji %{ppp_ver}
Group:		Applications/Communications
Requires:	%{name} = %{version}-%{release}
Requires:	ppp = 3:%{ppp_ver}

%description -n ppp-plugin-capi
capiplugin for pppd-%{ppp_ver}.

%description -n ppp-plugin-capi -l pl
Wtyczka capi dla pppd w wersji %{ppp_ver}.

%prep
%setup -q -n %{name}
%patch0 -p1
%if "%{_lib}" == "lib64"
%patch1 -p1
%endif

cat > .config << END
CONFIG_BINDIR='%{_bindir}'
CONFIG_SBINDIR='%{_sbindir}'
CONFIG_MANDIR='%{_mandir}'
CONFIG_AVMCAPICTRL=y
CONFIG_LIBDIR='%{_libdir}'
%{?with_capifax:CONFIG_CAPIFAX=y}
CONFIG_RCAPID=y
CONFIG_PPPDCAPIPLUGIN=y
END

install -p %{SOURCE1} .

%build
%{__make} subconfig
%{__make} \
	PPPVERSIONS=%{ppp_ver}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	PPPVERSIONS=%{ppp_ver} \
	DESTDIR=$RPM_BUILD_ROOT

# Firmware goes here - see LSB and kernel 2.6.x ISDN stuff
install -d $RPM_BUILD_ROOT%{_datadir}/isdn

# install capi configuration file used by capiinit
install -d $RPM_BUILD_ROOT%{_sysconfdir}/capi
install %{SOURCE10} $RPM_BUILD_ROOT%{_sysconfdir}/capi

# install capi startup script
install -D %{SOURCE11} $RPM_BUILD_ROOT%{_initrddir}/capi

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
/sbin/chkconfig --add capi
%service capi restart

%preun
if [ "$1" = "0" ]; then
	%service capi stop
	/sbin/chkconfig --del capi
fi

%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES pppdcapiplugin/examples
%attr(755,root,root) %{_bindir}/capiinfo
%attr(755,root,root) %{_sbindir}/capiinit
%attr(755,root,root) %{_sbindir}/avmcapictrl
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%attr(754,root,root) %{_initrddir}/capi
%{_mandir}/man8/capiinfo.8*
%{_mandir}/man8/avmcapictrl.8*
%dir %{_datadir}/isdn
%dir %{_sysconfdir}/capi
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/capi/capi.conf
# mi to nie chce dzialac, wypisuje ze brak pliku
#%ghost %{_sysconfdir}/capi.conf

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%if %{with capifax}
%files capifax
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/capifax*
%endif

%files remotecapi
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/rcapid

%files -n ppp-plugin-capi
%defattr(644,root,root,755)
%exclude %{_sysconfdir}/drdsl
%exclude %{_sysconfdir}/ppp
%{_libdir}/pppd/%{ppp_ver}/*
%{_mandir}/man8/capiplugin.8*
