import React, { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [scenarios, setScenarios] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchScenarios = async () => {
    const res = await axios.get("http://localhost:8082/scenarios");
    setScenarios(res.data.reverse());
  };

  const generateBug = async () => {
    setLoading(true);
    await axios.post("http://localhost:8082/generate");
    console.log('kiki')
    await fetchScenarios();
    setLoading(false);
  };

  useEffect(() => {
    fetchScenarios();
  }, []);

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h1>KubeChaosAI Dashboard</h1>
      <button onClick={generateBug} disabled={loading}>
        {loading ? "Generating..." : "Generate New Chaos YAML"}
      </button>

      <h2 style={{ marginTop: "2rem" }}>Generated Scenarios</h2>
      {scenarios.map((entry, idx) => (
        <div key={idx} style={{ background: "#f4f4f4", padding: "1rem", marginBottom: "1rem", borderRadius: "8px" }}>
          <strong>Time:</strong> {entry.timestamp} <br />
          <strong>File:</strong> {entry.scenario} <br />
          <strong>Issues:</strong>
          {entry.issues.length === 0 ? (
            <span style={{ color: "green" }}> ✅ No issues detected</span>
          ) : (
            <ul>
              {entry.issues.map((issue, i) => (
                <li key={i} style={{ color: "red" }}>
                  {issue.reason} — Pod: {issue.pod} in NS: {issue.namespace}
                </li>
              ))}
            </ul>
          )}
        </div>
      ))}
    </div>
  );
}

export default App;
