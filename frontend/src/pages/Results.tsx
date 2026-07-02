import { useLocation } from "react-router-dom";

export default function Results() {
  const location = useLocation();
  const data = location.state;

  if (!data) {
    return (
      <div className="p-8">
        No prediction available.
      </div>
    );
  }

  const isMalignant = data.prediction === "Malignant";
  const riskLevel =
    data.confidence > 0.8
      ? "High"
      : data.confidence > 0.5
      ? "Medium"
      : "Low";

  return (
    <div className="p-8 bg-white shadow rounded-xl">

  <h2 className="text-3xl font-bold mb-6">
    Analysis Result
  </h2>

  <div className="space-y-4">

    <div>
      <span className={
		  isMalignant ? "text-red-600" : "text-green-600"
	  }>
        Prediction:
      </span>{" "}
      {data.prediction}
    </div>

    <div>
      <span className="font-semibold">
        Confidence:
      </span>{" "}
      {(data.confidence * 100).toFixed(2)}%
    </div>
	<div>
	  <span className="font-semibold">
		Risk Level:
	  </span>{" "}
	  {riskLevel}
	</div>
    <div>
      <span className="font-semibold">
        Uploaded File:
      </span>{" "}
      {data.filename}
    </div>

  </div>

</div>
  );
}
