Summary:	Network Block Device support for MILLE-XTERM
Name:		mille-xterm-nbd
Version:	2.9.11
Release:	%mkrel 3
License:	GPL
Group:		System/Servers
URL:		http://sourceforge.net/projects/nbd
Source0:	http://prdownloads.sourceforge.net/nbd/nbd-%{version}.tar.gz
Source1:	nbd-server.wrapper
Source2:	nbd-server.xinetd
Source3:	README.fr
Source4:	INSTALL.fr
BuildRequires:	pkgconfig
BuildRequires:	glib2-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
%{_mandir}/man5/nbd-server.5*

%files -n %{name}-client
%defattr(-,root,root)
%{_bindir}/nbd-client
%{_mandir}/man8/nbd-client.8*


%changelog
* Fri Dec 10 2010 Oden Eriksson <oeriksson@mandriva.com> 2.9.11-3mdv2011.0
+ Revision: 620334
- the mass rebuild of 2010.0 packages

* Fri Sep 04 2009 Thierry Vignaud <tv@mandriva.org> 2.9.11-2mdv2010.0
+ Revision: 430032
- rebuild

* Sun Sep 07 2008 Oden Eriksson <oeriksson@mandriva.com> 2.9.11-1mdv2009.0
+ Revision: 282157
- 2.9.11

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Fri Dec 21 2007 Olivier Blin <oblin@mandriva.com> 2.8.6-2mdv2008.1
+ Revision: 136579
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request


* Mon Mar 05 2007 Oden Eriksson <oeriksson@mandriva.com> 2.8.6-2mdv2007.0
+ Revision: 133067
- bunzip sources

* Thu Feb 08 2007 Oden Eriksson <oeriksson@mandriva.com> 2.8.6-1mdv2007.1
+ Revision: 117780
- Import mille-xterm-nbd

* Fri Sep 29 2006 Oden Eriksson <oeriksson@mandriva.com> 2.8.6-1mdk
- initial Mandriva package (mille-xterm import)

