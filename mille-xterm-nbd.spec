Summary:	Network Block Device support for MILLE-XTERM
Name:		mille-xterm-nbd
Version:	2.8.6
Release:	%mkrel 4
License:	GPL
Group:		System/Servers
URL:		http://sourceforge.net/projects/nbd
Source:		http://prdownloads.sourceforge.net/nbd/nbd-%{version}.tar.bz2
Source1:	nbd-server.wrapper
Source2:	nbd-server.xinetd
Source3:	README.fr
Source4:	INSTALL.fr
BuildRequires:	pkgconfig
BuildRequires:	glib2-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
Network Block Device support for MILLE-XTERM. 

%package -n	%{name}-server
Summary:	NBD server 
Group:		System/Servers
Requires:	xinetd
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre): rpm-helper
Requires(postun): rpm-helper

%description -n	%{name}-server
NBD server for the MILLE-XTERM project.

%package -n	%{name}-client
Summary:	NBD client 
Group:		System/Servers

%description -n	%{name}-client
NBD client for the MILLE-XTERM project.

%prep 

%setup -q -n nbd-%{version}
cp %{SOURCE1} nbd-server.wrapper
cp %{SOURCE2} nbd-server.xinetd
cp %{SOURCE3} README.fr
cp %{SOURCE4} INSTALL.fr


chmod 644 README.fr INSTALL.fr

%build

%configure2_5x

%make

%install
rm -rf %{buildroot}

#It seems they have inverted sbin and bin!
%makeinstall sbindir=%{buildroot}%{_bindir} bindir=%{buildroot}%{_sbindir}

install -d %{buildroot}%{_sysconfdir}/xinetd.d

install -m0755 nbd-server.wrapper %{buildroot}%{_sbindir}/nbd-server.wrapper
install -m0644 nbd-server.xinetd %{buildroot}%{_sysconfdir}/xinetd.d/nbd-server

%pre -n %{name}-server
%{_datadir}/rpm-helper/add-user %{name}-server $1 nbd /var/lib/rpm /bin/false

%postun -n %{name}-server
%{_datadir}/rpm-helper/del-user %{name}-server $1 nbd
%{_initrddir}/xinetd restart

%post -n %{name}-server
if [ ! -d /swapfiles ]; then
    mkdir /swapfiles
    dd if=/dev/zero of=/swapfiles/default.swap bs=1024 count=32000
    mkswap /swapfiles/default.swap
    chown nbd:nbd -R /swapfiles
fi

if ! grep nbd-server %{_sysconfdir}/services; then
    echo -e "# nbd-server added by the %{name}-server-%{version}-%{release} package at `LC_ALL=C date`\nnbd-server\t3000/tcp\t\t\t# Network Block Device" >> %{_sysconfdir}/services
fi

%{_initrddir}/xinetd restart

%clean
rm -rf %{buildroot}

%files -n %{name}-server
%defattr(-,root,root)
%doc README* INSTALL*
%config(noreplace) %{_sysconfdir}/xinetd.d/nbd-server
%{_sbindir}/nbd-server
%{_sbindir}/nbd-server.wrapper
%{_mandir}/man1/nbd-server.1*

%files -n %{name}-client
%defattr(-,root,root)
%{_bindir}/nbd-client
%{_mandir}/man8/nbd-client.8*


