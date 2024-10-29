'use client'

import React, { useState, useRef, useEffect } from 'react';
import '@/styles/wiki/article.css';
import Comments from '@/components/layout/Comments';
import { getSession } from '@/lib/session';
import Showdown from "showdown";

export default function Article({ params }) {
    const [session, setSession] = useState(null);
    const textView = useRef(null);

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
            textView.current.innerHTML = sd.makeHtml(params?.content);
        }
    }, [params]);

    return (
        <div className='article-container'>
            <h1>{params?.title}</h1>
            <p ref={textView}></p>

            {params.isValidArticle ? (
                <Comments params={{ articleId: params?.articleId, userId: session?.userId }} />
            ) : null}
        </div>
    );
}
