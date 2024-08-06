# @web: https://aice.sjtu.edu.cn/msda/html/courseware.htm
from pprint import *
from collections import OrderedDict

class Netlist:
    def __init__(self):
        self._global      = set()
        self._param       = OrderedDict()
        self._subckt      = OrderedDict()
        self._device      = OrderedDict()
        self._include     = []
        self._option      = OrderedDict()
        self._temperature = None

    def append_lib(self, lib):
        self._include.append(lib)

    def get_lib(self):
        return self._include

    def set_temperature(self, temperature):
        self._temperature = temperature

    def get_temperature(self):
        return self._temperature

    def append_option(self, option):
        self._option.update(option)

    def get_option(self):
        return self._option

    def append_model(self, model):
        if not hasattr(self, "_models"):
            self._models = {}
        self._models[model.name] = model

    def get_model(self):
        return self._models

    def append_param(self, param):
        self._param.update(param)

    def get_param(self):
        params = OrderedDict()
        def dfs(netlist):
            for param_name, param_value in netlist._param.items():
                params[param_name] = param_value
            libs = netlist.get_lib()
            if libs:
                for inc in libs:
                    dfs(inc['netlist'])
        dfs(self)
        return params

    def append_global(self, nodes):
        self._global.update(nodes)

    def get_global(self):
        return self._global

    def append_device(self, device):
        # self._device.append(device)
        self._device[device.name] = device

    def get_device(self, name=None, nocase=True):
        devices = OrderedDict()
        def dfs(netlist):
            for device_name, device in netlist._device.items():
                devices[device_name] = device
            libs = netlist.get_lib()
            if libs:
                for inc in libs:
                    dfs(inc['netlist'])
        dfs(self)

        if name is None:
            return devices
        # if name in devices:
        #     return devices[name]
        for device_name, device in devices.items():
            if nocase:
                device_name = device_name.lower()
                name = name.lower()
            if device_name == name:
                return device
        return None

    def append_subckt(self, subckt):
        self._subckt[subckt.name] = subckt

    def __iadd__(self, subckt):
        self.append_subckt(subckt)

    def get_subckt(self, name=None, nocase=True):
        subckts = OrderedDict()
        def dfs(netlist):
            for subckt_name, subckt in netlist._subckt.items():
                subckts[subckt_name] = subckt
            libs = netlist.get_lib()
            if libs:
                for inc in libs:
                    dfs(inc['netlist'])
        dfs(self)

        if name is None:
            return subckts
        # if name in subckts:
        #     return subckts[name]
        for subckt_name, subckt in subckts.items():
            if nocase:
                subckt_name = subckt_name.lower()
                name = name.lower()
            if subckt_name == name:
                return subckt
        return None

    def __getitem__(self, subckt_name):
        return self.get_subckt(subckt_name)

    def __contains__(self, name):
        for subckt_name, subckt in self.get_subckt().items():
            if subckt_name == name:
                return True
        return False

    ############# netlist API ################
    '''
    netlist = {
        # <subckt> : <devices>
        "inv"   : ["pmos", "nmos"],
        "buffer": ["inv", "inv"],
        "nor"   : ["pmos", "pmos", "nmos", "nmos"],
        "or"    : ["nor", "inv"],
    }
    '''

    '''
    @method1:
        @step1:
            create two set(subckts & devices)
        @step2:
            traverse subckt and device, and add to set respectively

            <subckts>: inv, buffer, nor, or
            <devices>: pmos, nmos, inv, nor

        @step3:
            # find top subckt which is not in devices for subckt in subckts
            for subckt in subckts:
                if subckt not in devices:
                    subckt is top subckt
            or:
            <top subckt> = <subckts> - <devices>

                            V          V
            <subckts>: inv, buffer, nor, or
            <devices>: pmos, nmos, inv, nor
    '''

    '''
    @method2:
        @step1:
            create one dict to tag device and subckt(flag)
        @step2:
            traverse subckt and device, and add tag to dict

            <flag>:
                # <subckt> : <tags>
                pmos  : device
                nmos  : device
                inv   : subckt device
                buffer: subckt              <--
                nor   : subckt device
                or    : subckt              <--

        @step3:
            # find top subckt which is only one "subckt" tag for dict
            for subckt, tags in flag.items():
                if len(tags) == 1 and tags[0] == "subckt":
                    subckt is top subckt
    '''

    '''
    buffer:
        inv:
            pmos
            nmos
        inv:
            pmos
            nmos
    or:
        nor:
            pmos
            pmos
            nmos
            nmos
        inv:
            pmos
            nmos
    '''

    def find_top_subckt(self):
        top_subckts = set()

        for top_subckt_name, top_subckt in self.get_subckt().items():
            is_top = True
            for subckt_name, subckt in self.get_subckt().items():
                if top_subckt_name == subckt_name: # skip oneself
                    continue
                for device in subckt:
                    if not hasattr(device, "symbol"):
                        continue
                    if top_subckt_name == device.symbol.name: # Model.name
                        is_top = False
                if not is_top:  # break easily
                    break
            if is_top:
                top_subckts.add(top_subckt_name)
        return top_subckts

    def find_top_subckt1(self):
        top_subckts   = set()
        subckt_device = {}
        for subckt_name, subckt in self.get_subckt().items():
            for device in subckt:
                if hasattr(device, "symbol"):
                    subckt_device.setdefault(device.symbol.name, set()).add("device")
            subckt_device.setdefault(subckt_name, set()).add("subckt")
        for component, types in subckt_device.items():
            if len(types) == 1 and "subckt" in types:
                top_subckts.add(component)
        return top_subckts

    def find_top_subckt2(self):
        top_subckts   = set()
        subckts = set()
        devices = set()
        for subckt_name, subckt in self.get_subckt().items():
            for device in subckt:
                if hasattr(device, "symbol"):
                    devices.add(device.symbol.name)
            subckts.add(subckt_name)
        # for subckt_name in subckts:
        #     if subckt_name not in devices:
        #         top_subckts.add(subckt_name)
        # return top_subckts
        return subckts - devices

    def replace_subckt(self, find_name, replace):
        all_subckts = self.get_subckt()
        if find_name in all_subckts:
            del all_subckts[find_name]
        all_subckts[replace.name] = replace
        for subckt_name, subckt in all_subckts.items():
            subckt.replace_symbol(find=find_name, replace=replace.name)

    def flatten_subckt(self, subckt_name=None, max_layer=0):
        flatten_subckt = OrderedDict()

        def dfs(subckt_name, *, parent_name=None, layer=1):
            if max_layer > 0 and layer > max_layer:
                return
            subckt = self.get_subckt(name=subckt_name)
            if subckt is None:
                return
            if parent_name is None:
                parent_name = subckt_name
            flatten_subckt[parent_name] = {
                "layer" : layer,
                "subckt": subckt,
            }
            for device in subckt:
                if hasattr(device, "symbol"):
                    full_subckt_name = ".".join([parent_name, device.name])
                    layer += 1
                    dfs(device.symbol.name,
                        parent_name = full_subckt_name,
                        layer       = layer,
                        )
                    layer -= 1

        if subckt_name is None:
            for _subckt_name, subckt in self.get_subckt().items():
                dfs(_subckt_name)
        else:
            dfs(subckt_name)
        return flatten_subckt

    def trace_subckt(self, subckt_path, *, nocase=True):
        subckts = self.get_subckt()
        def dfs(subckt_name, paths):
            if not subckt_name in subckts:
                return None
            for device in subckts[subckt_name]:
                device_name = device.name
                current_device_name = paths[0]
                if nocase:
                    current_device_name = current_device_name.lower()
                    device_name = device_name.lower()
                if not current_device_name == device_name:
                    continue
                if len(paths) == 1:
                    return device
                if not hasattr(device, "symbol"):
                    continue
                symbol_name = device.symbol.name
                result = dfs(symbol_name, paths[1:])
                if result:
                    return result

        paths = subckt_path.split(".")
        top_subckt_name = paths.pop(0)
        if self.get_device(top_subckt_name, nocase=nocase):
            device = self.get_device(top_subckt_name, nocase=nocase)
            if len(paths) == 0:
                return device
            if not hasattr(device, "symbol"):
                return None
            symbol_name = device.symbol.name
            return dfs(symbol_name, paths)
        elif subckt := self.get_subckt(top_subckt_name, nocase=nocase):
            if len(paths) == 0:
                return self.get_subckt(top_subckt_name, nocase=nocase)
            return dfs(subckt.name, paths)
        return None

    def __str__(self):
        msg = ""
        if self._global:
            msg += f"global: {', '.join(self._global)}\n"
        if self._param:
            msg += f"param:\n"
            for key, value in self._param.items():
                msg += f"       {key}: {value}\n"
        if self._option:
            msg += f"option:\n"
            for key, value in self._option.items():
                if value is None:
                    msg += f"       {key}\n"
                else:
                    msg += f"       {key}: {value}\n"
        if self._temperature:
            msg += f"temperature: {', '.join([str(t) for t in self._temperature])}\n"
        if self._subckt:
            msg += f"subckt:\n"
            for key, value in self._subckt.items():
                msg += f"{value}"
        if self._device:
            msg += f"device:\n"
            for device in self._device.values():
                msg += f"   {device}\n"
        if self._include:
            msg += f"include:\n"
            for inc in self.get_lib():
                msg += f"   path: {inc['path']}\n"
                if inc["entry_name"]:
                    msg += f"   entry_name: {inc['entry_name']}\n"
                msg += f"   netlist:\n{inc['netlist']}\n"
        return msg

    @classmethod
    def from_dict(self, netlist_dict):
        pass

    def as_dict(self):
        pass

