# John Mark Dennis - 2015
# Tested running Python 2.7.8
# create a vlan in UCSM with simple script
# usage  -v (vlan_number)  -n (vlan_name)
#               python createvlan.py -v 314 -n VLAN314
#

from UcsSdk import *
from UcsSdk.MoMeta.FabricLanCloud import FabricLanCloud
from UcsSdk.MoMeta.FabricVlan import FabricVlan
import time
import optparse
import platform

if __name__ == "__main__":
    try:
        # Login Information
        ucsm_ip = '172.16.209.216'
        user = 'ucspe'
        password = 'ucspe'

        parser = optparse.OptionParser()
	parser.add_option('-v', '--VLAN_Number',dest="vlan_number",
		          help="[Mandatory] VLAN Number")
	parser.add_option('-n', '--VLAN_Name',dest="vlan_name",
		          help="[Mandatory] VLAN Name")

	(options, args) = parser.parse_args()
		
	if not options.vlan_number:
	    parser.print_help()
	    parser.error("Provide VLAN Number")
	if not options.vlan_name:
	    parser.print_help()
	    parser.error("Provide VLAN Name")

        fabric_vlan = "fabric/lan/net-" + options.vlan_name

        handle = UcsHandle()
        handle.Login(ucsm_ip, user, password)
        
        obj = handle.GetManagedObject(None, FabricLanCloud.ClassId(), {FabricLanCloud.DN:"fabric/lan"})
        handle.AddManagedObject(obj, FabricVlan.ClassId(), {FabricVlan.COMPRESSION_TYPE:"included", 
                                FabricVlan.DN:fabric_vlan, FabricVlan.MCAST_POLICY_NAME:"", 
                                FabricVlan.SHARING:"none", FabricVlan.PUB_NW_NAME:"", FabricVlan.ID:options.vlan_number, 
                                FabricVlan.POLICY_OWNER:"local", FabricVlan.NAME:options.vlan_name, FabricVlan.DEFAULT_NET:"no"})

        handle.Logout()

    except Exception, err:
        print "Exception:", str(err)
        import traceback, sys
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60
        handle.Logout()

        
