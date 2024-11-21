'use client';
import React, { useEffect, useState } from 'react';
import '@/styles/info/info.css';
import { getSession } from '@/lib/session';
import { useContext } from 'react';
import { InfoContext } from '@/contexts/infoProvider';
import { useRouter } from 'next/navigation';
import useMarkdownToHtml from '@/hooks/markdownToHtml';

export default function Info({ text, title, id, error }) {
    const { handleInfo } = useContext(InfoContext);
    const [session, setSession] = useState(null);
    const router = useRouter();

    useEffect(() => {
        async function fetchSession() {
            const sessionData = await getSession();
            setSession(sessionData);
        }

        fetchSession();
    }, []);

    return (
        <div className='info-container'>
            <div className="info-header">
                <h1>{title}</h1>
                {
                session?.role === 'admin' && session && (
                    <button 
                        type="submit"
                        onClick={() => {
                            handleInfo(title, text, id);
                            router.push(`/editar-info`);
                        }}                                    
                        className="edit-info">
                        <h2>Editar</h2>
                    </button>)
                }
            </div>
            <p style={{ marginTop: '20px' }} ref={useMarkdownToHtml(text)}></p>
        </div>
    );
}
