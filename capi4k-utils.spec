Summary:	CAPI 2.0 libraries and configuration tools
Summary(pl):	Biblioteki i narzedzia konfiguracyjne CAPI 2.0
Summary(de):	CAPI 2.0 Werkzeuge für verschiedene ISDN Karten
Name:		capi4k-utils
Version:	2004.03.31
Release:	1
License:	GPL
Group:		Applications/Communications
Source0:	ftp://ftp.in-berlin.de/pub/capi4linux/%{name}-2004-03-31.tar.gz
Source1:	ftp://ftp.in-berlin.de/pub/capi4linux/CHANGES
Source10:	capi.conf
Source11:	capi.init
Patch0:		%{name}-make.patch
URL:		ftp://ftp.in-berlin.de/pub/capi4linux/
BuildRequires:	libtool
BuildRequires:	ppp-plugin-devel
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		ppp_ver		%(awk -F'"' '/VERSION/ { print $2 }' /usr/include/pppd/patchlevel.h 2>/dev/null || echo ERROR)

%description
These are the necessary tools to operate various CAPI 2.0 compatible ISDN
adapters.

In order to use the tools you need to install the appropriate driver for the
adapter.
Native driver packages for some adapters are provided with the kernel.

%description -l pl
W tym pakiecie zawarte s± biblioteki wspó³dzielone libcapi20 oraz narzêdzia
s³u¿±ce do ³adowania i konfiguracji sterowników CAPI.

Aby skorzystaæ z tych narzêdzi bêdziesz potrzebowa³ jeszcze odpowiedniego
sterownika do swojej karty ISDN. Kilka takich sterowników znajduje siê ju¿
w j±drze.

%description -l de
Dies sind die notwendigen Grundprogramme um verschiedene CAPI 2.0 fähige Geräte
und ISDN Karten einzurichten.
Für einige Karten müssen Sie zusätzlich entsprechende Treiber installieren.

%package devel
Summary:	Static library and header files for capi development.
Summary(pl):	Pliki nag³ówkowe i biblioteki statyczne libcapi.
Summary(de):	Bibliotheken und Kopfdateien zur Entwicklung von CAPI Programmen
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains the capi static library and header
files required to develop capi applications.

%description devel
Ten pakiet zawiera pliki nag³ówkowe i biblioteki statyczne potrzebne
do budowania programów korzystaj±cych ze sterowników w standardzie CAPI
poprzez bibliotekê libcapi.

%description devel -l de
Dieses Paket stellt die notwendigen Bibliotheken und andere Dateien bereit um
CAPI Programme zu entwickeln oder neu zu Übersetzen.

%package capifax
Summary:	CAPI 2.0 fax tool
Summary(pl):	Proste narzêdzia do faksowania wykorzystuj±cy mo¿liwo¶ci CAPI 2.0
Summary(de):	CAPI 2.0 Fax Programm
Group:		Applications/Communications
Requires:	%{name} = %{version}-%{release}

%description capifax
Native tools for sending and receiving fax with CAPI 2.0.

HINT: If you intend to use other CAPI 2.0 compliant fax software you do not
      need to install this package.

%description capifax -l pl
Podstawowe programy do wysy³ania i odbierania faksów przez CAPI 2.0.

PORADA: Je¶li zamierzasz korzystaæ z innego pakietu do obs³ugi faksów
        (np. capisuite lub hylafax) to nie potrzebujesz tego pakietu.

%description capifax -l de
Basis Programm zum Senden und Empfangen von Fax mittels CAPI 2.0.

HINWEIS: Falls Sie andere CAPI 2.0 fähige Faxprogramme einsetzen wollen
         brauchen Sie dieses Paket nicht installieren.

%package remotecapi
Summary:	CAPI 2.0 remote tool
Summary(pl):	Program udostêpniaj±cy interface CAPI 2.0 przez sieæ
Summary(de):	CAPI 2.0 Fernsteuerungsprogramm
Group:		Applications/Communications
Requires:	%{name} = %{version}-%{release}

