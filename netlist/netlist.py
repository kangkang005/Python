import re, os, json, sys
from pprint import *

# nested dict
class DD(dict):
    def __init__(self, *args, **kwargs):
        super(type(self), self).__init__(*args, **kwargs)

    def __getitem__(self, key):
        if key in self:
            return super().__getitem__(key)
        return self.setdefault(key, type(self)())

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

ENG = {
    "" : 1,
    "a" : 1e-18,
    "f" : 1e-15,
    "p" : 1e-12,
    "n" : 1e-9,
    "u" : 1e-6,
    "m" : 1e-3,
    "k" : 1e3,
    "x" : 1e6,
    "g" : 1e9,
    "A" : 1e-18,
    "F" : 1e-15,
    "P" : 1e-12,
    "N" : 1e-9,
    "U" : 1e-6,
    "M" : 1e-3,
    "K" : 1e3,
    "X" : 1e6,
    "G" : 1e9,
    "meg": 1e6,
}

qrENG = re.compile(rf"^([+-]?\d+(?:\.\d+)?)({'|'.join([key for key in ENG.keys() if key])})$")
qrINC = re.compile(r"\.[inc|include|lib]\w*\s+[\"\'](.+)[\"\']", re.I)

def float2eng(val, *, fmt="%.3f", notation=None):
    val = float(re.sub(r"^[+-]", "", str(val)))
    symbol = ""
    if mat := re.match(r"([+-])", str(val)):
        symbol = mat.group(1)
    eng = ""
    if val >= 1:
        if val >= ENG['g']:
            eng = 'g'
        elif val >= ENG['x']:
            eng = 'x'
        elif val >= ENG['k']:
            eng = 'k'
        else:
            eng = ""
    else:
        if val < ENG['f']:
            eng = 'a'
        elif val < ENG['p']:
            eng = 'f'
        elif val < ENG['n']:
            eng = 'p'
        elif val < ENG['u']:
            eng = 'n'
        elif val < ENG['m']:
            eng = 'u'
        else:
            eng = 'm'
    if not notation and notation in ENG:
        eng = notation

    val = fmt % (val/ENG[eng])
    val = re.sub(r"\.?0+$", "", val)
    return symbol+val+eng

# print(float2eng(-12e-3))

def eng2float(eng):
    if mat := re.match(qrENG, eng):
        return float(mat.group(1)) * ENG[mat.group(2)]
    else:
        return eng

# print(eng2float("-12m"))
# print(eng2float("-12"))

