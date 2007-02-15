Summary:	Kernel GNU C Compiler
Summary(pl.UTF-8):	Kompilator GNU C dla jądra
Name:		kgcc
Version:	3.2.2
Release:	2
License:	GPL
Group:		Development/Languages
Source0:	ftp://gcc.gnu.org/pub/gcc/releases/gcc-%{version}/gcc-%{version}.tar.bz2
# Source0-md5:	962a2057a2572226bc99aaeba4255e9b
URL:		http://gcc.gnu.org/
BuildRequires:	bison
Requires:	binutils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Kernel GNU C Compiler.

%description -l pl.UTF-8
Kompilator GNU C dla jądra.

%prep
%setup -q -n gcc-%{version}

%build
#rm -rf gcc/{cp,f,objc}
#rm -rf lib{f2c,io}
#rm -rf texinfo

rm -rf obj-%{_target_platform}
install -d obj-%{_target_platform} && cd obj-%{_target_platform}

CFLAGS="%{rpmcflags}" \
CXXFLAGS="%{rpmcflags}" \
../configure \
	--prefix=%{_prefix} \
	--infodir=%{_infodir} \
	--enable-shared \
	--enable-threads=posix \
	--enable-languages="c" \
	--with-gnu-as \
	--with-gnu-ld \
	--with-system-zlib \
	--without-x \
	%{_target_platform}

PATH=$PATH:/sbin:%{_sbindir}
touch  ../gcc/c-gperf.h

%{__make} \
	bootstrap-lean

%install
rm -rf $RPM_BUILD_ROOT

cd obj-%{_target_platform}
PATH=$PATH:/sbin:%{_sbindir}

%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	infodir=$RPM_BUILD_ROOT%{_prefix}

mv -f $RPM_BUILD_ROOT%{_bindir}/gcc $RPM_BUILD_ROOT%{_bindir}/kgcc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{_libdir}/gcc-lib/%{_target_cpu}*/*
%dir %{_libdir}/gcc-lib/%{_target_cpu}*/*/include

%attr(755,root,root) %{_bindir}/kgcc
%attr(755,root,root) %{_libdir}/gcc-lib/%{_target_cpu}*/*/cc1
%attr(755,root,root) %{_libdir}/gcc-lib/%{_target_cpu}*/*/*cpp*
%attr(755,root,root) %{_libdir}/gcc-lib/%{_target_cpu}*/*/collect2
%{_libdir}/gcc-lib/%{_target_cpu}*/*/libgcc*
%{_libdir}/gcc-lib/%{_target_cpu}*/*/specs

%ifnarch alpha
%attr(755,root,root) %{_libdir}/gcc-lib/%{_target_cpu}*/*/*.o
%endif

%{_libdir}/gcc-lib/%{_target_cpu}*/*/include/*.h
