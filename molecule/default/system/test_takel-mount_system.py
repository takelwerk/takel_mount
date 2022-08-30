import pytest
import takeltest

testinfra_hosts = takeltest.hosts()


@pytest.fixture(name='mount_list')
def get_mount_list(host, testvars):
    return testvars['takel_mount_list']


def test_takel_mount_mounted(host, mount_list):
    activ_mounted = host.check_output('mount')
    for mount in mount_list:
        if mount['state'] == 'present':
            assert mount['path'] not in activ_mounted
        if mount['state'] == 'mounted':
            assert mount['path'] in activ_mounted