%description remotecapi
Native tool for remote control (login) with CAPI 2.0.

ATTENTION: This is extreme BETA.
           Avoid to install this package.

%description remotecapi -l pl
Program udostêpniaj±cy interface CAPI 2.0 przez sieæ

UWAGA: To jest na razie BETA. Tylko do testów.

%description remotecapi -l de
Basis Programm zu Fernsteuerung (Login) mittels CAPI 2.0.

ACHTUNG: Dieses Programm ist BETA Testsoftware.
         Vermeiden Sie dieses Paket zu installieren.

%package -n ppp-plugin-capi
Summary:	capiplugin for pppd-%{ppp_ver}
Summary(pl):	Wtyczka capi dla pppd w wersji %{ppp_ver}
Group:		Applications/Communications
Requires:	%{name} = %{version}-%{release}
Requires:	ppp = %{ppp_ver}

%description -n ppp-plugin-capi
capiplugin for pppd-%{ppp_ver}.

%description -n ppp-plugin-capi -l pl
Wtyczka capi dla pppd w wersji %{ppp_ver}.

%prep
%setup -q -n %{name}
%patch0 -p1

cat > .config << END
CONFIG_BINDIR='%{_bindir}'
CONFIG_SBINDIR='%{_sbindir}'
CONFIG_MANDIR='%{_mandir}'
CONFIG_AVMCAPICTRL=y
CONFIG_CAPIFAX=y
CONFIG_RCAPID=y
CONFIG_PPPDCAPIPLUGIN=y
END

install -p %{SOURCE1} .

%build
%{__make} subconfig
%{__make} PPPVERSIONS=%{ppp_ver}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} PPPVERSIONS=%{ppp_ver} install \
	DESTDIR=$RPM_BUILD_ROOT

# Firmware goes here - see LSB and kernel 2.6.x ISDN stuff
install -d %{buildroot}%{_datadir}/isdn

# install capi configuration file used by capiinit
install -d %{buildroot}%{_sysconfdir}/capi
install %{SOURCE10} %{buildroot}%{_sysconfdir}/capi/

# install capi startup script
install -D %{SOURCE11} %{buildroot}%{_initrddir}/capi

%post -n %{name}
/sbin/ldconfig
/sbin/chkconfig --add capi
exit 0

%preun -n %{name}
if [ "$1" = "0" ]; then
	/sbin/service capi stop > /dev/null 2>&1
	/sbin/chkconfig --del capi
fi
exit 0

%postun -n %{name}
/sbin/ldconfig
if [ "$1" -ge "1" ]; then
	/sbin/service capi stop > /dev/null 2>&1
fi
exit 0

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES
%doc pppdcapiplugin/examples
%attr(0755,root,root) %{_bindir}/capiinfo
%attr(0755,root,root) %{_sbindir}/capiinit
%attr(0755,root,root) %{_sbindir}/avmcapictrl
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%attr(754,root,root) %{_initrddir}/capi
%{_mandir}/man8/capiinfo.8*
%{_mandir}/man8/avmcapictrl.8*
%dir %{_datadir}/isdn
%dir %{_sysconfdir}/capi
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/capi/capi.conf
# mi to nie chce dzialac, wypisuje ze brak pliku
#%ghost %{_sysconfdir}/capi.conf

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/*
%{_libdir}/lib*.la
# to chyba powinno isc do -static, ale nie wiem...
%{_libdir}/lib*.a

%files capifax
%defattr(644,root,root,755)
%attr(0755,root,root) %{_bindir}/capifax*

%files remotecapi
%defattr(644,root,root,755)
%attr(0755,root,root) %{_sbindir}/rcapid

%files -n ppp-plugin-capi
%defattr(644,root,root,755)
%exclude %{_sysconfdir}/drdsl
%exclude %{_sysconfdir}/ppp
%{_libdir}/pppd/%{ppp_ver}/*
%{_mandir}/man8/capiplugin.8*
