import React, { useEffect, useState } from "react";
import "../style/review-table.css";

// function normalizeBool(v) {
//   if (v === true || v === false) return v;
//   if (v === 1 || v === "1") return true;
//   if (v === 0 || v === "0") return false;
//   if (typeof v === "string") {
//     const s = v.trim().toLowerCase();
//     if (["true", "yes", "y"].includes(s)) return true;
//     if (["false", "no", "n"].includes(s)) return false;
//   }
//   return null; // not been checked yet
// }

// // const CheckIcon = ({ value }) => {
// //   const cls = value === true ? "check-true" : value === false ? "check-false" : "check-pending";
// //   const symbol = value === true ? "✔" : value === false ? "✘" : "·";
// //   return <span className={`check ${cls}`}>{symbol}</span>;
// // };

// // 1) 可点击的图标：支持点击切换、加 title 提示、被改判时加样式
// const CheckIcon = ({ value, overridden, onClick }) => {
//   const cls =
//     value === true
//       ? "check-true"
//       : value === false
//       ? "check-false"
//       : "check-pending";
//   const symbol = value === true ? "✔" : value === false ? "✘" : "·";
//   const extra = overridden ? " check-overridden" : "";
//   return (
//     <span
//       className={`check ${cls}${extra} check-clickable`}
//       title={overridden ? "已人工改判（点击撤销或切换）" : "点击人工改判/撤销"}
//       onClick={onClick}
//       role="button"
//     >
//       {symbol}
//     </span>
//   );
// };

// // export default function ReviewTable({ rows: incomingRows = [] }) {
// //   const [rows, setRows] = useState([]);

// //   useEffect(() => {
// //     setRows((incomingRows || []).map(r => ({ ...r, check: normalizeBool(r.check) })));
// //   }, [incomingRows]);

// //   return (
// //     <div className="rt-card">
// //       <table className="rt-table">
// //         <thead>
// //           <tr><th>Data</th><th>Extracted</th><th>Expected</th><th>Previous</th></tr>
// //         </thead>
// //         <tbody>
// //           {rows.length === 0 && <tr><td colSpan="4">Loading…</td></tr>}
// //           {rows.map(r => (
// //             <tr key={r.key}>
// //               <td><CheckIcon value={r.check} /><span className="rt-label">{r.label}</span></td>
// //               <td>{r.extracted ?? "—"}</td>
// //               <td>{r.expected ?? "—"}</td>
// //               <td>{r.previous ?? "—"}</td>
// //             </tr>
// //           ))}
// //         </tbody>
// //       </table>
// //     </div>
// //   );
// // }

// export default function ReviewTable({ rows: incomingRows = [] }) {
//   const [rows, setRows] = useState([]);

//   // 保存后端原始判定，便于撤销
//   useEffect(() => {
//     const normalized = (incomingRows || []).map((r) => ({
//       ...r,
//       check: normalizeBool(r.check),          // 当前显示用
//       originalCheck: normalizeBool(r.check),  // 后端原值
//       overridden: false,                      // 是否被人工改判
//     }));
//     setRows(normalized);
//   }, [incomingRows]);

//   const toggleRow = (idx) => {
//     setRows((prev) =>
//       prev.map((r, i) => {
//         if (i !== idx) return r;

//         if (r.check === null) {
//           return { ...r, check: true, overridden: true };
//         }

//         if (r.overridden) {
//           const next =
//             r.check === r.originalCheck
//               ? !r.originalCheck
//               : r.originalCheck;
//           const stillOverridden = next !== r.originalCheck;
//           return {
//             ...r,
//             check: next,
//             overridden: stillOverridden,
//           };
//         }

//         return { ...r, check: !r.check, overridden: true };
//       })
//     );
//   };

