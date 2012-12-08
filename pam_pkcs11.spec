Summary:	A Pluggable Authentication Module for pkcs#11 environments
Name:		pam_pkcs11
Version:	0.6.8
Release:	1
License:	GPLv2+
URL:		http://www.opensc.org/pam_pkcs11/
Group:		System/Libraries
Source0:	http://www.opensc-project.org/files/pam_pkcs11/%{name}-%{version}.tar.gz
BuildRequires:	openssl-devel
BuildRequires:	libldap-devel >= 2.3.6
BuildRequires:	pam-devel
BuildRequires:	libxslt-proc docbook-style-xsl
BuildRequires:	libpcsclite-devel >= 1.2.9
%{?_with_curl:BuildRequires: curl-devel}
Provides:	pkcs11_login
Provides:	pam_pkcs11_login
Obsoletes:	pam_pkcs11_login < 0.6.0-1mdv
# there is no pam_opensc anymore
Obsoletes:	pam_opensc

%description 
This Linux-PAM login module allows a X.509 certificate based user login. 
The certificate and its dedicated private key are thereby accessed by means 
of an appropriate PKCS #11 module. For the verification of the users' 
certificates, locally stored CA certificates as well as either online or 
locally accessible CRLs are used.

%package tools
Group:		System/Libraries
Summary:	Companion tools for pkcs11_login
Requires:	pcsc-lite
Requires:	pam_pkcs11
Provides:	pkcs11_login-tools
Provides:	pam_pkcs11_login-tools
Obsoletes:	pam_pkcs11_login-tools < 0.6.0-1mdv

%description tools
This package contains several pam_pkcs11 related tools
- card_eventmgr: Generate card insert/removal events (pcsc-lite based)
- pkcs11_eventmgr: Generate actions on card insert/removal/timeout events
- pklogin_finder: Get the loginname that maps to a certificate
- pkcs11_inspect: Inspect the contents of a certificate

%prep
%setup -q

%build
%configure2_5x \
	--disable-dependency-tracking %{?_with_curl} \
	--with-ldap \
	--with-pcsclite \
	--disable-static

%make 

%install
%makeinstall_std mandir=%{_mandir}

# Hardcoded defaults... no sysconfdir
install -dm 755 %{buildroot}/%{_sysconfdir}/pam_pkcs11/cacerts
install -dm 755 %{buildroot}/%{_sysconfdir}/pam_pkcs11/crls
install -m 644 etc/pam_pkcs11.conf.example %{buildroot}/%{_sysconfdir}/pam_pkcs11/pam_pkcs11.conf
install -m 644 etc/card_eventmgr.conf.example %{buildroot}/%{_sysconfdir}/pam_pkcs11/card_eventmgr.conf
install -m 644 etc/pkcs11_eventmgr.conf.example %{buildroot}/%{_sysconfdir}/pam_pkcs11/pkcs11_eventmgr.conf

