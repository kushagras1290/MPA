import { useEffect, useMemo, useState } from "react";
import { listStagedProducts } from "../api/client";
import type { ProductStaging } from "../api/client";

export function DashboardPage() {
  const [products, setProducts] = useState<ProductStaging[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;

    async function loadProducts() {
      try {
        const stagedProducts = await listStagedProducts();
        if (!cancelled) {
          setProducts(stagedProducts);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : "Failed to load dashboard metrics");
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    void loadProducts();
    return () => {
      cancelled = true;
    };
  }, []);

  const metrics = useMemo(() => {
    const pending = products.filter((product) => product.stage_status === "pending_approval").length;
    const approved = products.filter((product) => product.stage_status === "approved").length;
    const rejected = products.filter((product) => product.stage_status === "rejected").length;
    return { pending, approved, rejected };
  }, [products]);

  return (
    <>
      <h2>Catalog Automation Dashboard</h2>
      <p className="muted">
        Operational overview for Magento product intake, validation, staging, export, and publishing.
      </p>

      <div className="grid grid-3">
        <div className="card">
          <div className="muted">Pending Approval</div>
          <div className="metric">{loading ? "-" : metrics.pending}</div>
        </div>
        <div className="card">
          <div className="muted">Approved</div>
          <div className="metric">{loading ? "-" : metrics.approved}</div>
        </div>
        <div className="card">
          <div className="muted">Rejected</div>
          <div className="metric">{loading ? "-" : metrics.rejected}</div>
        </div>
      </div>

      {error && <p className="alert alert-error">{error}</p>}

      <div className="card">
        <h3>Recommended workflow</h3>
        <p>
          Upload file -&gt; Validate -&gt; Stage -&gt; Review -&gt; Export Magento CSV or Push Draft
          -&gt; Publish from Magento.
        </p>
      </div>
    </>
  );
}
