import { useCallback, useEffect, useState } from "react";
import { approveStagedProduct, listStagedProducts, rejectStagedProduct } from "../api/client";
import type { ProductStaging } from "../api/client";

export function ReviewPage() {
  const [products, setProducts] = useState<ProductStaging[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [busyProductId, setBusyProductId] = useState<number | null>(null);

  const loadProducts = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      setProducts(await listStagedProducts());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load staged products");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void loadProducts();
  }, [loadProducts]);

  async function updateStatus(productId: number, action: "approve" | "reject") {
    setBusyProductId(productId);
    setError("");
    try {
      const updated =
        action === "approve"
          ? await approveStagedProduct(productId)
          : await rejectStagedProduct(productId);
      setProducts((current) =>
        current.map((product) => (product.id === productId ? updated : product)),
      );
    } catch (err) {
      setError(err instanceof Error ? err.message : "Status update failed");
    } finally {
      setBusyProductId(null);
    }
  }

  function formatNumber(value: number | null): string {
    return value === null ? "-" : value.toLocaleString();
  }

  return (
    <>
      <h2>Product Review</h2>
      <p className="muted">Review staged products before pushing to Magento.</p>

      <div className="card">
        <div className="toolbar">
          <button className="secondary-button" onClick={loadProducts} disabled={loading}>
            Refresh
          </button>
        </div>
        {error && <p className="alert alert-error">{error}</p>}
        {loading ? (
          <p className="muted">Loading staged products...</p>
        ) : products.length === 0 ? (
          <p className="empty-state">No staged products are waiting for review.</p>
        ) : (
          <div className="table-wrap">
            <table className="table">
              <thead>
                <tr>
                  <th>SKU</th>
                  <th>Name</th>
                  <th>Gemstone</th>
                  <th>Origin</th>
                  <th>Weight</th>
                  <th>Price</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {products.map((product) => (
                  <tr key={product.id}>
                    <td>{product.sku}</td>
                    <td>{product.name}</td>
                    <td>{product.gemstone ?? "-"}</td>
                    <td>{product.origin ?? "-"}</td>
                    <td>
                      {formatNumber(product.carat_weight)} ct /{" "}
                      {formatNumber(product.weight_ratti)} ratti
                    </td>
                    <td>{formatNumber(product.price)}</td>
                    <td>
                      <span className="badge">{product.stage_status}</span>
                    </td>
                    <td>
                      <div className="button-row">
                        <button
                          className="small-button"
                          onClick={() => void updateStatus(product.id, "approve")}
                          disabled={busyProductId === product.id}
                        >
                          Approve
                        </button>
                        <button
                          className="small-button danger-button"
                          onClick={() => void updateStatus(product.id, "reject")}
                          disabled={busyProductId === product.id}
                        >
                          Reject
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </>
  );
}
