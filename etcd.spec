%if 0%{?fedora}
%global with_devel 1
%global with_bundled 0
%global with_debug 1
%global with_check 1
%else
%global with_devel 0
%global with_bundled 1
%global with_debug 0
%global with_check 0
%endif

%if 0%{?with_debug}
# https://bugzilla.redhat.com/show_bug.cgi?id=995136#c12
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif
%global provider        github
%global provider_tld    com
%global project         coreos
%global repo            etcd
%global commit          ff8d1ecb9f2bf966c0e6929156be4432786b9217
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

%global import_path     %{provider}.%{provider_tld}/%{project}/%{repo}

Name:		%{repo}
Version:	2.1.2
Release:	1%{?dist}
Summary:	A highly-available key value store for shared configuration
License:	ASL 2.0
URL:		https://%{import_path}
Source0:	https://%{import_path}/archive/v%{version}.tar.gz
Source1:	%{name}.service
Source2:	%{name}.conf

ExclusiveArch:  %{ix86} x86_64 %{arm}
BuildRequires:	golang >= 1.2.1-3
%if ! 0%{?with_bundled}
BuildRequires: golang(github.com/bgentry/speakeasy)
BuildRequires: golang(github.com/boltdb/bolt)
BuildRequires: golang(github.com/codegangsta/cli)
BuildRequires: golang(github.com/coreos/go-etcd/etcd)
BuildRequires: golang(github.com/coreos/go-semver/semver)
BuildRequires: golang(github.com/coreos/pkg/capnslog)
BuildRequires: golang(github.com/gogo/protobuf/proto)
BuildRequires: golang(github.com/google/btree)
BuildRequires: golang(github.com/jonboulle/clockwork)
BuildRequires: golang(github.com/prometheus/client_golang/prometheus)
BuildRequires: golang(github.com/prometheus/procfs)
BuildRequires: golang(github.com/stretchr/testify/assert)
BuildRequires: golang(golang.org/x/crypto/bcrypt)
# tools/functional-tester/etcd-tester/cluster.go:main
#BuildRequires: golang(golang.org/x/net/context)
BuildRequires: golang(google.golang.org/grpc)
%endif
BuildRequires:	systemd
Requires(pre):	shadow-utils
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
A highly-available key value store for shared configuration.

%if 0%{?with_devel}
%package devel
BuildRequires:  golang >= 1.2.1-3
BuildRequires:  golang(github.com/bgentry/speakeasy)
BuildRequires:  golang(github.com/boltdb/bolt)
BuildRequires:  golang(github.com/codegangsta/cli)
BuildRequires:  golang(github.com/coreos/go-etcd/etcd)
BuildRequires:  golang(github.com/coreos/go-semver/semver)
BuildRequires:  golang(github.com/coreos/pkg/capnslog)
BuildRequires:  golang(github.com/gogo/protobuf/proto)
BuildRequires:  golang(github.com/google/btree)
BuildRequires:  golang(github.com/jonboulle/clockwork)
BuildRequires:  golang(github.com/prometheus/client_golang/prometheus)
BuildRequires:  golang(github.com/prometheus/procfs)
BuildRequires:  golang(github.com/stretchr/testify/assert)
BuildRequires:  golang(golang.org/x/crypto/bcrypt)
BuildRequires:  golang(golang.org/x/net/context)
BuildRequires:  golang(google.golang.org/grpc)

Requires: golang(github.com/bgentry/speakeasy)
Requires: golang(github.com/boltdb/bolt)
Requires: golang(github.com/codegangsta/cli)
Requires: golang(github.com/coreos/go-etcd/etcd)
Requires: golang(github.com/coreos/go-semver/semver)
Requires: golang(github.com/coreos/pkg/capnslog)
Requires: golang(github.com/gogo/protobuf/proto)
Requires: golang(github.com/google/btree)
Requires: golang(github.com/jonboulle/clockwork)
Requires: golang(github.com/prometheus/client_golang/prometheus)
Requires: golang(github.com/prometheus/procfs)
Requires: golang(github.com/stretchr/testify/assert)
Requires: golang(golang.org/x/crypto/bcrypt)
Requires: golang(golang.org/x/net/context)
Requires: golang(google.golang.org/grpc)

