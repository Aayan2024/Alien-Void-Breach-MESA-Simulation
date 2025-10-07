"""
main.py - entrypoint for Void Breach.

Usage:
    python main.py          # runs a headless simulation (short)
    python main.py --steps 200  # run 200 steps
"""
import argparse
import pandas as pd
from model import VoidBreachModel

def run_headless(steps=100, width=30, height=30, density_native=0.05, density_void=0.02):
    model = VoidBreachModel(width=width, height=height,
                            initial_natives=int(width*height*density_native),
                            initial_voidspawns=int(width*height*density_void))
    for i in range(steps):
        model.step()
    # collect results saved by model.data_collector
    df = model.get_results_df()
    out = "data/simulation_results.csv"
    df.to_csv(out, index=False)
    print(f"Saved results to {out}")
    return df

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, default=100, help="Number of simulation steps")
    parser.add_argument("--width", type=int, default=30)
    parser.add_argument("--height", type=int, default=30)
    parser.add_argument("--native-density", type=float, default=0.05)
    parser.add_argument("--void-density", type=float, default=0.02)
    args = parser.parse_args()

    df = run_headless(steps=args.steps, width=args.width, height=args.height,
                      density_native=args.native_density, density_void=args.void_density)
    print(df.tail())

if __name__ == "__main__":
    main()
