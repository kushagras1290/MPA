import { useEffect, useState } from "react";
import { listStagedProducts, ProductStaging } from "../api/client";

export function ReviewPage() {
  const [products, setProducts] = useState<ProductStaging[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    listStagedProducts().then(setProducts).catch((err) => setError(err.message));
  }, []);

  return (
    <>
      <h2>Product Review</h2>
      <p className="muted">Review staged products before pushing to Magento.</p>

      <div className="card">
        {error && <p>{error}</p>}
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
            </tr>
          </thead>
          <tbody>
            {products.map((product) => (
              <tr key={product.id}>
                <td>{product.sku}</td>
                <td>{product.name}</td>
                <td>{product.gemstone}</td>
                <td>{product.origin}</td>
                <td>{product.carat_weight} ct / {product.weight_ratti} ratti</td>
                <td>{product.price}</td>
                <td><span className="badge">{product.stage_status}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}
