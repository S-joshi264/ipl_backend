```mermaid
flowchart LR

A[User] --> B[Frontend UI\nHTML CSS JS]
B -->|POST /predict| C[FastAPI Backend]

C --> D[Data Processing]
D --> E[Feature Encoding + Scaling]
E --> F[ML Model]

F --> G[Prediction]
G --> C
C -->|Response| B

C --> H[Logs]

subgraph Training
I[Raw Data] --> J[Feature Engineering]
J --> K[Train Model]
K --> L[Model.pkl + Scaler.pkl]
end

L --> F
