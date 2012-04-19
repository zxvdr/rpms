Name:           stud
Version:        0.4
Release:        1%{?dist}
Summary:        Scalable TLS Unwrapping Daemon

Group:          System Environment/Daemons
License:        BSD
URL:            https://github.com/bumptech/stud
# git clone git://github.com/bumptech/stud
# cd stud
# git archive --prefix="stud-0.4/" --format=tar HEAD | gzip > stud-0.4.tar.gz
Source0:        %{name}-%{version}.tar.gz
Source1:        %{name}.conf
Source2:        %{name}.service
Patch0:         libev.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  openssl-devel
BuildRequires:  libev-devel
BuildRequires:  systemd-units

Requires(pre):      shadow-utils
Requires(post):     systemd-units
Requires(preun):    systemd-units
Requires(postun):   systemd-units

%description
stud is a network proxy that terminates TLS/SSL connections and forwards the
unencrypted traffic to some backend. It's designed to handle 10s of thousands
of connections efficiently on multicore machines.

%prep
%setup -q
%patch0 -p1 -b .libev


%build
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install PREFIX=$RPM_BUILD_ROOT%{_usr}
%{__install} -D -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
%{__install} -D -m 0644 %{SOURCE2} ${RPM_BUILD_ROOT}%{_unitdir}/%{name}.service

%clean
rm -rf $RPM_BUILD_ROOT


%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
    useradd -r -g %{name} -d / -s /sbin/nologin \
    -c "Stud user" %{name}
exit 0

%preun
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable %{name}.service > /dev/null 2>&1 || :
    /bin/systemctl stop %{name}.service > /dev/null 2>&1 || :
fi

%post
if [ $1 -eq 1 ] ; then 
    # Initial installation 
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart %{name}.service >/dev/null 2>&1 || :
fi

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%attr(0644,root,root) %{_unitdir}/%{name}.service
%doc LICENSE
%doc %{_mandir}/man8/stud.8*
%{_bindir}/stud


%changelog
* Thu Apr 19 2012 David Robinson <zxvdr.au@gmail.com> - 0.4-1
- new release

* Thu Nov 17 2011 David Robinson <zxvdr.au@gmail.com> - 0.3-1
- Initial packaging
