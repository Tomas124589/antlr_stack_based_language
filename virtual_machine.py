class VirtualMachine:
    @staticmethod
    def execute(byte_code: str):
        lines = byte_code.split('\n')
