from __future__     import annotations
from dataclasses    import dataclass, field
from collections    import abc

'''
class Subckt:
    def __init__(self,
                 name,
                 ports    = [],
                 property = None,
                 devices  = []
                 ):
        self.name = name
        self.ports = ports
        self.property = property
        self.devices = devices
'''

@dataclass
class Subckt:
    name     : str
    ports    : list[str]        = field(default_factory=list)
    property : dict | None      = None
    devices  : list[Device]     = field(default_factory=list)

    def __iadd__(self, device):
        self.devices.append(device)
        return self

@dataclass
class Device:
    name     : str
    parent   : Subckt | None    = None
    terminals: list | None      = None
    property : dict | None      = None
    symbol   : str | None       = None

if __name__ == "__main__":
    p_device = Device("nmos1")
    n_device = Device("pmos1")
    subckt = Subckt("inv")
    subckt += p_device
    subckt += n_device
    print(subckt)