class Model:
    def __init__(self, name, type=None, property={}):
        self.name       = name
        self.type       = type
        self.properties = property

    def add_property(self, name, value):
        if not hasattr(self, "properties"):
            self.properties = {}
        self.properties[name] = value

    def __str__(self):
        return self.name

class Device:
    def __init__(self, name):
        self.name       = name
        self.has_subckt = False

    def set_symbol(self, symbol):
        self.symbol = Model(symbol)

    def in_subckt(self, subckt):
        self.subckt     = subckt
        self.has_subckt = True

    def get_subckt(self):
        if hasattr(self, "subckt"):
            return self.subckt
        return None

    def add_terminal(self, terminal):
        if not hasattr(self, "terminals"):
            self.terminals = []
        if isinstance(terminal, list):
            for num, term in enumerate(terminal):
                self.terminals.append(Terminal(term, device=self, num=num))
        else:
            self.terminals.append(Terminal(terminal, device=self, num=len(self.terminals)))

    def get_terminal(self):
        return self.terminals

    def add_property(self, name, value):
        if not hasattr(self, "properties"):
            self.properties = {}
        self.properties[name] = value

    def get_property(self):
        return self.properties

    # maybe todo
    def add_neighbor(self, device, from_terminal, to_terminal):
        if not hasattr(self, "neighbors"):
            self.neighbors = {}
        self.neighbors.setdefault(device, set()).add(from_terminal.name)

    def get_neighbor(self):
        return self.neighbors

    def add_edge(self, from_terminal, to_terminal):
        from_device = from_terminal.device
        to_device   = to_terminal.device
        from_device.add_neighbor(to_device, from_terminal, to_terminal)
        to_device.add_neighbor(from_device, from_terminal, to_terminal)

    def remove_edge(self, device):
        self.get_neighbor().pop(device, None)
        device.get_neighbor().pop(self, None)

    def get_edges(self, device):
        if device in self.neighbors:
            return self.neighbors[device]
        return None

    def __str__(self):
        msg = f"{self.name}"
        if hasattr(self, "terminals"):
            for terminal in self.terminals:
                msg += f" {terminal}"
        if hasattr(self, "symbol"):
            msg += f" {self.symbol}"
        if hasattr(self, "properties"):
            for p_name, p_value in self.properties.items():
                msg += f" {p_name}={p_value}"
        return msg

    def __iter__(self):
        self.iter = iter(self.terminals)
        return self

    def __next__(self):
        terminal = next(self.iter)
        return terminal

    # dictionary convert to Device
    @classmethod
    def from_dict(self, dev_dict):
        device = self(dev_dict["NAME"])
        device.set_symbol(dev_dict["SYMBOL"])
        for terminal in dev_dict["PORT"]:
            device.add_terminal(terminal)
        if "PROPERTY" in dev_dict:
            for name, value in dev_dict["PROPERTY"].items():
                device.add_property(name, value)
        return device

    # Device convert to dictionary
    def as_dict(self):
        dev_dict = {}
        dev_dict["NAME"]   = self.name
        dev_dict["SYMBOL"] = self.symbol.name
        for terminal in self.terminals:
            dev_dict.setdefault("PORT", []).append(terminal.name)
        if hasattr(self, "properties"):
            dev_dict["PROPERTY"] = {}
            dev_dict["PROPERTY_LIST"] = {}
            for name, value in self.get_property():
                dev_dict["PROPERTY"][name] = value
                dev_dict["PROPERTY_LIST"].append(f"{name}={str(value)}")
        return dev_dict

