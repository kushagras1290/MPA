export function DashboardPage() {
  return (
    <>
      <h2>Catalog Automation Dashboard</h2>
      <p className="muted">
        Operational overview for Magento product intake, validation, staging, export, and publishing.
      </p>

      <div className="grid grid-3">
        <div className="card">
          <div className="muted">Pending Approval</div>
          <div className="metric">—</div>
        </div>
        <div className="card">
          <div className="muted">Validation Failed</div>
          <div className="metric">—</div>
        </div>
        <div className="card">
          <div className="muted">Magento Drafts</div>
          <div className="metric">—</div>
        </div>
      </div>

      <div className="card">
        <h3>Recommended workflow</h3>
        <p>
          Upload file → Validate → Stage → Review → Export Magento CSV or Push Draft → Publish from Magento.
        </p>
      </div>
    </>
  );
}
