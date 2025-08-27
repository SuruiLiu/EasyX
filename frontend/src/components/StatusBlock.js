import React, { useState } from "react";
import "../style/status-block.css";

/** 小徽章：右上角的 Status */
function Pill({ text = "match" }) {
  return <span className="pill">{text}</span>;
}

/** 勾/叉小圆点 */
function Bullet({ ok }) {
  return (
    <span className={`bullet ${ok ? "bullet-green" : "bullet-red"}`}>
      {ok ? "✓" : "✕"}
    </span>
  );
}

/** 可折叠区块（Email / Contract） */
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

/** 你要的整个模块 */
export default function StatusBlock({
  statusText = "Status",
  emailItems = [],
  contractItems = [],
}) {
  return (
    <section className="status-card">
      {/* 顶部标题行 */}
      <div className="card-head">
        <div className="card-title">
          Timesheet <span className="muted">Employee Name, Week Worked</span>
        </div>
        <div className="card-status">
          <Pill text={statusText} />
        </div>
      </div>

      {/* Email 折叠 */}
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

      {/* Contract Particulars 折叠 */}
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
