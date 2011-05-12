%if 0%{?fedora} > 12
%global with_csharp 0
%global with_ghc 1
%global with_java 1
%global with_php 1
%else
%global with_csharp 0
%global with_ghc 0
%global with_java 0
%global with_php 0
%endif

# Erlang
%global erlangdir %{_libdir}/erlang

# Haskell
%global pkg_name Thrift
%global ghc_pkg_deps ghc-HTTP-devel, ghc-binary-devel, ghc-network-devel, ghc-xhtml-devel

%bcond_without doc
%bcond_without prof
%bcond_without shared

# Python
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

# Fix private-shared-object-provides error
%{?filter_setup:
%filter_provides_in %{python_sitearch}.*\.so$
%filter_setup
}

# Ruby
%{!?ruby_sitelib: %global ruby_sitelib %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")}
%{!?ruby_sitearch: %global ruby_sitearch %(ruby -rrbconfig -e "puts Config::CONFIG['sitearchdir']")}

Name:             thrift
Version:          0.5.0
Release:          1%{?dist}
Summary:          A multi-language RPC and serialization framework

Group:            System Environment/Libraries
License:          ASL 2.0
URL:              http://incubator.apache.org/thrift
Source0:          http://www.apache.org/dist//incubator/thrift/%{version}-incubating/thrift-%{version}.tar.gz
Source1:          thrift_protocol.ini
Patch0:           thrift-0.5.0-noivy.patch
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    byacc
BuildRequires:    boost-devel >= 1.33.1
BuildRequires:    dos2unix
BuildRequires:    flex
BuildRequires:    libevent-devel
BuildRequires:    libtool
BuildRequires:    mono-devel >= 1.2.6
BuildRequires:    zlib-devel

%description
Thrift is a software framework for scalable cross-language services
development. It combines a powerful software stack with a code generation
engine to build services that work efficiently and seamlessly between C++,
Java, C#, Python, Ruby, Perl, PHP, Objective C/Cocoa, Smalltalk, Erlang,
Objective Caml, and Haskell.

%package cpp
Summary:          Libraries for %{name}
Group:            Development/Libraries

%description cpp
Libraries bindings for %{name}.

%package cpp-devel
Summary:          Development files for %{name}
Group:            Development/Libraries
Requires:         %{name}-cpp = %{version}-%{release}

%description cpp-devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%if 0%{?with_csharp}
%package csharp
Summary:          C# bindings for %{name}
Group:            Development/Libraries
# sparc64 doesn't have mono
ExcludeArch:      sparc64

%description csharp
C# bindings for %{name}.
%endif

%package erlang
Summary:          Erlang bindings for %{name}
Group:            Development/Libraries
BuildRequires:    erlang

%description erlang
Erlang bindings for %{name}.

%if 0%{?with_ghc}
%package ghc
Version:          0.2.0
Summary:          Haskell bindings for %{name}
Group:            Development/Libraries
ExclusiveArch:    %{ix86} x86_64 ppc alpha
BuildRequires:    cabal-install
BuildRequires:    ghc
BuildRequires:    ghc-prof
BuildRequires:    haddock
BuildRequires:    ghc-rpm-macros
%{?ghc_pkg_deps:BuildRequires:  %{ghc_pkg_deps}, %(echo %{ghc_pkg_deps} | sed -e "s/\(ghc-[^, ]\+\)-devel/\1-doc,\1-prof/g")}

%description ghc
Haskell bindings for %{name}.

%package ghc-devel
Version:          0.2.0
Summary:          Haskell %{pkg_name} library
Group:            Development/Libraries
Requires:         ghc
Requires(post):   ghc
Requires(preun):  ghc

%description ghc-devel
This package contains the development files for %{name}-ghc-devel
built for ghc.

%if %{with doc}
%package ghc-doc
Version:          0.2.0
Summary:          Documentation for %{name}-ghc
Group:            Development/Libraries
BuildRequires:    ghc-doc
Requires:         ghc-doc
Requires(post):   ghc-doc
Requires(postun): ghc-doc

%description ghc-doc
This package contains development documentation files for the %{name}-ghc
library.
%endif

%if %{with prof}
%package ghc-prof
Version:          0.2.0
Summary:          Profiling libraries for %{name}-ghc
Group:            Development/Libraries
BuildRequires:    ghc-prof
Requires:         %{name}-ghc = %{version}-%{release}
Requires:         ghc-prof

%description ghc-prof
This package contains profiling libraries for %{name}-ghc
built for ghc.
%endif
%endif

%if %{with_java}
%package java
Summary:          Java bindings for %{name}
Group:            Development/Libraries
BuildRequires:    ant
BuildRequires:    jakarta-commons-lang
BuildRequires:    java-1.6.0-openjdk-devel
BuildRequires:    slf4j
BuildRequires:    tomcat5-servlet-2.4-api
Requires:         jakarta-commons-lang
Requires:         java-1.6.0-openjdk
Requires:         slf4j
Requires:         tomcat5-servlet-2.4-api

%description java
Java bindings for %{name}.

%package javadoc
Summary:          Javadoc for %{name}-java
Group:            Documentation
BuildRequires:    java-1.6.0-openjdk-javadoc

%description javadoc
Javadoc for %{name}.
%endif

%package perl
Summary:          Perl bindings for %{name}
Group:            Development/Libraries
%if 0%{?fedora} > 6
BuildRequires:    perl-devel
%else
BuildRequires:    perl
%endif
Requires:         perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:         perl(Bit::Vector)
Requires:         perl(Class::Accessor)
Provides:         perl(Thrift) = %{version}-%{release}

%description perl
Perl bindings for %{name}.

%if 0%{?with_php}
%package php
Summary:          PHP bindings for %{name}
Group:            Development/Libraries
BuildRequires:    php-devel
%if 0%{?php_zend_api}
BuildRequires:    php-devel
Requires:         php(zend-abi) = %{php_zend_api}
Requires:         php(api) = %{php_core_api}
%endif

%description php
PHP bindings for %{name}.
%endif

%package python
Summary:          Python bindings for %{name}
Group:            Development/Libraries
BuildRequires:    python-devel

%description python
Python bindings for %{name}.

%package ruby
Summary:          Ruby bindings for %{name}
Group:            Development/Libraries
BuildRequires:    ruby
BuildRequires:    ruby-devel
Requires:         ruby(abi) = 1.8

%description ruby
Ruby bindings for %{name}.

%prep
%setup -q
%patch0 -p1

# Fix spurious-executable-perm warning
find tutorial/ -type f -exec chmod 0644 {} \;

# Haskell setup script won't run with blank or comment lines
sed -i '/#/d;/^$/d' lib/hs/Setup.lhs

%build
%configure \
  --without-haskell \
  --without-java \
  --without-perl \
  --without-php \
  --without-ruby \
  --enable-static=no
%{__make} %{?_smp_mflags}

# Build Haskell
%if 0%{?with_ghc}
pushd lib/hs
%ghc_lib_build
popd
%endif

%if 0%{?with_java}
# Build Java
pushd lib/java
ant dist javadoc -lib %{_javadir} -lib %{_javadir}/slf4j -Dnoivy=1
popd
%endif

# Build Perl
pushd lib/perl
perl Makefile.PL
%{__make} %{?_smp_mflags} CFLAGS="%{optflags}"
popd

# Build PHP
%if 0%{?with_php}
pushd lib/php/src/ext/thrift_protocol
phpize
%configure
%{__make} %{?_smp_mflags}
popd
%endif

# Build Ruby
pushd lib/rb
ruby setup.rb config
ruby setup.rb setup
popd

%install
%{__rm} -rf %{buildroot}

# Install everything not listed below
%{__make} DESTDIR=%{buildroot} install
# Remove "la" files
find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'

# Fix non-standard-executable-perm
%{__chmod} 0755 %{buildroot}%{python_sitearch}/%{name}/protocol/fastbinary.so

%if 0%{?with_csharp}
# Install C#
%{__mkdir_p} %{buildroot}%{_libdir}/mono/gac/
gacutil -i lib/csharp/Thrift.dll -f -package Thrift -root %{buildroot}%{_libdir}
%endif

# Install Haskell
%if 0%{?with_ghc}
pushd lib/hs
%ghc_lib_install
popd
%endif

# Install Java
%if 0%{?with_java}
pushd lib/java
%{__mkdir_p} %{buildroot}%{_javadir}
%{__cp} -p libthrift.jar %{buildroot}%{_javadir}
%{__mkdir_p} %{buildroot}%{_javadocdir}
%{__cp} -rp build/javadoc/org/apache/thrift %{buildroot}%{_javadocdir}
popd
%endif

# Install PHP
%if 0%{?with_php}
pushd lib/php/src/ext/thrift_protocol
%{__make} INSTALL_ROOT=%{buildroot} install
popd
# Install PHP INI
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.d
%{__cp} %{SOURCE1} %{buildroot}%{_sysconfdir}/php.d/
# Install PHP project files
%{__mkdir_p} %{buildroot}%{_datadir}/php/%{name}
%{__cp} -r lib/php/src/Thrift.php \
           lib/php/src/protocol \
           lib/php/src/transport \
           %{buildroot}%{_datadir}/php/%{name}/
%endif

# Install Perl
pushd lib/perl
%{__make} DESTDIR=%{buildroot} INSTALLSITELIB=%{perl_vendorlib} install
popd

# Cleanup Perl install
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -type f -name perllocal.pod -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

# Install Ruby
pushd lib/rb
ruby setup.rb install --prefix=%{buildroot}
popd

# Fix non-standard-executable-perm error
%{__chmod} 0755 %{buildroot}%{ruby_sitearch}/thrift_native.so

%clean
%{__rm} -rf %{buildroot}

%post cpp -p /sbin/ldconfig

%postun cpp -p /sbin/ldconfig

%if %{with_ghc}
%post ghc-devel
%ghc_register_pkg

%if %{with doc}
%post ghc-doc
%ghc_reindex_haddock
%endif

%preun ghc-devel
if [ "$1" -eq 0 ]; then
%ghc_unregister_pkg
fi

%if %{with doc}
%postun ghc-doc
if [ "$1" -eq 0 ]; then
%ghc_reindex_haddock
fi
%endif
%endif

%files
%defattr(-,root,root,-)
%doc CHANGES CONTRIBUTORS LICENSE NEWS NOTICE README doc/
%{_bindir}/thrift

%files cpp
%defattr(-,root,root,-)
%doc LICENSE
%{_libdir}/*.so.*

%files cpp-devel
%defattr(-,root,root,-)
%doc tutorial/README tutorial/cpp tutorial/*.thrift
%{_includedir}/thrift
%{_libdir}/*.so
%{_libdir}/pkgconfig/thrift*

%if 0%{?with_csharp}
%files csharp
%defattr(-,root,root,-)
%doc lib/csharp/README tutorial/csharp
%{_libdir}/mono/gac/Thrift
%{_libdir}/mono/thrift
%endif

%files erlang
%defattr(-,root,root,-)
%doc lib/erl/README tutorial/erl tutorial/*.thrift
%{erlangdir}/lib/%{name}-%{version}

%if 0%{?with_ghc}
%files ghc -f lib/hs/ghc-Thrift.files
%defattr(-,root,root,-)
%doc lib/hs/README lib/hs/TODO

%files ghc-devel -f lib/hs/ghc-Thrift-devel.files

%if %{with doc}
%files ghc-doc -f lib/hs/ghc-Thrift-doc.files
%endif

%if %{with prof}
%files ghc-prof -f lib/hs/ghc-Thrift-prof.files
%endif
%endif

%if 0%{?with_java}
%files java
%defattr(-,root,root,-)
%doc lib/java/README tutorial/java tutorial/*.thrift
%{_javadir}/libthrift.jar

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/thrift
%endif

%files perl
%defattr(-,root,root,-)
%doc lib/perl/README tutorial/perl tutorial/*.thrift
%{perl_vendorlib}/Thrift*

%if 0%{?with_php}
%files php
%defattr(-,root,root,-)
%doc lib/php/README lib/php/README.apache tutorial/php tutorial/*.thrift
%config(noreplace) %{_sysconfdir}/php.d/thrift_protocol.ini
%{_datadir}/php/%{name}
%{php_extdir}/thrift_protocol.so
%endif

%files python
%defattr(-,root,root,-)
%doc lib/py/README tutorial/py tutorial/*.thrift
%{python_sitearch}/%{name}
%if 0%{?fedora}  > 9
%{python_sitearch}/Thrift-*.egg-info
%endif

%files ruby
%defattr(-,root,root,-)
%doc lib/rb/CHANGELOG lib/rb/README tutorial/rb tutorial/*.thrift
%{ruby_sitearch}/thrift_native.so
%{ruby_sitelib}/thrift*

%changelog
* Tue Nov 02 2010 Silas Sewell <silas@sewell.ch> - 0.5.0-1
- Update to 0.5.0

* Mon Mar 01 2010 Silas Sewell <silas@sewell.ch> - 0.2.0-1
- Update to non-snapshot release
- Various tweaks for release package
- Add flag for csharp build

* Thu Jan 07 2010 Silas Sewell <silas@sewell.ch> - 0.2-0.6.20091112svn835538
- Disable ghc until rawhide is fixed

* Thu Jan 07 2010 Silas Sewell <silas@sewell.ch> - 0.2-0.5.20091112svn835538
- Add ghc-network-prof and ghc-network-devel dependencies

* Tue Dec 08 2009 Silas Sewell <silas@sewell.ch> - 0.2-0.4.20091112svn835538
- Tweaks for EL compatibility

* Thu Nov 12 2009 Silas Sewell <silas@sewell.ch> - 0.2-0.3.20091112svn835538
- Update to latest snapshot

* Mon Jul 20 2009 Silas Sewell <silas@sewell.ch> - 0.2-0.2.20090720svn795861
- Update to latest snapshot

* Mon May 25 2009 Silas Sewell <silas@sewell.ch> - 0.2-0.1.20090525svn777690
- Update to latest snapshot
- Fix version, release syntax and perl requires

* Wed May 06 2009 Silas Sewell <silas@sewell.ch> - 0.0-0.1.20090505svn770888
- Fix various require issues
- Change lib to cpp and devel to cpp-devel
- Use ghc version macro
- Add documentation to language specific libraries

* Fri May 01 2009 Silas Sewell <silas@sewell.ch> - 0.0-0.0.20090501svn770888
- Initial build
