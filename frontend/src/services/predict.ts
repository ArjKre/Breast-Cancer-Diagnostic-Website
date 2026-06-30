import { api } from "./api";

export async function predictImage(
  file: File
) {
  const formData = new FormData();

  formData.append("file", file);

  const response = await api.post(
    "/predict",
    formData
  );

  return response.data;
}
