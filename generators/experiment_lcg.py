# experiments/compare_lcgs.py
from lcg import LCG
from plotting import plot_histograms, plot_lag_scatter, plot_sequence
from datetime import datetime

SEED = 42
SAMPLE_SIZE = 2000

configs = {
    "glibc":              dict(modulus=2**31, multiplier=1103515245, increment=12345),
    "java_posix":         dict(modulus=2**48, multiplier=25214903917, increment=11),
    "zero_increment":     dict(modulus=2**16, multiplier=5, increment=0),
    "non_coprime":        dict(modulus=100, multiplier=3, increment=10),
    "short_period":       dict(modulus=64, multiplier=5, increment=1),
    "power_of_two_mod":   dict(modulus=2**8, multiplier=1103515245, increment=12345),
    "near_identity_mult": dict(modulus=2**16, multiplier=1, increment=1),
    "randu":              dict(modulus=2**31, multiplier=65539, increment=0),
}

def build_normalized_results():
    results = {}
    for name, params in configs.items():
        gen = LCG(SEED, **params)
        raw = gen.generate(SAMPLE_SIZE)
        results[name] = [v / params["modulus"] for v in raw]
    return results

if __name__ == "__main__":
    results = build_normalized_results()
    dt = datetime.now()
    date_string = dt.strftime("%Y-%m-%d_%H:%M:%S")
    plot_histograms(results, save_path=f'results/lcg_histograms_{date_string}.png')
    plot_lag_scatter(results, save_path=f'results/lcg_lag_scatter_{date_string}.png')
    plot_sequence(results, save_path=f'results/lcg_sequence_{date_string}.png')
    print("Saved plots to results/")
