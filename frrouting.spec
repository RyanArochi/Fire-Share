Summary:        Internet Routing Protocol
Name:           frr
Version:        8.2
Release:        14%{?dist}
License:        GPLv2+
URL:            https://frrouting.org/
Group:          System Environment/Daemons
BuildRequires:  bison
BuildRequires:  c-ares-devel
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  json-c-devel
BuildRequires:  libcap-devel
BuildRequires:  make
BuildRequires:  ncurses-devel
BuildRequires:  readline-devel
BuildRequires:  texinfo
BuildRequires:  libyang2-devel
BuildRequires:  python3-devel
BuildRequires:  python3-sphinx
BuildRequires:  systemd
BuildRequires:  systemd-devel
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

%build
make %{?_smp_mflags} MAKEINFO="makeinfo --no-split"
make info

%configure \
    --sbindir=%{_sbindir} \
    --sysconfdir=%{configdir} \
    --localstatedir=%{rundir} \
    --disable-static \
    --disable-werror \
    --enable-irdp \

%install
mkdir -p %{buildroot}%{_sysconfdir}/{frr,sysconfig,logrotate.d,pam.d,default} \
         %{buildroot}%{_localstatedir}/log/frr %{buildroot}%{_infodir}
make DESTDIR=%{buildroot} INSTALL="install -p" CP="cp -p" install

# Remove this file, as it is uninstalled and causes errors when building on RH9
rm -rf %{buildroot}/usr/share/info/dir

# Remove debian init script if it was installed
rm -f %{buildroot}%{_sbindir}/frr

# kill bogus libtool files
rm -vf %{buildroot}%{_libdir}/frr/modules/*.la
rm -vf %{buildroot}%{_libdir}/*.la
rm -vf %{buildroot}%{_libdir}/frr/libyang_plugins/*.la

# install /etc sources
mkdir -p %{buildroot}%{_unitdir}
install -m644 %{zeb_src}/tools/frr.service %{buildroot}%{_unitdir}/frr.service

%postuninstall-info --delete --info-dir=%{_infodir} %{_infodir}/autogen.info.gz

%check
make %{?_smp_mflags} check

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(-,root,root)

%files devel

%changelog
