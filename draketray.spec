%define gb_ver %(if rpm -q gambas-devel &>/dev/null; then rpm -q --qf '%%{version}' gambas-devel; else echo -n 3.20; fi)
%define gb_major %(echo %{gb_ver} |cut -d. -f1-2)
%define gb_next_major %(echo -n $(echo %{gb_major} |cut -d. -f1).; GB_MINOR=$(echo %{gb_ver}|cut -d. -f2); echo -n $((GB_MINOR+1)))

Summary:	Icon tray for DnfDrake and FlatDrake
Name:		draketray
Version:	3.11.1
Release:	1
License:	GPLv3
Group:		Graphical desktop/KDE
URL:		https://mib.pianetalinux.org
#URL:		https://github.com/astrgl/draketray
Source0:	https://github.com/astrgl/draketray/archive/%{version}/%{name}-%{version}.tar.gz


BuildRequires:	gambas-devel
BuildRequires:	gambas-gb.dbus
BuildRequires:	gambas-gb.form
BuildRequires:	gambas-gb.form.stock
BuildRequires:	gambas-gb.gui
BuildRequires:  gambas-gb.qt6
BuildRequires:	gambas-gb.image
BuildRequires:	gambas-gui-backend
BuildRequires:	imagemagick

Requires:	sudo
Requires:	(gambas-runtime >= %{gb_major} with gambas-runtime < %{gb_next_major})
Requires:	(gambas-gb.form >= %{gb_major} with gambas-gb.form < %{gb_next_major})
Requires:	(gambas-gb.image >= %{gb_major} with gambas-gb.image < %{gb_next_major})
Requires:	(gambas-gb.gui >= %{gb_major} with gambas-gb.gui < %{gb_next_major})
Requires:	(gambas-gb.qt6 >= %{gb_major} with gambas-gb.qt6 < %{gb_next_major})
Requires:	(gambas-gb.dbus >= %{gb_major} with gambas-gb.dbus < %{gb_next_major})
Requires:	(gambas-gb.form.stock >= %{gb_major} with gambas-gb.form.stock < %{gb_next_major})
Requires: 	hicolor-icon-theme
Requires:	lsb-release
Requires:	xrandr

Suggests:	dnfdrake
Suggests:	flatdrake

BuildArch: noarch

%description
DrakeTray is a tray updates notifier for DnfDrake and Flatdrake

%files
%license FILE-EXTRA/license
%{_bindir}/%{name}.gambas
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.xpm
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_iconsdir}/hicolor/*/apps/%{name}.svg

#---------------------------------------------------------------------------

%prep
%autosetup -p1


%build
gbc3 -e -a -g -t -f public-module -f public-control -j%{?_smp_mflags}
gba3

# unversion binary
mv %{name}-%{version}.gambas %{name}.gambas

%install
# binary
install -Dm 0755 %{name}.gambas -t %{buildroot}/%{_bindir}/

# data files
install -Dm 0644 FILE-EXTRA/%{name}-*-* -t %{buildroot}/%{_datadir}/%{name}/
install -Dm 0644 FILE-EXTRA/license -t %{buildroot}/%{_datadir}/%{name}/
install -Dm 0644 FILE-EXTRA/COPYING -t %{buildroot}/%{_datadir}/%{name}/
install -Dm 644 ICONS-EXTRA/*.png -t %{buildroot}/%{_datadir}/%{name}/icons
install -Dm 644 ICONS-EXTRA/*.svg -t %{buildroot}/%{_datadir}/%{name}/icons

#.desktop used by dnfdrake
install -Dm 0755 FILE-EXTRA/%{name}.desktop -t %{buildroot}/%{_datadir}/%{name}/
install -Dm 0755 FILE-EXTRA/%{name}.desktop -t %{buildroot}/%{_datadir}/applications/

# icons
install -Dm 0644 %{name}.svg -t %{buildroot}%{_iconsdir}/hicolor/scalable/apps/
for d in 16 32 48 64 72 128 256 512
do
	install -dm 0755 %{buildroot}%{_iconsdir}/hicolor/${d}x${d}/apps/
	convert -background none -scale ${d}x${d} %{name}.svg \
			%{buildroot}%{_iconsdir}/hicolor/${d}x${d}/apps/%{name}.png
done
install -dm 0755 %{buildroot}%{_datadir}/pixmaps/
convert -scale 32x32 %{name}.svg %{buildroot}%{_datadir}/pixmaps/%{name}.xpm
