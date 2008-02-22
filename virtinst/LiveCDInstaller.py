#
# An installer class for LiveCD images
#
# Copyright 2007  Red Hat, Inc.
# Mark McLoughlin <markmc@redhat.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free  Software Foundation; either version 2 of the License, or
# (at your option)  any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA.

import os
import Guest
import CapabilitiesParser
from virtinst import _virtinst as _

class LiveCDInstallerException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)

class LiveCDInstaller(Guest.Installer):
    def __init__(self, type = "xen", location = None):
        Guest.Installer.__init__(self, type, location)

    def prepare(self, guest, meter, distro = None):
        self.cleanup()

        if not os.path.exists(self.location):
            raise LiveCDInstallerException(_("LiveCD image '%s' does not exist") % self.location)

        capabilities = CapabilitiesParser.parse(guest.conn.getCapabilities())

        found = False
        for guest_caps in capabilities.guests:
            if guest_caps.os_type == "hvm":
                found = True
                break

        if not found:
            raise LiveCDInstallerException(_("HVM virtualisation not supported; cannot boot LiveCD"))

        disk = Guest.VirtualDisk(self.location,
                                 device = Guest.VirtualDisk.DEVICE_CDROM,
                                 readOnly = True)
        guest._install_disks.insert(0, disk)

    def _get_osblob(self, install, hvm, arch = None, loader = None):
        if install:
            return None

        osblob  = "<os>\n"
        osblob += "      <type>hvm</type>\n"
        if loader:
            osblob += "      <loader>%s</loader>\n" % loader
        osblob += "      <boot dev='cdrom'/>\n"
        osblob += "    </os>"

        return osblob

    def post_install_check(self, guest):
        return True
