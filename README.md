An end-to-end, unsupervised machine learning telemetry pipeline that parses unstructured, multi-gigabyte system logs, engineers temporal sliding-window features, filters system traits via a Deep Autoencoder neural network, and visualizes live anomalies.

[ Raw HDFS Logs ] ──> ( Drain3 Log Parser ) ──> [ Template Sequences ]
│
[ Web Dashboard ] <── ( FastAPI REST API ) <── [ Trained Autoencoder Weight Model ]

1. **Log Parsing Engine:** Streams free-text records line-by-line using a tree-based streaming clustering algorithm to replace variable data parameters with static template IDs.
2. **Feature Vectorization:** Slices sequential template strings into overlapping sliding sequences to construct spatial frequency matrices.
3. **Cloud GPU Acceleration:** Uses an unsupervised multi-layer PyTorch Autoencoder to map baseline operational behavior and pinpoint structural variations.
4. **Production Routing Server:** Re-maps trained weights down to a local FastAPI instance to serve real-time network endpoints without local GPU constraints.
5. **Analytics Interface:** Renders live, high-severity operational anomalies inside an optimized React dashboard.
