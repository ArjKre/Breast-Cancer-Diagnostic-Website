import UploadBox from "../components/UploadBox";

export default function Home() {
  return (
    <div className="min-h-screen bg-slate-100">

      <div className="max-w-4xl mx-auto p-10">

        <h1 className="text-5xl font-bold mb-4">
          Breast Cancer Screening Using CNN
        </h1>

        <p className="text-gray-600 mb-8">
          Upload a mammogram image and
          receive an AI-assisted analysis.
        </p>

        <div className="bg-white p-8 rounded-xl shadow">

          <UploadBox />

        </div>

        <div className="mt-8 text-sm text-gray-500">
          This tool is for educational and
          research purposes only and should
          not be used as a medical diagnosis.
        </div>

      </div>

    </div>
  );
}
