const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export type ProductStaging = {
  id: number;
  sku: string;
  name: string;
  gemstone: string | null;
  origin: string | null;
  carat_weight: number | null;
  weight_ratti: number | null;
  price: number | null;
  qty: number;
  is_in_stock: boolean;
  stage_status: string;
  validation_status: string;
};

export async function listStagedProducts(): Promise<ProductStaging[]> {
  const response = await fetch(`${API_BASE_URL}/api/products/staging`);
  if (!response.ok) {
    throw new Error("Failed to load staged products");
  }
  return response.json();
}

export async function uploadProductFile(file: File): Promise<{ batch_id: number; status: string; message: string; total_rows: number }> {
  const data = new FormData();
  data.append("file", file);

  const response = await fetch(`${API_BASE_URL}/api/uploads/product-file`, {
    method: "POST",
    body: data
  });

  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.detail ?? "Upload failed");
  }

  return response.json();
}

export function templateDownloadUrl(): string {
  return `${API_BASE_URL}/api/templates/product-upload`;
}

export function magentoCsvUrl(batchId: number): string {
  return `${API_BASE_URL}/api/uploads/${batchId}/magento-csv`;
}

export function errorReportUrl(batchId: number): string {
  return `${API_BASE_URL}/api/uploads/${batchId}/error-report`;
}
