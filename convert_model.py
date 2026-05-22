"""
convert_model.py — shrink the seed-ensemble for faster inference.
NO retraining, NO Optuna. Keeps the first N already-trained models.

Usage:
    python convert_model.py lightgbm_improved.p --keep 3
"""
import argparse, pickle, os

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src", help="path to trained pickle, e.g. lightgbm_improved.p")
    ap.add_argument("--keep", type=int, default=3, help="how many models to keep (1-5)")
    ap.add_argument("--out", default="models/model_lightgbm.p", help="output path")
    args = ap.parse_args()

    with open(args.src, "rb") as f:
        payload = pickle.load(f)

    model = payload["model"] if isinstance(payload, dict) else payload
    is_list = isinstance(model, (list, tuple))
    n_before = len(model) if is_list else 1
    size_before = os.path.getsize(args.src) / (1024 * 1024)

    if is_list:
        keep = max(1, min(args.keep, len(model)))
        new_model = list(model[:keep])
    else:
        new_model, keep = model, 1

    if isinstance(payload, dict):
        new_payload = dict(payload)          # preserve use_engineered, best_params, etc.
        new_payload["model"] = new_model
    else:
        new_payload = {"model": new_model, "use_engineered": False}

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "wb") as f:
        pickle.dump(new_payload, f)

    size_after = os.path.getsize(args.out) / (1024 * 1024)
    print(f"models: {n_before} -> {keep}")
    print(f"size:   {size_before:.1f} MB -> {size_after:.1f} MB")
    print(f"use_engineered: {new_payload.get('use_engineered')}")
    print(f"saved:  {args.out}")

if __name__ == "__main__":
    main()
