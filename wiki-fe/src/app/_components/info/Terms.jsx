'use client';
import React from 'react';
import '@/styles/auth/terms-box.css';
import { infoIds } from "@/assets/misc/InfoIds";
import useFetchInfo from '@/hooks/fetchInfo';
import useMarkdownToHtml from '@/hooks/markdownToHtml';

export default function Terms() {
    const { info, errorMessage } = useFetchInfo(infoIds[0].termsOfUse);
    const htmlContent = useMarkdownToHtml(
        typeof info?.text === 'string' ? info.text : JSON.stringify(info?.text || '')
    );

    return (
        <div className='terms-container'>
            {errorMessage ? (
                <p style={{ marginTop: '20px', color: 'red' }}>{errorMessage}</p>
            ) : (
                <div>
                    <h1>Termos de uso</h1>
                    <p  
                    ref={htmlContent}
                    ></p>
                </div>
                
                
            )}
        </div>
    );
}
