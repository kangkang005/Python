import re, os, json, sys, math
import numpy as np
from typing import List, Optional, Union, Generator

class Testbench():
    def __init__(self,
                 *,
                 path = None,
                 lib_corner = None,
                 layer = 0,
                 param_queue = None,
                 ) -> None:
        self.lines = []
        self.line_no = 0
        self.data = {}
        self.layer = layer
        self.lib_corner = lib_corner
        self.param_queue = param_queue
        self.data["PATH"] = path
        self.data["LAYER"] = self.layer
        if path:
            if os.path.exists(path) and os.access(path, os.R_OK):
                with open(path, "r") as r_testbench:
                    for line in r_testbench:
                        self.lines.append(line.strip())
            else:
                print(f"Path maybe not exist or readable for you: {path}")
                sys.exit()

    def parse_testbench(self, lines = []) -> None:
        if len(lines):
            self.lines = lines
        while(self.line_no < len(self.lines)):
            # try:
            self.eat_null_line()
            self.eat_comment_line()
            self.parse_lib(param_queue = self.param_queue)
            self.parse_param()
            self.parse_if()
            self.parse_meas()
            self.line_no += 1
            # except IndexError as e:
            #     pass

    def get_data(self):
        return self.data

    def parse_order(self, exclude=[]):
        self.eat_null_line()
        self.eat_comment_line()
        if not "lib" in exclude:
            self.parse_lib()
        self.parse_param()
        self.parse_if()
        self.parse_meas()

    def parse_lib(self,
                  *,
                  corner_key = None,
                  param_queue = None,
                  in_lib_block = False,
                  ):
        # param_queue include current and previous layer param
        if not param_queue:
            param_queue = []
        line = self.get_cur_line_with_plus()
        lib = {}
        if search_lib := re.search("^\s*\.(lib|inc)\s+[\'\"](.+)[\'\"](?:\s+(\S+))?", line, re.I):
            token, path, corner = search_lib.groups()
            lib = {
                "PATH" : path
            }
            if corner:
                lib["CORNER"] = corner
            if os.path.exists(path) and os.access(path, os.R_OK):
                self.layer += 1
                # merge current and prev layer
                param_queue.append(
                    self.get_data()["PARAM"] if "PARAM" in self.get_data() else {}
                    )
                tb = Testbench(
                    path = path,
                    lib_corner = corner,
                    layer = self.layer,
                    param_queue = param_queue
                    )
                tb.parse_testbench()
                lib["DATA"] = tb.get_data()
                self.layer -= 1
                param_queue.pop(-1)
            # self.data[token.upper()]
            # print(lib)
            # print(corner_key)
            if not corner_key:
                self.data.setdefault(token.upper(), []).append(lib)
        elif search_lib := re.search("^\s*\.(lib)\s+(\S+)\s*$", line, re.I):
            token, corner = search_lib.groups()
            # eat other lib block
            if self.lib_corner and self.lib_corner.lower() != corner.lower():
                while(not re.search("^\s*\.(endl)\s+(%s)\s*$"%corner, line, re.I)):
                    # print(line)
                    self.line_no += 1
                    line = self.get_cur_line_with_plus()
                self.line_no += 1
                return

            self.line_no += 1
            # queue.append(corner)
            self.parse_lib(
                corner_key = corner,
                param_queue = param_queue,
                in_lib_block = True,
                )
        elif search_lib := re.search("^\s*\.(endl)\s+(%s)\s*$"%corner_key, line, re.I):
            # self.line_no += 1
            return
        elif in_lib_block:
            # print(corner_key)
            # print(line)
            # self.parse_order(exclude=["lib"])
            # self.eat_null_line()
            self.eat_comment_line()
            self.parse_param()
            self.parse_if()
            self.parse_meas()
            # print(self.get_cur_line_with_plus())
            self.line_no += 1
            self.parse_lib(
                corner_key = corner_key,
                param_queue = param_queue
                )
            # print(self.get_cur_line_with_plus())

    def eat_null_line(self):
        if not self.lines[self.line_no].strip():
            if self.line_no < len(self.lines)-1:
                self.line_no += 1

    def eat_comment_line(self):
        if self.lines[self.line_no].find("*") == 0:
            if self.line_no < len(self.lines)-1:
                self.line_no += 1

    def get_cur_line_with_plus(self):
        def merge_multi_line(lines):
            return " ".join([re.sub("^\s*(?:\+)|\s*$", "", line) for line in lines])

        # avoid IndexError: list index out of range
        if self.line_no == len(self.lines):
            self.line_no -= 1

        if re.search("^\s*\+", self.lines[self.line_no]):
            # backtrack until no plus, but pointer not move
            line_no = self.line_no
            while(re.search("^\s*\+", self.lines[line_no])):
                line_no -= 1
            return merge_multi_line(self.lines[line_no:self.line_no+1])
        else:
            # forward and pointer move until last plus
            if self.line_no == len(self.lines)-1:
                return self.lines[self.line_no]
            else:
                return merge_multi_line(self.eat_continuation_line())

    # def eat_continuation_line(self, results=[]), results will always point to same address
    def eat_continuation_line(self, results=None):
        if results is None:
            results = []
        results.append(self.lines[self.line_no])
        self.line_no += 1
        if self.line_no == len(self.lines) or not re.search("^\s*\+", self.lines[self.line_no]):
            self.line_no -= 1
            return results
        return self.eat_continuation_line(results)

    def parse_param(self):
        line = self.get_cur_line_with_plus()
        search_param = re.search("^\s*\.param", line, re.I)
        if not search_param:
            return
        params = re.findall(r"([^\s]+\s*=\s*(?:[\'\"].+?[\'\"]|[^\s]+))", line)
        if not params:
            return

        self.data.setdefault("PARAM", {})
        for param in params:
            split = re.split("\s*=\s*", param)
            self.data["PARAM"][split[0]] = split[1]

    def get_param(self, *, param = ""):
        all_params = {}
        def dfs(data):
            if "PARAM" in data:
                # update() function include deduplication
                all_params.update(data["PARAM"])
            if "LIB" in data:
                for lib in data["LIB"]:
                    if "DATA" in lib:
                        dfs(lib["DATA"])
        dfs(self.get_data())
        if param:
            if param in all_params:
                return all_params[param]
            return
        return all_params

    def get_meas(self, *, variable = ""):
        all_variables = []
        def dfs(data):
            nonlocal all_variables
            if "MEAS" in data:
                if all_variables:
                    # deduplicate
                    for meas in data["MEAS"]:
                        tmp_variable_list = [x["variable"] for x in all_variables]
                        try:
                            idx = tmp_variable_list.index(meas["variable"])
                            all_variables[idx] = meas
                        except:
                            all_variables.append(meas)
                else:
                    all_variables += data["MEAS"]
            if "LIB" in data:
                for lib in data["LIB"]:
                    if "DATA" in lib:
                        dfs(lib["DATA"])
        dfs(self.get_data())
        if variable:
            for meas in all_variables:
                if variable == meas["variable"]:
                    return meas
            return
        return all_variables

    def search_related_param(self, param_name):
        result = []
        def remove_string_symbol(string):
            return string.strip("\'").strip("\"")
        params = self.get_param()
        meas_list = self.get_meas()
        def dfs(param_name):
            if params and param_name in params:
                if result and param_name in [x["param_name"] for x in result]:
                    # deduplicate
                    return
                result.append({
                    "param_name" : param_name,
                    "from" : "param",
                })
                parse_exp = ParseExpProc(remove_string_symbol(params[param_name]))
                parse_exp.parse()
                vars = parse_exp.get_vars()
                if not vars:
                    return
                vars = [x[1] for x in vars]
                for _var in vars:
                    dfs(_var)
            elif meas_list:
                for meas in meas_list:
                    if param_name in meas["variable"]:
                        if result and param_name in [x["param_name"] for x in result]:
                            # deduplicate
                            return
                        result.append({
                            "param_name" : param_name,
                            "from" : "meas",
                        })
                        if not "param" in meas:
                            return
                        parse_exp = ParseExpProc(remove_string_symbol(meas["param"]))
                        parse_exp.parse()
                        vars = parse_exp.get_vars()
                        if not vars:
                            return
                        vars = [x[1] for x in vars]
                        for _var in vars:
                            dfs(_var)
        dfs(param_name)
        return result

    # abandon
    # at current layer
    def depth_search_all_params(self, var):
        result = []
        def remove_string_symbol(string):
            return string.strip("\'").strip("\"")
        def dfs(var):
            if var in self.data["PARAM"]:
                if not var in result:
                    result.append(var)
                return
            for meas in self.data["MEAS"]:
                if not meas["variable"] == var:
                    continue
                if not var in result:
                    result.append(var)
                if not "param" in meas:
                    continue
                parse_exp = ParseExpProc(remove_string_symbol(meas["param"]), self.data["PARAM"])
                parse_exp.parse()
                vars = parse_exp.get_vars()
                if not vars:
                    continue
                vars = [x[1] for x in vars]
                for _var in vars:
                    dfs(_var)
        dfs(var)
        return result

    # not compress whitespace in quotation
    def compress_whitespace(self, line, compress_type=0):
        count = {k: 0 for k in ["single", "double"]}
        new_line = ""
        for char in line:
            if count["double"] == 0 and count["single"] == 0:
                if compress_type == 1:
                    # compress one whitespace before and after =
                    if not char.strip() and new_line != "" and new_line[-1] == "=":
                        # rise=   1  -> rise=1
                        continue
                    # add one whitespace before and after =
                    if char == "=" and new_line != "" and not new_line[-1].strip():
                        # rise   =1  -> rise=1
                        new_line = new_line[:-1]    # remove forward whitespace
                elif compress_type == 2:
                    if char == "=" and new_line != "" and new_line[-1].strip():
                        # rise=  1  -> rise =  1
                        new_line += " "
                    if char.strip() and new_line != "" and new_line[-1] == "=":
                        # rise  =1  -> rise  = 1
                        new_line += " "

            if char == "\"":
                count["double"] = 1-count["double"]
            if char == "\'":
                count["single"] = 1-count["single"]

            if count["double"] == 0 and count["single"] == 0:
                # outside double or single quotation
                if not char.strip() and new_line != "" and not new_line[-1].strip():
                    continue
            new_line += char
        return new_line

    def parse_meas(self):
        line = self.compress_whitespace(self.get_cur_line_with_plus(), compress_type=2).strip()
        meas = {}
        split_line = line.split(" ")
        search_meas = re.search("^\s*\.(meas\w*)", line, re.I)
        if not search_meas:
            return
        meas["token"] = split_line.pop(0)
        if split_line[0].lower() in ["tran", "dc", "ac"]:
            meas["simulation_type"] = split_line.pop(0)
        meas["variable"] = split_line.pop(0)
        meas["measurement_type"] = split_line.pop(0)
        if meas["measurement_type"] == "param":
            split_line.pop(0) # eat "="
            meas[meas["measurement_type"]] = " ".join(split_line)
        elif meas["measurement_type"] == "when":
            pass
        elif meas["measurement_type"] in ["trig", "min", "max", "avg"]:
            meas[meas["measurement_type"]] = {
                meas["measurement_type"] : split_line.pop(0)
            }
            measurement_type = meas["measurement_type"]
            while(split_line):
                key = split_line.pop(0)
                if not split_line[0] == "=":
                    measurement_type = key
                    meas[measurement_type] = {
                        measurement_type : split_line.pop(0)
                    }
                else:
                    split_line.pop(0) # eat "="
                    val = split_line.pop(0)
                    meas[measurement_type][key] = val

        if "MEAS" in self.data:
            # overwrite existing meas variable
            found = False
            for idx in range(len(self.data["MEAS"])):
                if self.data["MEAS"][idx]["variable"] == meas["variable"]:
                    found = True
                    self.data["MEAS"][idx] = meas
            if not found:
                self.data["MEAS"].append(meas)
        else:
            self.data.setdefault("MEAS", []).append(meas)

    def parse_if(
        self,
        /,
        level=0,
        result_if_expressions=None
        ):
        # >>>>>>> grammar <<<<<<<
        # S := if "("<booleanExp>")" <line>+ (elseif "("<booleanExp>")" <line>+)* (else <line>+)? endif
        if result_if_expressions is None:
            result_if_expressions = []
        # print(self.lines[self.line_no])
        if search_if := re.search("^\s*\.(if|elseif)\s*\((.+)\)", self.get_cur_line_with_plus(), re.I):
            expression = search_if.group(2)
            param_map = {}
            # upper layer param
            if self.param_queue:
                for par in self.param_queue:
                    param_map.update(par)
            # params of previous lines at current layer
            param_map.update(self.get_data()["PARAM"])
            result_if_expression = None
            try:
                result_if_expression = self.calculate_expression(expression, param_map)
            except SyntaxError as ae:
                raise SyntaxError(str(ae)+f" , in {self.data['PATH']}")
            if re.search("\.if", self.get_cur_line_with_plus(), re.I):
                level += 1
            result_if_expressions.append({
                "line"  : self.get_cur_line_with_plus(),
                "token" : search_if.group(1),
                "level" : level,
                "result": result_if_expression,
            })
            self.line_no += 1
            # print(level)
            # print(result_if_expressions)
            self.parse_if(level, result_if_expressions)
        elif search_if := re.search("\.(else)", self.get_cur_line_with_plus(), re.I):
            result_if_expressions.append({
                "line"  : self.get_cur_line_with_plus(),
                "token" : search_if.group(1),
                "level" : level,
                "result": True,
            })
            self.line_no += 1
            self.parse_if(level, result_if_expressions)
        elif search_if := re.search("\.endif", self.get_cur_line_with_plus(), re.I):
            # print(result_if_expressions)
            # if level > 1, pointer move next line. otherwise pointer stay
            if level > 1:
                self.line_no += 1
                while(result_if_expressions and level == result_if_expressions[-1]["level"]):
                    result_if_expressions.pop(-1)
                self.parse_if(level-1, result_if_expressions)
            else:
                if result_if_expressions:
                    result_if_expressions.pop(-1)
                return
        else:
            if not result_if_expressions:
                return
            result_if_expression = result_if_expressions[-1]
            # print(result_if_expressions)
            # print(self.lines[self.line_no])
            # print(level)
            if (result_if_expressions[-1]["result"] and (len(result_if_expressions) == 1 or \
                result_if_expressions[-2]["level"] != result_if_expressions[-1]["level"] or \
                (not result_if_expressions[-2]["result"] and result_if_expressions[-2]["level"] == result_if_expressions[-1]["level"]))):
                # judge if condition:
                # 1.current if condition must be True
                # 2.maybe if condition queue is only one
                # 3.maybe current if condition level differ from previous if condition level
                # 4.maybe previous if condition is False, and current if condition level is same as previous if condition level
                # at if block...
                self.eat_comment_line()
                self.parse_param()
                self.parse_meas()
                self.parse_lib(param_queue = self.param_queue)
            self.line_no += 1
            self.parse_if(level, result_if_expressions)

    def calculate_expression(self, expression, param_dict = {}):
        if not param_dict:
            param_dict = self.data["PARAM"]
        parse_expression = ParseExp(expression, param_dict)
        # return 1
        return parse_expression.parse()


