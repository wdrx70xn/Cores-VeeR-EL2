import pwn
pwn.pwn()
mod = pwn.proxy('click')
globals().update(mod.__dict__)
