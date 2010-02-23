%define	libversion	1.4
%define name		mpatrol
%define	release		%mkrel 10
%define	version		1.4.8

%define	major	1
%define libname	%mklibname %{name} %major
%define develname	%mklibname %{name} -d

Summary:	A library for controlling and tracing dynamic memory allocations
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source:		%{name}_%{version}.tar.bz2
URL:		http://mpatrol.sourceforge.net/
License:	LGPL
Group:		System/Libraries
Requires(post):	info-install
Requires(preun):info-install
BuildRequires:	binutils-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The mpatrol library is yet another link library that attempts to
diagnose run-time errors that are caused by the wrong use of
dynamically allocated memory. It acts as a malloc() debugger for
debugging dynamic memory allocations, although it can also trace and
profile calls to malloc() and free() too.

%package -n	%{libname}
Summary:	A library for controlling and tracing dynamic memory allocations
Group:		System/Libraries

%description -n	%{libname}
The mpatrol library is yet another link library that attempts to
diagnose run-time errors that are caused by the wrong use of
dynamically allocated memory. It acts as a malloc() debugger for
debugging dynamic memory allocations, although it can also trace and
profile calls to malloc() and free() too.

%package -n	%{develname}
Summary: 	A library for controlling and tracing dynamic memory allocations
Group:		Development/Other
Requires:	%{libname} >= %{version}
Provides:	%{name}-devel
Obsoletes:	%{mklibname mpatrol 1 -d}

%description -n %{develname}
The mpatrol library is yet another link library that attempts to
diagnose run-time errors that are caused by the wrong use of
dynamically allocated memory. It acts as a malloc() debugger for
debugging dynamic memory allocations, although it can also trace and
profile calls to malloc() and free() too.

%prep
rm -rf $RPM_BUILD_ROOT

%setup -q -n %{name}
touch `find . -type f`

%build
cd build/unix
%make libmpatrol.a libmpatrol.so.%{libversion}
%make libmpatrolmt.a libmpatrolmt.so.%{libversion}
%make libmpalloc.a libmpalloc.so.%{libversion}
%make libmptools.a
%make mpatrol mprof mleak mptrace


%install
%__rm -rf %{buildroot}

%__mv doc/README README.DOC
%__mv man/README README.MAN

#create the dirs
%__mkdir_p %{buildroot}{%{_bindir},%{_libdir},%{_infodir},%{_includedir}/mpatrol}
%__mkdir_p %{buildroot}{%{_mandir}/man{1,3},%{_datadir}/aclocal}

%__install -m755 build/unix/mpatrol %{buildroot}/%{_bindir}
%__install -m755 build/unix/mprof %{buildroot}/%{_bindir}
%__install -m755 build/unix/mptrace %{buildroot}/%{_bindir}
%__install -m755 build/unix/mleak %{buildroot}/%{_bindir}
%__install -m755 bin/mpsym %{buildroot}/%{_bindir}
%__install -m755 bin/mpedit %{buildroot}/%{_bindir}
%__install -m755 bin/hexwords %{buildroot}/%{_bindir}

%__install -m644 src/mpatrol.h %{buildroot}/%{_includedir}
%__install -m644 src/mpalloc.h %{buildroot}/%{_includedir}
%__install -m644 src/mpdebug.h %{buildroot}/%{_includedir}

%__install -m644 tools/*.h %{buildroot}/%{_includedir}/mpatrol
%__install -m644 tools/*.h %{buildroot}/%{_includedir}/mpatrol

%__install -m644 doc/mpatrol.info* %{buildroot}/%{_infodir}

%__install -m755 build/unix/*.so* %{buildroot}/%{_libdir}
%__install -m644 build/unix/*.a* %{buildroot}/%{_libdir}

%__install -m644 man/man1/*.1 %{buildroot}/%{_mandir}/man1
%__install -m644 man/man3/*.3 %{buildroot}/%{_mandir}/man3

%__install -m644 extra/mpatrol.m4 %{buildroot}/%{_datadir}/aclocal

cd %{buildroot}/%{_libdir}

%__ln_s libmpatrol.so.1.4 libmpatrol.so.1
%__ln_s libmpatrol.so.1 libmpatrol.so

%__ln_s libmpatrolmt.so.1.4 libmpatrolmt.so.1
%__ln_s libmpatrolmt.so.1 libmpatrolmt.so

%__ln_s libmpalloc.so.1.4 libmpalloc.so.1
%__ln_s libmpalloc.so.1 libmpalloc.so

#remove unwanted files
rm -rf $RPM_BUILD_ROOT%_libdir/Makefile.aix

%clean
%__rm -rf $RPM_BUILD_ROOT


%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%post
%_install_info %{name}.info*

%preun
%_remove_install_info %{name}.info*

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif


%files
%defattr(-,root,root)
%doc README COPYING COPYING.LIB NEWS ChangeLog
%doc README.DOC README.MAN AUTHORS THANKS
%doc doc/*.ps doc/*.pdf doc/*.txt doc/*.dvi doc/*.tex doc/*.texi
%doc doc/*.html doc/images
%{_bindir}/*
%{_mandir}/man1/*
%{_infodir}/*
%{_datadir}/aclocal/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_mandir}/man3/*

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/*.a
%{_libdir}/*.so
%{_includedir}/mpalloc.h
%{_includedir}/mpatrol.h
%{_includedir}/mpdebug.h
%{_includedir}/mpatrol
