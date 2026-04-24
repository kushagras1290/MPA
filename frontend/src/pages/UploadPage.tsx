import { useState } from "react";
import { errorReportUrl, magentoCsvUrl, templateDownloadUrl, uploadProductFile } from "../api/client";

export function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [batchId, setBatchId] = useState<number | null>(null);
  const [message, setMessage] = useState<string>("");

  async function onUpload() {
    if (!file) return;
    setMessage("Uploading and validating...");
    try {
      const response = await uploadProductFile(file);
      setBatchId(response.batch_id);
      setMessage(`${response.message} Rows: ${response.total_rows}`);
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Upload failed");
    }
  }

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
          <button className="primary-button" onClick={onUpload} disabled={!file}>
            Validate and Stage
          </button>
        </div>
        {message && <p>{message}</p>}
      </div>

      {batchId && (
        <div className="card">
          <h3>3. Output</h3>
          <p>Batch ID: <strong>{batchId}</strong></p>
          <a className="secondary-button" href={magentoCsvUrl(batchId)} style={{ marginRight: 12 }}>
            Download Magento CSV
          </a>
          <a className="secondary-button" href={errorReportUrl(batchId)}>
            Download Error Report
          </a>
        </div>
      )}
    </>
  );
}
