import React, { useEffect, useState } from "react";
import StatusBlock from "../components/StatusBlock";
import PdfPreview from "../components/PdfPreview";
import ReviewTable from "../components/ReviewTable";

const API_BASE = "http://localhost:5001";
const CHECK_URL = `${API_BASE}/timesheet/check`;

const toBackendKey = (label) => {
  if (label === "Signatures?") return "Signatures";
  if (label === "Additional Text?") return "Additional Text";
  return label;
};

const rowsTemplate = [
  { key:"week", label:"Week Worked",       extracted:"11-17 August 2025", expected:"11-17 August 2025", previous:"4-10 August 2025" },
  { key:"mon",  label:"Monday Hours",      extracted:"8hrs",    expected:"8hrs",    previous:"8hrs" },
  { key:"tue",  label:"Tuesday Hours",     extracted:"7.5hrs",  expected:"8hrs",    previous:"7.5hrs" },
  { key:"wed",  label:"Wednesday Hours",   extracted:"6.25hrs", expected:"8hrs",    previous:"6.25hrs" },
  { key:"thu",  label:"Thursday Hours",    extracted:"8.75hrs", expected:"8hrs",    previous:"8.75hrs" },
  { key:"fri",  label:"Friday Hours",      extracted:"8hrs",    expected:"8hrs",    previous:"8hrs" },
  { key:"sat",  label:"Saturday Hours",    extracted:"0hrs",    expected:"0hrs",    previous:"0hrs" },
  { key:"sun",  label:"Sunday Hours",      extracted:"0hrs",    expected:"0hrs",    previous:"0hrs" },
  { key:"total",label:"Total Hours",       extracted:"40hrs",   expected:"40hrs",   previous:"40hrs" },
  { key:"sign", label:"Signatures?",       extracted:"Yes",     expected:"Yes",     previous:"" },
  { key:"extra",label:"Additional Text?",  extracted:"No",      expected:"No",      previous:"" },
];

export default function TimesheetReview() {
  const emailItems = [
    { label: "Expected email address", ok: true },
    { label: "Expected email subject", ok: true },
    { label: "No additional attachments", ok: true },
    { label: "Date Received, Email Text/Link to email", ok: true },
  ];
  const contractItems = [
    { label: "Employee Name", ok: true },
    { label: "Company", ok: true },
    { label: "PO#", ok: true },
    { label: "Customer", ok: true },
  ];

  const [rows, setRows] = useState(rowsTemplate);

  useEffect(() => {
    const f = (k) => rowsTemplate.find(r => r.key === k);
    const payload = {
      extracted: {
        week_worked: f("week")?.extracted,
        hours: {
          Mon: f("mon")?.extracted, Tue: f("tue")?.extracted, Wed: f("wed")?.extracted,
          Thu: f("thu")?.extracted, Fri: f("fri")?.extracted, Sat: f("sat")?.extracted, Sun: f("sun")?.extracted,
        },
        total_hours: f("total")?.extracted,
        signatures: (f("sign")?.extracted || "").toString().toLowerCase().startsWith("y"),
        additional_text: f("extra")?.extracted ?? "No",
        employee_name: "John Doe",
        po_number: "PO-001",
      },
      expected: {
        week_worked: f("week")?.expected,
        hours: {
          Mon: f("mon")?.expected, Tue: f("tue")?.expected, Wed: f("wed")?.expected,
          Thu: f("thu")?.expected, Fri: f("fri")?.expected, Sat: f("sat")?.expected, Sun: f("sun")?.expected,
        },
        total_hours: f("total")?.expected,
        employee_name: "John Doe",
        po_number: "PO-001",
        require_signature: true,
      }
    };

    (async () => {
      try {
        const res = await fetch(CHECK_URL, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });

        console.log("CHECK status:", res.status);
        const text = await res.text(); 
        let result = {};
        try { result = JSON.parse(text); } catch {}

        console.log("CHECK result:", result || text);

        if (!result || typeof result !== "object") {
          setRows(rowsTemplate);
          return;
        }

        const merged = rowsTemplate.map(r => {
          const k = toBackendKey(r.label);
          const v = Object.prototype.hasOwnProperty.call(result, k) ? result[k] : null;
          return { ...r, check: v === true ? true : v === false ? false : null };
        });
        setRows(merged);
      } catch (e) {
        console.error("POST /timesheet/check failed", e);
        setRows(rowsTemplate);
      }
    })();
  }, []);

  return (
    <div>
      <StatusBlock statusText="Status" emailItems={emailItems} contractItems={contractItems} />
      <div style={{ display:'flex', alignItems:'flex-start', gap:'24px', width:'95%', maxWidth:'1600px', margin:'0 auto' }}>
        <div style={{ flex:7 }}><PdfPreview pdfUrl="/sample.pdf" title=" " /></div>
        <div style={{ flex:5 }}><ReviewTable rows={rows} /></div>
      </div>
    </div>
  );
}
