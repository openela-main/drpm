# Do not build with zstd for RHEL < 8
%if (0%{?rhel} && 0%{?rhel} < 8) || (0%{?suse_version} && 0%{?suse_version} < 1500)
%bcond_with zstd
%else
%bcond_without zstd
%endif

Name:           drpm
Version:        0.4.1
Release:        3%{?dist}
Summary:        A library for making, reading and applying deltarpm packages
# the entire source code is LGPLv2+, except src/drpm_diff.c and src/drpm_search.c which are BSD
License:        LGPLv2+ and BSD
URL:            https://github.com/rpm-software-management/%{name}
Source:         %{url}/releases/download/%{version}/%{name}-%{version}.tar.bz2

# add workaround for gcc7 on ppc64le temporary before it's fixed in gcc
# https://bugzilla.redhat.com/show_bug.cgi?id=1420350
Patch1:         drpm-0.3.0-workaround-ppc64le-gcc.patch
Patch2:         Fix-a-memory-leak-on-invalid-input.patch

BuildRequires:  cmake >= 2.8.5
BuildRequires:  gcc

BuildRequires:  rpm-devel
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel
BuildRequires:  bzip2-devel
BuildRequires:  xz-devel
%if %{with zstd}
BuildRequires:  pkgconfig(libzstd)
%endif

BuildRequires:  pkgconfig
BuildRequires:  doxygen

BuildRequires:  libcmocka-devel >= 1.0
%ifarch %{valgrind_arches}
BuildRequires:  valgrind
%endif

%description
The drpm package provides a library for making, reading and applying deltarpms,
compatible with the original deltarpm packages.

%package devel
Summary:        C interface for the drpm library
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The drpm-devel package provides a C interface (drpm.h) for the drpm library.

%prep
%autosetup -p1
mkdir build

%build
pushd build
%cmake .. -DWITH_ZSTD:BOOL=%{?with_zstd:ON}%{!?with_zstd:OFF} -DHAVE_LZLIB_DEVEL:BOOL=%{?suse_version:ON}%{!?suse_version:OFF} 
%make_build
make doc
popd

%install
pushd build
%make_install
popd

%check
pushd build
ctest -VV
popd

%if (0%{?rhel} && 0%{?rhel} < 8) || 0%{?suse_version}
%ldconfig_scriptlets
%endif

%files
%license COPYING LICENSE.BSD
%{_libdir}/libdrpm.so.*

%files devel
%doc build/doc/html/
%{_libdir}/libdrpm.so
%{_includedir}/drpm.h
%{_libdir}/pkgconfig/drpm.pc

%changelog
* Tue Aug 11 2020 Nicola Sella <nsella@redhat.com> - 0.4.1-3
- Fix a memory leak on invalid input (RhBug:1866786)

* Tue Jun 02 2020 Ales Matej <amatej@gmail.com> 0.4.1-2
- Rebuild with zstd support (RhBug:1842036)

* Wed Oct 23 2019 Ales Matej <amatej@gmail.com> 0.4.1-1
- Update to 0.4.1
- Relicense to LGPLv2+
- Fix number of bugs mainly with drpm_make and drpm_apply
- Add support for zstd drpms
- CMake cleanups
- Make running tests optional
- Small spec improvements

* Fri Aug  3 2018 Florian Weimer <fweimer@redhat.com> - 0.3.0-14
- Honor %%{valgrind_arches}

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.3.0-12
- Switch to %%ldconfig_scriptlets

* Fri Aug 11 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.3.0-11
- Rebuilt after RPM update (№ 3)

* Thu Aug 10 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.3.0-10
- Rebuilt for RPM soname bump

* Thu Aug 10 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.3.0-9
- Rebuilt for RPM soname bump

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Apr 13 2017 Than Ngo <than@redhat.com> - 0.3.0-6
- updated workaround patch

* Tue Mar 28 2017 Than Ngo <than@redhat.com> - 0.3.0-5
- added workaround for gcc7 bug on ppc64le temporary

* Thu Sep 29 2016 Pete Walter <pwalter@fedoraproject.org> - 0.3.0-4
- Simplify spec file

* Tue May 3 2016 Matej Chalk <mchalk@redhat.com> 0.3.0-3
- Now contains makedeltarpm and applydeltarpm functionality
- Added lzlib-devel dependency for OpenSUSE

* Tue Apr 12 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.3.0-2
- Cleanup spec
- Make build out-of-tree
- Sync with valgrind arches
- Build documentation

* Thu Sep 3 2015 Matej Chalk <mchalk@redhat.com> 0.3.0-1
- Bumped minor version (deltarpm creation added)

* Tue Aug 4 2015 Matej Chalk <mchalk@redhat.com> 0.2.1-1
- Added openssl dependency

* Fri Jul 24 2015 Matej Chalk <mchalk@redhat.com> 0.2.0-2
- Fixed bug in test suite

* Tue Jun 23 2015 Matej Chalk <mchalk@redhat.com> 0.2.0-1
- Bumped minor version

* Fri Jun 19 2015 Matej Chalk <mchalk@redhat.com> 0.1.3-4
- Memory test only for architectures that have valgrind (#1232157)

* Wed Mar 11 2015 Matej Chalk <mchalk@redhat.com> 0.1.3-3
- Added cmocka and valgrind package dependencies

* Fri Mar 6 2015 Matej Chalk <mchalk@redhat.com> 0.1.3-2
- Added check section

* Fri Feb 13 2015 Matej Chalk <mchalk@redhat.com> 0.1.3-1
- Bumped version to 0.1.3
- Added CMake tool

* Fri Dec 19 2014 Matej Chalk <mchalk@redhat.com> 0.1.2-4
- Enabled hardened build

* Mon Dec 15 2014 Matej Chalk <mchalk@redhat.com> 0.1.2-3
- Added unversioned .so to package to enable linking with -ldrpm

* Thu Dec 11 2014 Matej Chalk <mchalk@redhat.com> 0.1.2-2
- Removed unversioned .so from package
- Included copies of both GPLv3 and LGPLv3

* Wed Dec 3 2014 Matej Chalk <mchalk@redhat.com> 0.1.2-1
- Bumped version to 0.1.2
- Added drpm.pc file for pkgconfig tool

* Thu Nov 6 2014 Matej Chalk <mchalk@redhat.com> 0.1.1-1
- Bumped version to 0.1.1

* Wed Nov 5 2014 Matej Chalk <mchalk@redhat.com> 0.1.0-1
- Initial RPM release