class Netlist():
    def __init__(self, *, file=None, text=None):
        self.file = file
        self.text = text
        if not self.loadNetlist():
            sys.exit()

    def loadNetlist(self):
        if self.file and not os.path.exists(self.file):
            print(f"not found file: {self.file}")
            return 0

        if self.file:
            with open(self.file, "r") as FILE:
                self.text = FILE.read()
        lines = []
        for line in self.text.split("\n"):
            line = line.strip()
            if re.match(r"^\s*$", line):
                continue
            if re.match(r"^\*", line):
                continue
            if mat := re.match(r"^\+(\s*.*)", line):
                lines[-1] += " " + mat.group(1)
            else:
                lines.append(line)
        netlist            = DD()
        param              = DD()
        subckt_info        = DD()
        device_sequence    = 1
        subckt_sequence    = 1
        for line in lines:
            if re.match(r"\.param\s+(.+)", line, re.I):
                pass
            elif mat := re.match(r"\.global\s+(.+)", line, re.I):
                param.setdefault("GLOBAL", []).extend(mat.group(1).split())
            elif mat := re.match(r"\.connect\s+(\S+)\s(\S+)$", line, re.I):
                param["CONNECT"][mat.group(1)] = mat.group(2)
            elif mat := re.match(qrINC, line):
                netlist.setdefault("INCLUDE", []).append({
                    "PATH"      : mat.group(1),
                    "NETLIST"   : Netlist(file=mat.group(1)),
                })
            elif mat := re.match(r"\.SUBCKT", line, re.I):
                subckt_statement = re.split("\s+", line)
                subckt_statement.pop(0)
                subckt_info["NAME"] = subckt_statement.pop(0)
                for item in subckt_statement:
                    if mat := re.match(r"^(\S+)\=(\S+)$", item):
                        subckt_info["PROPERTY"][mat.group(1)] = mat.group(2)
                    else:
                        subckt_info.setdefault("PORT", []).append(item)
                subckt_info["SEQUENCE"] = subckt_sequence
                subckt_sequence += 1
            elif re.match(r"^\.ENDS\s*", line, re.I):
                netlist["SUBCKT"][subckt_info["NAME"]] = subckt_info
                subckt_info = DD()
            elif "NAME" in subckt_info:
                if re.match(r"\s*\.", line, re.I):
                    continue
                device = self.parse_device(line=line)
                if not device:
                    print(f"parse device fail! line: {line}")
                    return
                device["SEQUENCE"] = device_sequence
                device_sequence += 1
                subckt_info["DEVICE"][device["NAME"]] = device
            elif mat := re.match(r"\.(\S+)\s*(.+)", line, re.I):
                param[mat.group(1)] = mat.group(2)
        netlist["PARAM"] = param
        self.DATA = netlist
        self.build_node()
        return 1

    def __iter__(self):
        self.iter = iter(self.DATA["SUBCKT"])
        return self

    def __next__(self):
        key = next(self.iter)
        return key, self.DATA["SUBCKT"][key]

    def parse_device(self, line):
        device_statement = re.split("\s+", line)
        if len(device_statement) < 2:
            print(f"Device statement error: {line}")
            return
        device = DD()
        device["NAME"] = device_statement[0]
        device["PROPERTY_LIST"] = []
        if mat := re.match(r"^[RC].*", device["NAME"], re.I):
            if len(device_statement) < 3:
                print(f"Device statement error: {device_statement}")
                return
            device["PORT"]          = device_statement[1:2]
            device["PROPERTY_LIST"] = device_statement[3:]
            device["SYMBOL"]        = device_statement[0][0:1]
        else:
            symbol_pos = 0
            for index in range(len(device_statement)-1, 0, -1):
                if re.match(r"^(\S+)\=(\S+)$", device_statement[index], re.I) or re.match(r"^\$.*", device_statement[index], re.I) or is_float(device_statement[index]):
                    continue
                else:
                    symbol_pos = index
                    break
            if symbol_pos == 0:
                print(f"Device statement error: {line}")
                return
            for index in range(1, len(device_statement)):
                if index < symbol_pos:
                    device.setdefault("PORT", []).append(device_statement[index])
                elif index == symbol_pos:
                    device["SYMBOL"] = device_statement[index]
                else:
                    device.setdefault("PROPERTY_LIST", []).append(device_statement[index])
        for property_item in device["PROPERTY_LIST"]:
            if mat := re.match(r"^(\S+)\=(\S+)$", property_item, re.I):
                device["PROPERTY"][mat.group(1)] = mat.group(2)
        return device

    def build_node(self, stop_cells=None):
        if stop_cells is None:
            stop_cells = []
        for _, subckt in self:
            if list(filter(lambda x: re.match(rf"^\Q{subckt['NAME']}\E$", x, re.I), stop_cells)):
                continue
            node = {}
            for device in subckt["DEVICE"].values():
                for PORT in device["PORT"]:
                    node.setdefault(PORT, []).append(device["NAME"])
            subckt["NODE"] = node

    def get_subckt(self, name=""):
        all_subckts = list(self.DATA["SUBCKT"].keys())
        if name in self.DATA["SUBCKT"]:
            return self.DATA["SUBCKT"][name]
        if "INCLUDE" in self.DATA:
            for inc in self.DATA["INCLUDE"]:
                netlist = inc['NETLIST']
                subckt = netlist.get_subckt(name)
                if name and subckt:
                    return subckt
                if name == "":
                    all_subckts += subckt
        if name:
            return 0
        return all_subckts

    def __getitem__(self, name):
        return self.get_subckt(name)

    def is_mos(self, mos):
        if re.match(r"m", mos["NAME"], re.I) and re.match(r"p|n", mos["SYMBOL"], re.I):
            return 1
        return 0

    def are_diff_mos(self, mos1, mos2):
        if mos1["SYMBOL"] != mos2["SYMBOL"]:
            return 1
        return 0

    def get_mos_port(self, mos):
        if not self.is_mos(mos=mos):
            return
        return {
            "D" : mos["PORT"][0],
            "G" : mos["PORT"][1],
            "S" : mos["PORT"][2],
            "B" : mos["PORT"][3],
        }

    def get_child_device_path(self,
        subckt_name,
        filter     = "",
        stop_level = -1
    ):
        result = {}
        def dfs(
            subckt_name,
            filter      = "",
            deep_level  = 1,
            path        = "",
            stop_level = -1,
        ):
            nonlocal result
            if not path:
                path = subckt_name
            subckt = self.get_subckt(name=subckt_name)
            if not subckt:
                return
            if stop_level > -1 and deep_level > stop_level:
                return
            for device in sorted(subckt["DEVICE"].values(), key=lambda s: s["SEQUENCE"]):
                current_path = f"{path}.{device['NAME']}"
                is_subckt = 1 if self.get_subckt(name=device["SYMBOL"]) else 0
                if is_subckt and filter and re.search(filter, device["SYMBOL"], re.I):
                    continue
                device_info = {
                    "NAME"      : device["NAME"],
                    "SYMBOL"    : device["SYMBOL"],
                    "IS_SUBCKT" : is_subckt,
                    "PORT"      : device["PORT"],
                    "PARENT"    : path,
                    "SEQUENCE"  : len(result),
                    "DEEP_LEVEL": deep_level,
                }
                result[current_path] = device_info
                dfs(
                    subckt_name = device["SYMBOL"],
                    filter      = filter,
                    deep_level  = deep_level+1,
                    path        = current_path,
                    stop_level = stop_level,
                )
            return result
        if self.get_subckt(name=subckt_name):
            result[subckt_name] = {
                "NAME"      : subckt_name,
                "SYMBOL"    : subckt_name,
                "IS_SUBCKT" : 1,
                "SEQUENCE"  : len(result),
                "DEEP_LEVEL": 0,
                "PARENT"    : "",
            }
        dfs(
            subckt_name = subckt_name,
            filter      = filter,
            stop_level  = stop_level,
        )
        return result

    def expand_subckt(self,
        subckt_name,
        deep_level = 0,
        stop_level = -1
    ):
        subckt = self.get_subckt(name=subckt_name)
        if not subckt:
            return
        if not deep_level:
            print(" " * deep_level * 2 + subckt["NAME"],end=" ")
            print(" ".join(subckt["PORT"]))
        for device in sorted(subckt["DEVICE"].values(), key=lambda s: s["SEQUENCE"]):
            if stop_level != -1 and stop_level == deep_level+1:
                return
            print(" " * (deep_level+1) * 2 + device["NAME"], end=" ")
            print(" ".join(device["PORT"]), end=" ")
            print(device["SYMBOL"], end=" ")
            if "PROPERTY_LIST" in device:
                print(" ".join(device["PROPERTY_LIST"]), end=" ")
            print("")
            self.expand_subckt(
                subckt_name = device["SYMBOL"],
                deep_level  = deep_level+1,
                stop_level  = stop_level,
            )

    def print_netlist(self, subckt_name, stop_level=-1):
        subckt = self.get_subckt(name=subckt_name)
        if not subckt:
            return

        # bfs
        visited = {}
        queue = [(subckt, 0)]
        while(queue):
            cur_subckt, deep_level = queue.pop(0)
            if stop_level != -1 and deep_level >= stop_level:
                continue
            line_list = []
            line_list.append(".SUBCKT")
            line_list.append(cur_subckt["NAME"])
            line_list.append(" ".join(cur_subckt["PORT"]))
            if "PROPERTY" in cur_subckt:
                for k,w in cur_subckt["PROPERTY"].items():
                    line_list.append(f"{k}={w}")
            print(" ".join(line_list))
            for device in sorted(cur_subckt["DEVICE"].values(), key=lambda s: s["SEQUENCE"]):
                line_list = []
                line_list.append(device["NAME"])
                line_list.append(" ".join(device["PORT"]))
                line_list.append(device["SYMBOL"])
                if "PROPERTY_LIST" in device:
                    line_list.append(" ".join(device["PROPERTY_LIST"]))
                print(" ".join(line_list))
                subckt = self.get_subckt(name=device["SYMBOL"])
                if subckt:
                    if not device["SYMBOL"] in visited:
                        visited[device["SYMBOL"]] = 1
                        subckt = self.get_subckt(name=device["SYMBOL"])
                        queue.append((subckt, deep_level+1))
            print(f".ENDS {cur_subckt['NAME']}")

    def replace_symbol(self, subckt_name, old, new, need_print=1):
        subckt = self.get_subckt(name=subckt_name)
        if not subckt:
            return
        def dfs(subckt_name, old, new):
            subckt = self.get_subckt(name=subckt_name)
            if not subckt:
                return
            for device in sorted(subckt["DEVICE"].values(), key=lambda s: s["SEQUENCE"]):
                # replace symbol
                if device["SYMBOL"] == old:
                    device["SYMBOL"] = new
                dfs(
                    subckt_name = device["SYMBOL"],
                    old         = old,
                    new         = new,
                    need_print  = need_print,
                )
        dfs(
            subckt_name = subckt_name,
            old         = old,
            new         = new,
        )
        if need_print:
            self.print_netlist(subckt_name=subckt_name)

    def replace_net_name(self, subckt_name, old, new, need_print=1):
        subckt = self.get_subckt(name=subckt_name)
        if not subckt:
            return
        if old in subckt["PORT"]:
            subckt["PORT"] = [new if i == old else i for i in subckt["PORT"]]
        for device in sorted(subckt["DEVICE"].values(), key=lambda ckt: ckt["SEQUENCE"]):
            if old in device["PORT"]:
                device["PORT"] = [new if i == old else i for i in device["PORT"]]
        if need_print:
            self.print_netlist(subckt_name=subckt_name, stop_level=1)

    def add_property(self, subckt_name, name, property_list=[]):
        subckt = self.get_subckt(name=subckt_name)
        if not subckt:
            return
        for device in sorted(subckt["DEVICE"].values(), key=lambda ckt: ckt["SEQUENCE"]):
            if device["NAME"] == name and property_list:
                device["PROPERTY_LIST"].extend(property_list)
                for property in property_list:
                    k, v = property.split("=")
                    device["PROPERTY"][k] = v
        self.print_netlist(subckt_name=subckt_name, stop_level=1)

    def get_sibling_device(self, subckt_name, device_name):
        subckt = self.get_subckt(name=subckt_name)
        if not subckt:
            return
        sibling_devices = []
        for port, devices in subckt["NODE"].items():
            if device_name in devices and len(devices) > 1:
                for dev in devices:
                    if dev == device_name or dev in sibling_devices:
                        continue
                    sibling_devices.append(dev)
        return sibling_devices

    def is_connect(self, subckt_name, device1, device2):
        subckt = self.get_subckt(name=subckt_name)
        if not subckt:
            return
        for port, devices in subckt["NODE"].items():
            if device1 in devices and device2 in devices:
                return 1
        return 0

    def bfs_traverse(self, subckt_name, device_name):
        subckt = self.get_subckt(name=subckt_name)
        if not subckt:
            return

        visited = []
        queue = [(device_name, 0)]
        while(queue):
            dev_name, deep_level = queue.pop(0)
            print(" " * 2 * deep_level + dev_name)
            for sibling_device in self.get_sibling_device(subckt_name, dev_name):
                if not sibling_device in visited:
                    queue.append((sibling_device, deep_level+1))
                    visited.append(sibling_device)

    def dfs_traverse(self, subckt_name, device_name, visited=[], deep_level=0):
        subckt = self.get_subckt(name=subckt_name)
        if not subckt:
            return
        print(" " * 2 * deep_level + device_name)
        for sibling_device in self.get_sibling_device(subckt_name, device_name):
            if not sibling_device in visited:
                visited.append(sibling_device)
                deep_level += 1
                self.dfs_traverse(subckt_name=subckt_name, device_name=sibling_device, visited=visited, deep_level=deep_level)
                deep_level -= 1

    def get_floating_port(self, subckt_name, filter=r"VDD|VSS|GND"):
        subckt = self.get_subckt(name=subckt_name)
        if not subckt:
            return
        floating_infos = []
        for port, devices in subckt["NODE"].items():
            if port in subckt["PORT"]:
                if len(devices) == 0:
                    floating_infos.append({
                        "port" : port,
                    })
            elif len(devices) < 2:
                if re.match(filter, port, re.I):
                    continue
                floating_infos.append({
                    "port" : port,
                    "device" : devices[0],
                })
        return floating_infos

    def is_floating_port(self, subckt_name, port):
        subckt = self.get_subckt(name=subckt_name)
        if not subckt:
            return
        if port in subckt["PORT"]:
            if len(subckt["NODE"][port]) > 0:
                return 0
            else:
                return 1
        elif port in subckt["NODE"]:
            if len(subckt["NODE"][port]) > 1:
                return 0
            else:
                return 1
        return -1

    def get_floating_device(self, subckt_name):
        subckt = self.get_subckt(name=subckt_name)
        if not subckt:
            return
        floating_devices = []
        for device in sorted(subckt["DEVICE"].values(), key=lambda ckt: ckt["SEQUENCE"]):
            is_floating_device = 1
            for port in device["PORT"]:
                if len(subckt["NODE"][port]) > 1:
                    is_floating_device = 0
                    break
            if is_floating_device:
                floating_devices.append(device["NAME"])
        return floating_devices

    # TODO: if device_name not in subckt_name
    def is_floating_device(self, subckt_name, name):
        subckt = self.get_subckt(name=subckt_name)
        if not subckt:
            return
        for port, devices in subckt["NODE"].items():
            if name in devices and len(devices) > 1:
                return 0
        return 1

    def get_other_port(self, subckt_name, device_name, port):
        subckt = self.get_subckt(name=subckt_name)
        if not subckt:
            return
        other_ports = []
        for device in sorted(subckt["DEVICE"].values(), key=lambda ckt: ckt["SEQUENCE"]):
            if device["NAME"] == device_name:
                for p in device["PORT"]:
                    if not p == port:
                        other_ports.append(p)
        return other_ports

    # top cell is only called firstly
    # create netlist tree
    def get_top_cell(self):
        count = {}
        for subckt_name in self.get_subckt():
            subckt = self.get_subckt(name=subckt_name)
            if not subckt["NAME"] in count:
                count[subckt["NAME"]] = 0
            count[subckt["NAME"]] += 1
            for device in sorted(subckt["DEVICE"].values(), key=lambda ckt: ckt["SEQUENCE"]):
                if not device["SYMBOL"] in count:
                    count[device["SYMBOL"]] = 0
                count[device["SYMBOL"]] += 1
        return [name for name, num in count.items() if num == 1]

    def get_top_cell(self):
        device_subckt_map = {}
        for subckt_name in self.get_subckt():
            subckt = self.get_subckt(name=subckt_name)
            for device in sorted(subckt["DEVICE"].values(), key=lambda ckt: ckt["SEQUENCE"]):
                device_subckt_map[device["SYMBOL"]] = subckt["NAME"]
        find_top_cells = []
        for subckt_name in self.get_subckt():
            subckt = self.get_subckt(name=subckt_name)
            if not subckt["NAME"] in device_subckt_map:
                find_top_cells.append(subckt["NAME"])
        return find_top_cells

    def instance_top_cell(self, begin=0):
        inst_list = []
        for subckt_name in self.get_top_cell():
            subckt = self.get_subckt(name=subckt_name)
            inst_list.append(f"X{begin} {' '.join(subckt['PORT'])} {subckt['NAME']}")
            begin += 1
        return inst_list

