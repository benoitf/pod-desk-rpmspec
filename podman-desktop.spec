Name:           podman-desktop
Version:        1.18.0
Release:        1%{?dist}
Summary:        GUI for managing Podman containers

License:        Apache-2.0
URL:            https://github.com/podman-desktop/podman-desktop
ExclusiveArch:  x86_64 aarch64

# Define two binaries of Podman Desktop for the 2 supported arches
Source0:         https://github.com/podman-desktop/podman-desktop/releases/download/v%{version}/podman-desktop-%{version}.tar.gz
Source1:        https://github.com/podman-desktop/podman-desktop/releases/download/v%{version}/podman-desktop-%{version}-arm64.tar.gz

Source2:        https://raw.githubusercontent.com/podman-desktop/podman-desktop/v%{version}/LICENSE
Source3:        https://raw.githubusercontent.com/podman-desktop/podman-desktop/v%{version}/.flatpak.desktop
Source4:        https://raw.githubusercontent.com/podman-desktop/podman-desktop/v%{version}/buildResources/icon-512x512.png

Requires: podman
Requires: libX11

%global debug_package %{nil}
%define _build_id_links none

%description
Podman Desktop is a graphical tool for managing containers using Podman. It allows users to run, manage, and configure containers and container images using a desktop GUI.

%prep
# do not use %setup as we have Source0/x64 and Source1/arm64
#rm -rf %{_builddir}/podman-desktop-%{version}
#mkdir -p %{_builddir}/podman-desktop-%{version}
%setup -T -c

# Unpack the correct tarball depending on architecture
%ifarch x86_64
tar -xzf %{SOURCE0} --strip-components=1
%endif

%ifarch aarch64
tar -xzf %{SOURCE1} --strip-components=1
%endif


cp %{SOURCE2} LICENSE

# Patch .desktop file
cp %{SOURCE3} .podman-desktop.desktop
sed -i \
  -e 's|Exec=.*|Exec=/opt/podman-desktop/podman-desktop|' \
  -e 's|Icon=.*|Icon=podman-desktop|' \
  -e '/^X-Flatpak/d' \
  .podman-desktop.desktop

%build
# No build needed, it’s a binary distribution

%install
mkdir -p %{buildroot}/opt/podman-desktop
cp -a * %{buildroot}/opt/podman-desktop/

# Add desktop file
mkdir -p %{buildroot}%{_datadir}/applications
install -m 644 %{SOURCE3} %{buildroot}%{_datadir}/applications/podman-desktop.desktop

# Add icon
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/512x512/apps
install -m 644 %{SOURCE4} %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/podman-desktop.png


%files
%license LICENSE

/opt/podman-desktop
%{_datadir}/applications/podman-desktop.desktop
%{_datadir}/icons/hicolor/512x512/apps/podman-desktop.png

%check
# No test suite available for this prebuilt binary

%changelog
* Sat Apr 19 2025 Florent Benoit <fbenoit@redhat.com> - 1.18.0-1
- Initial RPM release of Podman Desktop 1.18.0

