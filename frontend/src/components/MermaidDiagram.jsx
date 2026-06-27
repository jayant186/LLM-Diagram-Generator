import { useEffect, useRef } from "react";
import mermaid from "mermaid";

mermaid.initialize({
  startOnLoad: false,
  securityLevel: "loose",
  theme: "default",

  flowchart: {
    useMaxWidth: false,
    htmlLabels: true,
    nodeSpacing: 70,
    rankSpacing: 80,
    curve: "basis",
  },
});

function MermaidDiagram({ chart }) {
  const ref = useRef(null);

useEffect(() => {
  let cancelled = false;

  const renderDiagram = async () => {
    if (!chart || !ref.current) return;

    ref.current.innerHTML = "";

    try {
      const id = `mermaid-${crypto.randomUUID()}`;
      const { svg } = await mermaid.render(id, chart);

      if (!cancelled && ref.current) {
        ref.current.innerHTML = svg;
      }
    } catch (err) {
      console.error("Mermaid Error:", err);

      if (!cancelled && ref.current) {
        ref.current.innerHTML = `
          <div style="color:red;padding:10px">
            Invalid Mermaid syntax.
          </div>
        `;
      }
    }
  };

  renderDiagram();

  return () => {
    cancelled = true;
  };
}, [chart]);

  return <div ref={ref}></div>;
}

export default MermaidDiagram;