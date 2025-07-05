#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_without	tests	# unit tests

Summary:	Automatic links from code examples to reference documentation
Summary(pl.UTF-8):	Automatyczne odnośniki z przykładów kodu do dokumentacji referencyjnej
Name:		python3-sphinx_codeautolink
Version:	0.17.4
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/sphinx-codeautolink/
Source0:	https://files.pythonhosted.org/packages/source/s/sphinx_codeautolink/sphinx_codeautolink-%{version}.tar.gz
# Source0-md5:	52daf9dc365efc7ad1cd47204cb180a8
URL:		https://pypi.org/project/sphinx-codeautolink/
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.10
BuildRequires:	python3-setuptools >= 1:61.0
BuildRequires:	python3-wheel
%if %{with tests}
BuildRequires:	python3-Sphinx >= 3.2.0
BuildRequires:	python3-bs4 >= 4.8.1
BuildRequires:	python3-ipython >= 8.8.0
BuildRequires:	python3-pytest >= 6
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	python3-docutils >= 0.19
BuildRequires:	python3-ipython >= 8.22.2
BuildRequires:	python3-matplotlib >= 3.8.3
BuildRequires:	python3-sphinx_rtd_theme >= 2.0.0
BuildRequires:	sphinx-pdg-3 >= 7.2.6
%endif
Requires:	python3-modules >= 1:3.10
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
sphinx-codeautolink makes code examples clickable by inserting links
from individual code elements to the corresponding reference
documentation. It aims for a minimal setup assuming your examples are
already valid Python.

%description -l pl.UTF-8
sphinx-codeautolink czyni przykłady kodu klikalnymi poprzez wstawianie
odnośników z poszczególnych elementów kodu do odpowiadającej mu
dokumentacji referencyjnej. Celem jest minimalna konfiguracja przy
założeniu, że przykłady są już poprawnym Pythonem.

%package apidocs
Summary:	API documentation for Python sphinx_codeautolink module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona sphinx_codeautolink
Group:		Documentation

%description apidocs
API documentation for Python sphinx_codeautolink module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona sphinx_codeautolink.

%prep
%setup -q -n sphinx_codeautolink-%{version}

%build
%py3_build_pyproject

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest tests
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
sphinx-build-3 -b html docs/src docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%{__rm} $RPM_BUILD_ROOT%{py3_sitescriptdir}/sphinx_codeautolink/locale/*.pot
%{__rm} $RPM_BUILD_ROOT%{py3_sitescriptdir}/sphinx_codeautolink/locale/*/LC_MESSAGES/*.po

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE readme_pypi.rst
%dir %{py3_sitescriptdir}/sphinx_codeautolink
%{py3_sitescriptdir}/sphinx_codeautolink/*.py
%{py3_sitescriptdir}/sphinx_codeautolink/__pycache__
%{py3_sitescriptdir}/sphinx_codeautolink/extension
%dir %{py3_sitescriptdir}/sphinx_codeautolink/locale
%lang(de) %{py3_sitescriptdir}/sphinx_codeautolink/locale/de
%lang(es) %{py3_sitescriptdir}/sphinx_codeautolink/locale/es
%lang(fi) %{py3_sitescriptdir}/sphinx_codeautolink/locale/fi
%lang(fr) %{py3_sitescriptdir}/sphinx_codeautolink/locale/fr
%lang(it) %{py3_sitescriptdir}/sphinx_codeautolink/locale/it
%lang(nl) %{py3_sitescriptdir}/sphinx_codeautolink/locale/nl
%lang(ru) %{py3_sitescriptdir}/sphinx_codeautolink/locale/ru
%lang(uk) %{py3_sitescriptdir}/sphinx_codeautolink/locale/uk
%{py3_sitescriptdir}/sphinx_codeautolink/static
%{py3_sitescriptdir}/sphinx_codeautolink-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_images,_static,plot_directive,*.html,*.js}
%endif
