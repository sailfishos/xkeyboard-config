Name:       xkeyboard-config

Summary:    Alternative xkb data files
Version:    2.37
Release:    1
License:    MIT
BuildArch:  noarch
URL:        http://www.freedesktop.org/wiki/Software/XKeyboardConfig
Source0:    %{name}-%{version}.tar.bz2
Patch1:     0001-Workaround-devices-with-bad-headset-event-on-Sailfis.patch
Patch2:     0002-Map-camera-focus-and-snapshot-keys.-Contributes-to-M.patch
Patch3:     0003-Map-Select-key.-Contributes-to-JB-39965.patch
Patch4:     0004-Map-Xperia-10-III-assistant-button-to-camera.patch
BuildRequires:  meson
BuildRequires:  gettext gettext-devel
BuildRequires:  libxslt
BuildRequires:  perl(XML::Parser)
BuildRequires:  pkgconfig(glib-2.0)

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
%meson -Dcompat-rules=true -Dxorg-rules-symlinks=true
%meson_build

%install
%meson_install

# Remove unnecessary symlink
rm -f $RPM_BUILD_ROOT%{_datadir}/X11/xkb/compiled
%find_lang %{name}

# Create filelist
{
   FILESLIST=${PWD}/files.list
   pushd $RPM_BUILD_ROOT
   find .%{_datadir}/X11/xkb -type d | sed -e "s/^\./%dir /g" > $FILESLIST
   find .%{_datadir}/X11/xkb -type f | sed -e "s/^\.//g" >> $FILESLIST
   popd
}

%files -f files.list -f %{name}.lang
%defattr(-,root,root,-)
%license COPYING
%{_datadir}/X11/xkb/rules/xorg
%{_datadir}/X11/xkb/rules/xorg.lst
%{_datadir}/X11/xkb/rules/xorg.xml
%exclude %{_mandir}/man7/xkeyboard-config.*

%files devel
%defattr(-,root,root,-)
%{_datadir}/pkgconfig/xkeyboard-config.pc
