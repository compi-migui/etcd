# https://bugzilla.redhat.com/show_bug.cgi?id=995136#c12
%global _dwz_low_mem_die_limit 0
%global provider        github
%global provider_tld    com
%global project         coreos
%global repo            etcd

%global import_path     %{provider}.%{provider_tld}/%{project}/%{repo}

Name:		%{repo}
Version:	2.0.1
Release:	0.2%{?dist}
Summary:	A highly-available key value store for shared configuration
License:	ASL 2.0
URL:		https://%{import_path}
Source0:	https://%{import_path}/archive/v%{version}.tar.gz
Source1:	%{name}.service
Source2:	%{name}.conf

Patch0: 	etcd-2.0.1-Replace-depricated-ErrWrongType-with-its-local-defin.patch

ExclusiveArch:  %{ix86} x86_64 %{arm}
BuildRequires:	golang >= 1.3.3
BuildRequires:	golang(code.google.com/p/gogoprotobuf/proto)
BuildRequires:	golang(github.com/codegangsta/cli)
BuildRequires:	golang(github.com/coreos/go-etcd/etcd)
BuildRequires:  golang(golang.org/x/net/context)
BuildRequires:  golang(github.com/jonboulle/clockwork)
BuildRequires:  golang(github.com/stretchr/testify/assert)
BuildRequires:	systemd
Requires(pre):	shadow-utils
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
A highly-available key value store for shared configuration.

%package devel
BuildRequires:  golang >= 1.2.1-3
BuildRequires:	golang(code.google.com/p/gogoprotobuf/proto)
BuildRequires:	golang(github.com/codegangsta/cli)
BuildRequires:	golang(github.com/coreos/go-etcd/etcd)
BuildRequires:  golang(golang.org/x/net/context)
BuildRequires:  golang(github.com/jonboulle/clockwork)
BuildRequires:  golang(github.com/stretchr/testify/assert)
Requires:       golang >= 1.2.1-3
Provides:       golang(%{import_path}) = %{version}-%{release}
Provides:       golang(%{import_path}/client) = %{version}-%{release}
Provides:       golang(%{import_path}/discovery) = %{version}-%{release}
Provides:       golang(%{import_path}/error) = %{version}-%{release}
Provides:       golang(%{import_path}/etcdctl) = %{version}-%{release}
Provides:       golang(%{import_path}/etcdctl/command) = %{version}-%{release}
Provides:       golang(%{import_path}/etcdmain) = %{version}-%{release}
Provides:       golang(%{import_path}/etcdserver) = %{version}-%{release}
Provides:       golang(%{import_path}/etcdserver/etcdhttp) = %{version}-%{release}
Provides:       golang(%{import_path}/etcdserver/etcdhttp/httptypes) = %{version}-%{release}
Provides:       golang(%{import_path}/etcdserver/etcdserverpb) = %{version}-%{release}
Provides:       golang(%{import_path}/etcdserver/stats) = %{version}-%{release}
Provides:       golang(%{import_path}/migrate) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/cors) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/crc) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/fileutil) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/flags) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/ioutils) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/pbutil) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/testutil) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/transport) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/types) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/wait) = %{version}-%{release}
Provides:       golang(%{import_path}/proxy) = %{version}-%{release}
Provides:       golang(%{import_path}/raft) = %{version}-%{release}
Provides:       golang(%{import_path}/raft/raftpb) = %{version}-%{release}
Provides:       golang(%{import_path}/rafthttp) = %{version}-%{release}
Provides:       golang(%{import_path}/snap) = %{version}-%{release}
Provides:       golang(%{import_path}/snap/snappb) = %{version}-%{release}
Provides:       golang(%{import_path}/store) = %{version}-%{release}
Provides:       golang(%{import_path}/wal) = %{version}-%{release}
Provides:       golang(%{import_path}/wal/walpb) = %{version}-%{release}
Summary:        etcd golang devel libraries
ExclusiveArch:  %{ix86} x86_64 %{arm}

%description devel
golang development libraries for etcd, a highly-available key value store for
shared configuration.

%prep
%setup -qn %{name}-%{version}
rm -rf Godeps/_workspace/src/github.com/{codegangsta,coreos,stretchr,jonboulle}
rm -rf Godeps/_workspace/src/{code.google.com,bitbucket.org,golang.org}

