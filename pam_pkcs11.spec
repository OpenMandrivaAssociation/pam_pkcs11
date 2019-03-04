Summary:	A Pluggable Authentication Module for pkcs#11 environments
Name:		pam_pkcs11
Version:	0.6.10
Release:	1
License:	GPLv2+
Group:		System/Libraries
Url:		http://www.opensc.org/pam_pkcs11/
Source0:	http://www.opensc-project.org/files/pam_pkcs11/%{name}-%{version}.tar.gz
BuildRequires:	docbook-style-xsl
BuildRequires:	xsltproc
BuildRequires:	openldap-devel >= 2.3.6
BuildRequires:	pam-devel
BuildRequires:	pkgconfig(libpcsclite)
BuildRequires:	pkgconfig(openssl)
%{?_with_curl:BuildRequires: pkgconfig(libcurl)}
Provides:	pkcs11_login
Provides:	pam_pkcs11_login
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

%description tools
This package contains several pam_pkcs11 related tools
- card_eventmgr: Generate card insert/removal events (pcsc-lite based)
- pkcs11_eventmgr: Generate actions on card insert/removal/timeout events
- pklogin_finder: Get the loginname that maps to a certificate
- pkcs11_inspect: Inspect the contents of a certificate

%prep
%autosetup -p1

%build
./bootstrap

%configure \
	--disable-dependency-tracking %{?_with_curl} \
	--with-ldap \
	--with-pcsclite \
	--disable-static

%make_build

%install
%make_install mandir=%{_mandir}

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

%files tools -f %{name}.lang
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

