Summary:        Internet Routing Protocol
Name:           frr
Version:        8.2
Release:        14%{?dist}
License:        
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
Requires:       frrouting
%description    devel
It contains the libraries and header files to create applications

%package pythontools
Summary: python tools for frr
BuildRequires:  python3
Group: System Environment/Daemons

%package devel
Summary: Header and object files for frr development
Group: System Environment/Daemons
Requires: %{name} = %{version}-%{release}

%description devel
The frr-devel package contains the header and object files neccessary for
developing OSPF-API and frr applications.

%package snmp
Summary: SNMP support
Group: System Environment/Daemons
BuildRequires: net-snmp-devel
Requires: %{name} = %{version}-%{release}

%description snmp
Adds SNMP support to FRR's daemons by attaching to net-snmp's snmpd
through the AgentX protocol.  Provides read-only access to current
routing state through standard SNMP MIBs.


%prep
%setup -q -n frr-%{frrversion}

%prep
%autosetup -p1
sed -i 's@\(ln -s -f \)$(PREFIX)/bin/@\1@' Makefile
sed -i "s@(PREFIX)/man@(PREFIX)/share/man@g" Makefile

%build
MFLAGS=
make VERBOSE=1 %{?_smp_mflags} -f Makefile-frr_frr-pythontools $MFLAGS
make clean %{?_smp_mflags}
make VERBOSE=1 %{?_smp_mflags} $MFLAGS

%install

%check
make %{?_smp_mflags} check

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(-,root,root)

%files devel

%changelog
