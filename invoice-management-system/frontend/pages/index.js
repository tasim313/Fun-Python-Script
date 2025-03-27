// frontend/pages/index.js
import { useState } from 'react';
import axios from 'axios';

export default function Home() {
  const [file, setFile] = useState(null);
  const [invoice, setInvoice] = useState(null);

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append('file', file);
  
    try {
      const response = await axios.post('http://localhost:8881/api/upload-invoice', formData);
      setInvoice(response.data);
    } catch (error) {
      console.error('Error uploading invoice:', error);
    }
  };

  return (
    <div>
      <h1>Invoice Management System</h1>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload}>Upload</button>
      {invoice && (
        <div>
          <h2>Invoice Details</h2>
          <p>Invoice Number: {invoice.invoice_number}</p>
          <p>Date: {invoice.date}</p>
          <p>Vendor: {invoice.vendor}</p>
          <p>Total Amount: {invoice.total_amount}</p>
        </div>
      )}
    </div>
  );
}