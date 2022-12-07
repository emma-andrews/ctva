import collections
import re

import config

# Class for taking Verilog source code and translating it into useful structures


class Parser:
    def __init__(self):
        """Initialize data values"""
        self.states = []
        self.graph = collections.defaultdict(set)

    def read_file(self, _filename: str):
        """Read from specified Verilog source code"""
        self.filename = _filename
        with open(self.filename, "r") as f:
            # Store the file contents for multiple parse passes
            self.filecontents = f.read()

    def parse(self):
        """Parse contents of Verilog source code into useable data structures"""
        stripped = self.filecontents.replace(" ", "")
        i = stripped.find(config.state_reg)
        if i < 0:
            print("Verilog source does not contain " +
                  config.state_reg + " register.")
            return

        # Populate the states list with the state names and case block for it
        self.populate_states(stripped)

        # Populate the transitions between the states
        self.populate_transitions()

    def populate_states(self, stripped: str):
        """Populate the known states and associated case block"""
        # Find the case statement
        case_index = stripped.find("case(" + config.state_reg + ")")
        end_index = stripped.find("endcase")
        case_stmt = stripped[case_index:end_index + 7]

        # Find each case statement individually
        for stmt in re.finditer('([0-9a-zA-Z])+:begin', case_stmt):
            label = case_stmt[stmt.start():stmt.end()]
            state = label[:label.find(":")]
            begin_cnt = 1
            end_cnt = 0
            case_blk = ""

            # Find the case body for the current state label
            for line in case_stmt[stmt.end():].splitlines(keepends=True):
                if line.find("begin") >= 0:
                    begin_cnt += 1
                elif line.find("end") >= 0:
                    end_cnt += 1

                if begin_cnt == end_cnt:
                    break

                case_blk += line

            # Add state and its case block to states list
            self.states.append((state, case_blk))

    def populate_transitions(self):
        """Populate the state transitions into the graph"""
        for state, blk in self.states:
            for transition in re.finditer(config.state_reg, blk):
                # Can have blocking (=) and non-blocking (<=) assigns, so find position of =
                index = blk.find("=", transition.end())

                # Find end of line, ;
                semi_index = blk.find(";", transition.end())
                result = self.translate_literals(blk[index + 1:semi_index])
                cost = self.calculate_cost(blk, state, result)
                self.graph[state].add((result, cost))

    def translate_literals(self, value: str):
        """Translate Verilog literals to real numbers.
        Returns a string of resulting number."""
        # Verilog only has decimal literals up to 32 bits
        # Anything larger or in a different form is prepended with # of bits, ', type of number
        # e.g. 2'b11 is 3 in binary, 2'h3 is 3 in hex
        # Only supporting b, h, and d literals
        index = value.find("'")
        if index < 0:
            return value

        # Convert the literals appropriately
        num_type = value[index + 1]
        number = value[index + 2:]
        if num_type == "b":
            return str(int(number, 2))
        elif num_type == "h":
            return str(int(number, 16))
        elif num_type == "d":
            return number

        # Return state 0 if unsupported
        return "0"

    def calculate_cost(self, blk: str, state, transition):
        cost = 0
        ifnest = 0
        statenest = 0
        nestcost = []
        nestcost.append(0)

        for line in blk.splitlines():
            if line.startswith("if"):
                ifnest += 1
                if ifnest > len(nestcost) - 1:
                    nestcost.append(0)
                else:
                    nestcost[ifnest] = 0
                continue
            elif line.startswith("else if"):
                ifnest += 1
                if ifnest > len(nestcost) - 1:
                    nestcost.append(0)
                else:
                    nestcost[ifnest] = 0
                continue
            elif line.startswith("else"):
                ifnest += 1
                if ifnest > len(nestcost) - 1:
                    nestcost.append(0)
                else:
                    nestcost[ifnest] = 0
                continue
            elif line == "end":
                if ifnest == statenest:
                    cost = sum(nestcost[:ifnest + 1])
                    return cost
                nestcost[ifnest] = 0
                ifnest -= 1
            elif line.startswith(config.state_reg) and line.endswith("=" + transition + ";"):
                statenest = ifnest
            else:
                # See if statement has a cost
                if line.find("+") >= 0:
                    nestcost[ifnest] += config.add_cost
                elif line.find("-") >= 0:
                    nestcost[ifnest] += config.sub_cost
                elif line.find("*") >= 0:
                    nestcost[ifnest] += config.mult_cost
                elif line.find("/") >= 0:
                    nestcost[ifnest] += config.div_cost
                elif line.find("%") >= 0:
                    nestcost[ifnest] += config.mod_cost
                elif line.find("^") >= 0:
                    nestcost[ifnest] += config.bitxor_cost
                elif line.find("~") >= 0:
                    nestcost[ifnest] += config.bitnot_cost
                elif line.find("&") >= 0 and line.find("&&") < 0:
                    # Make sure we don't take logical and by accident
                    nestcost[ifnest] += config.bitand_cost
                elif line.find("|") >= 0 and line.find("||") < 0:
                    nestcost[ifnest] += config.bitor_cost

        return nestcost[0]
