%define name	pam_pkcs11
%define version	0.6.0
%define release	2

Summary:	A Pluggable Authentication Module for pkcs#11 environments
Name:		%{name}
Version:	%{version}
Release:	%mkrel %{release}
Source0:	http://www.opensc-project.org/files/pam_pkcs11/%{name}-%{version}.tar.gz
License:	GPLv2+
URL:		http://www.opensc.org/pam_pkcs11/
Group:		System/Libraries
BuildRequires:	openssl-devel
BuildRequires:	libldap-devel >= 2.3.6
BuildRequires:	pam-devel
BuildRequires:	libxslt-proc docbook-style-xsl
BuildRequires:	libpcsclite-devel >= 1.2.9
%{?_with_curl:BuildRequires: curl-devel}
Provides:	pkcs11_login
Provides:	pam_pkcs11_login
Obsoletes:	pam_pkcs11_login < 0.5.3-1mdk
# there is no pam_opensc anymore
Obsoletes:	pam_opensc
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description 
This Linux-PAM login module allows a X.509 certificate based user login. 
The certificate and its dedicated private key are thereby accessed by means 
of an appropriate PKCS #11 module. For the verification of the users' 
certificates, locally stored CA certificates as well as either online or 
locally accessible CRLs are used.

%package tools
Group:          System/Libraries
Summary:        Companion tools for pkcs11_login
Requires:       pcsc-lite
Requires:       pam_pkcs11
Provides:       pkcs11_login-tools
Provides:	pam_pkcs11_login-tools
Obsoletes:	pam_pkcs11_login-tools < 0.5.3-1mdk

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
	--with-pcsclite

%make 

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

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

# cleanup
rm -f %{buildroot}/%{_lib}/security/*.*a
rm -f %{buildroot}/%{_libdir}/pam_pkcs11/*.*a

%find_lang %name

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README TODO ChangeLog NEWS
%doc doc/pam_pkcs11.html
%doc doc/README.autologin
%doc doc/README.mappers
%doc doc/README.ldap_mapper
%{_mandir}/man8/*
%{_sysconfdir}/pam_pkcs11/cacerts
%{_sysconfdir}/pam_pkcs11/crls
%config(noreplace) %{_sysconfdir}/pam_pkcs11/pam_pkcs11.conf
%{_bindir}/make_hash_link.sh
%{_libdir}/pam_pkcs11/*.so
/%{_lib}/security/*
%{_datadir}/pam_pkcs11/pam_pkcs11.conf.example
%{_datadir}/pam_pkcs11/pam.d_login.example
%{_datadir}/pam_pkcs11/subject_mapping.example
%{_datadir}/pam_pkcs11/mail_mapping.example
%{_datadir}/pam_pkcs11/digest_mapping.example

%files tools -f %name.lang
%defattr(-,root,root,-)
%doc doc/README.eventmgr
%{_mandir}/man1/*
%config(noreplace) %{_sysconfdir}/pam_pkcs11/card_eventmgr.conf
%config(noreplace) %{_sysconfdir}/pam_pkcs11/pkcs11_eventmgr.conf
%{_bindir}/pkcs11_listcerts
%{_bindir}/pkcs11_setup
%{_bindir}/pkcs11_eventmgr
%{_bindir}/pklogin_finder
%{_bindir}/pkcs11_inspect
%{_datadir}/pam_pkcs11/card_eventmgr.conf.example
%{_datadir}/pam_pkcs11/pkcs11_eventmgr.conf.example
