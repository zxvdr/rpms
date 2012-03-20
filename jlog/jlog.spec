Name: jlog
Version: 1.1
Release: 1%{?dist}
Summary: Journaled Log (JLog)

Group: Development/Libraries
License: BSD
URL: https://labs.omniti.com/labs/jlog

# git svn clone https://labs.omniti.com/jlog/ -T trunk -b branches -t tags
# cd jlog
# git archive --format=tar --prefix=jlog-1.1/ HEAD | gzip >jlog-1.1.tar.gz
#
# or
#
# wget https://labs.omniti.com/labs/jlog/changeset/52/tags/1.1?old_path=%2F&format=zip
Source0: jlog-1.1.tar.gz
Patch0: rpath.patch
Patch1: perl.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: perl-ExtUtils-MakeMaker

%package devel
Summary: Libraries, includes, etc to develop with JLog
Requires: %{name} = %{version}-%{release}

%package perl
Summary: Perl bindings for JLog
Requires: %{name} = %{version}-%{release}

%description
JLog is short for "journaled log" and this package is
really an API and implementation that is libjlog. What
is libjlog? libjlog is a pure C, very simple durable
message queue with multiple subscribers and publishers
(both thread and multi-process safe).

%description devel
JLog is short for "journaled log" and this package is
really an API and implementation that is libjlog. What
is libjlog? libjlog is a pure C, very simple durable
message queue with multiple subscribers and publishers
(both thread and multi-process safe).

This sub-package provides the libraries and includes
necessary for developing against the JLog library.

%description perl
JLog is short for "journaled log" and this package is
really an API and implementation that is libjlog. What
is libjlog? libjlog is a pure C, very simple durable
message queue with multiple subscribers and publishers
(both thread and multi-process safe).

This sub-package provides Perl bindings for the JLog
library.

%prep
%setup -q -n jlog-1.1
%patch0 -p1
%patch1 -p1

%build
autoconf
%configure --disable-static
make


%install
make install DESTDIR=$RPM_BUILD_ROOT
#rm -rf $RPM_BUILD_ROOT/%{_libdir}/perl5
#rm -rf $RPM_BUILD_ROOT//usr/share/man/man3


%check
./jthreadtest safety safe

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc LICENSE
%{_bindir}/jlogctl
%{_bindir}/jlog_change_endian
%{_bindir}/jlog_sanity_check
#%{_libdir}/libjlog.so.1
#%{_libdir}/libjlog.so.1.*

%files devel
%defattr(-,root,root,-)
%doc LICENSE
%{_includedir}/jlog.h
%{_includedir}/jlog_config.h
%{_libdir}/libjlog.a
%{_libdir}/libjlog.so

%files perl
%defattr(-,root,root,-)
%{perl_archlib}/perllocal.pod
%{perl_vendorarch}/JLog.pm
%{perl_vendorarch}/JLog/Reader.pm
%{perl_vendorarch}/JLog/Writer.pm
%{perl_vendorarch}/auto/JLog/.packlist
%{perl_vendorarch}/auto/JLog/JLog.bs
%{perl_vendorarch}/auto/JLog/JLog.so
%{_mandir}/man3/JLog.3pm.gz
%{_mandir}/man3/JLog::Reader.3pm.gz
%{_mandir}/man3/JLog::Writer.3pm.gz

%changelog
* Sat Jul 16 2011 David Robinson <zxvdr.au@gmail.com> - 1.1-1
- Initial Fedora package
