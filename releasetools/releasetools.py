# Copyright (C) 2012 The Android Open Source Project
# Copyright (C) 2013-2015 The CyanogenMod Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import hashlib
import common
import re

def FullOTA_Assertions(info):
  AddBootloaderAssertion(info)
  AddTrustZoneAssertion(info, info.input_zip)
  return

def IncrementalOTA_Assertions(info):
  AddBootloaderAssertion(info)
  AddTrustZoneAssertion(info, info.target_zip)
  return

def AddBootloaderAssertion(info):
  info.script.AppendExtra('assert(run_program("/sbin/sh", "-c", "aboot=`strings /dev/block/platform/msm_sdcc.1/by-name/aboot | grep mdss_mdp.panel=`; if [ -z \\"$aboot\\" ]; then exit 1; fi") == 0 || abort("Wrong Aboot version, please update!"););')
  return

def AddTrustZoneAssertion(info, input_zip):
  android_info = info.input_zip.read("OTA/android-info.txt")
  m = re.search(r'require\s+version-trustzone\s*=\s*(\S+)', android_info)
  if m:
    versions = m.group(1).split('|')
    if len(versions) and '*' not in versions:
      cmd = 'assert(g2.verify_trustzone(' + ','.join(['"%s"' % tz for tz in versions]) + ') == "1");'
      info.script.AppendExtra(cmd)
  return
