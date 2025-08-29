import React, { useState, useMemo } from "react";
import "../style/pdf-preview.css";

export default function PdfPreview({ pdfUrl, title = "PDF Preview" }) {
  const [errored, setErrored] = useState(false);

  const src = useMemo(() => {
    if (!pdfUrl) return "";
    const join = pdfUrl.includes("#") ? "&" : "#";
    return `${pdfUrl}${join}zoom=page-width&view=FitH&toolbar=0&navpanes=0`;
  }, [pdfUrl]);

  return (
    <section className="pdf-card">
      <div className="pdf-header">{title}</div>

      {!pdfUrl || errored ? (
        <div className="pdf-placeholder">PDF Preview</div>
      ) : (
        <div className="pdf-frame">
          <embed
            src={src}
            type="application/pdf"
            className="pdf-embed"
            onError={() => setErrored(true)}
          />
        </div>
      )}
    </section>
  );
}
