export interface PredictionResponse {
  prediction: string;
  confidence: number;
  risk_level: "High" | "Medium" | "Low";
  filename: string;
}
