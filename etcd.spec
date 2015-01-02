%global debug_package   %{nil}
%global provider        github
%global provider_tld    com
%global project         coreos
%global repo            etcd

%global import_path     %{provider}.%{provider_tld}/%{project}/%{repo}

Name:		%{repo}
Version:	2.0.0
Release:	1.rc1%{?dist}
Summary:	A highly-available key value store for shared configuration
License:	ASL 2.0
URL:		https://%{import_path}
Source0:	https://%{import_path}/archive/v%{version}-rc.1.tar.gz
Source1:	%{name}.service
Source2:	%{name}.conf
BuildRequires:	golang >= 1.3.3
BuildRequires:	golang(bitbucket.org/kardianos/osext)
BuildRequires:	golang(code.google.com/p/gogoprotobuf)
BuildRequires:	golang(github.com/BurntSushi/toml)
BuildRequires:	golang(github.com/codegangsta/cli)
BuildRequires:	golang(github.com/coreos/go-etcd/etcd)
BuildRequires:	golang(github.com/coreos/go-log/log)
BuildRequires:	golang(github.com/coreos/go-systemd)
BuildRequires:	golang(github.com/gorilla/mux)
BuildRequires:	golang(github.com/mreiferson/go-httpclient)
BuildRequires:	golang(github.com/rcrowley/go-metrics)
BuildRequires:  golang(golang.org/x/net/context)
BuildRequires:	systemd
Requires(pre):	shadow-utils
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
A highly-available key value store for shared configuration.

%package devel
BuildRequires:  golang >= 1.2.1-3
BuildRequires:  golang(bitbucket.org/kardianos/osext)
BuildRequires:  golang(code.google.com/p/gogoprotobuf)
BuildRequires:  golang(github.com/BurntSushi/toml)
BuildRequires:  golang(github.com/coreos/go-log/log)
BuildRequires:  golang(github.com/coreos/go-systemd)
BuildRequires:  golang(github.com/gorilla/mux)
BuildRequires:  golang(github.com/mreiferson/go-httpclient)
BuildRequires:  golang(github.com/rcrowley/go-metrics)
BuildRequires:  golang(github.com/stretchr/testify/assert)
Requires:       golang >= 1.2.1-3
Provides:   golang(%{import_path}) = %{version}-%{release}
Provides:   golang(%{import_path}/client) = %{version}-%{release}
Provides:   golang(%{import_path}/discovery) = %{version}-%{release}
Provides:   golang(%{import_path}/error) = %{version}-%{release}
Provides:   golang(%{import_path}/etcdmain) = %{version}-%{release}
Provides:   golang(%{import_path}/etcdserver) = %{version}-%{release}
Provides:   golang(%{import_path}/migrate) = %{version}-%{release}
Provides:   golang(%{import_path}/pkg/cors) = %{version}-%{release}
Provides:   golang(%{import_path}/pkg/crc) = %{version}-%{release}
Provides:   golang(%{import_path}/pkg/fileutil) = %{version}-%{release}
Provides:   golang(%{import_path}/pkg/flags) = %{version}-%{release}
Provides:   golang(%{import_path}/pkg/ioutils) = %{version}-%{release}
Provides:   golang(%{import_path}/pkg/pbutil) = %{version}-%{release}
Provides:   golang(%{import_path}/pkg/testutil) = %{version}-%{release}
Provides:   golang(%{import_path}/pkg/transport) = %{version}-%{release}
Provides:   golang(%{import_path}/pkg/types) = %{version}-%{release}
Provides:   golang(%{import_path}/pkg/wait) = %{version}-%{release}
Provides:   golang(%{import_path}/proxy) = %{version}-%{release}
Provides:   golang(%{import_path}/raft) = %{version}-%{release}
Provides:   golang(%{import_path}/rafthttp) = %{version}-%{release}
Provides:   golang(%{import_path}/snap) = %{version}-%{release}
Provides:   golang(%{import_path}/store) = %{version}-%{release}
Provides:   golang(%{import_path}/wal) = %{version}-%{release}
Summary:    etcd golang devel libraries
ExclusiveArch:  %{ix86} x86_64 %{arm}

%description devel
golang development libraries for etcd, a highly-available key value store for
shared configuration.

%prep
%setup -qn %{name}-%{version}-rc.1
rm -rf Godeps/_workspace/src/github.com/{codegangsta,coreos,stretchr}
rm -rf Godeps/_workspace/src/{code.google.com,bitbucket.org}

find . -name "*.go" \
       -print |\
       xargs sed -i 's/github.com\/coreos\/etcd\/Godeps\/_workspace\/src\///g'

%build
# Make link for etcd itself
mkdir -p src/github.com/coreos
ln -s ../../../ src/github.com/coreos/etcd

