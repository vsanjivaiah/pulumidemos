"""An Azure RM Python Pulumi program"""

import pulumi
from pulumi_azure_native import storage
from pulumi_azure_native import resources
from pulumi_azure_native import network
from pulumi_azure_native import compute

rg1 = resources.ResourceGroup(
        resource_name="rg1",
        resource_group_name="rg-vi-network01",
        location="westus2"
      )

rg2 = resources.ResourceGroup(
        resource_name="rg2",
        resource_group_name="rg-vi-workload01",
        location="westus2"
      )

vn = network.VirtualNetwork(
    resource_name="vnet1",
    resource_group_name=rg1.name,
    location=rg1.location,
    virtual_network_name="vn-vinayvnet01",
    address_space= network.AddressSpaceArgs(
        address_prefixes=["10.0.0.0/16"]
    ),
   
)

nsg1 = network.NetworkSecurityGroup(
    resource_name= "nsg1",
    resource_group_name=rg1.name,
    location=rg1.location,
    network_security_group_name="nsg-vm1",
    security_rules=[
        network.SecurityRuleArgs(
            name="inbound-ssh",
            access="Allow",
            destination_address_prefix="*",
            destination_port_range="22",
            priority=100,
            protocol="TCP",
            source_address_prefix="*",
            source_port_range="*",
            direction="Inbound"

        )
    
    ]
)
sn = network.Subnet(
    resource_name="sn1",
    subnet_name="subnet1",
    virtual_network_name=vn.name,
    resource_group_name=rg1.name,
    address_prefix="10.0.0.0/24",
    network_security_group=
        network.NetworkSecurityGroupArgs(
            id= nsg1.id
        )
        
)



pip1 = network.PublicIPAddress(
    resource_name= "pip1",
    resource_group_name=rg2.name,
    location=rg2.location,
    public_ip_address_name="pip-vm1",
    public_ip_allocation_method=network.IPAllocationMethod.DYNAMIC


)





vm_nic1 = network.NetworkInterface(
    resource_name="vm_nic1",
    network_interface_name= "vm1-nic1",
    resource_group_name=rg2.name,
    location=rg2.location,
    ip_configurations=[
        network.NetworkInterfaceIPConfigurationArgs(
            name="ipconfig1",
            subnet=network.SubnetArgs(
                id= sn.id,

            ),
            primary=True,
            public_ip_address= network.PublicIPAddressArgs(
                id= pip1.id
            )
        )
    ],
   
)

vm1 = compute.VirtualMachine(
    resource_name="vm1",
    vm_name="vm1",
    resource_group_name=rg2.name,
    location=rg2.location,
    os_profile= compute.OSProfileArgs(
        computer_name="vm1",
        admin_password="f;a=3WvW~u;?Q}",
        admin_username="e360user"
    ),
    hardware_profile= compute.HardwareProfileArgs(
        vm_size="Standard_D2s_v3",

    ),
    network_profile= compute.NetworkProfileArgs(
        network_interfaces=[
            compute.NetworkInterfaceReferenceArgs(
                id= vm_nic1.id,
                primary=True
            )
        ]
    ),
    storage_profile= compute.StorageProfileArgs(
        os_disk= compute.OSDiskArgs(
            name="VM1-OSDisk",
            create_option="FromImage",
            caching="ReadWrite",
            disk_size_gb=60,
            managed_disk= compute.ManagedDiskParametersArgs(
                storage_account_type=compute.StorageAccountType.PREMIUM_LRS
            )
        ),
        image_reference= compute.ImageReferenceArgs(
            offer="UbuntuServer",
            publisher= "Canonical",
            sku= "18.04-LTS",
            version="latest"
        )
    )
    
)


