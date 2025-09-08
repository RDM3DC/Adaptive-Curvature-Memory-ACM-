#!/usr/bin/env python3
import json, argparse, math
from curve_memory import encode_curve

def spiral_points(n=500, a=0.0, b=0.05):
    pts = []
    for i in range(n):
        t = i*0.1
        r = a + b*t
        x = r*math.cos(t)
        y = r*math.sin(t)
        pts.append((x,y))
    return pts

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=500)
    ap.add_argument("--out", type=str, default="examples/spiral.cma.json")
    args = ap.parse_args()
    pts = spiral_points(args.n)
    cma = encode_curve(pts, pi_mode={"type":"adaptive","alpha":0.1,"mu":0.02})
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(cma, f, indent=2)
    print(f"Wrote {args.out}")