def get_subckt_list(netlist_path):
    with open(netlist_path, "r") as r_netlist:
        netlist_text = r_netlist.read()

    netlist = DD()
    for find_subckt_block in re.finditer(rf"\.subckt\s+(\S+).+\n(?:\+.+\n)*((?:.*\n)+?)\.end.+", netlist_text, re.I):
        netlist[find_subckt_block[1]]["subckt"] = {
            "subckt" : find_subckt_block[0],
            "device" : find_subckt_block[2],
            }
    return netlist

def inst_subckt(netlist_path, subckt_name):
    with open(netlist_path, "r") as r_netlist:
        netlist_text = r_netlist.read()

    if search_defined_subckt := re.search(rf"\.subckt\s+({subckt_name})(.+\n(?:\+.+\n)*)", netlist_text, re.I):
        return "X1" + search_defined_subckt[2] + "+ " + search_defined_subckt[1]

def remove_continuation(netlist_path):
    with open(netlist_path, "r") as r_netlist:
        netlist_text = r_netlist.read()

    return re.sub(r"\s*\n\+\s*", " ", netlist_text)

if 0:
    netlist = Netlist(file="netlist.cir")
    subckt = netlist.get_subckt(name="yufei")
    # print(json.dumps(subckt, indent=2))
    path = netlist.get_child_device_path(subckt_name="yufei")
    print(json.dumps(path, indent=2))
    netlist.expand_subckt(subckt_name="yufei")