//   return (
//     <div className="rt-card">
//       <div style={{ padding: "8px 12px", color: "#64748b", fontSize: 14 }}>
//         Hint: You can manually review by click ✔/✘ to switch the results.
//       </div>
//       <table className="rt-table">
//         <thead>
//           <tr>
//             <th>Data</th>
//             <th>Extracted</th>
//             <th>Expected</th>
//             <th>Previous</th>
//           </tr>
//         </thead>
//         <tbody>
//           {rows.length === 0 && (
//             <tr>
//               <td colSpan="4">Loading…</td>
//             </tr>
//           )}
//           {rows.map((r, idx) => (
//             <tr key={r.key}>
//               <td>
//                 <CheckIcon
//                   value={r.check}
//                   overridden={r.overridden}
//                   onClick={() => toggleRow(idx)}
//                 />
//                 <span className="rt-label">{r.label}</span>
//                 {r.overridden && (
//                   <span className="rt-badge">Overridden</span>
//                 )}
//               </td>
//               <td>{r.extracted ?? "—"}</td>
//               <td>{r.expected ?? "—"}</td>
//               <td>{r.previous ?? "—"}</td>
//             </tr>
//           ))}
//         </tbody>
//       </table>
//     </div>
//   );
// }

function normalizeBool(v) {
  if (v === true || v === false) return v;
  if (v === 1 || v === "1") return true;
  if (v === 0 || v === "0") return false;
  if (typeof v === "string") {
    const s = v.trim().toLowerCase();
    if (["true", "yes", "y"].includes(s)) return true;
    if (["false", "no", "n"].includes(s)) return false;
  }
  return null;
}

const CheckIcon = ({ value, overridden, onClick }) => {
  const cls =
    value === true
      ? "check-true"
      : value === false
      ? "check-false"
      : "check-pending";
  const symbol = value === true ? "✔" : value === false ? "✘" : "·";
  const extra = overridden ? " check-overridden" : "";
  return (
    <span
      className={`check ${cls}${extra} check-clickable`}
      title={overridden ? "已人工改判（点击撤销或切换）" : "点击人工改判/撤销"}
      onClick={onClick}
      role="button"
    >
      {symbol}
    </span>
  );
};

export default function ReviewTable({ rows: incomingRows = [] }) {
  const [rows, setRows] = useState([]);
  const [allApproved, setAllApproved] = useState(false);

  useEffect(() => {
    const normalized = (incomingRows || []).map((r) => ({
      ...r,
      check: normalizeBool(r.check),
      originalCheck: normalizeBool(r.check),
      overridden: false,
    }));
    setRows(normalized);
    setAllApproved(normalized.every((r) => r.check === true));
  }, [incomingRows]);

  const toggleRow = (idx) => {
    setRows((prev) => {
      const updated = prev.map((r, i) => {
        if (i !== idx) return r;

        if (r.check === null) {
          return { ...r, check: true, overridden: true };
        }

        if (r.overridden) {
          const next = r.check === r.originalCheck ? !r.originalCheck : r.originalCheck;
          const stillOverridden = next !== r.originalCheck;
          return { ...r, check: next, overridden: stillOverridden };
        }

        return { ...r, check: !r.check, overridden: true };
      });

      // 检查是否全为 true
      const all = updated.every((r) => r.check === true);
      setAllApproved(all);

      return updated;
    });
  };

  return (
    <div className="rt-card">
      <div style={{ padding: "8px 12px", color: "#64748b", fontSize: 14 }}>
        Hint: You can manually review by clicking ✔/✘ to switch the results.
      </div>
      <table className="rt-table">
        <thead>
          <tr>
            <th>Data</th>
            <th>Extracted</th>
            <th>Expected</th>
            <th>Previous</th>
          </tr>
        </thead>
        <tbody>
          {rows.length === 0 && (
            <tr>
              <td colSpan="4">Loading…</td>
            </tr>
          )}
          {rows.map((r, idx) => (
            <tr key={r.key}>
              <td>
                <CheckIcon
                  value={r.check}
                  overridden={r.overridden}
                  onClick={() => toggleRow(idx)}
                />
                <span className="rt-label">{r.label}</span>
                {r.overridden && (
                  <span className="rt-badge">Overridden</span>
                )}
              </td>
              <td>{r.extracted ?? "—"}</td>
              <td>{r.expected ?? "—"}</td>
              <td>{r.previous ?? "—"}</td>
            </tr>
          ))}
        </tbody>

        {allApproved && (
          <tfoot>
            <tr>
              <td colSpan="4" style={{
                textAlign: "right",
                paddingTop: "10px",
                fontStyle: "italic",
                color: "#3b82f6",
                fontSize: "14px"
              }}>
                🖋 Auto Signature by Reviewer
              </td>
            </tr>
          </tfoot>
        )}
      </table>
    </div>
  );
}