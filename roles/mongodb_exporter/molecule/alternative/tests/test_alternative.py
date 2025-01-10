from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from testinfra_helpers import get_target_hosts

testinfra_hosts = get_target_hosts()


def test_directories(host):
    dirs = [
        "/etc/mongodb_exporter"
    ]
    for dir in dirs:
        d = host.file(dir)
        assert d.is_directory
        assert d.exists


def test_service(host):
    s = host.service("mongodb_exporter")
    try:
        assert s.is_running
    except AssertionError:
        # Capture service logs
        journal_output = host.run('journalctl -u mongodb_exporter --since "1 hour ago"')
        print("\n==== journalctl -u mongodb_exporter Output ====\n")
        print(journal_output)
        print("\n============================================\n")
        raise  # Re-raise the original assertion error


def test_protecthome_property(host):
    s = host.service("mongodb_exporter")
    p = s.systemd_properties
    assert p.get("ProtectHome") == "yes"


def test_socket(host):
    sockets = [
        "tcp://127.0.1.1:9216"
    ]
    for socket in sockets:
        s = host.socket(socket)
        assert s.is_listening
