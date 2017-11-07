etcdctl*.1 to etcdctl3*.1

for line in $(ls *.1); do mv $line $(echo $line | sed "s/etcdctl/etcdctl3/"); done

rename refs in man pages

sed -i "s/\\\fBetcdctl\\\-/\\\fBetcdctl3\\\-/g" *.1

sed -i s"/^etcdctl/ETCDCTL=3 etcdctl/" etcdctl3*.1

etcdctl*.1 to etcdctl2*.1

for line in $(ls *.1); do mv $line $(echo $line | sed "s/etcdctl/etcdctl3/"); done

rename refs in man pages

sed -i "s/\\\fBetcdctl-/\\\fBetcdctl2-/g" *.1

