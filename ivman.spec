Summary:	An extremely flexible desktop independent frontend to HAL
Summary(pl):	Wysoce konfigurowalny, niezale¿ny od zarz±dcy okien frontend do HAL
Name:		ivman
Version:	0.6.10
Release:	1
License:	QPL
Group:		Daemons
Source0:	http://dl.sourceforge.net/ivman/%{name}-%{version}.tar.bz2
# Source0-md5:	b21a844ff549613831e033d1e21238ea
Source1:	%{name}.init
URL:		http://ivman.sourceforge.net
BuildRequires:	dbus-devel >= 0.34
BuildRequires:	dbus-glib-devel >= 0.3
BuildRequires:	glib2-devel >= 2.6
BuildRequires:	hal-devel >= 0.4
BuildRequires:	libxml2-devel >= 2.6.17
BuildRequires:	pkgconfig
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
Obsoletes:	ivman-devel
Obsoletes:	ivman-static
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

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 211 plugdev
%useradd -u 211 -d /usr/share/empty -s /bin/false -c "ivman daemon" -g plugdev ivman

%post
/sbin/chkconfig --add ivman
%service ivman restart

%preun
if [ "$1" = "0" ]; then
	%service -q ivman stop
	/sbin/chkconfig --del ivman
fi

%postun
if [ "$1" = "0" ]; then
	%userremove ivman
	%groupremove plugdev
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog README TODO
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ivman/*
%attr(754,root,root) /etc/rc.d/init.d/*
%attr(755,root,root) %{_bindir}/ivman
%attr(755,root,root) %{_bindir}/ivman-launch
%{_mandir}/man5/*.5*
%{_mandir}/man8/*.8*
