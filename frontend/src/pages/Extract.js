import React, { useState } from 'react';

const Extract = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [extractedData, setExtractedData] = useState(null);
  const [pdfText, setPdfText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [pdfUrl, setPdfUrl] = useState('');

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file && file.type === 'application/pdf') {
      setSelectedFile(file);
      setExtractedData(null);
      setPdfText('');
      setError('');
      
      // Create URL for PDF preview
      const fileUrl = URL.createObjectURL(file);
      setPdfUrl(fileUrl);
    } else {
      setError('Please select a valid PDF file');
      setSelectedFile(null);
      setPdfUrl('');
    }
  };

  const handleExtract = async () => {
    if (!selectedFile) return;

    setLoading(true);
    setError('');

    const formData = new FormData();
    formData.append('pdf_file', selectedFile);

    try {
      const response = await fetch('http://localhost:5001/api/extract-meta', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      
      if (result.success) {
        setExtractedData(result.meta_data);
        const textResponse = await fetch('http://localhost:5001/api/extract-pdf', {
          method: 'POST',
          body: formData,
        });
        if (textResponse.ok) {
          const textResult = await textResponse.json();
          if (textResult.success) {
            setPdfText(textResult.pdf_text);
          }
        }
      } else {
        setError(result.error || 'Extraction failed');
      }
    } catch (error) {
      console.error('Error:', error);
      setError('Failed to extract data from PDF');
    } finally {
      setLoading(false);
    }
  };

  const renderExtractedTable = (tableData) => {
    if (!tableData || !Array.isArray(tableData) || tableData.length === 0) {
      return <p>No table data found</p>;
    }

    // Check if tableData is an array of objects (current format)
    if (tableData[0] && typeof tableData[0] === 'object' && !Array.isArray(tableData[0])) {
      return (
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '10px' }}>
            <thead>
              <tr style={tableHeaderStyle}>
                <th style={tableCellStyle}>Data Point</th>
                <th style={tableCellStyle}>Extracted</th>
                <th style={tableCellStyle}>Expected</th>
                <th style={tableCellStyle}>Previous</th>
              </tr>
            </thead>
            <tbody>
              {tableData.map((row, rowIndex) => (
                <tr key={rowIndex} style={{ backgroundColor: rowIndex % 2 === 0 ? '#f8f9fa' : 'white' }}>
                  <td style={tableCellStyle}>{row.data_point || ''}</td>
                  <td style={tableCellStyle}>{row.extracted || ''}</td>
                  <td style={tableCellStyle}>{row.expected || ''}</td>
                  <td style={tableCellStyle}>{row.previous || ''}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      );
    }

    // Check if tableData is a 2D array (alternative format)
    if (Array.isArray(tableData[0])) {
      return (
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '10px' }}>
            <thead>
              <tr style={tableHeaderStyle}>
                {tableData[0].map((header, index) => (
                  <th key={index} style={tableCellStyle}>{header}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {tableData.slice(1).map((row, rowIndex) => (
                <tr key={rowIndex} style={{ backgroundColor: rowIndex % 2 === 0 ? '#f8f9fa' : 'white' }}>
                  {row.map((cell, cellIndex) => (
                    <td key={cellIndex} style={tableCellStyle}>{cell}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      );
    }

    return <p>Invalid table data format</p>;
  };

  const tableHeaderStyle = {
    backgroundColor: '#007bff',
    color: 'white',
    padding: '8px',
    textAlign: 'left',
    border: '1px solid #dee2e6'
  };

  const tableCellStyle = {
    padding: '8px',
    border: '1px solid #dee2e6',
    textAlign: 'left'
  };

  const fileInputStyle = {
    display: 'none'
  };

  const customFileInputStyle = {
    display: 'inline-block',
    padding: '10px 20px',
    backgroundColor: '#007bff',
    color: 'white',
    borderRadius: '5px',
    cursor: 'pointer',
    border: 'none',
    fontSize: '14px',
    fontWeight: '500',
    transition: 'background-color 0.3s',
    marginBottom: '15px'
  };

  const extractButtonStyle = {
    padding: '12px 24px',
    backgroundColor: '#28a745',
    color: 'white',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
    fontSize: '16px',
    fontWeight: '500',
    transition: 'background-color 0.3s',
    width: '100%'
  };

  const extractButtonDisabledStyle = {
    ...extractButtonStyle,
    backgroundColor: '#6c757d',
    cursor: 'not-allowed'
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>PDF Timesheet Extraction</h2>
      <div style={{ display: 'flex', gap: '20px', marginTop: '20px' }}>
        {/* Left Panel: PDF Upload and Preview */}
        <div style={{ flex: 1, border: '1px solid #ccc', padding: '15px', borderRadius: '8px', backgroundColor: '#f9f9f9' }}>
          <h3>Upload PDF</h3>
          
          {/* Custom File Input */}
          <label htmlFor="file-upload" style={customFileInputStyle}>
            {selectedFile ? selectedFile.name : 'Choose PDF File'}
          </label>
          <input
            id="file-upload"
            type="file"
            accept=".pdf"
            onChange={handleFileChange}
            style={fileInputStyle}
          />
          
          <button 
            onClick={handleExtract} 
            disabled={!selectedFile || loading} 
            style={!selectedFile || loading ? extractButtonDisabledStyle : extractButtonStyle}
            onMouseOver={(e) => {
              if (!(!selectedFile || loading)) {
                e.target.style.backgroundColor = '#218838';
              }
            }}
            onMouseOut={(e) => {
              if (!(!selectedFile || loading)) {
                e.target.style.backgroundColor = '#28a745';
              }
            }}
          >
            {loading ? 'Extracting...' : 'Extract Data'}
          </button>
          
          {error && (
            <p style={{ color: 'red', marginTop: '10px' }}>Error: {error}</p>
          )}

          {/* PDF Preview */}
          {selectedFile && (
            <div style={{ marginTop: '20px', borderTop: '1px solid #eee', paddingTop: '15px' }}>
              <h4>PDF Preview:</h4>
              <div style={{ 
                height: '500px', 
                backgroundColor: 'white', 
                padding: '10px', 
                borderRadius: '5px', 
                border: '1px solid #ddd',
                textAlign: 'center',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center'
              }}>
                {pdfUrl ? (
                  <iframe
                    src={pdfUrl}
                    title="PDF Preview"
                    style={{ 
                      width: '100%', 
                      height: '100%', 
                      border: 'none',
                      minHeight: '480px'
                    }}
                  />
                ) : (
                  <div style={{ color: '#dc3545', padding: '20px' }}>
                    <p>No PDF preview available.</p>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Right Panel: Extracted Information */}
        <div style={{ flex: 1, border: '1px solid #ccc', padding: '15px', borderRadius: '8px', backgroundColor: '#f9f9f9' }}>
          <h3>Extracted Information</h3>
          {extractedData ? (
            <div>
              {/* Basic Information */}
              {extractedData.base && (
                <div style={{ marginBottom: '20px' }}>
                  <h4 style={{ color: '#007bff', marginBottom: '10px' }}>Basic Information</h4>
                  <div style={{ backgroundColor: 'white', padding: '10px', borderRadius: '5px', border: '1px solid #ddd' }}>
                    <div style={{ marginBottom: '5px' }}>
                      <strong>PO Number:</strong> {extractedData.base.po_number}
                    </div>
                    <div style={{ marginBottom: '5px' }}>
                      <strong>Client:</strong> {extractedData.base.client}
                    </div>
                    <div style={{ marginBottom: '5px' }}>
                      <strong>Supervisor:</strong> {extractedData.base.supervisor}
                    </div>
                  </div>
                </div>
              )}

              {/* Employee Information */}
              {extractedData.employee && (
                <div style={{ marginBottom: '20px' }}>
                  <h4 style={{ color: '#007bff', marginBottom: '10px' }}>Employee Information</h4>
                  <div style={{ backgroundColor: 'white', padding: '10px', borderRadius: '5px', border: '1px solid #ddd' }}>
                    <div style={{ marginBottom: '5px' }}>
                      <strong>Name:</strong> {extractedData.employee.name}
                    </div>
                    <div style={{ marginBottom: '5px' }}>
                      <strong>Company:</strong> {extractedData.employee.company}
                    </div>
                  </div>
                </div>
              )}

              {/* Work Entries */}
              {extractedData.work_entries && extractedData.work_entries.length > 0 && (
                <div style={{ marginBottom: '20px' }}>
                  <h4 style={{ color: '#007bff', marginBottom: '10px' }}>Daily Work Hours</h4>
                  <div style={{ overflowX: 'auto' }}>
                    <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '10px' }}>
                      <thead>
                        <tr style={tableHeaderStyle}>
                          <th style={tableCellStyle}>Day</th>
                          <th style={tableCellStyle}>Date</th>
                          <th style={tableCellStyle}>Morning</th>
                          <th style={tableCellStyle}>Afternoon</th>
                          <th style={tableCellStyle}>Total</th>
                        </tr>
                      </thead>
                      <tbody>
                        {extractedData.work_entries.map((entry, index) => (
                          <tr key={index} style={{ backgroundColor: index % 2 === 0 ? '#f8f9fa' : 'white' }}>
                            <td style={tableCellStyle}>{entry.weekday}</td>
                            <td style={tableCellStyle}>{entry.date_original}</td>
                            <td style={tableCellStyle}>{entry.morning.time}</td>
                            <td style={tableCellStyle}>{entry.afternoon.time}</td>
                            <td style={tableCellStyle}>
                              <strong>{entry.total_daily_hours}</strong>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}

              {/* Weekly Total */}
              {extractedData.weekly_total && (
                <div style={{ marginBottom: '20px' }}>
                  <h4 style={{ color: '#007bff', marginBottom: '10px' }}>Weekly Summary</h4>
                  <div style={{ backgroundColor: 'white', padding: '10px', borderRadius: '5px', border: '1px solid #ddd' }}>
                    <div style={{ marginBottom: '5px' }}>
                      <strong>Total Hours:</strong> {extractedData.weekly_total.total_hours}
                    </div>
                    <div style={{ marginBottom: '5px' }}>
                      <strong>Decimal Hours:</strong> {extractedData.weekly_total.total_decimal_hours}
                    </div>
                  </div>
                </div>
              )}

              {/* Tasks */}
              {extractedData.tasks && extractedData.tasks.length > 0 && (
                <div style={{ marginBottom: '20px' }}>
                  <h4 style={{ color: '#007bff', marginBottom: '10px' }}>Tasks</h4>
                  {extractedData.tasks.map((task, index) => (
                    <div key={index} style={{ backgroundColor: 'white', padding: '10px', borderRadius: '5px', border: '1px solid #ddd', marginBottom: '10px' }}>
                      <div style={{ marginBottom: '5px' }}>
                        <strong>Task:</strong> {task.task_name}
                      </div>
                      <div style={{ marginBottom: '5px' }}>
                        <strong>Total Hours:</strong> {task.total_hours} ({task.decimal_hours} hours)
                      </div>
                      <div style={{ fontSize: '0.9em', color: '#666' }}>
                        <strong>Per Day:</strong> Mon: {task.per_day.Mon}, Tues: {task.per_day.Tues}, Wed: {task.per_day.Wed}, Thur: {task.per_day.Thur}, Fri: {task.per_day.Fri}
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {/* Date */}
              {extractedData.date && (
                <div style={{ marginBottom: '20px' }}>
                  <h4 style={{ color: '#007bff', marginBottom: '10px' }}>Date</h4>
                  <div style={{ backgroundColor: 'white', padding: '10px', borderRadius: '5px', border: '1px solid #ddd' }}>
                    <div style={{ marginBottom: '5px' }}>
                      <strong>Date:</strong> {extractedData.date}
                    </div>
                  </div>
                </div>
              )}
            </div>
          ) : (
            <p>Upload a PDF and click "Extract Data" to see the extracted information here.</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default Extract;
