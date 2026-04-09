/**
 * ProductList — displays the product catalog and handles purchases.
 *
 * Also includes the "Add 5 credits" button since it's closely related
 * to the purchasing flow (user needs credits to buy).
 *
 * Props:
 *   credits        — current user balance (for disabling buy buttons)
 *   onBalanceChange — callback to refresh balance in parent after purchase/topup
 */

import { useState, useEffect } from "react";
import { fetchProducts, purchaseProduct, addCredits } from "../api";

const cardStyle = {
  border: "1px solid #ddd",
  borderRadius: 8,
  padding: 16,
  marginBottom: 12,
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
};

const sectionStyle = {
  marginBottom: 32,
};

export default function ProductList({ credits, onBalanceChange }) {
  const [products, setProducts] = useState([]);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(true);

  // Fetch products on mount
  useEffect(() => {
    fetchProducts()
      .then(setProducts)
      .catch(() => setMessage("Failed to load products."))
      .finally(() => setLoading(false));
  }, []);

  /** Add 5 credits to the user's balance */
  const handleAddCredits = async () => {
    try {
      await addCredits();
      onBalanceChange(); // Refresh balance in parent
      setMessage("Added 5 credits!");
    } catch {
      setMessage("Failed to add credits.");
    }
  };

  /** Purchase a product by ID */
  const handleBuy = async (productId, productName) => {
    try {
      await purchaseProduct(productId);
      onBalanceChange(); // Refresh balance in parent
      setMessage(`Purchased "${productName}" successfully!`);
    } catch (err) {
      const detail = err.response?.data?.detail || "Purchase failed.";
      setMessage(detail);
    }
  };

  if (loading) return <p>Loading products...</p>;

  return (
    <section style={sectionStyle}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h2>Products</h2>
        <button onClick={handleAddCredits} style={{ padding: "8px 16px" }}>
          + Add 5 Credits
        </button>
      </div>

      {message && (
        <p style={{ color: "#1976d2", marginBottom: 12 }}>{message}</p>
      )}

      {products.map((product) => (
        <div key={product.id} style={cardStyle}>
          <div>
            <strong>{product.name}</strong>
            <p style={{ margin: "4px 0", color: "#666", fontSize: 14 }}>
              {product.description}
            </p>
            <span style={{ fontWeight: "bold" }}>{product.price} credits</span>
          </div>
          <button
            onClick={() => handleBuy(product.id, product.name)}
            disabled={credits < product.price}
            style={{ padding: "8px 16px", whiteSpace: "nowrap" }}
          >
            {credits < product.price ? "Not enough credits" : "Buy"}
          </button>
        </div>
      ))}
    </section>
  );
}
