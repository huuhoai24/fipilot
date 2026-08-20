# M6 Latency

Query embedding latency is batch-amortized for Vector/Hybrid; QG latency is measured separately.

## NO_RAG

`{"question_generation": {"mean_ms": 3046.38451563369, "median_ms": 2848.217000020668, "p95_ms": 5081.967500038445}, "retrieval": {"mean_ms": 0.0, "median_ms": 0.0, "p95_ms": 0.0}, "total_pipeline": {"mean_ms": 3046.38451563369, "median_ms": 2848.217000020668, "p95_ms": 5081.967500038445}}`

## LEXICAL

`{"question_generation": {"mean_ms": 3340.448140625085, "median_ms": 3244.4921499700285, "p95_ms": 4956.711600068957}, "retrieval": {"mean_ms": 5.575090617639944, "median_ms": 5.2756500081159174, "p95_ms": 7.944599958136678}, "total_pipeline": {"mean_ms": 3346.023231242725, "median_ms": 3250.2106499741785, "p95_ms": 4960.897900047712}}`

## VECTOR

`{"question_generation": {"mean_ms": 3054.013387503801, "median_ms": 3095.050449948758, "p95_ms": 4307.049699942581}, "retrieval": {"mean_ms": 499.9537156181759, "median_ms": 499.6300468847039, "p95_ms": 522.6962468514103}, "total_pipeline": {"mean_ms": 3553.967103121977, "median_ms": 3586.06099680037, "p95_ms": 4805.063446860004}}`

## HYBRID

`{"question_generation": {"mean_ms": 3056.6975999972783, "median_ms": 2980.208399996627, "p95_ms": 4522.003100020811}, "retrieval": {"mean_ms": 505.62424997769995, "median_ms": 505.03039696923224, "p95_ms": 531.9484468709561}, "total_pipeline": {"mean_ms": 3562.3218499749782, "median_ms": 3487.6614467866602, "p95_ms": 5026.938447022985}}`
