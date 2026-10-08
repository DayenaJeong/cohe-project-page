"""Derive website data from a separately downloaded public artifact; no training."""
import argparse
import csv
import hashlib
import json
import re
import subprocess
from pathlib import Path
from statistics import mean, stdev

parser = argparse.ArgumentParser()
parser.add_argument('--artifact', type=Path, required=True)
parser.add_argument('--paper', type=Path, required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
records = root / 'src/data/records'
records.mkdir(parents=True, exist_ok=True)
paths = {
    'dino': 'experiments/dinov2_gate3/statistics/dinov2_clean_5seed_all_conditions.csv',
    'ddpm': 'experiments/ddpm_ordering/per_seed_results.csv',
    'imagenet': 'experiments/imagenet1k_vae_gate3/SEED_LEVEL_RESULTS.csv',
    'dinoStats': 'experiments/dinov2_gate3/statistics/dinov2_clean_5seed_all_conditions.json',
    'ddpmStats': 'experiments/ddpm_ordering/summary.json',
    'imagenetStats': 'experiments/imagenet1k_vae_gate3/FINAL_STATISTICS.json',
    'dependence': 'results/aggregate/dinov2_scalar/cifar100_dinov2_dependence.csv',
    'prediction': 'results/aggregate/dinov2_scalar/cifar100_dinov2_predictive_r2.csv',
    'positive': 'results/aggregate/positive_control/positive_task_aligned_control_summary.json',
}
inputs = {}
hashes = {}
for key, path in paths.items():
    content = (args.artifact / path).read_bytes()
    (records / Path(path).name).write_bytes(content)
    hashes[path] = hashlib.sha256(content).hexdigest()
    inputs[key] = json.loads(content) if path.endswith('.json') else list(csv.DictReader(content.decode().splitlines()))

def paired(hard, random, critical):
    deltas = [h-r for h, r in zip(hard, random)]
    m = mean(deltas)
    half = critical * stdev(deltas) / len(deltas)**0.5
    return dict(n=len(deltas), hard=hard, random=random, deltas=deltas,
                hardMean=mean(hard), randomMean=mean(random), delta=m, ci=[m-half, m+half])

dino = []
for condition, label in [('ordinary_10', '10% subset'), ('ordinary_30', '30% subset'), ('ordinary_50', '50% subset'), ('class_balanced_10', 'Balanced 10%')]:
    rows = [r for r in inputs['dino'] if r['condition'] == condition]
    assert [int(r['seed']) for r in rows] == list(range(5))
    result = paired([float(r['hard_top1']) for r in rows], [float(r['random_top1']) for r in rows], 2.7764451051977987)
    expected = inputs['dinoStats']['conditions'][condition]
    assert abs(result['delta'] - expected['delta_mean']) < 1e-10
    assert max(abs(a-b) for a,b in zip(result['ci'], expected['ci95'])) < 1e-8
    assert all(d < 0 for d in result['deltas'])
    dino.append(dict(label=label, condition=condition, **result))

rows = inputs['ddpm']
assert [int(r['seed']) for r in rows] == list(range(8))
assert all(r['run_status'] == 'completed' for r in rows)
ddpm = []
for label, a, b, key in [('Easy-to-Hard', 'easy_top1', 'random_top1', 'easy_minus_random'), ('Shuffled-Proxy Order', 'shuffled_top1', 'random_top1', 'shuffled_minus_random'), ('Easy − Shuffled', 'easy_top1', 'shuffled_top1', 'easy_minus_shuffled')]:
    result = paired([float(r[a]) for r in rows], [float(r[b]) for r in rows], 2.3646242515927844)
    expected = inputs['ddpmStats'][key]
    assert abs(result['delta'] - expected['mean_pp']) < 1e-10
    assert max(abs(a-b) for a,b in zip(result['ci'], expected['ci95_pp'])) < 1e-8
    ddpm.append(dict(label=label, p=expected['paired_t_pvalue'], **result))

rows = inputs['imagenet']
assert [int(r['seed']) for r in rows] == list(range(5))
imagenet = {}
for endpoint, suffix, expected_key in [('best', 'best', 'best_checkpoint'), ('final', 'final', 'final_epoch_90')]:
    result = paired([float(r[f'proxy_hard_top1_{suffix}']) for r in rows], [float(r[f'random_top1_{suffix}']) for r in rows], 2.7764451051977987)
    expected = inputs['imagenetStats'][expected_key]['top1']
    assert abs(result['delta'] - expected['paired_delta_mean']) < 1e-10
    assert max(abs(a-b) for a,b in zip(result['ci'], expected['paired_95_ci'])) < 1e-8
    imagenet[endpoint] = result

dependence = next(r for r in inputs['dependence'] if r['target'] == 'First-learning epoch')
prediction = next(r for r in inputs['prediction'] if r['target'] == 'First-learning epoch')
tex = args.paper.read_text()
abstract = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', tex, re.S).group(1).strip()
abstract = abstract.replace(r'\emph{Cross-Objective Hardness Evaluation}', 'Cross-Objective Hardness Evaluation')
abstract = abstract.replace(r'\rho', 'ρ').replace(r'\Rtwo', 'R²').replace(r'\%', '%').replace('$', '')
assert '\\' not in abstract
data = dict(artifactCommit=subprocess.check_output(['git', '-C', str(args.artifact), 'rev-parse', 'HEAD'], text=True).strip(),
            sources=paths, hashes=hashes, paperHash=hashlib.sha256(args.paper.read_bytes()).hexdigest(),
            dino=dino, ddpm=ddpm, imagenet=imagenet,
            firstLearning=dict(rho=float(dependence['spearman_rho']), r2=float(prediction['best_single_proxy_r2_mean'])),
            positive=inputs['positive'], abstract=abstract)
(root / 'src/data/verified-results.json').write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
print('Verified four DINOv2 conditions, eight DDPM pairs, both ImageNet endpoints, relational summaries, and final abstract.')