class Terminal:
    def __init__(self, name, *, device=None, num=None):
        self.name   = name
        self.num    = num
        self.device = device

    def __str__(self):
        return self.name

class Res(Device):
    pass

class Mos(Device):
    pass

class Cap(Device):
    pass

class Ind(Device):
    pass

class Subckt:
    def __init__(self, name):
        self.name = name

    def add_port(self, port):
        if not hasattr(self, "ports"):
            self.ports = []
        if isinstance(port, list):
            for num, pt in enumerate(port):
                self.ports.append(Port(pt, subckt=self, num=num))
        else:
            self.ports.append(Port(port, subckt=self, num=len(self.ports)))

    def add_property(self, name, value):
        if not hasattr(self, "properties"):
            self.properties = {}
        self.properties[name] = value

    def get_net(self):
        return self.nodes

    # add device, node and neighbor
    def add_device(self, device):
        # add device
        if not hasattr(self, "devices"):
            self.devices = []
        self.devices.append(device)
        device.in_subckt(self)

        # node connect to device
        if not hasattr(self, "nodes"):
            self.nodes = Node()
        for terminal in device.get_terminal():
            self.nodes.append(terminal)

        # add neighbor
        for terminal in device.get_terminal():
            for term in self.nodes[terminal.name]:
                # term.device: neighbor device
                if device == term.device:
                    continue
                device.add_edge(
                    from_terminal = terminal,
                    to_terminal   = term,
                    )

    # remove device, node and neighbor
    def remove_device(self, device):
        # remove device
        self.devices.remove(device)

        # remove node
        self.nodes.remove(device)

        # remove neighbor
        for dev in list(device.get_neighbor().keys())[:]:
            device.remove_edge(dev)

    def get_device(self, name=None):
        if name is None:
            return self.devices
        if name in self:
            return self[name]
        return None

    def set_netlist(self, netlist):
        self.netlist = netlist

    def __iter__(self):
        self.iter = iter(self.devices)
        return self

    def __next__(self):
        return next(self.iter)

    def __iadd__(self, device):
        self.add_device(device)
        return self

    def __isub__(self, device):
        self.remove_device(device)
        return self

    def __contains__(self, device_name):
        for device in self.devices:
            if device.name == device_name:
                return True
        return False

    def __getitem__(self, device_name):
        for device in self.devices:
            if device.name == device_name:
                return device
        return None

    def __str__(self):
        msg = f".SUBCKT {self.name}"
        if hasattr(self, "ports"):
            for port in self.ports:
                msg += f" {port}"
        if hasattr(self, "properties"):
            for p_name, p_value in self.properties.items():
                msg += f" {p_name}={p_value}"
        if hasattr(self, "devices"):
            for device in self.devices:
                msg += f"\n{device}"
        msg += f"\n.ENDS {self.name}\n"
        return msg

    ############## subckt API #####################
    def floating_net(self, global_net=[]):
        floating_nets = set()
        for node_name, terminals in self.nodes:
            if len(terminals) == 1:
                if global_net and node_name in global_net:
                    # one terminal connect to global net
                    pass
                elif node_name.lower() in [t.name.lower() for t in self.ports]: # Port.name
                    # one terminal connect to subckt port
                    pass
                else:
                    floating_nets.add(node_name)
        return floating_nets

    def replace_symbol(self, find, replace):
        replace_ok = False
        for device in self:
            if not hasattr(device, "symbol"):
                continue
            if device.symbol.name == find:
                replace_ok = True
                device.set_symbol(replace)
        return replace_ok

    def is_connected(self, device_name1, device_name2):
        device1 = self.get_device(device_name1)
        device2 = self.get_device(device_name2)
        if not device1 or not device2:
            return None
        if device1.get_edges(device2):
            return True
        return False

    def highlight_net(self, net_name):
        for node_name, terminals in self.nodes:
            if node_name == net_name:
                return terminals
        return None

    # graph search
    def find_inverter(self):
        inverters = []
        visited   = {}
        for device in self:
            visited[device] = False
        def dfs(device, path=None):
            if path is None:
                path = []
            nonlocal visited, inverters

            path.append(device)
            visited[device] = True
            if len(path) >= 2:
                device1 = path[-2]
                device2 = path[-1]
                if  (
                        hasattr(device1, "symbol") and hasattr(device1, "symbol") and \
                        device1.symbol.name != device2.symbol.name) and \
                    (
                        len(device1.get_terminal()) == len(device2.get_terminal()) == 4) and \
                    (
                        device1.get_terminal()[0].name == device2.get_terminal()[0].name and \
                        device1.get_terminal()[1].name == device2.get_terminal()[1].name and \
                        device1.get_terminal()[2].name != device2.get_terminal()[2].name) \
                :
                    inverter = set(path[len(path)-2:len(path)])
                    if not inverters:
                        inverters.append(inverter)
                    else:
                        found = 1
                        for _inverter in inverters:
                            if _inverter == inverter:
                                found = 0
                        if found:
                            inverters.append(inverter)
            for neighbor_device in device.get_neighbor().keys():
                if not visited[neighbor_device]:
                    dfs(neighbor_device, path)
            visited[device] = False
            path.pop(-1)
        for device in self:
            dfs(device)
        return inverters

    @classmethod
    def from_dict(self, subckt_dict):
        subckt = self(subckt_dict["NAME"])
        for dev_dict in subckt_dict["DEVICE"].values():
            subckt += Device.from_dict(dev_dict)
        for port in subckt_dict["PORT"]:
            subckt.add_port(port)
        if "PROPERTY" in subckt_dict:
            for name, value in subckt_dict["PROPERTY"].items():
                subckt.add_property(name, value)
        return subckt

    def as_dict(self):
        subckt_dict = {}
        subckt_dict["NAME"] = self.name
        for port in self.ports:
            subckt_dict.setdefault("PORT", []).append(port.name)
        subckt_dict["DEVICE"] = {}
        for device in self:
            subckt_dict["DEVICE"][device.name] = device.as_dict()
        subckt_dict["NODE"] = self.nodes.as_dict()
        if hasattr(self, "properties"):
            subckt_dict["PROPERTY"] = {}
            for name, value in self.properties.items():
                subckt_dict["PROPERTY"][name] = value
        return subckt_dict

