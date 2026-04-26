import pwn
pwn.pwn()
mod = pwn.proxy('unidiff')
globals().update(mod.__dict__)
