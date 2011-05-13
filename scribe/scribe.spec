%if (0%{?fedora} > 10 || 0%{?rhel} > 5)
%global with_boost_patch 0
%else
%global with_boost_patch 1
%endif

%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global config_opts --disable-static --with-thriftpath=%{_prefix} --with-fb303path=%{_prefix} --with-boost-system=boost_system --with-boost-filesystem=boost_filesystem

Name:             scribe
Version:          2.2
Release:          4%{?dist}
Summary:          A server for aggregating log data streamed in real time

Group:            Development/Libraries
License:          ASL 2.0
URL:              https://github.com/facebook/scribe
Source0:          https://github.com/downloads/facebook/%{name}/%{name}-%{version}.tar.gz
Source1:          scribed.init
Source2:          scribed.sysconfig
Source3:          logrotate
# make scribe 2.2 work with boost 1.33
Patch0:           boost-1.33.patch
# Patch below is from: http://github.com/bterm/sandbox.git
# make scribe 2.2 work with thrift 0.5.0
Patch1:           thrift-0.5.0.patch
# Patch below is from: http://github.com/zxvdr/scribe.git
# it fixes the initial filename for hourly rolled logs
Patch2:           hourly_roll_period_initial_filename.patch
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    automake
%if %{with_boost_patch}
BuildRequires:    boost-devel >= 1.33
%else
BuildRequires:    boost-devel >= 1.36
%endif
BuildRequires:    fb303-devel >= 0.5.0
BuildRequires:    libevent-devel
BuildRequires:    thrift >= 0.5.0
BuildRequires:    thrift-cpp-devel

Requires:         %{name}-python
Requires:         fb303 >= 0.5.0
Requires(pre):    shadow-utils
Requires(post):   chkconfig

%description
Scribe is a server for aggregating log data streamed in real time from a large
number of servers. It is designed to be scalable, extensible without
client-side modification, and robust to failure of the network or any specific
machine.

%package python
Summary:          Python bindings for %{name}
Group:            Development/Libraries
BuildRequires:    python-devel
Requires:         fb303-python

%description python
Python bindings for %{name}.

%prep
%setup -q
%if %{with_boost_patch}
%patch0 -p1
%endif
%patch1 -p1
%patch2 -p1

%build
./bootstrap.sh %{config_opts}
%configure %{config_opts}
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{__make} DESTDIR=%{buildroot} install

# Install manually
%{__install} -D -m 755 ./examples/scribe_cat %{buildroot}%{_bindir}/scribe_cat
%{__install} -D -m 755 ./examples/scribe_ctrl %{buildroot}%{_bindir}/scribe_ctrl
%{__install} -D -m 755 ./src/libscribe.so %{buildroot}%{_libdir}/libscribe.so
%{__install} -D -m 644 ./examples/example1.conf %{buildroot}%{_sysconfdir}/scribed/default.conf
%{__install} -D -m 755 %{SOURCE1} %{buildroot}%{_sysconfdir}/rc.d/init.d/scribed
%{__install} -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/scribed
%{__install} -D -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/scribe
%{__install} -d -m 755 %{buildroot}%{_localstatedir}/spool/scribed
%{__install} -d -m 755 %{buildroot}%{_localstatedir}/run/scribed

# Remove scripts
%{__rm} ./examples/scribe_*

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE examples/
%config(noreplace) %{_sysconfdir}/scribed/default.conf
%config(noreplace) %{_sysconfdir}/sysconfig/scribed
%config(noreplace) %{_sysconfdir}/logrotate.d/scribe
%{_bindir}/scribed
%{_libdir}/libscribe.so
%{_sysconfdir}/rc.d/init.d/scribed
%{_bindir}/scribe_ctrl
%attr(0750,scribe,scribe) %{_localstatedir}/spool/scribed
%attr(-,scribe,scribe) %{_localstatedir}/run/scribed

%files python
%defattr(-,root,root,-)
%doc LICENSE
%{python_sitelib}/%{name}
%if (0%{?fedora} > 9 || 0%{?rhel} > 5)
%{python_sitelib}/%{name}-*.egg-info
%endif
%{_bindir}/scribe_cat

%pre
getent group scribe >/dev/null || groupadd -r scribe
getent passwd scribe >/dev/null || \
    useradd -r -g scribe -d /var/log -s /sbin/nologin \
    -c "Scribe pseudo-user" scribe
exit 0

%post
/sbin/chkconfig --add scribed

%preun
if [ $1 = 0 ]; then
  /sbin/service scribed stop > /dev/null 2>&1
  /sbin/chkconfig --del scribed
fi

%changelog
* Fri May 13 2011 David Robinson <zxvdr.au@gmail.com> - 2.2-4
- fixed hourly roll period initial filename

* Wed May 11 2011 David Robinson <zxvdr.au@gmail.com> - 2.2-3
- added logrotate config

* Thu May 05 2011 David Robinson <zxvdr.au@gmail.com> - 2.2-2
- added scribe user
- run scribed as non-root user

* Wed Apr 20 2011 David Robinson <zxvdr.au@gmail.com> - 2.2-1
- rebuilt for RHEL 6
- rebuilt for thrift 2.2
- Update to 2.2

* Mon Dec 07 2009 Silas Sewell <silas@sewell.ch> - 2.1-1
- Update to 2.1

* Fri May 01 2009 Silas Sewell <silas@sewell.ch> - 2.0.1-1
- Initial build
