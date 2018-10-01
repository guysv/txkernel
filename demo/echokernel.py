# Copyright (c) 2018 guysv
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file or http://www.wtfpl.net/ 
# for more details.

from txkernel.kernelbase import KernelBase
from txkernel.kernelapp import KernelApp

class EchoKernel(KernelBase):
    implementation = "iecho"
    implementation_version = "1.0"
    language_info = {
        'name': 'Any text',
        'mimetype': 'text/plain',
        'file_extension': '.txt',
    }
    banner = "Echo kernel - txkernel demo"
    
    def do_execute(self, code, silent, store_history=True,
                   user_expressions=None, allow_stdin=False):
        self.execution_count += 1

        if not silent:
            self.send_update('stream', {'name': 'stdout', 'text': code})

        return {
            'status': 'ok',
            # The base class increments the execution count
            'execution_count': self.execution_count,
            'payload': [],
            'user_expressions': {},
        }
    
    def do_is_complete(self, code):
        return {'status': 'complete'}

if __name__ == '__main__':
    KernelApp(EchoKernel).run()