class Unit:
    def __init__(self) -> None:
        """
        Do not return anything
        """
        self.ENG = {
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
        }
        self.qrENG = re.compile(r"^([+-]?\d+(?:\.\d+)?(?:[eE](?:[+-]?\d+))?)([" + "".join(self.ENG.keys()) + r"])$")

    def is_float(string: str) -> bool:
        try:
            float(string)
            return True
        except ValueError:
            return False

    def float2eng(self, val: float, fmt: str = "%.3f") -> str:
        mat = re.match(r"([+-])", str(val))
        symbol = ""
        if mat:
            symbol = mat.group(1)
        val = float(re.sub(r"^[+-]", "", str(val)))
        eng = ""
        if val >= 1:
            if val >= self.ENG['g']:
                eng = 'g'
            elif val >= self.ENG['x']:
                eng = 'x'
            elif val >= self.ENG['k']:
                eng = 'k'
            else:
                eng = ""
        elif val < 1 and val > 0:
            if val < self.ENG['f']:
                eng = 'a'
            elif val < self.ENG['p']:
                eng = 'f'
            elif val < self.ENG['n']:
                eng = 'p'
            elif val < self.ENG['u']:
                eng = 'n'
            elif val < self.ENG['m']:
                eng = 'u'
            else:
                eng = 'm'
        elif val == 0:
            eng = ''

        val = fmt % (val/self.ENG[eng])
        val = re.sub(r"\.?0+$", "", val)
        return symbol+val+eng

    def eng2float(self, eng: str) -> float:
        mat = re.match(self.qrENG, eng)
        if mat:
            return float(mat.group(1)) * self.ENG[mat.group(2)]
        return float(eng)

    # with decimal
    def bin2dec(self, bin: str) -> float:
        bin = str(bin)
        search_bin = re.search(r"^([+-])?0b([01]+)(?:.([01]+))?", bin, re.I)
        dec = 0
        if search_bin:
            _bin = search_bin.group(2)[::-1]
            for i in range(len(_bin)):
                dec += int(_bin[i])*(2**i)
            if _bin := search_bin.group(3):
                for i in range(len(_bin)):
                    dec += int(_bin[i])*(2**((i+1)*-1))
            if _sign := search_bin.group(1):
                if _sign == "-":
                    dec *= -1
        return dec

    def hex2dec(self, hex: str) -> float:
        hex = str(hex)
        def letter2number(letter):
            if letter.lower() == 'a':
                return 10
            if letter.lower() == 'b':
                return 11
            if letter.lower() == 'c':
                return 12
            if letter.lower() == 'd':
                return 13
            if letter.lower() == 'e':
                return 14
            if letter.lower() == 'f':
                return 15
            return letter
        search_hex = re.search(r"^([+-])?0x([0-9a-f]+)(?:.([0-9a-f]+))?", hex, re.I)
        dec = 0
        if search_hex:
            _hex = search_hex.group(2)[::-1]
            for i in range(len(_hex)):
                num = letter2number(_hex[i])
                dec += int(num)*(16**i)
            if _hex := search_hex.group(3):
                for i in range(len(_hex)):
                    num = letter2number(_hex[i])
                    dec += int(num)*(16**((i+1)*-1))
            if _sign := search_hex.group(1):
                if _sign == "-":
                    dec *= -1
        return dec

