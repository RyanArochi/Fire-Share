Summary:        Internet Routing Protocol
Name:           frr-stable
Version:        8.2
Release:        1%{?dist}
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

# general defines
%define     configdir   %{_sysconfdir}/%{name}
%define     frr_run       /var/run/frr
%define     frr_bindir    %{_libdir}/frr
%define     frr_includedir    %{_includedir}/frr

%configure \
    --sbindir=%{frr_bindir} \
    --sysconfdir= %{_configdir} \
    --localstatedir=%{frr_run} \
    --disable-static \
    --disable-werror \
    --enable-multipath=64 \
    --enable-ospfclient \
    --enable-ospfapi \
    --enable-irdp \
    --disable-ldpd \
    --enable-fpm \
    --enable-user=frr \

%build
make %{?_smp_mflags}
make check %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

# Remove debian init script if it was installed
rm -f %{buildroot}%{frr_bindir}/frr

# kill bogus libtool filesvoi
rm -vf %{buildroot}%{_libdir}/frr/modules/*.la
rm -vf %{buildroot}%{_libdir}/*.la
rm -vf %{buildroot}%{_libdir}/frr/libyang_plugins/*.la

# install /etc sources
mkdir -p %{buildroot}%{_unitdir}
install -m644 %{_builddir}/%{name}-%{version}/tools/frr.service %{buildroot}%{_unitdir}/frr.service
 
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
%{_bindir}/mtracebis
%{_bindir}/vtysh
%{_datadir}/yang/*
%{_datadir}/info/frr.info.gz
%{_libdir}/libfrr.so*
%{_libdir}/libfrrcares*
%{_libdir}/libfrrospf*
%{_libdir}/frr/modules/bgpd_bmp.so
%{frr_bindir}/ospfd
%{frr_bindir}/bgpd
%{frr_bindir}/frr-reload
%{frr_bindir}/frrcommon.sh
%{frr_bindir}/frrinit.sh
%{frr_bindir}/watchfrr.sh


%files devel
%{frr_includedir}/*.h
%{frr_bindir}/*
%{_libdir}/lib*.so
%{_datadir}/man/*
%dir %{frr_includedir}/ospfapi
%{frr_includedir}/ospfapi/*.h
%{frr_includedir}/ospfd/*.h
%{frr_includedir}/eigrpd/*.h
%{frr_includedir}/bfdd/*.h


%files pythontools
%{frr_bindir}/generate_support_bundle.py
%{frr_bindir}/frr-reload.py
%{frr_bindir}/frr_babeltrace.py


%changelog
*   Wed Apr 6 2022 Roye Eshed <eshedr@vmware.com> 8.2-1
-   First Version created. Based off the frrouting Redhat spec file and modified for photon.
-   https://github.com/FRRouting/frr/blob/master/redhat/frr.spec.in
