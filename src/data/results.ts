import data from './verified-results.json';
export const results = data;
export const artifact = 'https://github.com/DayenaJeong/cohe-artifact';
export const release = `${artifact}/releases/tag/v1.0-neurips2026`;
export const paper = 'https://neurips.cc/virtual/2026/poster/139659';
export const source = (path: string) => `${artifact}/blob/${data.artifactCommit}/${path}`;
export const number = (n: number, digits = 2) => n.toFixed(digits).replace('-', '−');
export const bibtex = `@inproceedings{jeong2026cohe,
  title = {COHE: Auditing Non-Transitivity in Sample Difficulty Proxies for Vision Models},
  author = {Jeong, Dayena and Choi, Sunglok},
  booktitle = {Advances in Neural Information Processing Systems},
  year = {2026},
  note = {Evaluations \\& Datasets Track},
  url = {https://neurips.cc/virtual/2026/poster/139659}
}`;