class ParseExp(Unit):
    # >>>>>>> grammar <<<<<<<
    # <booleanExp> := <booleanExp> or <booleanExp> | <booleanExp> and <booleanExp> | not <booleanExp> | "("<booleanExp>")" | <expression> <rop> <expression> | <expression>
    # <rop> := ==|<=|<|>=|>
    ############ simply =>
    # <booleanExp> := <orExp> or <orExp>
    # <orExp> := <andExp> and <andExp>
    # if use <booleanExp> not use <expression>:
    #   <andExp> := not <booleanExp> | "("<booleanExp>")" | <expression> <rop> <expression> | <expression>
    # else:
    #   <andExp> := not <booleanExp> | <expression> <rop> <expression> | <expression>
    ######################
    # <expression> := <term> <addExp> <term>
    # <addExp> := "+" | "-"
    # <term> := <factor> <mulExp> <factor>
    # <mulExp> := "*" | "/" | "%"
    # if use <booleanExp>:
    ##   <factor> := <func_exp> | <var> | <exponent> | <float> | <number> | '(' <booleanExp> ')' | <addExp> [<exponent> | <float> | <number>]
    #   <factor> := <var>(<func_exp>)? | <exponent> | <float> | <number> | '(' <booleanExp> ')' | <addExp> [<exponent> | <float> | <number>]
    # else:
    ##   <factor> := <func_exp> | <var> | <exponent> | <float> | <number> | '(' <expression> ')' | <addExp> [<exponent> | <float> | <number>]
    #   <factor> := <var>(<func_exp>)? | <exponent> | <float> | <number> | '(' <expression> ')' | <addExp> [<exponent> | <float> | <number>]
    # <exponent> := [0-9]+(.[0-9]+)?[eE]([+-]?[0-9+])
    # <float> := [0-9]+.[0-9]+
    # <number> := [0-9]+
    # <var> := [a-zA-Z_][a-zA-Z0-9_]*
    ## <func_exp> := <func> '(' <expression> (',' <expression>)* ')'
    # <func_exp> := '(' <expression> (',' <expression>)* ')'
    # remove: <factor> := <func_exp> | <var> | <exponent> | <float> | <number> | '(' <expression> ')' | <addExp> [<exponent> | <float> | <number>]
    ############ simply =>
    # <func_exp> := <func> '(' <list> ')'
    # <list> := <expression> (',' <list>) | ε
    # <func> := max[n]|min[n]|sum
    ######################
    # ε is end of char
    ############ BNF -> EBNF ############
    # BNF:
    #   AddExp -> AddExp opt1 MulExp | MulExp
    # EBNF:
    #   AddExp -> MulExp {opt1 MulExp}
    # EBNF Code:
    # function AddExp() {
    #     MulExp();
    #     while(opt1()) {
    #         MulExp();
    #     }
    #     ...
    # }
    def __init__(self, text: str, param: dict = {}) -> None:
        super(ParseExp, self).__init__()
        self.tokens = self.tokenize(text)
        self.token_queue = []
        self.vars = []
        self.param = param
        self.prev_token = None
        self.current_token = None
        self.next_token()

    # 获取下一个token
    def next_token(self) -> None:
        self.prev_token = self.current_token
        try:
            self.current_token = next(self.tokens)
        except StopIteration:
            self.current_token = None

    # 验证当前token是否匹配给定类型
    def match(self, token_type: List[str]) -> None:
        if self.current_token and self.current_token[0] == token_type:
            self.next_token()
        else:
            raise SyntaxError(f'Expected {token_type}, but got {self.current_token[0]}')

    def parse_boolean_exp(self) -> Union[list, str]:
        or_exp1 = self.parse_or_exp()
        while self.current_token and self.current_token[0] == "OR":
            or_token = self.current_token
            self.match(or_token[0])
            or_exp2 = self.parse_or_exp()
            or_exp1 = self.or_exp(or_exp1, or_token, or_exp2)
        return or_exp1

    def or_exp(self,
               or_exp1: List[str],
               token: List[str],
               or_exp2: List[str]
               ) -> Optional[bool]:
        if token[0] == 'OR':
            return or_exp1 or or_exp2

    def parse_or_exp(self) -> Union[list, str]:
        and_exp1 = self.parse_and_exp()
        while self.current_token and self.current_token[0] == "AND":
            and_token = self.current_token
            self.match(and_token[0])
            and_exp2 = self.parse_and_exp()
            and_exp1 = self.and_exp(and_exp1, and_token, and_exp2)
        return and_exp1

    def and_exp(self,
                and_exp1: List[str],
                token: List[str],
                and_exp2: List[str]
                ) -> Optional[bool]:
        if token[0] == 'AND':
            return and_exp1 and and_exp2

    """
    def parse_and_exp(self):
        if self.current_token and self.current_token[0] == 'NOT':
            not_token = self.current_token
            self.match('NOT')
            boolean_exp = self.parse_boolean_exp()
            return self.get_not_exp(not_token, boolean_exp)
        elif self.current_token:
            if self.current_token[0] != 'LPAREN':
                expression1 = self.parse_expression()
                if self.current_token and self.current_token[0] == "ROP":
                    rop_token = self.current_token
                    self.match('ROP')
                    expression2 = self.parse_expression()
                    expression1 = self.parse_rop(expression1, rop_token, expression2)
                    return expression1
                return expression1
            else:
                self.match('LPAREN')
                boolean_exp = self.parse_boolean_exp()
                self.match('RPAREN')
                print("there")
                return boolean_exp
    """
    def parse_and_exp(self) -> Union[list, str]:
        if self.current_token and self.current_token[0] == 'NOT':
            not_token = self.current_token
            self.match('NOT')
            boolean_exp = self.parse_boolean_exp()
            return self.get_not_exp(not_token, boolean_exp)
        else:
            expression1 = self.parse_expression()
            if self.current_token and self.current_token[0] == "ROP":
                rop_token = self.current_token
                self.match('ROP')
                expression2 = self.parse_expression()
                expression1 = self.parse_rop(expression1, rop_token, expression2)
                return expression1
            return expression1

    def get_not_exp(self, token: List[str], boolean_exp: bool) -> Optional[bool]:
        if token[0] == 'NOT':
            return not boolean_exp

    def parse_rop(self,
                  expr1: Union[float, int],
                  token: List[str],
                  expr2: Union[float, int]
                  ) -> Optional[bool]:
        expr1 = float(expr1)
        expr2 = float(expr2)
        if not token[0] == "ROP":
            raise SyntaxError(f'Unexpected {token[0]}')
        if re.search("\=\=", token[1]):
            return expr1 == expr2
        elif re.search("\!\=", token[1]):
            return not expr1 == expr2
        elif re.search("\<\=", token[1]):
            return expr1 <= expr2
        elif re.search("\<", token[1]):
            return expr1 < expr2
        elif re.search("\>\=", token[1]):
            return expr1 >= expr2
        elif re.search("\>", token[1]):
            return expr1 > expr2

    # 解析expression规则
    def parse_expression(self) -> Union[int, float]:
        term1 = self.parse_term()
        while self.current_token and self.current_token[0] in ["PLUS", "MINUS"]:
            add_token = self.current_token
            self.match(add_token[0])
            term2 = self.parse_term()
            term1 = self.add_exp(term1, add_token, term2)
        return term1

    def add_exp(self,
                term1: Union[float, int],
                token: List[str],
                term2: Union[float, int]
                ) -> Optional[int or float]:
        if token[0] == 'PLUS':
            return term1 + term2
        elif token[0] == "MINUS":
            return term1 - term2

    # 解析term规则
    def parse_term(self) -> Union[int, float]:
        factor1 = self.parse_factor()
        while self.current_token and self.current_token[0] in ["TIMES", "DIVISION", "MOD"]:
            mul_exp = self.current_token
            self.match(mul_exp[0])
            factor2 = self.parse_factor()
            factor1 = self.mul_exp(factor1, mul_exp, factor2)
        return factor1

    def mul_exp(self,
                factor1: Union[int, float],
                token: List[str],
                factor2: Union[int, float]
                ) -> Union[int, float]:
        if token[0] == 'TIMES':
            return factor1 * factor2
        elif token[0] == "DIVISION":
            return factor1 / factor2
        elif token[0] == "MOD":
            return factor1 % factor2

    # 解析factor规则
    def parse_factor(self) -> Union[int, float, str]:
        # if self.current_token and self.current_token[0] == 'FUNC':
        #     func_exp_token = self.current_token
        #     self.match('FUNC')
        #     self.match('LPAREN')
        #     func_exp = self.parse_list()
        #     self.match('RPAREN')
        #     return self.get_func(func_exp_token, func_exp)
        if self.current_token and self.current_token[0] == 'VAR':
            var_token = self.current_token
            self.match('VAR')
            if self.current_token and self.current_token[0] == 'LPAREN':
                self.match('LPAREN')
                func_exp = self.parse_list()
                self.match('RPAREN')
                return self.get_func(var_token, func_exp)
            return self.get_var(var_token)
        elif self.current_token and self.current_token[0] == 'BIN':
            bin_token = self.current_token
            self.match('BIN')
            if self.current_token and self.current_token[0] == "VAR":
                unit_token = self.current_token
                self.match("VAR")
                return self.get_bin(bin_token, unit_token)
            return self.get_bin(bin_token)
        elif self.current_token and self.current_token[0] == 'HEX':
            hex_token = self.current_token
            self.match('HEX')
            if self.current_token and self.current_token[0] == "VAR":
                unit_token = self.current_token
                self.match("VAR")
                return self.get_hex(hex_token, unit_token)
            return self.get_hex(hex_token)
        elif self.current_token and self.current_token[0] == 'EXPONENT':
            exponent_token = self.current_token
            self.match('EXPONENT')
            if self.current_token and self.current_token[0] == "VAR":
                unit_token = self.current_token
                self.match("VAR")
                return self.get_exponent(exponent_token, unit_token)
            return self.get_exponent(exponent_token)
        elif self.current_token and self.current_token[0] == 'FLOAT':
            float_token = self.current_token
            self.match('FLOAT')
            if self.current_token and self.current_token[0] == "VAR":
                unit_token = self.current_token
                self.match("VAR")
                return self.get_float(float_token, unit_token)
            return self.get_float(float_token)
        elif self.current_token and self.current_token[0] == 'NUMBER':
            number_token = self.current_token
            self.match('NUMBER')
            if self.current_token and self.current_token[0] == "VAR":
                unit_token = self.current_token
                self.match("VAR")
                return self.get_number(number_token, unit_token)
            return self.get_number(number_token)
        elif self.current_token and self.current_token[0] == 'LPAREN':
            self.match('LPAREN')
            # expression = self.parse_expression()
            expression = self.parse_boolean_exp()
            self.match('RPAREN')
            return expression
        elif self.current_token and self.current_token[0] in ['MINUS', 'PLUS']:
            sign_token = self.current_token
            self.match(self.current_token[0])
            if self.current_token and self.current_token[0] == 'BIN':
                bin_token = self.current_token
                self.match('BIN')
                if self.current_token and self.current_token[0] == "VAR":
                    unit_token = self.current_token
                    self.match("VAR")
                    return self.get_sign_bin(sign_token, bin_token, unit_token)
                return self.get_sign_bin(sign_token, bin_token)
            elif self.current_token and self.current_token[0] == 'HEX':
                hex_token = self.current_token
                self.match('HEX')
                if self.current_token and self.current_token[0] == "VAR":
                    unit_token = self.current_token
                    self.match("VAR")
                    return self.get_sign_hex(sign_token, hex_token, unit_token)
                return self.get_sign_hex(sign_token, hex_token)
            elif self.current_token and self.current_token[0] == 'EXPONENT':
                exponent_token = self.current_token
                self.match('EXPONENT')
                if self.current_token and self.current_token[0] == "VAR":
                    unit_token = self.current_token
                    self.match("VAR")
                    return self.get_sign_exponent(sign_token, exponent_token, unit_token)
                return self.get_sign_exponent(sign_token, exponent_token)
            elif self.current_token and self.current_token[0] == 'FLOAT':
                float_token = self.current_token
                self.match('FLOAT')
                if self.current_token and self.current_token[0] == "VAR":
                    unit_token = self.current_token
                    self.match("VAR")
                    return self.get_sign_float(sign_token, float_token, unit_token)
                return self.get_sign_float(sign_token, float_token)
            elif self.current_token and self.current_token[0] == 'NUMBER':
                number_token = self.current_token
                self.match('NUMBER')
                if self.current_token and self.current_token[0] == "VAR":
                    unit_token = self.current_token
                    self.match("VAR")
                    return self.get_sign_number(sign_token, number_token, unit_token)
                return self.get_sign_number(sign_token, number_token)
            else:
                raise SyntaxError(f'Unexpected {self.current_token[0]}')
        else:
            raise SyntaxError(f'Unexpected {self.current_token[0]}')

    def get_func(self, func_token: List[str], func_exp: List[int or float or str]) -> Optional[int or float or str]:
        expr = None
        if re.search("max", func_token[1], re.I):
            expr = max(func_exp)
        elif re.search("min", func_token[1], re.I):
            expr = min(func_exp)
        elif re.search("sum", func_token[1], re.I):
            expr = sum(func_exp)
        elif re.search("abs", func_token[1], re.I):
            expr = abs(func_exp[0])
        elif re.search("sin", func_token[1], re.I):
            expr = math.sin(func_exp[0])
        elif re.search("cos", func_token[1], re.I):
            expr = math.cos(func_exp[0])
        elif re.search("tan", func_token[1], re.I):
            expr = math.tan(func_exp[0])
        elif re.search("atan2", func_token[1], re.I):
            expr = math.atan2(float(func_exp[0]), float(func_exp[1]))
        elif re.search("exp", func_token[1], re.I):
            expr = math.exp(func_exp[0])
        elif re.search("sgn", func_token[1], re.I):
            expr = np.sign(func_exp[0])
        elif re.search("int", func_token[1], re.I):
            expr = int(func_exp[0])
        elif re.search("pow", func_token[1], re.I):
            expr = float(func_exp[0])**float(func_exp[1])
        elif re.search("sqrt", func_token[1], re.I):
            expr = math.sqrt(float(func_exp[0]))
        elif re.search("avg", func_token[1], re.I):
            expr = np.mean(func_exp)
        elif re.search("msr", func_token[1], re.I):
            expr = math.sqrt(sum([x**2 for x in func_exp])/len(func_exp))
        elif re.search("bin", func_token[1], re.I):
            expr = bin(int(float(func_exp[0])))
        elif re.search("hex", func_token[1], re.I):
            expr = hex(int(float(func_exp[0])))
        elif re.search("log", func_token[1], re.I):
            expr = math.log(float(func_exp[0]), float(func_exp[1]))
        elif re.search("par", func_token[1], re.I):
            expr = func_exp[0].strip("\"").strip("\'")
        return expr

    def parse_list(self, result: List[int or float or str] = None) -> List[int or float or str]:
        if result is None:
            result = []
        expression1 = self.parse_expression()
        result.append(expression1)
        while(self.current_token and self.current_token[0] == "NEXT"):
            self.match("NEXT")
            self.parse_list(result)
        return result

    def get_var(self, token: List[str]) -> Union[int, float, str]:
        self.vars.append(token)
        if token[1] in self.param:
            return self.param[token[1]]
        raise SyntaxError(f"{token[1]} not in parameter list")

    def get_bin(self, token: List[str], unit_token: List[str] = None) -> Union[int, float]:
        if unit_token:
            return self.eng2float(self.bin2dec(token[1])+unit_token[1])
        return self.bin2dec(token[1])

    def get_hex(self, token: List[str], unit_token: List[str] = None) -> Union[int, float]:
        if unit_token:
            return self.eng2float(self.hex2dec(token[1])+unit_token[1])
        return self.hex2dec(token[1])

    def get_exponent(self, token: List[str], unit_token: List[str] = None) -> Union[int, float]:
        if unit_token:
            return self.eng2float(token[1]+unit_token[1])
        return float(token[1])

    def get_float(self, token: List[str], unit_token: List[str] = None) -> Union[int, float]:
        if unit_token:
            return self.eng2float(token[1]+unit_token[1])
        return float(token[1])

    def get_number(self, token: List[str], unit_token: List[str] = None) -> Union[int, float]:
        if unit_token:
            return self.eng2float(token[1]+unit_token[1])
        return int(token[1])

    def get_sign_bin(self, token: List[str], bin: List[str], unit_token: List[str] = None) -> Union[int, float]:
        if unit_token:
            return self.eng2float(str(self.bin2dec(token[1]+bin[1]))+unit_token[1])
        return self.bin2dec(token[1]+bin[1])

    def get_sign_hex(self, token: List[str], hex: List[str], unit_token: List[str] = None) -> Union[int, float]:
        if unit_token:
            return self.eng2float(str(self.hex2dec(token[1]+hex[1]))+unit_token[1])
        return self.hex2dec(token[1]+hex[1])

    def get_sign_exponent(self, token: List[str], _float: List[str], unit_token: List[str] = None) -> Union[int, float]:
        if unit_token:
            return self.eng2float(token[1]+_float[1]+unit_token[1])
        return float(token[1] + _float[1])

    def get_sign_float(self, token: List[str], _float: List[str], unit_token: List[str] = None) -> Union[int, float]:
        if unit_token:
            return self.eng2float(token[1]+_float[1]+unit_token[1])
        return float(token[1] + _float[1])

    def get_sign_number(self, token: List[str], number: List[str], unit_token: List[str] = None) -> Union[int, float]:
        if unit_token:
            return self.eng2float(token[1]+number[1]+unit_token[1])
        return int(token[1] + number[1])

    def tokenize(self, text: str) -> Generator[List[str], None, None]:
        token_spec = [
            ("OR", "or|\|\|"),
            ("AND", "and|\&\&"),
            ("ROP", "\=\=|\!\=|\<\=|\<|\>\=|\>"),
            ("NOT", "not|\!"),
            ("NEXT", ","),
            # ("FUNC", r"(?:max\d*)|(?:min\d*)|sum|abs|sin|cos|tan|exp|sgn|int|pow|sqrt|avg|msr|bin|hex"),
            ("VAR", r"[a-zA-Z_][a-zA-Z0-9_]*"),
            ("BIN", r"0b[01\.]+"),
            ("HEX", r"0x[0-9a-fA-F\.]+"),
            ("EXPONENT", r"\d+(?:\.\d+)?[eE](?:[+-])?\d+"),
            ("FLOAT", r"\d+\.\d+"),
            ("NUMBER", r"\d+"),
            ("PLUS", r"\+"),
            ("MINUS", r"\-"),
            ("TIMES", r"\*"),
            ("DIVISION", r"\/"),
            ("MOD", r"%"),
            # ("FLOAT", r"[+-]?\d+\.\d+"),
            # ("NUMBER", r"[+-]?\d+"),
            ("LPAREN", r"\("),
            ("RPAREN", r"\)"),
            ("SKIP", r"[ \t\n]+"),
            ("INVALID", r"."),
        ]
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_spec)
        for mo in re.finditer(tok_regex, text):
            kind = mo.lastgroup
            value = mo.group()
            if kind != "SKIP" and kind != "INVALID":
                # print((kind, value))
                self.token_queue.append((kind, value))
                yield kind, value

    def parse(self) -> Union[int, float, str]:
        return self.parse_boolean_exp()
        # return self.parse_expression()

    def get_tokens(self) -> List[List[str]]:
        return self.token_queue

    def get_vars(self) -> List[List[str]]:
        return self.vars