find . -name "*.go" \
       -print |\
       xargs sed -i 's/github.com\/coreos\/etcd\/Godeps\/_workspace\/src\///g'

%patch0 -p1

%build
# Make link for etcd itself
mkdir -p src/github.com/coreos
ln -s ../../../ src/github.com/coreos/etcd

export GOPATH=$(pwd):%{gopath}:$GOPATH
# *** ERROR: No build ID note found in /.../BUILDROOT/etcd-2.0.0-1.rc1.fc22.x86_64/usr/bin/etcd
function gobuild { go build -a -ldflags "-B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \n')" -v -x "$@"; }
gobuild -o bin/etcd %{import_path}
gobuild -o bin/etcdctl %{import_path}/etcdctl
gobuild -o bin/etcd-migrate %{import_path}/tools/%{name}-migrate


%install
install -D -p -m 0755 bin/%{name} %{buildroot}%{_bindir}/%{name}
install -D -p -m 0755 bin/%{name}ctl %{buildroot}%{_bindir}/%{name}ctl
install -D -p -m 0755 bin/%{name}-migrate %{buildroot}%{_bindir}/%{name}-migrate
install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -d -m 0755 %{buildroot}%{_sysconfdir}/%{name}
install -m 644 -t %{buildroot}%{_sysconfdir}/%{name} %{SOURCE2}


# And create /var/lib/etcd
install -d -m 0755 %{buildroot}%{_sharedstatedir}/%{name}

# Install files for devel sub-package
install -d %{buildroot}/%{gopath}/src/%{import_path}
cp -pav main.go %{buildroot}/%{gopath}/src/%{import_path}/
for dir in client discovery error etcdctl etcdmain etcdserver \
        migrate pkg proxy raft rafthttp snap store version wal \
	integration
do
    cp -rpav ${dir} %{buildroot}/%{gopath}/src/%{import_path}/
done

%check
export GOPATH=%{buildroot}%{gopath}:%{gopath}
go test %{import_path}/client
go test %{import_path}/discovery
go test %{import_path}/error
go test %{import_path}/etcdctl/command
go test %{import_path}/etcdmain
#go test %{import_path}/etcdserver
#go test %{import_path}/etcdserver/etcdhttp
#go test %{import_path}/etcdserver/etcdhttp/httptypes
#go test %{import_path}/integration
go test %{import_path}/migrate
#go test %{import_path}/pkg/fileutil
go test %{import_path}/pkg/flags
go test %{import_path}/pkg/ioutil
go test %{import_path}/pkg/transport
go test %{import_path}/pkg/types
go test %{import_path}/pkg/wait
go test %{import_path}/proxy
go test %{import_path}/raft
go test %{import_path}/rafthttp
go test %{import_path}/snap
#go test %{import_path}/store
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
* Wed Feb 18 2015 jchaloup <jchaloup@redhat.com> - 2.0.1-0.2
- Update configuration and service file
  Fix depricated ErrWrongType after update of gogo/protobuf
  related: #1191441

* Wed Feb 11 2015 jchaloup <jchaloup@redhat.com> - 2.0.1-0.1
- Update to 2.0.1
  resolves: #1191441

* Mon Feb 09 2015 jchaloup <jchaloup@redhat.com> - 2.0.0-0.5
- Add missing debug info to binaries (patch from Jan Kratochvil)
  resolves: #1184257

* Fri Jan 30 2015 jchaloup <jchaloup@redhat.com> - 2.0.0-0.4
- Update to etcd-2.0.0
- use gopath as the last directory to search for source code
  related: #1176138

* Mon Jan 26 2015 jchaloup <jchaloup@redhat.com> - 2.0.0-0.3.rc1
- default to /var/lib/etcd/default.etcd as 2.0 uses that default (f21 commit byt eparis)
  related: #1176138
  fix /etc/etcd/etcd.conf path

* Tue Jan 20 2015 jchaloup <jchaloup@redhat.com> - 2.0.0-0.2.rc1
- Update of BuildRequires/Requires, Provides and test
  Add BuildRequire on jonboulle/clockwork
  related: #1176138

* Tue Dec 23 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2.0.0-0.1.rc1
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
