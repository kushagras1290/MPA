import { useState } from "react";
import { errorReportUrl, magentoCsvUrl, templateDownloadUrl, uploadProductFile } from "../api/client";
import type { UploadResult } from "../api/client";

export function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<UploadResult | null>(null);
  const [error, setError] = useState<string>("");
  const [isUploading, setIsUploading] = useState(false);

  async function onUpload() {
    if (!file) return;
    setIsUploading(true);
    setError("");
    setResult(null);
    try {
      const response = await uploadProductFile(file);
      setResult(response);
    } catch (error) {
      setError(error instanceof Error ? error.message : "Upload failed");
    } finally {
      setIsUploading(false);
    }
  }

  const canDownloadCsv = result?.status === "validated";
  const canDownloadErrorReport = result !== null && result.status !== "validated";

  return (
    <>
      <h2>Bulk Product Upload</h2>
      <p className="muted">
        Upload Magento CSV/Excel product details. Products are validated and staged before publishing.
      </p>

      <div className="card">
        <h3>1. Download staff template</h3>
        <a className="secondary-button" href={templateDownloadUrl()}>
          Download Excel Template
        </a>
      </div>

      <div className="card">
        <h3>2. Upload product file</h3>
        <input
          className="input"
          type="file"
          accept=".csv,.xlsx,.xls"
          onChange={(event) => setFile(event.target.files?.[0] ?? null)}
        />
        <div style={{ marginTop: 16 }}>
          <button className="primary-button" onClick={onUpload} disabled={!file || isUploading}>
            {isUploading ? "Validating..." : "Validate and Stage"}
          </button>
        </div>
        {error && <p className="alert alert-error">{error}</p>}
        {result && (
          <p className={result.status === "validated" ? "alert alert-success" : "alert alert-error"}>
            {result.message} Rows: {result.total_rows}
          </p>
        )}
      </div>

      {result && (
        <div className="card">
          <h3>3. Output</h3>
          <p>
            Batch ID: <strong>{result.batch_id}</strong>
          </p>
          <div className="button-row">
            {canDownloadCsv && (
              <a className="secondary-button" href={magentoCsvUrl(result.batch_id)}>
                Download Magento CSV
              </a>
            )}
            {canDownloadErrorReport && (
              <a className="secondary-button" href={errorReportUrl(result.batch_id)}>
                Download Error Report
              </a>
            )}
          </div>
        </div>
      )}
    </>
  );
}
