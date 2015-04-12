# NOTE: for more recent CAPI utils see isdn4k-utils.spec
#
# Conditional build:
%bcond_with	capifax	# capifax has some error and won't build right now

Summary:	CAPI 2.0 libraries and configuration tools
Summary(de.UTF-8):	CAPI 2.0 Werkzeuge für verschiedene ISDN Karten
Summary(pl.UTF-8):	Biblioteki i narzędzia konfiguracyjne CAPI 2.0
Name:		capi4k-utils
Version:	2005.07.18
Release:	4
License:	GPL v2+
Group:		Applications/Communications
Source0:	ftp://ftp.in-berlin.de/pub/capi4linux/%{name}-2005-07-18.tar.gz
# Source0-md5:	c745759b6b3d64e19763727176648cdf
Source1:	ftp://ftp.in-berlin.de/pub/capi4linux/CHANGES
# Source1-md5:	03739a0170eba14f03f7dc7ccc58bba8
Source10:	capi.conf
Source11:	capi.init
Patch0:		%{name}-include.patch
Patch1:		%{name}-make.patch
Patch2:		%{name}-msg2str_safety.patch
Patch3:		%{name}-ppd244.patch
Patch4:		%{name}-ppd245.patch
Patch5:		%{name}-rcapid.patch
Patch6:		%{name}-amd64.patch
Patch7:		%{name}-ppd247.patch
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

%description -l de.UTF-8
Dies sind die notwendigen Grundprogramme um verschiedene CAPI 2.0
fähige Geräte und ISDN Karten einzurichten. Für einige Karten müssen
Sie zusätzlich entsprechende Treiber installieren.

%description -l pl.UTF-8
W tym pakiecie zawarte są biblioteki współdzielone libcapi20 oraz
narzędzia służące do ładowania i konfiguracji sterowników CAPI.

Aby skorzystać z tych narzędzi potrzebny jest jeszcze odpowiedni
sterownik do karty ISDN. Kilka takich sterowników znajduje się już w
jądrze.

%package devel
Summary:	Header files for capi development
Summary(de.UTF-8):	Kopfdateien zur Entwicklung von CAPI Programmen
Summary(pl.UTF-8):	Pliki nagłówkowe capi
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the header files required to develop capi
applications.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe potrzebne do budowania programów
korzystających ze sterowników w standardzie CAPI poprzez bibliotekę
libcapi.

%description devel -l de.UTF-8
Dieses Paket stellt die Dateien bereit um CAPI Programme zu entwickeln
oder neu zu Übersetzen.

%package static
Summary:	Static capi libraries
Summary(pl.UTF-8):	Statyczne biblioteki capi
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static versions of capi libraries.

%description static -l pl.UTF-8
Statyczne wersje bibliotek capi.

%package capifax
Summary:	CAPI 2.0 fax tool
Summary(de.UTF-8):	CAPI 2.0 Fax Programm
Summary(pl.UTF-8):	Proste narzędzia do faksowania wykorzystujący możliwości CAPI 2.0
Group:		Applications/Communications
Requires:	%{name} = %{version}-%{release}

%description capifax
Native tools for sending and receiving fax with CAPI 2.0.

HINT: If you intend to use other CAPI 2.0 compliant fax software you
      do not need to install this package.

%description capifax -l de.UTF-8
Basis Programm zum Senden und Empfangen von Fax mittels CAPI 2.0.

HINWEIS: Falls Sie andere CAPI 2.0 fähige Faxprogramme einsetzen
         wollen brauchen Sie dieses Paket nicht installieren.

%description capifax -l pl.UTF-8
Podstawowe programy do wysyłania i odbierania faksów przez CAPI 2.0.

PORADA: Jeśli zamierzasz korzystać z innego pakietu do obsługi faksów
        (np. capisuite lub hylafax) to nie potrzebujesz tego pakietu.

%package remotecapi
Summary:	CAPI 2.0 remote tool
Summary(de.UTF-8):	CAPI 2.0 Fernsteuerungsprogramm
Summary(pl.UTF-8):	Program udostępniający interfejs CAPI 2.0 przez sieć
Group:		Applications/Communications
Requires:	%{name} = %{version}-%{release}

%description remotecapi
Native tool for remote control (login) with CAPI 2.0.

ATTENTION: This is extreme BETA.
           Avoid to install this package.

%description remotecapi -l de.UTF-8
Basis Programm zu Fernsteuerung (Login) mittels CAPI 2.0.

ACHTUNG: Dieses Programm ist BETA Testsoftware.
         Vermeiden Sie dieses Paket zu installieren.

%description remotecapi -l pl.UTF-8
Program udostępniający interfejs CAPI 2.0 przez sieć.

UWAGA: Jest on na razie BETA. Tylko do testów.

%package -n ppp-plugin-capi
Summary:	CAPI plugin for pppd
Summary(pl.UTF-8):	Wtyczka CAPI dla pppd
Group:		Applications/Communications
Requires:	%{name} = %{version}-%{release}
Requires:	ppp

%description -n ppp-plugin-capi
CAPI plugin for pppd.

%description -n ppp-plugin-capi -l pl.UTF-8
Wtyczka CAPI dla pppd.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1
%patch2 -p0
%patch3 -p0
%patch4 -p0
%patch5 -p1
%patch6 -p1
%patch7 -p1

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
%{__make} subconfig \
	CC="%{__cc}"

%{__make} \
	CC="%{__cc}"
	PPPVERSIONS=%{ppp_ver}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	PPPVERSIONS=%{ppp_ver} \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_libdir}/pppd/{%{ppp_ver},plugins}

# Firmware goes here - see LSB and kernel 2.6.x ISDN stuff
install -d $RPM_BUILD_ROOT%{_datadir}/isdn

# install capi configuration file used by capiinit
install -d $RPM_BUILD_ROOT%{_sysconfdir}/capi
install %{SOURCE10} $RPM_BUILD_ROOT%{_sysconfdir}/capi

# install capi startup script
install -D %{SOURCE11} $RPM_BUILD_ROOT/etc/rc.d/init.d/capi

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
%attr(755,root,root) %{_sbindir}/avmcapictrl
%attr(755,root,root) %{_sbindir}/capiinit
%attr(755,root,root) %{_libdir}/libcapi20.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libcapi20.so.3
%attr(754,root,root) /etc/rc.d/init.d/capi
%{_mandir}/man8/avmcapictrl.8*
%{_mandir}/man8/capiinfo.8*
%dir %{_datadir}/isdn
%dir %{_sysconfdir}/capi
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/capi/capi.conf

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcapi20.so
%{_libdir}/libcapi20.la
%{_includedir}/capi20.h
%{_includedir}/capicmd.h
%{_includedir}/capiutils.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libcapi20.a
%{_libdir}/libcapi20dyn.a

%if %{with capifax}
%files capifax
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/capifax
%attr(755,root,root) %{_bindir}/capifaxrcvd
%endif

%files remotecapi
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/rcapid

%files -n ppp-plugin-capi
%defattr(644,root,root,755)
%exclude %{_sysconfdir}/drdsl
%exclude %{_sysconfdir}/ppp
%attr(755,root,root) %{_libdir}/pppd/plugins/capiplugin.so
%attr(755,root,root) %{_libdir}/pppd/plugins/userpass.so
%{_mandir}/man8/capiplugin.8*
