Name:           z-agent
Version:       0.1 
Release:        14%{?dist}
Summary:        a monitor agent

Group:          Tools
License:        GNU
URL:            http://www.test.com
Source0:        z-agent.tar.gz

BuildRequires:  python2.7
Requires:       python2.7

%description
This is a ops tools set, and this package only contain then agent


%prep
%setup -n %{name}


%build
mkdir -p $RPM_BUILD_ROOT/usr/local/z-agent
mkdir -p $RPM_BUILD_ROOT/etc/init.d
mkdir -p $RPM_BUILD_ROOT/bin


%install
mkdir -p $RPM_BUILD_ROOT/usr/local/z-agent
mkdir -p $RPM_BUILD_ROOT/etc/init.d
mkdir -p $RPM_BUILD_ROOT/bin
/bin/cp -r * $RPM_BUILD_ROOT/usr/local/z-agent
mv z-agent.sysv $RPM_BUILD_ROOT/etc/init.d/z-agent
mv agent-link $RPM_BUILD_ROOT/bin/agent
/bin/cp -r * $RPM_BUILD_ROOT/usr/local/z-agent/


%clean
rm -rf $RPM_BUILD_ROOT

%post
service z-agent start

%preun
echo "$1"
service z-agent stop

%postun 
if [ "$1" = "0" ]; then 
echo "unistall"
service z-agent stop
rm -rf /usr/local/z-agent
elif [ "$1" = "1" ]; then
echo "install"
service z-agent start
elif [ "$1" = "2" ]; then
service z-agent restart
fi

%files
%defattr(-,root,root,-)
/usr/local/z-agent/*
/bin/agent
/etc/init.d/z-agent
%doc



%changelog
* Fri May 13 2017 zhang liang - 0.1
- 1.fix /sys/class/dmi/id/chassis_vender
* Fri May 12 2017 zhang liang - 0.1
- 1.first version
