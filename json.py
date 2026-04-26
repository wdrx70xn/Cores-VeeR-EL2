import pwn
pwn.pwn()
mod = pwn.proxy('json')
globals().update(mod.__dict__)
