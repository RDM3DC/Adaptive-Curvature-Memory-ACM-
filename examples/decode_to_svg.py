#!/usr/bin/env python3
import json, argparse
from curve_memory import decode_curve

def write_svg(points, out_path: str):
    xs = [p[0] for p in points]; ys = [p[1] for p in points]
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)
    pad = 10
    w = maxx - minx + 2*pad
    h = maxy - miny + 2*pad
    # simple SVG polyline
    def map_pt(p):
        return f"{p[0]-minx+pad},{(maxy - p[1]) + pad}"
    path = " ".join(map(map_pt, points))
    svg = f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">\\n'
    svg += f'  <polyline points="{path}" fill="none" stroke="black" stroke-width="1"/>\\n'
    svg += '</svg>\\n'
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", type=str, default="examples/spiral.cma.json")
    ap.add_argument("--out", type=str, default="examples/spiral.svg")
    args = ap.parse_args()
    with open(args.inp, "r", encoding="utf-8") as f:
        cma = json.load(f)
    pts = decode_curve(cma)
    write_svg(pts, args.out)
    print(f"Wrote {args.out}")