class ParseExpProc(ParseExp):
    def __init__(self, text, param = {}):
        # parse express process could not need to param variable
        super(ParseExpProc, self).__init__(text, param)

    def add_exp(self, term1, token, term2):
        return [term1, token, term2]

    def mul_exp(self, factor1, token, factor2):
        return [factor1, token, factor2]

    def get_var(self, token):
        self.vars.append(token)
        return token

    def get_bin(self, token, unit_token = None):
        if unit_token:
            return [token, unit_token]
        return token

    def get_hex(self, token, unit_token = None):
        if unit_token:
            return [token, unit_token]
        return token

    def get_exponent(self, token, unit_token = None):
        if unit_token:
            return [token, unit_token]
        return token

    def get_float(self, token, unit_token = None):
        if unit_token:
            return [token, unit_token]
        return token

    def get_number(self, token, unit_token = None):
        if unit_token:
            return [token, unit_token]
        return token

    def get_sign_bin(self, token, bin, unit_token = None):
        if unit_token:
            return [token, bin, unit_token]
        return [token, bin]

    def get_sign_hex(self, token, hex, unit_token = None):
        if unit_token:
            return [token, hex, unit_token]
        return [token, hex]

    def get_sign_exponent(self, token, _float, unit_token = None):
        if unit_token:
            return [token, _float, unit_token]
        return [token, _float]

    def get_sign_float(self, token, _float, unit_token = None):
        if unit_token:
            return [token, _float, unit_token]
        return [token, _float]

    def get_sign_number(self, token, number, unit_token = None):
        if unit_token:
            return [token, number, unit_token]
        return [token, number]

    def get_func(self, func_token, func_exp):
        return [func_token, func_exp]

    def or_exp(self, or_exp1, token, or_exp2):
        if token[0] == 'OR':
            return [or_exp1, token, or_exp2]

    def and_exp(self, and_exp1, token, and_exp2):
        if token[0] == 'AND':
            return [and_exp1, token, and_exp2]

    def get_not_exp(self, token, boolean_exp):
        if token[0] == 'NOT':
            return [token, boolean_exp]

    def parse_rop(self, expr1, token, expr2):
        return [expr1, token, expr2]

