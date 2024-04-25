import base64

import picklescan
import torch


def scan_file(path):
    safe = True

    scan_result = picklescan.scanner.scan_file_path(path)

    if scan_result.scan_err:
        return False

    if len(scan_result.globals) > 0:
        for g in scan_result.globals:
            if g.safety == picklescan.scanner.SafetyLevel.Dangerous:
                print(f"Dangerous global: {g.module}.{g.name}")
                safe = False

    return safe


if __name__ == "__main__":

    inp = input("Give me your model (base64): ").strip()

    with open("model.pkl", "wb") as f:
        f.write(base64.b64decode(inp))

    safe = scan_file("model.pkl")

    if safe:
        torch.load("model.pkl")
