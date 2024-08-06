from __future__ import annotations
from typing import Type
import sys

class Simulation():
    def __init__(self):
        self.msg = "End simulation"

    def prepare(self):
        print("prepare simulation")

# "factory" create "Power" and "Timing"
class QAFactory():
    def __init__(self):
        pass

    def create_QA(self, flow: Type[Flow]):
        if flow.qa_type == "power":
            return Power()
        elif flow.qa_type == "timing":
            return Timing()
        else:
            print(f"ERROR: invalid qa_type: {flow.qa_type}")
            sys.exit(1)

class Power(Simulation):
    def __init__(self):
        super(Power, self).__init__()
        self.name = "power"

    def run(self):
        self.prepare()
        print(f"running {self.name}...")
        print(self.msg)

class Timing(Simulation):
    def __init__(self):
        super(Timing, self).__init__()
        self.name = "timing"

    def run(self):
        self.prepare()
        print(f"running {self.name}...")
        print(self.msg)

# main entry
class Flow():
    def __init__(self):
        self.qa_type = "power"

    def run_flow(self):
        qa_factory = QAFactory()
        qa = qa_factory.create_QA(self)
        qa.run()

if __name__ == "__main__":
    flow = Flow()
    flow.run_flow()