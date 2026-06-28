import { useState, useRef } from "react";
import { toPng } from "html-to-image";
import MermaidDiagram from "./components/MermaidDiagram";
const API_URL = "https://llm-diagram-generator.onrender.com";

function App() {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [pdfFile, setPdfFile] = useState(null);
  const [mermaidCode, setMermaidCode] = useState("");
  const [error, setError] = useState("");
  const diagramRef = useRef(null);

  const handlePdfChange = (e) => {
    setPdfFile(e.target.files[0]);
  };

  const handlePdfUpload = async () => {

    if (!pdfFile) {
        alert("Please select a PDF");
        return;
    }

    setLoading(true);
    setMermaidCode("");
    setError("");

    const formData = new FormData();

    formData.append("pdf", pdfFile);

    try {

        const response = await fetch(`${API_URL}/generate-pdf`,
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        if (!response.ok) {
        throw new Error(data.error || "Something went wrong");
        }

        // setResult(data);
        setMermaidCode(data.mermaid);
        setError("");

    } catch (err) {

        setError(err.message);
        console.error(err);

    } finally {

        setLoading(false);
    }
  };

  const handleGenerate = async () => {
    setLoading(true);
    // setResult(null);
    setMermaidCode("");
    setError("");

    try {
      const response = await fetch(
        `${API_URL}/generate`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            text,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Something went wrong");
      }

      // setResult(data);
      setMermaidCode(data.mermaid);
      setError("");
    } catch (err) {
      setError(err.message);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleExportPNG = async () => {
    if (!diagramRef.current) return;

    try {
      const dataUrl = await toPng(diagramRef.current);

      const link = document.createElement("a");
      link.download = "diagram.png";
      link.href = dataUrl;
      link.click();
    } catch (err) {
      console.error("Export failed:", err);
    }
  };

  const handleExportSVG = () => {
    if (!diagramRef.current) return;

    const svg = diagramRef.current.querySelector("svg");

    if (!svg) {
      alert("No diagram found.");
      return;
    }

    const svgData = new XMLSerializer().serializeToString(svg);

    const blob = new Blob([svgData], {
      type: "image/svg+xml;charset=utf-8",
    });

    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = url;
    link.download = "diagram.svg";
    link.click();

    URL.revokeObjectURL(url);
  };

  return (
    <div style={{ padding: "20px",textAlign: "center", }}>
      <h1>LLM Diagram Generator</h1>

      <textarea
        rows="8"
        cols="60"
        placeholder="Enter your paragraph..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <br />
      <br />

      <select value="flowchart" disabled>
        <option value="flowchart">Flowchart</option>
      </select>

      <br />
      <br />

      <button
        onClick={handleGenerate}
        disabled={loading}
      >
        {loading
          ? "Generating..."
          : "Generate Diagram"}
      </button>

      <hr />

      <h2>Generate Diagram from PDF</h2>

      <input
        type="file"
        accept=".pdf"
        onChange={handlePdfChange}
      />

      <br />
      <br />

      <button
        onClick={handlePdfUpload}
        disabled={loading || !pdfFile}
      >
        {loading ? "Generating..." : "Generate From PDF"}
      </button>

      {error && (
        <p
          style={{
            color: "red",
            fontWeight: "bold",
            marginTop: "10px",
          }}
        >
          {error}
        </p>
      )}

      <br />
      <br />
      {mermaidCode && (
        <div
          style={{
            maxWidth: "900px",
            margin: "0 auto",
          }}
        >
          <h2>Editable Mermaid Code</h2>

          <textarea
            spellCheck={false}
            value={mermaidCode}
            onChange={(e) => setMermaidCode(e.target.value)}
            rows={12}
            style={{
              width: "100%",
              minHeight: "250px",
              resize: "vertical",
              fontFamily: "monospace",
              fontSize: "15px",
              padding: "10px",
              border: "1px solid #ccc",
              borderRadius: "6px",
            }}
          />

          <br />
          <br />

          <h2>Diagram Preview</h2>

          <div
            style={{
              overflowX: "auto",
              padding: "20px",
            }}
          >
            <div ref={diagramRef}>
              <MermaidDiagram chart={mermaidCode} />
            </div>
          </div>

          <br />

          <div
            style={{
              display: "flex",
              justifyContent: "center",
              gap: "12px",
              marginTop: "20px",
            }}
          >
            <button onClick={handleExportPNG}>
              Export PNG
            </button>

            <button onClick={handleExportSVG}>
              Export SVG
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;