Provides: golang(%{import_path}/client) = %{version}-%{release}
Provides: golang(%{import_path}/discovery) = %{version}-%{release}
Provides: golang(%{import_path}/error) = %{version}-%{release}
Provides: golang(%{import_path}/etcdctl/command) = %{version}-%{release}
Provides: golang(%{import_path}/etcdmain) = %{version}-%{release}
Provides: golang(%{import_path}/etcdserver) = %{version}-%{release}
Provides: golang(%{import_path}/etcdserver/auth) = %{version}-%{release}
Provides: golang(%{import_path}/etcdserver/etcdhttp) = %{version}-%{release}
Provides: golang(%{import_path}/etcdserver/etcdhttp/httptypes) = %{version}-%{release}
Provides: golang(%{import_path}/etcdserver/etcdserverpb) = %{version}-%{release}
Provides: golang(%{import_path}/etcdserver/stats) = %{version}-%{release}
Provides: golang(%{import_path}/integration) = %{version}-%{release}
Provides: golang(%{import_path}/migrate) = %{version}-%{release}
Provides: golang(%{import_path}/migrate/etcd4pb) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/cors) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/crc) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/fileutil) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/flags) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/idutil) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/ioutil) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/netutil) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/osutil) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/pbutil) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/runtime) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/testutil) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/timeutil) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/transport) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/types) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/wait) = %{version}-%{release}
Provides: golang(%{import_path}/proxy) = %{version}-%{release}
Provides: golang(%{import_path}/raft) = %{version}-%{release}
Provides: golang(%{import_path}/raft/raftpb) = %{version}-%{release}
Provides: golang(%{import_path}/raft/rafttest) = %{version}-%{release}
Provides: golang(%{import_path}/rafthttp) = %{version}-%{release}
Provides: golang(%{import_path}/snap) = %{version}-%{release}
Provides: golang(%{import_path}/snap/snappb) = %{version}-%{release}
Provides: golang(%{import_path}/storage) = %{version}-%{release}
Provides: golang(%{import_path}/storage/backend) = %{version}-%{release}
Provides: golang(%{import_path}/storage/storagepb) = %{version}-%{release}
Provides: golang(%{import_path}/store) = %{version}-%{release}
Provides: golang(%{import_path}/tools/functional-tester/etcd-agent/client) = %{version}-%{release}
Provides: golang(%{import_path}/version) = %{version}-%{release}
Provides: golang(%{import_path}/wal) = %{version}-%{release}
Provides: golang(%{import_path}/wal/walpb) = %{version}-%{release}
Summary:        etcd golang devel libraries
ExclusiveArch:  %{ix86} x86_64 %{arm}

%description devel
golang development libraries for etcd, a highly-available key value store for
shared configuration.
%endif

%prep
%setup -qn %{name}-%{version}
%if ! 0%{?with_bundled}
rm -rf Godeps/_workspace/src/github.com/{codegangsta,coreos,stretchr,jonboulle}
rm -rf Godeps/_workspace/src/{code.google.com,bitbucket.org,golang.org}

find . -name "*.go" \
       -print |\
       xargs sed -i 's/github.com\/coreos\/etcd\/Godeps\/_workspace\/src\///g'

%endif

%build
%if ! 0%{?with_bundled}
# Make link for etcd itself
mkdir -p src/github.com/coreos
ln -s ../../../ src/github.com/coreos/etcd

export GOPATH=$(pwd):%{gopath}

%if 0%{?with_debug}
# *** ERROR: No build ID note found in /.../BUILDROOT/etcd-2.0.0-1.rc1.fc22.x86_64/usr/bin/etcd
function gobuild { go build -a -ldflags "-B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \n') -X %{import_path}/version.GitSHA %{shortcommit}" -v -x "$@"; }
%else
function gobuild { go build -a -ldflags "-X %{import_path}/version.GitSHA %{shortcommit}" "$@"; }
%endif

gobuild -o bin/etcd %{import_path}
gobuild -o bin/etcdctl %{import_path}/etcdctl
gobuild -o bin/etcd-migrate %{import_path}/tools/%{name}-migrate
%else
./build
%endif


%install
install -D -p -m 0755 bin/%{name} %{buildroot}%{_bindir}/%{name}
install -D -p -m 0755 bin/%{name}ctl %{buildroot}%{_bindir}/%{name}ctl
%if 0%{?fedora}
%if ! 0%{?with_bundled}
install -D -p -m 0755 bin/%{name}-migrate %{buildroot}%{_bindir}/%{name}-migrate
%endif
%endif
install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -d -m 0755 %{buildroot}%{_sysconfdir}/%{name}
install -m 644 -t %{buildroot}%{_sysconfdir}/%{name} %{SOURCE2}


# And create /var/lib/etcd
install -d -m 0755 %{buildroot}%{_sharedstatedir}/%{name}

%if 0%{?with_devel}
# Install files for devel sub-package
install -d %{buildroot}/%{gopath}/src/%{import_path}
cp -pav main.go %{buildroot}/%{gopath}/src/%{import_path}/
for dir in client discovery error etcdctl etcdmain etcdserver \
        integration migrate pkg proxy raft rafthttp snap storage \
        store tools version wal
do
    cp -rpav ${dir} %{buildroot}/%{gopath}/src/%{import_path}/
done
%endif

