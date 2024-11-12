'use client';
import React, { useRef, useEffect } from 'react';
import '@/styles/auth/terms-box.css';
import Showdown from "showdown";
import PrivacyPolicy from "@/assets/json/privacy-policy.json";

export default function Terms() {
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
        if (textView.current) {
            textView.current.innerHTML = sd.makeHtml(PrivacyPolicy?.terms);
        }
    }, []);

    return (
        <div className='terms-container'>
            <p style={{ marginTop: '20px' }} ref={textView}></p>
        </div>
    );
}
