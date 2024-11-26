'use client'
import React from 'react';
import '@/styles/layout/report-button.css';
import { useRouter } from 'next/navigation';

export default function ReportButton() {
  const router = useRouter();
  
  const handleReport = () => {
    router.push('/denuncia');
  }

  return (
    <div className="report-button-container">   
        <button className="report-button" onClick={handleReport}>Denuncie um caso de dengue!</button>
    </div>
  );
}
