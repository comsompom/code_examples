from operations import MetamaskOperation
from methods import EtheriumMethods


address = "0x107119102c2EC84099cDce3D5eFDE2dcbf4DEB2a"
operation = EtheriumMethods().get_balance
mm_operation = MetamaskOperation(address, operation)
print(mm_operation.get_balance())