class Node: # net
    def __init__(self):
        self.node = {}

    def append(self, terminal):
        # "terminal" instance include device info
        self.node.setdefault(terminal.name, []).append(terminal)

    def remove(self, device):
        remove_node_names = []
        for node_name, terminals in self:
            for terminal in terminals[:]:
                if terminal == device:
                    terminals.remove(device)
            if not terminals:
                remove_node_names.append(node_name)
        for node_name in remove_node_names:
            del self.node[node_name]

    def __str__(self):
        msg_line = []
        for node_name, terminals in self:
            msg_line.append(f"{node_name}: {', '.join(['#'.join([terminal.device.name, str(terminal.num)]) for terminal in terminals])}")
        return "\n".join(msg_line)

    def __iter__(self):
        self.iter = iter(self.node)
        return self

    def __next__(self):
        key = next(self.iter)
        return key, self.node[key]

    def __delitem__(self, node_name):
        del self.node[node_name]

    def __getitem__(self, node_name):
        if node_name in self.node:
            return self.node[node_name]
        return None

    def __contains__(self, node_name):
        return node_name in self.node

    def __isub__(self, device):
        self.remove(device)
        return self

    def as_dict(self):
        node_dict = {}
        for node_name, terminals in self:
            for terminal in terminals:
                node_dict.setdefault(node_name, []).append(terminal.device.name)
        return node_dict

