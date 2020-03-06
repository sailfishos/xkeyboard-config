Name:       xkeyboard-config

Summary:    Alternative xkb data files
Version:    2.17
Release:    1
License:    MIT
BuildArch:  noarch
URL:        http://www.freedesktop.org/wiki/Software/XKeyboardConfig
Source0:    %{name}-%{version}.tar.bz2
Patch0:     0001-build-without-docs-so-we-don-t-require-xorg-macros.patch
Patch3:     0002-Workaround-devices-with-bad-headset-event-on-Sailfis.patch
Patch4:     0003-upstream-Map-camera-focus-and-snapshot-keys.-Contrib.patch
Patch5:     0004-sbj-Map-Select-key.-Contributes-to-JB-39965.patch
BuildRequires:  perl(XML::Parser)
BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  fdupes
Provides:   xkbdata
Obsoletes:   xorg-x11-xkbdata

%description
Alternative xkb data files.

%package devel
Summary:    Devel package for alternative xkb data files
Requires:   %{name} = %{version}-%{release}

%description devel
Development files for %{name}.

%prep
%autosetup -p1 -n %{name}-%{version}/upstream

%build
%autogen --disable-static \
    --enable-compat-rules \
    --with-xkb-base=%{_datadir}/X11/xkb \
    --disable-xkbcomp-symlink \
    --with-xkb-rules-symlink=xorg \
    --disable-runtime-deps

make %{?_smp_mflags}

%install
%make_install

# Remove unnecessary symlink
rm -f $RPM_BUILD_ROOT%{_datadir}/X11/xkb/compiled

# Bernie: remove locale stuff
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale

# Create filelist
{
FILESLIST=${PWD}/files.list
pushd $RPM_BUILD_ROOT
find ./usr/share/X11 -type d | sed -e "s/^\./%dir /g" > $FILESLIST
find ./usr/share/X11 -type f | sed -e "s/^\.//g" >> $FILESLIST
popd
}

%fdupes  %{buildroot}//usr/share/X11

%files -f files.list
%defattr(-,root,root,-)
%{_datadir}/X11/xkb/rules/xorg
%{_datadir}/X11/xkb/rules/xorg.lst
%{_datadir}/X11/xkb/rules/xorg.xml

%files devel
%defattr(-,root,root,-)
%{_datadir}/pkgconfig/xkeyboard-config.pc