export GOPATH=%{gopath}:$(pwd):$(pwd)/Godeps/_workspace:$GOPATH
go build -v -x -o bin/etcd %{import_path}
go build -a -ldflags '-s' -o bin/etcdctl %{import_path}/etcdctl
go build -v -x -o bin/etcd-migrate %{import_path}/migrate/cmd/%{name}-migrate


%install
install -D -p -m 0755 bin/%{name} %{buildroot}%{_bindir}/%{name}
install -D -p -m 0755 bin/%{name}ctl %{buildroot}%{_bindir}/%{name}ctl
install -D -p -m 0755 bin/%{name}-migrate %{buildroot}%{_bindir}/%{name}-migrate
install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -D -p -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/%{name}

# And create /var/lib/etcd
install -d -m 0755 %{buildroot}%{_sharedstatedir}/%{name}

# Install files for devel sub-package
install -d %{buildroot}/%{gopath}/src/%{import_path}
cp -pav main.go %{buildroot}/%{gopath}/src/%{import_path}/
for dir in client discovery error etcdctl etcdmain etcdserver \
        migrate pkg proxy raft rafthttp snap store version wal
do
    cp -rpav ${dir} %{buildroot}/%{gopath}/src/%{import_path}/
done

%check
export GOPATH=%{gopath}:%{buildroot}%{gopath}:$(pwd)/Godeps/_workspace
go test %{import_path}/client
go test %{import_path}/discovery
go test %{import_path}/error
go test %{import_path}/etcdmain
go test %{import_path}/etcdserver
go test %{import_path}/migrate
#go test %{import_path}/pkg/fileutil
go test %{import_path}/pkg/flags
go test %{import_path}/pkg/ioutils
go test %{import_path}/pkg/transport
go test %{import_path}/pkg/types
go test %{import_path}/pkg/wait
go test %{import_path}/proxy
go test %{import_path}/raft
go test %{import_path}/rafthttp
go test %{import_path}/snap
go test %{import_path}/store
go test %{import_path}/wal

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || useradd -r -g %{name} -d %{_sharedstatedir}/%{name} \
	-s /sbin/nologin -c "etcd user" %{name}

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files
%config(noreplace) %{_sysconfdir}/%{name}
%{_bindir}/%{name}
%{_bindir}/%{name}ctl
%{_bindir}/%{name}-migrate
%dir %attr(-,%{name},%{name}) %{_sharedstatedir}/%{name}
%{_unitdir}/%{name}.service
%doc LICENSE README.md Documentation/internal-protocol-versioning.md

%files devel
%doc LICENSE README.md Documentation/internal-protocol-versioning.md
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}
%{gopath}/src/%{import_path}

%changelog
* Tue Dec 23 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2.0.0-1.rc1
- Resolves: rhbz#1176138 - update to v2.0.0-rc1
- do not redefine gopath
- use jonboulle/clockwork from within Godeps

* Fri Oct 17 2014 jchaloup <jchaloup@redhat.com> - 0.4.6-7
- Add ExclusiveArch for go_arches

* Mon Oct 06 2014 jchaloup <jchaloup@redhat.com> - 0.4.6-6
- related: #1047194
  Remove dependency on go.net

* Mon Oct 06 2014 jchaloup <jchaloup@redhat.com> - 0.4.6-5
- Fix the .service file so it can launch!
  related: #1047194

* Mon Sep 22 2014 jchaloup <jchaloup@redhat.com> - 0.4.6-4
- resolves: #1047194
  Update to 0.4.6 from https://github.com/projectatomic/etcd-package

* Tue Aug 19 2014 Adam Miller <maxamillion@fedoraproject.org> - 0.4.6-3
- Add devel sub-package

* Wed Aug 13 2014 Eric Paris <eparis@redhat.com> - 0.4.6-2
- Bump to 0.4.6
- run as etcd, not root

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Oct 20 2013 Peter Lemenkov <lemenkov@gmail.com> - 0.1.2-5
- goprotobuf library unbundled (see rhbz #1018477)
- go-log library unbundled (see rhbz #1018478)
- go-raft library unbundled (see rhbz #1018479)
- go-systemd library unbundled (see rhbz #1018480)
- kardianos library unbundled (see rhbz #1018481)

* Sun Oct 13 2013 Peter Lemenkov <lemenkov@gmail.com> - 0.1.2-4
- go.net library unbundled (see rhbz #1018476)

* Sat Oct 12 2013 Peter Lemenkov <lemenkov@gmail.com> - 0.1.2-3
- Prepare for packages unbundling
- Verbose build

* Sat Oct 12 2013 Peter Lemenkov <lemenkov@gmail.com> - 0.1.2-2
- Fix typo in the etc.service file

* Sat Oct 12 2013 Peter Lemenkov <lemenkov@gmail.com> - 0.1.2-1
- Ver. 0.1.2
- Integrate with systemd

* Mon Aug 26 2013 Luke Cypret <cypret@fedoraproject.org> - 0.1.1-1
- Initial creation
