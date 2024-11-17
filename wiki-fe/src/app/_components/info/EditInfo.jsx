"use client"
import "@/styles/info/edit-info.css";
import ErrorMessage from "@/components/auth/ErrorMessage";
import Showdown from "showdown";
import { useRouter } from 'next/navigation';
import { useContext } from 'react';
import { InfoContext } from '@/contexts/infoProvider';
import React, { useState, useRef, useEffect } from 'react';

export default function EditArticle() {
    const router = useRouter();
    const [text, setText] = useState('');
    const [title, setTitle] = useState('');
    const [infoId, setInfoId] = useState('');
    const [errorMessage, setErrorMessage] = useState(null);

    const { info } = useContext(InfoContext);

    useEffect(() =>{
        setInfoId(info.id);
        setText(info.text);
        setTitle(info.title);
        setPreview(info.text);
    }, []);

    const sd = new Showdown.Converter(
        {
            tables: true,
            tasklists: true,
            strikethrough: true,
            emoji: true,
            simpleLineBreaks: true,
            openLinksInNewWindow: true,
            backslashEscapesHTMLTags: true,
            smoothLivePreview: true,
            simplifiedAutoLink: true,
            simpleLineBreaks: true,
            requireSpaceBeforeHeadingText: true,
            ghMentions: true,
            ghMentionsLink: '/user/{u}',
            ghCodeBlocks: true,
            emoji: true,
            underline: true,
            completeHTMLDocument: true,
            metadata: true,
            parseImgDimensions: true,
            encodeEmails: true,
            openLinksInNewWindow: true
        });

    const previewRef = useRef(null);
    
    const setPreview = (text) => {
        if (previewRef.current) {
            previewRef.current.innerHTML = sd.makeHtml(text);
        }
    }
    
    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const response = await fetch(`http://127.0.0.1:8000/siteinfo/update/${infoId}/`, {
                method: 'PUT',
                headers: { 
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    title,
                    text,
                    siteinfo_id: infoId,
                }), 
            });
            
            if (!response.ok) {
                setErrorMessage("Não foi possivel editar a informação!");
                return;
            }       

            router.back();
        } catch (error) {
            setErrorMessage("Não foi possivel editar a informação!");
        }
    };

    return (
        <div className="edit-info-container">
            <form onSubmit={(e) => {
                const confirmed = confirm('Você confirma as atualizações?');
                e.preventDefault();

                if (confirmed) {
                    handleSubmit(e);
                }
            }}>
                <div className="title-container">
                    <label htmlFor="title">Título da informação</label>
                        <textarea 
                            type="text"
                            id="title"
                            value={title}
                            onChange={(e) => setTitle(e.target.value)}
                            required
                    />
                </div>

                <div className="text-container">
                    <div>
                    <h2>Conteúdo do texto</h2>
                        <textarea 
                            type="text"
                            id="text"
                            value={text}
                            onChange={(e) => 
                                {
                                    setText(e.target.value)
                                    setPreview(e.target.value)
                                }}
                            required
                        />
                    </div>
                <div className="editor">

                    <h2>Prévia do texto</h2>
                    <div className="preview-container">
                        <div ref={previewRef} className="preview-text"></div>
                    </div>
                </div>
                </div>
                <div className="submitButton-container" style={{ marginTop: '20px', marginBottom: '20px' }}>
                    <button type="submit">Atualizar informação</button>
                </div>

                <ErrorMessage message={errorMessage} /> 
            </form>
        </div>
    )
}