# move pam module to its place
mkdir -p %{buildroot}/%{_lib}/security
mv %{buildroot}%{_libdir}/security/* %{buildroot}/%{_lib}/security/

mkdir %{buildroot}%{_datadir}/doc/%{name}-tools/
mv %{buildroot}%{_datadir}/doc/pam_pkcs11/card_eventmgr.conf.example %{buildroot}%{_datadir}/doc/pam_pkcs11/pkcs11_eventmgr.conf.example %{buildroot}%{_datadir}/doc/%{name}-tools/

%find_lang %name

%files
%doc AUTHORS COPYING README TODO ChangeLog NEWS
%doc doc/pam_pkcs11.html
%doc doc/README.autologin
%doc doc/README.mappers
%doc doc/README.ldap_mapper
%{_mandir}/man8/*
%{_sysconfdir}/pam_pkcs11/cacerts
%{_sysconfdir}/pam_pkcs11/crls
%config(noreplace) %{_sysconfdir}/pam_pkcs11/pam_pkcs11.conf
%{_libdir}/pam_pkcs11/*.so
/%{_lib}/security/*
%{_bindir}/pkcs11_make_hash_link

%files tools -f %name.lang
%doc doc/README.eventmgr
%{_mandir}/man1/*
%config(noreplace) %{_sysconfdir}/pam_pkcs11/card_eventmgr.conf
%config(noreplace) %{_sysconfdir}/pam_pkcs11/pkcs11_eventmgr.conf
%{_bindir}/pkcs11_listcerts
%{_bindir}/pkcs11_setup
%{_bindir}/card_eventmgr
%{_bindir}/pkcs11_eventmgr
%{_bindir}/pklogin_finder
%{_bindir}/pkcs11_inspect


%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 0.6.6-2mdv2011.0
+ Revision: 666980
- mass rebuild

* Wed Dec 08 2010 Tomas Kindl <supp@mandriva.org> 0.6.6-1mdv2011.0
+ Revision: 616337
- add missing strings patch
- update to 0.6.6

* Sat Dec 04 2010 Tomas Kindl <supp@mandriva.org> 0.6.3-1mdv2011.0
+ Revision: 609460
- update to 0.6.3
- drop unneeded patch

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0.6.2-4mdv2011.0
+ Revision: 607060
- rebuild

* Wed Apr 07 2010 Funda Wang <fwang@mandriva.org> 0.6.2-3mdv2010.1
+ Revision: 532511
- rebuild

* Fri Feb 26 2010 Oden Eriksson <oeriksson@mandriva.com> 0.6.2-2mdv2010.1
+ Revision: 511610
- rebuilt against openssl-0.9.8m

  + Tomas Kindl <supp@mandriva.org>
    - bump to 0.6.2

* Wed Jul 08 2009 Guillaume Rousse <guillomovitch@mandriva.org> 0.6.1-1mdv2010.0
+ Revision: 393698
- new version
- rediff format errors patch

* Sat Apr 11 2009 Funda Wang <fwang@mandriva.org> 0.6.0-2mdv2009.1
+ Revision: 365983
- fix str fmt

  + Antoine Ginies <aginies@mandriva.com>
    - rebuild

* Thu Feb 07 2008 Funda Wang <fwang@mandriva.org> 0.6.0-1mdv2008.1
+ Revision: 163624
- New version 0.6.0

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Tue Dec 25 2007 Oden Eriksson <oeriksson@mandriva.com> 0.5.3-4mdv2008.1
+ Revision: 137781
- rebuilt against openldap-2.4.7 libs

* Mon Dec 17 2007 Thierry Vignaud <tv@mandriva.org> 0.5.3-3mdv2008.1
+ Revision: 131001
- kill re-definition of %%buildroot on Pixel's request


* Fri Jan 12 2007 Andreas Hasenack <andreas@mandriva.com> 0.5.3-3mdv2007.0
+ Revision: 107941
- rebuilt
- using mkrel
- Import pam_pkcs11

* Thu Dec 08 2005 Andreas Hasenack <andreas@mandriva.com> 0.5.3-2mdk
- obsolete pam_opensc

* Mon Nov 07 2005 Andreas Hasenack <andreas@mandriva.com> 0.5.3-1mdk
- updated to version 0.5.3
- the tarball was renamed upstream: now we are pam_pkcs11 (without "login")
- updated url tag: project was absorbed by OpenSC
- removed pam_pkcs11_x86_64_Makefile.patch.bz2, already applied
- force rebuild with openldap 2.3.x
- marked pam_pkcs11.conf, card_eventmgr.conf and pkcs11_eventmgr.conf
  as %%config(noreplace) files
- config directory changed from /etc/pkcs11 to /etc/pam_pkcs11
- added buildrequires for libpcsclite-devel >= 1.2.9

* Sat May 07 2005 Udo Rader <udo.rader@bestsolution.at> 0.5.1-2mdk
- fixed specfile duplicate files issues
- fixed build issues on x86_64

* Sun Apr 24 2005 Udo Rader <udo.rader@bestsolution.at> 0.5.1-1mdk
- initial version

