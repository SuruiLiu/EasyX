import React, { useState } from "react";
import "../style/status-block.css";

/** Status at top right */
function Pill({ text = "match" }) {
  return <span className="pill">{text}</span>;
}

/** right/wrong/dot */
function Bullet({ ok }) {
  return (
    <span className={`bullet ${ok ? "bullet-green" : "bullet-red"}`}>
      {ok ? "✓" : "✕"}
    </span>
  );
}

/** Folded area（Email / Contract） */
function Collapse({ title, children, defaultOpen = true }) {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <div className="collapse">
      <button className="collapse-head" onClick={() => setOpen(o => !o)}>
        <span className="collapse-title">{title}</span>
        <span className={`chev ${open ? "chev-open" : ""}`}>⌄</span>
      </button>
      {open && <div className="collapse-body">{children}</div>}
    </div>
  );
}

export default function StatusBlock({
  statusText = "Status",
  emailItems = [],
  contractItems = [],
}) {
  return (
    <section className="status-card">
      <div className="card-head">
        <div className="card-title">
          Timesheet <span className="muted">Employee Name, Week Worked</span>
        </div>
        <div className="card-status">
          <Pill text={statusText} />
        </div>
      </div>

      <Collapse title="Email" defaultOpen={true}>
        <ul className="checklist">
          {emailItems.map((it, i) => (
            <li key={i} className="check-item">
              <Bullet ok={!!it.ok} />
              <span>{it.label}</span>
            </li>
          ))}
        </ul>
      </Collapse>

      <Collapse title="Contract Particulars" defaultOpen={false}>
        <ul className="checklist">
          {contractItems.map((it, i) => (
            <li key={i} className="check-item">
              <Bullet ok={!!it.ok} />
              <span>{it.label}</span>
            </li>
          ))}
        </ul>
      </Collapse>
    </section>
  );
}
