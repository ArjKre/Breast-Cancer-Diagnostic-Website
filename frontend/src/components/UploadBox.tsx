import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { predictImage } from "../services/predict";

export default function UploadBox() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [preview, setPreview] = useState("");

  const navigate = useNavigate();

  const handleUpload = async () => {
	  if (!file) return;

	  try{
		  setLoading(false);

		  const formData = new FormData();
		  formData.append("file",file);

		  const response = predictImage(file);

		  navigate("/results",{
			  state: response,
		  });
	  }catch(error){
		  console.log(error);
		  alert("Upload Failed");
	  }finally{
		  setLoading(false);
	  }
  }

  return (
    <div className="flex flex-col gap-4">
      <input
        type="file"
        accept="image/*"
        onChange={(e) => {
			const selectedFile = e.target.files?.[0];
			
			if (!selectedFile) return;

			setFile(selectedFile);
			setPreview(
				URL.createObjectURL(selectedFile)
			);
        }}
      />
		{preview && (
		  <img
			src={preview}
			alt="preview"
			className="w-80 rounded border"
		  />
		)}
      <button onClick = {handleUpload} className="bg-blue-500 text-white p-2 rounded">
	  {loading ? "Analyzing.." : "Analyzed Mammogram"}
      </button>
    </div>
  );
}