if __name__ == "__main__":
    lines = r"""
test
+1
+2
.param bank=1
+mux = 2 nwl = "16/2" nbl = "8*2"
.param word_write=1 red = 0 pg=1
.param me_gating=1 dr=0

.param psv = 0.88
.param psvi="1.0*psv"

.if
+(psv > 0.7)
.param tcyc = 20n
.param tas_set = 5n
.if (red < 0)
.param tcyc = 0n
.elseif (red > 0)
.param tcyc = 1n
.else
.param tas_set = 0n
.endif
.elseif (psv > 0.6)
.param tcyc = 100n
.param tas_set = 20n
.else
.param tcyc = 200n
.param tas_set = 40n
.endif

.tran 0.01n "13*tcyc"
.probe v(*) i(*)
.end

*********
.meas tran tsaen_rise       trig v(ck)      val=v50 rise =  1 td=c05
+                           targ v(xlio_r.xsa.saen)   val=v80 rise=1 td=c05
.meas tran tsaen_risex      param = '0.8*  tsaen_rise'
.meas tran tsaen_risez      param = '0.8*  tsaen_risex'
.meas tran tsaen_risey      param = '0.8*  tsaen_risez + tsaen_risex + tcyc'
.meas tran iVDD_std_ck      avg i(VDD) from="tcyc*36" to="tcyc*40"
.lib "D:\Project\Python\testbench\test.lib" FFGS
""".split("\n")
    # print(lines)
    testbench = Testbench()
    testbench.parse_testbench(lines)
    print(json.dumps(testbench.get_data(), indent=4))
    # print(testbench.compress_whitespace(".meas tran  tsaen_risex      param='0.8*    tsaen_rise'"))
    print(json.dumps(testbench.get_param(), indent=4))
    print(json.dumps(testbench.get_param(param="flag"), indent=4))
    print(json.dumps(testbench.get_meas(), indent=4))
    print(json.dumps(testbench.get_meas(variable="iVDD_std_ck"), indent=4))
    print(json.dumps(testbench.search_related_param(param_name="iVDD_std_ck"), indent=4))
    print(json.dumps(testbench.search_related_param(param_name="tsaen_risey"), indent=4))
    print(json.dumps(testbench.search_related_param(param_name="test"), indent=4))
    print(json.dumps(testbench.search_related_param(param_name="demo"), indent=4))

    string = '3.2 + 1*  (var1 + 2)+1'
    string = '3.2 + min(1,2)*  max2(var1, min(12, 1, 0))+1'
    # string = '-5 != (1*  (var1 + 2)+1)'
    # string = '(var1 and 0) or 1'
    # string = '1*  (var1 + 2)+1'
    # string = 'var1 > 1.1'
    # string = '-1-1'
    # string = '-1-1-(-3)'
    string = '(-3)-1'
    # string = '(12-1)'
    # string = '-3'
    # string = '(3+1)+1+1'
    # string = '(3)+1+1'
    string = '12e-1'
    string = '3.2 + 1*  (var1 + 2)+12e-1m'
    string = 'sum(12,-0b11m,1n)'
    # string = '0.8*  tsaen_rise'
    # string = 'sqrt(1e-4)'
    # string = 'avg(10,0)'
    parser = ParseExp(string, {"var1" : 2})
    # parser = ParseExpProc(string, {"var1" : 2})
    # parser = ParseExpProc(string)
    result = parser.parse()
    print(result)
    print(parser.get_tokens())
    print(parser.get_vars())

    # print(testbench.depth_search_all_params("tsaen_risey"))

    # unit = Unit()
    # print(unit.bin2dec("-0b10.1"))
    # print(unit.hex2dec("-0xf.1"))