if 0:
    netlist = Netlist(file="adder.cir")
    subckt = netlist.get_subckt(name="DOT")
    # print(json.dumps(subckt, indent=2))
    path = netlist.get_child_device_path(subckt_name="DOT")
    # print(json.dumps(path, indent=2))
    # netlist.expand_subckt(subckt_name="DOT")
    netlist.print_netlist(subckt_name="DOT")
    # netlist.replace_symbol(subckt_name="DOT", old="lpfet", new="test")
    # netlist.replace_symbol(subckt_name="DOT", old="lnfet", new="test")
    netlist.replace_net_name(subckt_name="DOT", old="P1G2", new="test")
    netlist.add_property(subckt_name="DOT", name="XOR1", property_list=["L='L'"])
    print(netlist.get_sibling_device(subckt_name="DOT", device_name="XOR1"))
    netlist.bfs_traverse(subckt_name="OR2", device_name="xpmos9")
    netlist.dfs_traverse(subckt_name="OR2", device_name="xpmos9")
    print(netlist.get_floating_port(subckt_name="OR2"))
    print(netlist.is_floating_port(subckt_name="OR2", port="X3"))
    print(netlist.is_floating_port(subckt_name="OR2", port="X32"))
    print(netlist.get_floating_device(subckt_name="OR2"))
    print(netlist.is_floating_device(subckt_name="OR2", name="xpmos11"))
    print()
    netlist.find_inverter(subckt_name="OR2")

    print(netlist.get_top_cell())
    print(netlist.instance_top_cell())
    subckt = netlist.get_subckt()
    pprint(subckt)

if 1:
    netlist = Netlist(file="adder.cir")
    path = netlist.get_child_device_path(subckt_name="DOT", stop_level=1)
    print(json.dumps(path, indent=2))

if 1:
    netlist = get_subckt_list("adder.cir")
    pprint(netlist)