%check
%if 0%{?with_check}
%if 0%{?with_bundled}
export GOPATH=$(pwd)/Godeps/_workspace:%{gopath}
%else
export GOPATH=%{buildroot}%{gopath}:%{gopath}
%endif
#go test %{import_path}/client
go test %{import_path}/discovery
go test %{import_path}/error
go test %{import_path}/etcdctl/command
go test %{import_path}/etcdmain
#go test %{import_path}/etcdserver
go test %{import_path}/etcdserver/auth
#go test %{import_path}/etcdserver/etcdhttp
#go test %{import_path}/etcdserver/etcdhttp/httptypes
#go test %{import_path}/integration
go test %{import_path}/migrate
#go test %{import_path}/pkg/cors
go test %{import_path}/pkg/crc
#go test %{import_path}/pkg/fileutil
go test %{import_path}/pkg/flags
go test %{import_path}/pkg/idutil
go test %{import_path}/pkg/ioutil
go test %{import_path}/pkg/netutil
go test %{import_path}/pkg/osutil
go test %{import_path}/pkg/pbutil
go test %{import_path}/pkg/timeutil
#go test %{import_path}/pkg/transport
go test %{import_path}/pkg/types
go test %{import_path}/pkg/wait
go test %{import_path}/proxy
go test %{import_path}/raft
#go test %{import_path}/raft/rafttest
go test %{import_path}/rafthttp
go test %{import_path}/snap
#go test %{import_path}/storage
#go test %{import_path}/storage/backend
#go test %{import_path}/store
#go test %{import_path}/tools/functional-tester/etcd-agent
go test %{import_path}/version
go test %{import_path}/wal
%endif

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
%if 0%{?fedora}
%if ! 0%{?with_bundled}
%{_bindir}/%{name}-migrate
%endif
%endif
%dir %attr(-,%{name},%{name}) %{_sharedstatedir}/%{name}
%{_unitdir}/%{name}.service
%doc LICENSE README.md Documentation/internal-protocol-versioning.md
%doc Godeps/Godeps.json

%if 0%{?with_devel}
%files devel
%doc LICENSE README.md Documentation/internal-protocol-versioning.md
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}
%{gopath}/src/%{import_path}
%doc Godeps/Godeps.json
%endif

%changelog
* Mon Aug 31 2015 jchaloup <jchaloup@redhat.com> - 2.1.2-1
- Update to v2.1.2
  resolves: #1258599

* Thu Jul 30 2015 jchaloup <jchaloup@redhat.com> - 2.1.1-2
- Enable debug info again
  related: #1214958

* Mon Jul 20 2015 jchaloup <jchaloup@redhat.com> - 2.1.1-1
- fix definition of GOPATH for go1.5
- fix definition of gobuild function for non-debug way
- Update to v2.1.1
  resolves: #1214958

* Fri Jul 10 2015 jchaloup <jchaloup@redhat.com> - 2.0.13-3
- set GOMAXPROCS to use all processors available

* Mon Jun 29 2015 jchaloup <jchaloup@redhat.com> - 2.0.13-2
- Remove -s option from -ldflags string as it removes symbol table
  'go tool l6' gives explanation of all available options
  resolves: #1236320

* Fri Jun 26 2015 jchaloup <jchaloup@redhat.com> - 2.0.13-1
- Update to v2.0.13

* Thu Jun 25 2015 jchaloup <jchaloup@redhat.com> - 2.0.12-2
- Add restart policy and set LimitNOFILE to/in etcd.service file
- Update etcd.config file: add new flags and remove depricated
- Update 'go build' flags for GIT_SHA (used in build script)
- Don't use 4001 and 7001 ports in etcd.conf, they are replaced with 2379 and 2380

* Wed Jun 24 2015 jchaloup <jchaloup@redhat.com> - 2.0.12-1
- Update to v2.0.12
- Polish spec file

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 22 2015 jchaloup <jchaloup@redhat.com> - 2.0.11-2
- ETCD_ADVERTISE_CLIENT_URLS has to be set if ETCD_LISTEN_CLIENT_URLS is
  related: #1222416

* Mon May 18 2015 jchaloup <jchaloup@redhat.com> - 2.0.11-1
- Update to v2.0.11
  resolves: #1222416

* Thu Apr 23 2015 jchaloup <jchaloup@redhat.com> - 2.0.10-1
- Update to v2.0.10
  resolves: #1214705

* Wed Apr 08 2015 jchaloup <jchaloup@redhat.com> - 2.0.9-1
- Update to v2.0.9
  resolves: #1209666

* Fri Apr 03 2015 jchaloup <jchaloup@redhat.com> - 2.0.8-0.2
- Update spec file to fit for rhel too (thanks to eparis)
  related: #1207881

* Wed Apr 01 2015 jchaloup <jchaloup@redhat.com> - 2.0.8-0.1
- Update to v2.0.8
  resolves: #1207881

* Tue Mar 31 2015 jchaloup <jchaloup@redhat.com> - 2.0.7-0.1
- Update to v2.0.7
  Add Godeps.json to doc
  related: #1191441

* Thu Mar 12 2015 jchaloup <jchaloup@redhat.com> - 2.0.5-0.1
- Bump to 9481945228b97c5d019596b921d8b03833964d9e (v2.0.5)

* Tue Mar 10 2015 Eric Paris <eparis@redhat.com> - 2.0.3-0.2
- Fix .service files to work if no config file

* Fri Feb 20 2015 jchaloup <jchaloup@redhat.com> - 2.0.3-0.1
- Bump to upstream 4d728cc8c488a545a8bdeafd054d9ccc2bfb6876

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
