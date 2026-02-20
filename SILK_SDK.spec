#
# Conditional build:
%bcond_with	float		# use FLP flavour instead of FIX (when not ARM/MIPS)
#
%ifarch	%{arm}
%define	flavour	ARM
%else
%ifarch mips mipsel
%define	flavour	MIPS
%else
%define	flavour	%{?with_float:FLP}%{!?with_float:FIX}
%endif
%endif
Summary:	SILK audio codec SDK
Summary(pl.UTF-8):	SDK kodeka dźwięku SILK
Name:		SILK_SDK
Version:	1.0.9
Release:	3
License:	BSD-like
Group:		Libraries
Source0:	http://cdn.dev.skype.com/upload/SILK_SDK_SRC_v%{version}.zip
# Source0-md5:	90b330d48b04fb189a4f524e46d55f8f
URL:		http://dev.skype.com/silk
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains SILK audio codec SDK library.

%description -l pl.UTF-8
Ten pakiet zawiera bibliotekę SDK kodeka dźwięku SILK.

%package devel
Summary:	Header files for SKP SILK SDK library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki SKP SILK SDK
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for SKP SILK SDK library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki SKP SILK SDK.

%package static
Summary:	Static SKP SILK SDK library
Summary(pl.UTF-8):	Statyczna biblioteka SKP SILK SDK
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static SKP SILK SDK library.

%description static -l pl.UTF-8
Statyczna biblioteka SKP SILK SDK.

%prep
%setup -q -c

%build
dir=SILK_SDK_SRC_%{flavour}_v%{version}
%{__make} -j1 -C $dir \
	ADDED_CFLAGS="%{rpmcflags}" \
	CC="libtool --mode=compile --tag=CC %{__cc}" \
	CXX="libtool --mode=compile --tag=CXX %{__cxx}" \
	LDLIBS="$(pwd)/$dir/libSKP_SILK_SDK.la" \
	LINK.o="libtool --mode=link --tag=CC %{__cc}" \
	ARCHIVE.cmdline='libtool --mode=link --tag=CC %{__cc} -rpath %{_libdir} -o $(@:.a=.la) $(^:.o=.lo)'

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_includedir},%{_libdir},%{_bindir}}

dir=SILK_SDK_SRC_%{flavour}_v%{version}
libtool --mode=install install $dir/libSKP_SILK_SDK.la $RPM_BUILD_ROOT%{_libdir}
cp -p $dir/interface/SKP_Silk_*.h $RPM_BUILD_ROOT%{_includedir}
libtool --mode=install install $dir/decoder $RPM_BUILD_ROOT%{_bindir}/silk-decoder
libtool --mode=install install $dir/encoder $RPM_BUILD_ROOT%{_bindir}/silk-encoder

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc SILK_SDK_SRC_%{flavour}_v%{version}/{readme.txt,doc/SILK_Evaluation.pdf}
%attr(755,root,root) %{_bindir}/silk-decoder
%attr(755,root,root) %{_bindir}/silk-encoder
%attr(755,root,root) %{_libdir}/libSKP_SILK_SDK.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libSKP_SILK_SDK.so.0

%files devel
%defattr(644,root,root,755)
%doc SILK_SDK_SRC_%{flavour}_v%{version}/doc/{SILK_RTP_PayloadFormat.pdf,SILK_SDK_API.pdf}
%attr(755,root,root) %{_libdir}/libSKP_SILK_SDK.so
%{_libdir}/libSKP_SILK_SDK.la
%{_includedir}/SKP_Silk_*.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libSKP_SILK_SDK.a
