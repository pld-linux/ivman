Summary:	An extremely flexible desktop independent frontend to HAL
Summary(pl):	Wysoce konfigurowalny, niezale¿ny od zarz±dcy okien frontend do HAL
Name:		ivman
Version:	0.6.5
Release:	1
License:	QPL
Group:		Daemons
Source0:	http://dl.sourceforge.net/ivman/%{name}-%{version}.tar.bz2
# Source0-md5:	0d83d1d5df716c120de201d5cf3e6e9b
Source1:	%{name}.init
URL:		http://ivman.sourceforge.net
BuildRequires:	dbus-devel >= 0.34
BuildRequires:	dbus-glib-devel >= 0.3
BuildRequires:	glib2-devel >= 2.6
BuildRequires:	hal-devel >= 0.4
BuildRequires:	libxml2-devel >= 2.6.17
Requires(post,preun):	/sbin/chkconfig
Requires(pre):  /bin/id
Requires(pre):  /usr/bin/getgid
Requires(pre):  /usr/sbin/useradd
Requires(pre):  /usr/sbin/groupadd
Requires(postun):	/usr/sbin/userdel
Requires(postun):	/usr/sbin/groupdel
Requires:	hal >= 0.4
Requires:	rc-scripts >= 0.2.0
Provides:	user(ivman)
Provides:	group(plugdev)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Ivman is an extremely flexible desktop independent frontend to HAL,
the userspace Hardware Abstraction Layer for Linux. It can be used to
execute arbitrary commands when devices are added to or removed from
your system, when device properties change, or when devices emit
conditions. Any properties of the new or changed device can be
included within the executed command.

%description -l pl
Ivman jest wysoce konfigurowalnym frontendem do HAL (Hardware
Abstraction Layer). Mo¿e byæ u¿ywany do wykonywania poleceñ podczas
dodawania, usuwania urz±dzeñ, zmiany ich w³a¶ciwo¶ci b±d¼ te¿ w
odpowiedzi na komunikaty pochodz±ce od urz±dzeñ. Wszelkie w³a¶ciwo¶ci
urz±dzenia mog± byæ wykorzystane w wykonywanym poleceniu.

%package devel
Summary:	Development files for ivman
Summary(pl):	Pliki niezbêdne programistom u¿ywaj±cym ivmana
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	dbus-glib-devel >= 0.3
Requires:	glib2-devel >= 2.6
Requires:	hal-devel >= 0.4
Requires:	libxml2-devel >= 2.6.17

%description devel
Ivman is an extremely flexible desktop independent frontend to HAL,
the userspace Hardware Abstraction Layer for Linux. It can be used to
execute arbitrary commands when devices are added to or removed from
your system, when device properties change, or when devices emit
conditions. Any properties of the new or changed device can be
included within the executed command. This package contains files
needed for development.

%description devel -l pl
Ivman jest wysoce konfigurowalnym frontendem do HAL (Hardware
Abstraction Layer). Mo¿e byæ u¿ywany do wykonywania poleceñ podczas
dodawania, usuwania urz±dzeñ, zmiany ich w³a¶ciwo¶ci b±d¼ te¿ w
odpowiedzi na komunikaty pochodz±ce od urz±dzeñ. Wszelkie w³a¶ciwo¶ci
urz±dzenia mog± byæ wykorzystane w wykonywanym poleceniu. Ten pakiet
zawiera pliki niezbêdne programistom.

%package static
Summary:	Static libraries for ivman
Summary(pl):	Biblioteki statyczne ivman
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Ivman is an extremely flexible desktop independent frontend to HAL,
the userspace Hardware Abstraction Layer for Linux. It can be used to
execute arbitrary commands when devices are added to or removed from
your system, when device properties change, or when devices emit
conditions. Any properties of the new or changed device can be
included within the executed command. This package contains static
libraries.

%description static -l pl
Ivman jest wysoce konfigurowalnym frontendem do HAL (Hardware
Abstraction Layer). Mo¿e byæ u¿ywany do wykonywania poleceñ podczas
dodawania, usuwania urz±dzeñ, zmiany ich w³a¶ciwo¶ci b±d¼ te¿ w
odpowiedzi na komunikaty pochodz±ce od urz±dzeñ. Wszelkie w³a¶ciwo¶ci
urz±dzenia mog± byæ wykorzystane w wykonywanym poleceniu. Ten pakiet
zawiera biblioteki statyczne.

%prep
%setup -q

%build
%configure

%{__make} \
	OPTFLAGS="%{rpmcflags}" \
	CC="%{__cc}" \
	bindir=%{_bindir} \
	datadir=%{_datadir} \
	sysconfdir=%{_sysconfdir}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	bindir=%{_bindir} \
	datadir=%{_datadir} \
	sysconfdir=%{_sysconfdir}

install -D %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/ivman

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 211 plugdev
%useradd -u 211 -d /usr/share/empty -s /bin/false -c "ivman daemon" -g plugdev ivman

%post
/sbin/ldconfig
/sbin/chkconfig --add ivman
%service ivman restart

%preun
if [ "$1" = "0" ]; then
	%service -q ivman stop
	/sbin/chkconfig --del ivman
fi

%postun
/sbin/ldconfig
if [ "$1" = "0" ]; then
	%userremove ivman
	%groupremove plugdev
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog README TODO
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ivman/*
%attr(754,root,root) /etc/rc.d/init.d/*
%attr(755,root,root) %{_bindir}/ivman
%attr(755,root,root) %{_libdir}/libIvmConfig.so.*.*.*
%{_mandir}/man5/*.5*
%{_mandir}/man8/*.8*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libIvmConfig.so
%{_libdir}/libIvmConfig.la

%files static
%defattr(644,root,root,755)
%{_libdir}/libIvmConfig.a
