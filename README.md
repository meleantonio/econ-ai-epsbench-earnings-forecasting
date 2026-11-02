# EPSBench for economists: why the wrong EPS is usually the naive one

EPSBench turns quarterly earnings into a benchmark for a very economist problem: you have a number, a calendar date, and a temptation to forecast by eyeballing the last number. The project gives you 149 firm-quarters from 86 US companies and the table pieces you need to test that habit against actual reported EPS.

Use the benchmark as a disciplined error audit, not a demo of model magic. The important question is whether an LLM agent can turn filings, earnings-call transcripts, and news into the right earnings number without leaning on a stale shortcut.

## Named object

The named object is the public EPSBench benchmark tables in `JadeXu16/EPSBench`, especially:

- `data/instances.csv`
- `data/ground_truth.csv`
- `data/prices.csv`

Those tables define 149 firm-quarters from 86 U.S. companies and attach each quarter to a release date, cutoff date, and outcome.

## Stake

This number matters because earnings forecasts are not a parlour trick. They decide whether an AI system is merely summarising the past or actually helping you screen firms, compare analyst-style forecasts, or study how narrative evidence maps into an accounting target. If the benchmark is wrong, every downstream claim about agent quality is wrong too.

## Naive path

The obvious path is to use last quarter’s EPS as the forecast.

That fails with a wrong number. For AMGN in 2025Q4, the benchmark says reported GAAP diluted EPS was 2.46, while last quarter’s EPS was 5.93. The naive forecast is wrong by 3.47 EPS points before you even touch a model.

Year-ago anchoring is also weak: AMGN’s year-ago EPS was 1.16, still far from 2.46.

## Technique

The point of EPSBench is to make the accounting structure explicit and then score forecasts against the reported outcome.

A practical workflow is:

1. Load the three tables.
2. Merge them on `ticker` and `fiscal_quarter`.
3. Compute naive baselines from `eps_last_quarter` and `eps_year_ago`.
4. Compare those baselines to `eps_gaap_diluted` and scale errors by the stock price if you want a PDE-style scale.
5. Inspect which firms are especially embarrassing for the naive path.

That is the baseline economists should beat before they start talking about agentic forecasting.

RELAI in plain sight:

- **Examine** the benchmark tables and the quarter identifiers.
- **eXplain** the stake: one wrong EPS changes the conclusion.
- **Probe** the naive baselines and the error distribution.
- **Link to economics** through accounting identities, analyst consensus, and forecast error.
- **Output prediction** before running the script: guess which firms have the largest last-quarter misses.
- **Recreate** with `python tutorial.py`.
- **Extend** by adding your own benchmark slice, such as a sector-only sample or a consensus-matched score.

## You will get this wrong

- You will treat the last quarter as if it were information-neutral, which it is not.
- You will confuse a reported EPS target with adjusted earnings.
- You will forget to align on the release date and accidentally use information that was not yet public.
- You will look only at point error and ignore how badly the forecast interval is calibrated.
- You will assume that a model that sounds sensible is automatically competitive with a simple accounting baseline.

## Controversy

There are at least three live arguments here.

First, should earnings benchmarks reward a model for sounding like a careful analyst, or only for getting the number right? Those are not the same thing.

Second, how much should we trust analyst consensus as a reference? It is a useful benchmark, but it is not information-matched to the agent and it may itself be noisy or delayed.

Third, does an accounting-calculator benchmark overstate progress by turning the hard part into a line-item decomposition problem? Proponents say that is exactly the point; critics say the benchmark can hide failure modes in retrieval, evidence selection, and uncertainty.

## Recreate

Run:

```bash
python tutorial.py
```

The script downloads the benchmark tables, merges them, and prints a short audit of naive errors plus one concrete wrong-number example.

## Extend

A harder version is to replace the naive baselines with a stricter model comparison: use the benchmark’s own earnings-history fields, add a sector dummy, or score against analyst consensus where available. That is the point where the tutorial stops being a demo and starts becoming a research design.

## References

- EPSBench GitHub repository: https://github.com/JadeXu16/EPSBench
- EPSBench paper: https://arxiv.org/abs/2610.38293