# general defines
%define     debug_package %{nil}
%define     frrversion  8.2
%define     configdir   %{_sysconfdir}/%{name}
%define     _sbindir    /usr/lib/frr
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
    --enable-irdp \

%build
make

%install
sudo make install

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

%changelog
