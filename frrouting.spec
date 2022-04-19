Summary:        Internet Routing Protocol
Name:           frr
Version:        8.2.2
Release:        2%{?dist}
License:        GPLv2+
URL:            https://frrouting.org/
Group:          System Environment/Daemons
BuildRequires:  autoconf
BuildRequires:  automake
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
BuildRequires:  elfutils-devel
BuildRequires:  python3

%if 0%{?with_check:1}
BuildRequires:  python3-pytest
%endif

Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/FRRouting/frr/archive/refs/heads/stable/%{name}-%{version}.tar.gz

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

%description pythontools
Python Tools

%package python3
Summary: python3 for frr

%description python3
Python3

%pre
echo 'new install'

%prep
%autosetup -p1

./bootstrap.sh

# general defines
%define     frr_libdir        /usr/local/lib
%define     frr_bindir        /usr/local/bin
%define     frr_sbindir       /usr/local/sbin
%define     frr_datadir       /usr/local/share
%define     frr_includedir    /usr/local/include

sh ./configure --host=%{_host} --build=%{_build} \
    --sysconfdir=%{_sysconfdir}/frr \
    --libexecdir=%{_libexecdir}/frr \
    --localstatedir=%{_localstatedir}/run/frr \
    --with-moduledir=%{_libdir}/frr/modules \
    --disable-static \
    --disable-werror \
    --enable-multipath=64 \
    --enable-ospfclient \
    --enable-ospfapi \
    --enable-irdp \
    --disable-ldpd \
    --enable-fpm \
    --enable-user=frr \
    --enable-vtysh=yes \

%build
make %{?_smp_mflags}

%if 0%{?with_check:1}
%check
make check %{?_smp_mflags}
%endif

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

# Remove debian init script if it was installed
rm -f %{buildroot}%{frr_bindir}/frr

# kill bogus libtool filesvoi
rm -vf %{buildroot}%{_libdir}/frr/modules/*.la
rm -vf %{buildroot}%{_libdir}/*.la
rm -vf %{buildroot}%{_libdir}/frr/libyang_plugins/*.la

# install /etc sources
mkdir -p %{buildroot}%{_unitdir}
install -m644 %{_builddir}/%{name}-%{version}/tools/frr.service %{buildroot}%{_unitdir}/frr.service
install -p -m 755 tools/frrinit.sh %{_libexecdir}/frr
install -p -m 755 tools/frrcommon.sh %{_libexecdir}/frrcommon.sh
install -p -m 755 tools/watchfrr.sh %{_libexecdir}/watchfrr.sh

# Delete libtool archives
find %{buildroot} -type f -name "*.la" -delete -print

%post
-p /sbin/ldconfig
%systemd_post frr.service

%preun
%systemd_preun frr.service

%postun
-p /sbin/ldconfig
%systemd_postun_with_restart frr.service

%files
%doc COPYING
%doc doc/mpls
%doc README.md
%{_unitdir}/frr.service
%{frr_bindir}/mtracebis
%{frr_bindir}/vtysh
%{frr_datadir}/yang/*
%{frr_datadir}/info/frr.info
%{frr_libdir}/libfrr.so*
%{frr_libdir}/libfrrcares*
%{frr_libdir}/libfrrospf*
%{_libdir}/frr/modules/bgpd_bmp.so
%exclude %{_libdir}/debug
%{frr_sbindir}/ospfd
%{frr_sbindir}/bgpd
%{frr_sbindir}/frr-reload
%{frr_sbindir}/frrcommon.sh
%{frr_sbindir}/frrinit.sh
%{frr_sbindir}/watchfrr.sh
%{frr_sbindir}/babeld
%{frr_sbindir}/eigrpd
%{frr_sbindir}/fabricd
%{frr_sbindir}/frr
%{frr_sbindir}/isisd
%{frr_sbindir}/nhrpd
%{frr_sbindir}/bfdd
%{frr_sbindir}/ospf6d
%{frr_sbindir}/pathd
%{frr_sbindir}/pbrd
%{frr_sbindir}/pimd
%{frr_sbindir}/ripd
%{frr_sbindir}/ripngd
%{frr_sbindir}/ssd
%{frr_sbindir}/staticd
%{frr_sbindir}/vrrpd
%{frr_sbindir}/watchfrr
%{frr_sbindir}/zebra

%files devel
%{frr_includedir}/frr/*.h
%{frr_libdir}/lib*.so
%{frr_datadir}/man/*
%dir %{frr_includedir}/frr/ospfapi
%{frr_includedir}/frr/ospfapi/*.h
%{frr_includedir}/frr/ospfd/*.h
%{frr_includedir}/frr/eigrpd/*.h
%{frr_includedir}/frr/bfdd/*.h

%files pythontools
%{frr_sbindir}/generate_support_bundle.py
%{frr_sbindir}/frr-reload.py
%{frr_sbindir}/frr_babeltrace.py

%changelog
*   Fri Apr 8 2022 Roye Eshed <eshedr@vmware.com> 8.2-1
-   General fixes including changing relative paths to absolute paths and adding commands for frr.service
*   Wed Apr 6 2022 Roye Eshed <eshedr@vmware.com> 8.2-1
-   First Version created. Based off the frrouting Redhat spec file and modified for photon.
-   https://github.com/FRRouting/frr/blob/master/redhat/frr.spec.in
