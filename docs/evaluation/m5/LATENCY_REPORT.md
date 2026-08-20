# M5 Online Retrieval Latency

M1 question generation P95 is 4,384.58 ms and Planner P95 is 7,269.80 ms; these project measurements provide context rather than a universal threshold.

```json
{
  "cold_query_embedding": {
    "failures": 0,
    "max_ms": 1606.396900024265,
    "mean_ms": 1606.396900024265,
    "median_ms": 1606.396900024265,
    "min_ms": 1606.396900024265,
    "p95_ms": 1606.396900024265,
    "sample_count": 1
  },
  "cold_vector_total_ms": 2266.7806999525055,
  "firestore": {
    "failures": 0,
    "max_ms": 1199.4357999647036,
    "mean_ms": 635.1115224824753,
    "median_ms": 656.4076000358909,
    "min_ms": 326.5207000076771,
    "p95_ms": 1069.3109999410808,
    "sample_count": 40
  },
  "hybrid_parallel": {
    "failures": 0,
    "max_ms": 1592.8725000703707,
    "mean_ms": 1119.6669249911793,
    "median_ms": 1090.4261500108987,
    "min_ms": 725.2489000093192,
    "p95_ms": 1556.2837000470608,
    "sample_count": 20
  },
  "hybrid_sequential": {
    "failures": 0,
    "max_ms": 2214.7631000261754,
    "mean_ms": 1187.9186899925116,
    "median_ms": 1121.097449969966,
    "min_ms": 721.3147999718785,
    "p95_ms": 2185.025699902326,
    "sample_count": 20
  },
  "query_builder": {
    "failures": 0,
    "max_ms": 0.03430002834647894,
    "mean_ms": 0.020157493418082595,
    "median_ms": 0.019550032448023558,
    "min_ms": 0.015099998563528061,
    "p95_ms": 0.0271000899374485,
    "sample_count": 40
  },
  "vector_online": {
    "failures": 0,
    "max_ms": 2169.049199903384,
    "mean_ms": 1131.5822174714413,
    "median_ms": 1078.992799972184,
    "min_ms": 679.2508000507951,
    "p95_ms": 1591.8730999110267,
    "sample_count": 40
  },
  "warm_query_embedding": {
    "failures": 0,
    "max_ms": 1493.6870000092313,
    "mean_ms": 496.4505374955479,
    "median_ms": 421.66205000830814,
    "min_ms": 352.6958000147715,
    "p95_ms": 714.1584000783041,
    "sample_count": 40
  }
}
```
