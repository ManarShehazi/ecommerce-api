/**
 * OrderHistory — displays the user's past purchases.
 *
 * Fetches orders from the API and shows them in a table.
 * Includes a refresh button so users can see newly purchased items
 * without reloading the page.
 */

import { useState, useEffect } from "react";
import { fetchOrders } from "../api";

const tableStyle = {
  width: "100%",
  borderCollapse: "collapse",
  marginTop: 12,
};

const thTdStyle = {
  padding: "8px 12px",
  borderBottom: "1px solid #ddd",
  textAlign: "left",
};

export default function OrderHistory() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadOrders = () => {
    setLoading(true);
    fetchOrders()
      .then(setOrders)
      .catch(() => {})
      .finally(() => setLoading(false));
  };

  // Fetch on mount
  useEffect(() => {
    loadOrders();
  }, []);

  return (
    <section>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h2>Order History</h2>
        <button onClick={loadOrders} style={{ padding: "6px 12px" }}>
          Refresh
        </button>
      </div>

      {loading && <p>Loading orders...</p>}

      {!loading && orders.length === 0 && (
        <p style={{ color: "#888" }}>No purchases yet.</p>
      )}

      {!loading && orders.length > 0 && (
        <table style={tableStyle}>
          <thead>
            <tr>
              <th style={thTdStyle}>Product</th>
              <th style={thTdStyle}>Price Paid</th>
              <th style={thTdStyle}>Date</th>
            </tr>
          </thead>
          <tbody>
            {orders.map((order) => (
              <tr key={order.id}>
                <td style={thTdStyle}>{order.product_name}</td>
                <td style={thTdStyle}>{order.price_paid} credits</td>
                <td style={thTdStyle}>
                  {new Date(order.created_at).toLocaleString()}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  );
}
