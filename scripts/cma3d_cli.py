#!/usr/bin/env python
"""CMA-3D command-line tool.

Subcommands:
  encode        CSV (x,y,z) -> memory (.npz/.json)
  reconstruct   memory -> CSV (choose --ds or --num)
  convert       memory format conversion (.npz <-> .json)

CSV format: header optional; if present first line must start with 'x'.
"""
from __future__ import annotations
import argparse, csv, json, os, math
from typing import Dict, Any, Iterable, List
import numpy as np

from curve_memory.cma3d import curve_memory_3d, reconstruct_from_memory

def read_csv_points(path: str) -> np.ndarray:
    pts: List[List[float]] = []
    with open(path, 'r', newline='') as f:
        r = csv.reader(f)
        first = True
        for row in r:
            if not row:
                continue
            if first and row[0].lower().startswith('x'):
                first = False
                continue
            first = False
            if len(row) < 3:
                raise ValueError(f"Expected 3 columns, got: {row}")
            pts.append([float(row[0]), float(row[1]), float(row[2])])
    if not pts:
        raise ValueError("No points read from CSV")
    return np.asarray(pts, dtype=float)

def write_csv_points(path: str, pts: np.ndarray) -> None:
    with open(path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['x','y','z'])
        for p in pts:
            w.writerow([f"{p[0]:.9g}", f"{p[1]:.9g}", f"{p[2]:.9g}"])

def save_npz(path: str, mem: Dict[str, Any]) -> None:
    np.savez_compressed(path, L=mem['L'], u=mem['u'], kappa=mem['kappa'], tau=mem['tau'])

def load_npz(path: str) -> Dict[str, Any]:
    data = np.load(path, allow_pickle=False)
    return {"L": float(data["L"]), "u": data["u"], "kappa": data["kappa"], "tau": data["tau"]}

def save_json(path: str, mem: Dict[str, Any]) -> None:
    with open(path, 'w') as f:
        json.dump({"L": float(mem['L']),
                   "u": mem['u'].tolist(),
                   "kappa": mem['kappa'].tolist(),
                   "tau": mem['tau'].tolist()}, f)

def load_json(path: str) -> Dict[str, Any]:
    with open(path, 'r') as f:
        obj = json.load(f)
    return {"L": float(obj['L']),
            "u": np.array(obj['u'], dtype=float),
            "kappa": np.array(obj['kappa'], dtype=float),
            "tau": np.array(obj['tau'], dtype=float)}

def cmd_encode(args: argparse.Namespace) -> None:
    pts = read_csv_points(args.infile)
    mem = curve_memory_3d(pts, levels=args.levels)
    if args.out.lower().endswith('.npz'):
        save_npz(args.out, mem)
    elif args.out.lower().endswith('.json'):
        save_json(args.out, mem)
    else:
        raise SystemExit('--out must end with .npz or .json')
    print(f"Encoded {len(pts)} points -> {args.out}")

def cmd_reconstruct(args: argparse.Namespace) -> None:
    if args.infile.lower().endswith('.npz'):
        mem = load_npz(args.infile)
    elif args.infile.lower().endswith('.json'):
        mem = load_json(args.infile)
    else:
        raise SystemExit('--in must be .npz or .json')
    ds = None
    if args.ds is not None:
        ds = float(args.ds)
    elif args.num is not None:
        L = float(mem['L'])
        ds = L / int(args.num)
    rec = reconstruct_from_memory(mem, ds=ds)
    write_csv_points(args.out, rec)
    print(f"Reconstructed {rec.shape[0]} points -> {args.out}")

def cmd_convert(args: argparse.Namespace) -> None:
    if args.infile.lower().endswith('.npz'):
        mem = load_npz(args.infile)
    elif args.infile.lower().endswith('.json'):
        mem = load_json(args.infile)
    else:
        raise SystemExit('--in must be .npz or .json')
    if args.out.lower().endswith('.npz'):
        save_npz(args.out, mem)
    elif args.out.lower().endswith('.json'):
        save_json(args.out, mem)
    else:
        raise SystemExit('--out must be .npz or .json')
    print(f"Converted {args.infile} -> {args.out}")

def make_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description='CMA-3D command-line tool')
    sub = p.add_subparsers(dest='cmd', required=True)

    p_enc = sub.add_parser('encode', help='Encode CSV points to CMA-3D memory (NPZ/JSON)')
    p_enc.add_argument('--in', dest='infile', required=True, help='Input CSV of x,y,z points')
    p_enc.add_argument('--out', dest='out', required=True, help='Output .npz or .json memory file')
    p_enc.add_argument('--levels', type=int, default=3, help='Multiscale levels (default=3)')
    p_enc.set_defaults(func=cmd_encode)

    p_rec = sub.add_parser('reconstruct', help='Reconstruct points from CMA-3D memory to CSV')
    p_rec.add_argument('--in', dest='infile', required=True, help='Input memory (.npz/.json)')
    p_rec.add_argument('--out', dest='out', required=True, help='Output CSV for reconstructed points')
    g = p_rec.add_mutually_exclusive_group()
    g.add_argument('--ds', type=float, help='Arclength step size for reconstruction')
    g.add_argument('--num', type=int, help='Number of output samples (alternative to --ds)')
    p_rec.set_defaults(func=cmd_reconstruct)

    p_conv = sub.add_parser('convert', help='Convert memory between NPZ and JSON')
    p_conv.add_argument('--in', dest='infile', required=True, help='Input memory (.npz/.json)')
    p_conv.add_argument('--out', dest='out', required=True, help='Output memory (.npz/.json)')
    p_conv.set_defaults(func=cmd_convert)

    return p

def main(argv=None):
    args = make_parser().parse_args(argv)
    args.func(args)

if __name__ == '__main__':
    main()
