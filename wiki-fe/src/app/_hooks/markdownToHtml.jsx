'use client'
import { useEffect, useRef } from 'react';
import sd from './Showdown';

const useMarkdownToHtml = (text) => {
    const textView = useRef(null);

    useEffect(() => {
        if (textView.current) {
            textView.current.innerHTML = sd.makeHtml(text);
        }
    }, [text]);

    return textView;
};

export default useMarkdownToHtml;