class Port:
    def __init__(self, name, subckt, num):
        self.name   = name
        self.subckt = subckt
        self.num    = num

    def __str__(self):
        return self.name

if __name__ == "__main__":
    r1 = Res(name="R1")
    r2 = Res(name="R2")

    c1 = Cap(name="C1")
    c2 = Cap(name="C2")

    l1 = Ind(name="L1")
    l2 = Ind(name="L2")

    d1 = Device("nmos1")
    d1.set_symbol("nmos")
    d1.add_terminal("GND")
    d1.add_terminal("VSS")
    d1.add_terminal("A")
    print(d1.get_terminal())
    print(d1)

    d2 = Device("pmos2")
    d2.set_symbol("pmos")
    d2.add_terminal("A")
    d2.add_terminal("GND")
    d2.add_terminal("VSS")
    print(d2.get_terminal())
    print(d2)

    d3 = Device("pmos3")
    d3.set_symbol("pmos")
    d3.add_terminal("A")
    d3.add_terminal("A")
    d3.add_terminal("VSS")

    # dict convert to Device
    device_data = {
        "NAME" : "pmos4",
        "SYMBOL" : "pmos",
        "PORT" : ["A", "B", "C", "VSS"],
    }
    d4 = Device.from_dict(device_data)
    print(device_data)
    print(d4.as_dict())

    ckt1 = Subckt("OR2")
    ckt1.add_port("A")
    ckt1.add_port("B")
    ckt1 += d1
    ckt1 += d2
    ckt1 += d3
    # ckt1.add_device(d1)
    print(ckt1)
    print(ckt1["nmos1"])
    print(ckt1.nodes)
    print(d1.get_neighbor())
    print(d2.get_neighbor())

    pprint(ckt1.as_dict())
    print("######## after remove #########")
    ckt1 -= d2
    print(ckt1)
    print(ckt1.nodes)
    print(d1.get_neighbor())
    print(d2.get_neighbor())
    # print(ckt1.floating_net())
    # print(ckt1.floating_net(global_net=["GND", "VSS"]))