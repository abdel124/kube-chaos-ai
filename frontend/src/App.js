import React, { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [scenarios, setScenarios] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchScenarios = async () => {
    try {
      const res = await axios.get("http://localhost:8082/scenarios");
      setScenarios(res.data.reverse());
    } catch (err) {
      console.error("Failed to fetch scenarios:", err);
    }
  };

  const generateBug = async () => {
    setLoading(true);
    try {
      await axios.post("http://localhost:8082/generate");
      await fetchScenarios();
    } catch (err) {
      console.error("Generation failed:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchScenarios();
  }, []);

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h1>KubeChaosAI Dashboard</h1>
      <button
        onClick={generateBug}
        disabled={loading}
        style={{ padding: "0.5rem 1rem", background: "#007bff", color: "#fff", border: "none", borderRadius: "5px" }}
      >
        {loading ? "Generating..." : "Generate Chaos Scenario"}
      </button>

      <h2 style={{ marginTop: "2rem" }}>Generated Scenarios</h2>
      {scenarios.length === 0 ? (
        <p>No scenarios yet.</p>
      ) : (
        scenarios.map((entry, idx) => (
          <div
            key={idx}
            style={{ background: "#f9f9f9", padding: "1rem", borderRadius: "8px", marginBottom: "1rem" }}
          >
            <strong>Timestamp:</strong> {entry.timestamp} <br />
            <strong>File:</strong> {entry.scenario} <br />
            <strong>Issues:</strong>
            {entry.issues.length === 0 ? (
              <span style={{ color: "green" }}> ✅ No issues</span>
            ) : (
              <ul style={{ color: "red" }}>
                {entry.issues.map((issue, i) => (
                  <li key={i}>
                    {issue.reason} — Pod: {issue.pod}, NS: {issue.namespace}
                  </li>
                ))}
              </ul>
            )}
          </div>
        ))
      )}
    </div>
  );
}

export default App;
