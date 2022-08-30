import takeltest
import re
import pytest

testinfra_hosts = takeltest.hosts()


@pytest.fixture(name='mount_list')
def get_mount_list(host, testvars):
    return testvars['takel_mount_list']


def test_takel_mount_fstab_file(host, testvars):
    fstab_file_location = testvars['takel_mount_fstab']
    assert host.file(fstab_file_location).exists
    assert host.file(fstab_file_location).is_file


def test_takel_mount_target_directories(host, mount_list):
    for mount in mount_list:
        assert host.file(mount['path']).exists
        assert host.file(mount['path']).is_directory
        assert host.file(mount['path']).user == mount['user']
        assert host.file(mount['path']).group == mount['group']


def test_takel_mount_fstab_content(host, mount_list):
    fstab = host.file('/etc/fstab').content.decode('utf-8')
    for mount in mount_list:
        regex_pattern = \
            f"^(.*?)[ ]+{mount['path']}[ ]+(.*?)[ ]+(.*?)[ ]+(.*?).*"
        mount_options = re.match(regex_pattern, fstab)
        if mount_options is not None:
            src = mount_options.group(1)
            dest = mount_options.group(2)
            filesystem = mount_options.group(3)
            options = mount_options.group(4)
            assert src == mount['src']
            assert dest == mount.path
            assert filesystem == mount.fstype
            assert options == ','.join(mount.options)