# lib: grammar

# @STRING:
# string ::= "'" string_item* "'" | """ string_item* """
# string_item ::= string_char | string_escape_seq
# string_char ::= <any source character except "\" or newline or the quote>
# string_escape_seq ::= "\" <any source character>

# @INTEGER:
# integer      ::=  decinteger | bininteger | octinteger | hexinteger
# decinteger   ::=  nonzerodigit (["_"] digit)* | "0"+ (["_"] "0")*
# bininteger   ::=  "0" ("b" | "B") (["_"] bindigit)+
# octinteger   ::=  "0" ("o" | "O") (["_"] octdigit)+
# hexinteger   ::=  "0" ("x" | "X") (["_"] hexdigit)+
# nonzerodigit ::=  "1"..."9"
# digit        ::=  "0"..."9"
# bindigit     ::=  "0" | "1"
# octdigit     ::=  "0"..."7"
# hexdigit     ::=  digit | "a"..."f" | "A"..."F"

# @FLOAT:
# floatnumber   ::=  pointfloat | exponentfloat
# pointfloat    ::=  [digitpart] fraction | digitpart "."
# exponentfloat ::=  (digitpart | pointfloat) exponent
# digitpart     ::=  digit (["_"] digit)*
# fraction      ::=  "." digitpart
# exponent      ::=  ("e" | "E") ["+" | "-"] digitpart

# @ATOM
# atom ::= identifier | literal | enclosure

# @LITERAL
# literal ::= string | integer | floatnumber

# @ENCLOSURE
# enclosure ::=  parenth_form | list_display

# @PRIMARY
# primary ::=  atom

# @DICT
# dict_display       ::=  "{" key_datum+ "}"
# key_datum          ::=  atom (":" atom ";") | ("(" argument_list* ")" ";" | dict_display)
# argument_list      ::=  positional_item ("," positional_item)*
# positional_item    ::=  atom
# grammar = {
#     'dict_display': [['{', 'key_dat', '}']],
#     'key_dat' : [['key_datum'], ["key_dat"]],
#     'key_datum': [['atom', 'property']],
#     'property' : [[':', 'atom', ';'], ['(', 'argument_list', ')', 'property_end']],
#     'property_end' : [[';'], ['dict_display']],
#     'argument_list': [['positional_item', ',', 'argument_list'], ['positional_item']],
#     'positional_item': [['atom']],
#     'atom' : [["ID"], ["INTEGER"], ["STRING"], ["REAL_CONST"]],
# }