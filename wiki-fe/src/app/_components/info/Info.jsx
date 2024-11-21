'use client';
import React, { useRef, useEffect, useState } from 'react';
import '@/styles/info/info.css';
import Showdown from "showdown";
import { getSession } from '@/lib/session';
import { useContext } from 'react';
import { InfoContext } from '@/contexts/infoProvider';
import { useRouter } from 'next/navigation';

export default function Info({ text, title, id, error }) {
    const textView = useRef(null);
    const { handleInfo } = useContext(InfoContext);
    const [session, setSession] = useState(null);
    const router = useRouter();

    const sd = new Showdown.Converter({
        tables: true,
        tasklists: true,
        strikethrough: true,
        emoji: true,
        simpleLineBreaks: true,
        openLinksInNewWindow: true,
        backslashEscapesHTMLTags: true,
        smoothLivePreview: true,
        simplifiedAutoLink: true,
        requireSpaceBeforeHeadingText: true,
        ghMentions: true,
        ghMentionsLink: '/user/{u}',
        ghCodeBlocks: true,
        underline: true,
        completeHTMLDocument: true,
        metadata: true,
        parseImgDimensions: true,
        encodeEmails: true
    });
    
    useEffect(() => {
        async function fetchSession() {
            const sessionData = await getSession();
            setSession(sessionData);
        }

        fetchSession();
    }, []);

    useEffect(() => {
        if (textView.current) {
            textView.current.innerHTML = sd.makeHtml(text);
        }
    }, [text]);

    return (
        <div className='info-container'>
            <div className="info-header">
                <h1>{title}</h1>
                {
                session?.role !== 'user' && session && (
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
            <p style={{ marginTop: '20px' }} ref={textView}></p>
        </div>
    );
}
