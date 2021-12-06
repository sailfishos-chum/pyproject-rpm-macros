# Adapted for the use with SailfishOS
# + Release -> Version
# + Add Fedora as upstream
# + Disable tests by default

Name:           pyproject-rpm-macros
Summary:        RPM macros for PEP 517 Python packages
License:        MIT

%bcond_with tests

# Keep the version at zero and increment only release
Version:        50
Release:        0

# Macro files
Source0: %{name}-%{version}.tar.gz
# Add missing %py3_shebang_fix
Source1: macros.py3_shebang_fix
# Workaround for missing pathfix.py
Source2: pathfix.py
# Workaround for https://github.com/pypa/pip/pull/7873
# Also sed -E -> sed -r
Patch1: pip_workaround.patch

URL:            https://src.fedoraproject.org/rpms/pyproject-rpm-macros

BuildArch:      noarch

%if %{with tests}
BuildRequires: python3dist(pytest)
BuildRequires: python3dist(pyyaml)
BuildRequires: python3dist(packaging)
BuildRequires: python3dist(pip)
BuildRequires: python3dist(setuptools)
BuildRequires: python3dist(toml)
BuildRequires: python3dist(tox-current-env) >= 0.0.6
BuildRequires: python3dist(wheel)
%endif

# We build on top of those:
Requires:      python-rpm-macros
Requires:      python-srpm-macros
Requires:      python3-rpm-macros


%description
These macros allow projects that follow the Python packaging specifications
to be packaged as RPMs.

They are still provisional: we can make non-backwards-compatible changes to
the API.
Please subscribe to Fedora's python-devel list if you use the macros.

They work for:

* traditional Setuptools-based projects that use the setup.py file,
* newer Setuptools-based projects that have a setup.cfg file,
* general Python projects that use the PEP 517 pyproject.toml file
  (which allows using any build system, such as setuptools, flit or poetry).

These macros replace %%py3_build and %%py3_install,
which only work with setup.py.


%prep
# Not strictly necessary but allows working on file names instead
# of source numbers in install section
%autosetup -n %{name}-%{version}/upstream

# Switch rpm vendor from redhat to meego
sed -e 's/redhat/meego/g' -i macros.pyproject



%build
# nothing to do, sources are not buildable

%install
mkdir -p %{buildroot}%{_bindir}
install -m 755 %{SOURCE2} %{buildroot}%{_bindir}

mkdir -p %{buildroot}%{_rpmmacrodir}
mkdir -p %{buildroot}%{_rpmconfigdir}/meego
install -m 644 macros.pyproject %{buildroot}%{_rpmmacrodir}/
install -m 644 %{SOURCE1} %{buildroot}%{_rpmmacrodir}/
install -m 644 pyproject_buildrequires.py %{buildroot}%{_rpmconfigdir}/meego/
install -m 644 pyproject_convert.py %{buildroot}%{_rpmconfigdir}/meego/
install -m 644 pyproject_save_files.py  %{buildroot}%{_rpmconfigdir}/meego/
install -m 644 pyproject_preprocess_record.py %{buildroot}%{_rpmconfigdir}/meego/
install -m 644 pyproject_construct_toxenv.py %{buildroot}%{_rpmconfigdir}/meego/
install -m 644 pyproject_requirements_txt.py %{buildroot}%{_rpmconfigdir}/meego/

%if %{with tests}
%check
export HOSTNAME="rpmbuild"  # to speedup tox in network-less mock, see rhbz#1856356
%{python3} -m pytest -vv --doctest-modules
%endif


%files
%{_bindir}/pathfix.py
%{_rpmmacrodir}/macros.pyproject
%{_rpmmacrodir}/macros.py3_shebang_fix
%{_rpmconfigdir}/meego/pyproject_buildrequires.py
%{_rpmconfigdir}/meego/pyproject_convert.py
%{_rpmconfigdir}/meego/pyproject_save_files.py
%{_rpmconfigdir}/meego/pyproject_preprocess_record.py
%{_rpmconfigdir}/meego/pyproject_construct_toxenv.py
%{_rpmconfigdir}/meego/pyproject_requirements_txt.py

%doc README.md
%license LICENSE
