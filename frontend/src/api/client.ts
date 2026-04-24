const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

type JsonRecord = Record<string, unknown>;

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

export type UploadResult = {
  batch_id: number;
  status: string;
  message: string;
  total_rows: number;
};

export type AttributeMapping = {
  id: number;
  attribute_code: string;
  human_value: string;
  magento_label: string;
  magento_option_id: string;
  is_active: boolean;
};

export type AttributeMappingInput = Omit<AttributeMapping, "id">;

function isRecord(value: unknown): value is JsonRecord {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

async function errorMessage(response: Response): Promise<string> {
  const body: unknown = await response.json().catch(() => undefined);
  if (isRecord(body) && typeof body.detail === "string") {
    return body.detail;
  }
  return `Request failed with status ${response.status}`;
}

async function requestJson<T>(input: RequestInfo | URL, init?: RequestInit): Promise<T> {
  const response = await fetch(input, init);
  if (!response.ok) {
    throw new Error(await errorMessage(response));
  }
  return response.json() as Promise<T>;
}

export async function listStagedProducts(): Promise<ProductStaging[]> {
  return requestJson<ProductStaging[]>(`${API_BASE_URL}/api/products/staging`);
}

export async function uploadProductFile(file: File): Promise<UploadResult> {
  const data = new FormData();
  data.append("file", file);

  return requestJson<UploadResult>(`${API_BASE_URL}/api/uploads/product-file`, {
    method: "POST",
    body: data
  });
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

export async function approveStagedProduct(productId: number): Promise<ProductStaging> {
  return requestJson<ProductStaging>(`${API_BASE_URL}/api/products/staging/${productId}/approve`, {
    method: "POST"
  });
}

export async function rejectStagedProduct(productId: number): Promise<ProductStaging> {
  return requestJson<ProductStaging>(`${API_BASE_URL}/api/products/staging/${productId}/reject`, {
    method: "POST"
  });
}

export async function listMappings(): Promise<AttributeMapping[]> {
  return requestJson<AttributeMapping[]>(`${API_BASE_URL}/api/mappings`);
}

export async function createMapping(payload: AttributeMappingInput): Promise<AttributeMapping> {
  return requestJson<AttributeMapping>(`${API_BASE_URL}/api/mappings`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  });
}
