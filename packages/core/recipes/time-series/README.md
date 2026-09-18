## Time series

<!-- nota:ejemplo temporal -->

```html
{{EXAMPLE}}
```

**Use and limits:** Compare dated observations with UTC millisecond positions. Dates must be valid, unique, increasing ISO days. Absolute change is current minus previous; relative change divides by the absolute previous value. A zero baseline makes percentage change undefined; missing values prevent comparison. Name the compared records. No aggregation, timezone repair, causal inference or automatic judgment that an increase is good.
