#!/bin/bash
# set -m
# set -x

VM_SSHKEY=/root/bullseye.id_rsa
VMPORT=22
PIDFILE=/root/vm.pid
TMPDIR=/tmp/d4256c2e2a95127a5aab929cc1208f2d7f0df27e/fZdT0KF2

vmcmd_user()
{
    local cmd="${1}"

    ssh -i "${VM_SSHKEY}" -p "${VMPORT}" -o UserKnownHostsFile=/dev/null \
        -o StrictHostKeyChecking=no -q user@localhost "${cmd}"
}

vmcmd()
{
    local cmd="${1}"

    ssh -i "${VM_SSHKEY}" -p "${VMPORT}" -o UserKnownHostsFile=/dev/null \
        -o StrictHostKeyChecking=no -q root@localhost "${cmd}"
}

vmcopy()
{
    local src="${1}"
    local dst="${2}"

    scp -r -i "${VM_SSHKEY}" -P "${VMPORT}" -o UserKnownHostsFile=/dev/null \
        -o StrictHostKeyChecking=no -q "${src}" root@localhost:"${dst}"
}

wait_vm()
{
    vmcmd "exit"
    while [[ ${?} -ne 0 ]]; do
        sleep 1
        vmcmd "exit"
    done
}

vmstart()
{

    echo "Starting VM"
    # timeout --foreground 300
    /usr/bin/qemu-system-x86_64 \
        -cpu kvm64 \
        -m 2G \
        -kernel /root/bzImage \
        -drive file=/root/bullseye.img,format=raw \
        -device e1000,netdev=net0 \
        -netdev user,id=net0,hostfwd=tcp:0.0.0.0:${VMPORT}-:22,hostfwd=tcp:0.0.0.0:1337-:1337  \
        -nographic \
        -no-reboot \
        -append "console=ttyS0 root=/dev/sda net.ifnames=0" \
        -pidfile ${PIDFILE} &
        # -monitor none \

    echo "VM started"

    wait_vm

    echo "VM ready to use"
}

vmstart

vmcmd_user "socat -v TCP-LISTEN:1337,reuseaddr,fork EXEC:/chall/infiltration,nofork" &

wait
