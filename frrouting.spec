# general defines
%define     debug_package %{nil}
%define     frrversion  8.2
%define     configdir   %{_sysconfdir}/%{name}
%define     _sbindir    /usr/lib/frr
%define     _slibdir    /usr/include/frr
%define     zeb_src     %{_builddir}/%{name}-%{frrversion}

# defines for configure
%define     rundir  %{_localstatedir}/run/%{name}

############################################################################

Summary:        Internet Routing Protocol
Name:           frr-stable
Version:        %{frrversion}
Release:        14%{?dist}
License:        GPLv2+
URL:            https://frrouting.org/
Group:          System Environment/Daemons
BuildRequires:  bison
BuildRequires:  c-ares-devel
BuildRequires:  python3-devel
BuildRequires:  python3-sphinx
BuildRequires:  systemd
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  json-c-devel
BuildRequires:  libcap-devel
BuildRequires:  make
BuildRequires:  ncurses-devel
BuildRequires:  readline-devel
BuildRequires:  texinfo
BuildRequires:  libyang-devel
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/FRRouting/frr/archive/refs/heads/stable/%{version}.zip

%description
FRRouting is a free software that manages TCP/IP based routing
protocol. It takes multi-server and multi-thread approach to resolve
the current complexity of the Internet.

%package        devel
Summary:        Header and development files for frrouting
Requires: %{name} = %{version}-%{release}
%description    devel
It contains the libraries and header files to create applications

%package pythontools
Summary: python tools for frr
BuildRequires:  python3

%description pythontools
Python Tools

%pre
echo 'new install'

%prep
%autosetup -p1

./bootstrap.sh


%configure \
    --sbindir=%{_sbindir} \
    --sysconfdir=/etc/frr \
    --localstatedir=/var/run/frr \
    --disable-static \
    --disable-werror \
    --enable-multipath=64 \
    --enable-ospfclient \
    --enable-ospfapi \
    --enable-irdp \
    --disable-ldpd \
    --enable-fpm \
    --enable-user=frr \
    SPHINXBUILD=/usr/bin/sphinx-build

%build
make %{?_smp_mflags}
make check %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

# Remove this file, as it is uninstalled and causes errors when building on RH9
rm -rf %{buildroot}/usr/share/info/dir

# Remove debian init script if it was installed
rm -f %{buildroot}%{_sbindir}/frr

# kill bogus libtool filesvoi
rm -vf %{buildroot}%{_libdir}/frr/modules/*.la
rm -vf %{buildroot}%{_libdir}/*.la
rm -vf %{buildroot}%{_libdir}/frr/libyang_plugins/*.la

# install /etc sources
mkdir -p %{buildroot}%{_unitdir}
install -m644 %{zeb_src}/tools/frr.service %{buildroot}%{_unitdir}/frr.service

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%doc COPYING
%doc doc/mpls
%doc README.md
%{_unitdir}/frr.service
/usr/bin/mtracebis                                                                                                      
/usr/bin/vtysh
/usr/share/yang/*
/usr/share/man/*
/usr/share/info/frr.info.gz
%{_libdir}/libfrr.so*
%{_libdir}/libfrrcares*
%{_libdir}/libfrrospf*
%{_libdir}/frr/modules/bgpd_bmp.so
%{_sbindir}/ospfd
%{_sbindir}/bgpd
%{_sbindir}/frr-reload
%{_sbindir}/frrcommon.sh
%{_sbindir}/frrinit.sh
%{_sbindir}/watchfrr.sh


%files devel
%{_slibdir}/*.h
%{_sbindir}/*
/usr/lib/lib*.so
%dir %{_includedir}/%{name}/ospfapi
%{_slibdir}/ospfapi/*.h
%{_slibdir}/ospfd/*.h
%{_slibdir}/eigrpd/*.h
%{_slibdir}/bfdd/*.h


%files pythontools
%{_sbindir}/generate_support_bundle.py
%{_sbindir}/frr-reload.py
%{_sbindir}/frr_babeltrace.py


%changelog
