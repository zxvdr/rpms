%if 0%{?fedora} > 11
%global with_java 1
%global with_php 1
%else
%global with_java 0
%global with_php 0
%endif

%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:             fb303
Version:          0.2.0
Release:          1%{?dist}
Summary:          Facebook Bassline

Group:            Development/Libraries
License:          ASL 2.0
URL:              http://incubator.apache.org/thrift
Source0:          http://www.apache.org/dist/incubator/thrift/%{version}-incubating/thrift-%{version}-incubating.tar.gz
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    automake
BuildRequires:    byacc
BuildRequires:    boost-devel >= 1.33.1
BuildRequires:    flex
BuildRequires:    libevent-devel
BuildRequires:    libtool
BuildRequires:    thrift = %{version}
BuildRequires:    thrift-cpp-devel = %{version}
BuildRequires:    zlib-devel

%description
Facebook Baseline is a standard interface to monitoring, dynamic options and
configuration, uptime reports, activity, and more.

%package devel
Summary:          Development files for %{name}
Group:            Development/Libraries
Requires:         %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%if %{with_java}
%package java
Summary:          Java bindings for %{name}
Group:            Development/Libraries
BuildRequires:    ant 
BuildRequires:    java-1.6.0-openjdk-devel
BuildRequires:    jpackage-utils
BuildRequires:    thrift-java = %{version}
Requires:         java-1.6.0-openjdk
Requires:         thrift-java = %{version}

%description java
Java bindings for %{name}.
%endif

%package python
Summary:          Python bindings for %{name}
Group:            Development/Libraries
BuildRequires:    python-devel
Requires:         thrift-python = %{version}

%description python
Python bindings for %{name}.

%if %{with_php}
%package php
Summary:          PHP bindings for %{name}
Group:            Development/Libraries
BuildRequires:    php-devel
Requires:         thrift-php = %{version}

%description php
PHP bindings for %{name}.
%endif

%prep
%setup -q -n thrift-%{version}
cd ./contrib/fb303

# Fix non-executable-script error
sed -i '/^#!\/usr\/bin\/env python/,+1 d' \
  py/fb303_scripts/*.py \
  py/fb303/FacebookBase.py

%build
cd ./contrib/fb303
./bootstrap.sh
%configure --enable-static=no --with-thriftpath=%{_prefix}
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
cd ./contrib/fb303

# Fix install path
sed -i 's/shareddir = lib/shareddir = ${prefix}\/lib/g' cpp/Makefile

%{__make} DESTDIR=%{buildroot} install

# Install Java
%if %{with_java}
pushd java/
ant install -Dthrift_home=%{_prefix} -Ddist.dir=%{buildroot}%{_prefix} -Ddist.lib.dir=%{buildroot}%{_javadir} -lib %{_javadir} -lib %{_javadir}/slf4j -Dnoivy=
popd
%endif

# Install PHP
%if %{with_php}
%{__mkdir_p} %{buildroot}%{_datadir}/php/%{name}
%{__cp} -r php/FacebookBase.php %{buildroot}%{_datadir}/php/%{name}/
%endif

# Fix lib install path on x86_64
%{__mv} %{buildroot}/usr/lib/libfb303.so %{buildroot}%{_libdir}/libfb303.so || true

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README
%{_datadir}/fb303
%{_libdir}/*.so

%files devel
%defattr(-,root,root,-)
%doc README
%{_includedir}/thrift/fb303
#%{_libdir}/*.so

%if %{with_java}
%files java
%defattr(-,root,root,-)
%doc README
%{_javadir}/libfb303.jar
%endif

%if %{with_php}
%files php
%defattr(-,root,root,-)
%doc README
%{_datadir}/php/%{name}
%endif

%files python
%defattr(-,root,root,-)
%doc README
%{python_sitelib}/%{name}
%{python_sitelib}/%{name}_scripts
%if 0%{?fedora}  > 9
%{python_sitelib}/%{name}-*.egg-info
%endif

%changelog
* Wed Mar 03 2010 Silas Sewell <silas@sewell.ch> - 0.2.0-1
- Update to non-snapshot release

* Wed Dec 09 2009 Silas Sewell <silas@sewell.ch> - 0.2-0.4.20091117svn835538
- Tweaks for EL compatibility

* Tue Nov 17 2009 Silas Sewell <silas@sewell.ch> - 0.2-0.3.20091117svn835538
- Update to thrift snapshot

* Tue Jul 21 2009 Silas Sewell <silas@sewell.ch> - 0.2-0.2.20090721svn795861
- Update to latest snapshot

* Fri May 01 2009 Silas Sewell <silas@sewell.ch> - 0.2-0.1.20090501svn770888
- Initial build
