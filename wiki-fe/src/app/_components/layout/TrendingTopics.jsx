'use client';
import React, { useEffect, useState } from 'react';
import '@/styles/layout/trending-topics.css';
import Link from 'next/link';
import Showdown from 'showdown';

export default function TrendingTopics() {
    const [articles, setArticles] = useState([]);
    const [errorMessage, setErrorMessage] = useState('');

    const CHARACTER_LIMIT = 100; 

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
        const fetchArticles = async () => {
            try {
                const response = await fetch(`http://127.0.0.1:8000/article/list/${4}`, {
                    method: 'GET',
                    headers: { 'Content-Type': 'application/json' },
                });

                const data = await response.json();

                if (!response.ok) {
                    return;
                }

                setArticles(data);
            } catch (error) {
                setErrorMessage('Um erro ocorreu ao tentar carregar os artigos.');
            }
        };

        fetchArticles();
    }, []);

    return (
        <div className='trending-topics-container'>
            <h1>Tópicos em alta</h1>
            {errorMessage && <p className="error-message">{errorMessage}</p>}
            <div className='trending-topics'>
                {articles.map((article, index) => {
                    const truncatedText = article.text.length > CHARACTER_LIMIT
                        ? article.text.slice(0, CHARACTER_LIMIT) + '...'
                        : article.text;

                    return (
                        <Link href={`/wiki/${article.id}/${article.title.split(' ').join('-')}`} key={index} passHref style={{ textDecoration: 'none' }}>
                            <div className='article-preview'>
                                <h3>{article.title}</h3>
                                <p dangerouslySetInnerHTML={{ __html: sd.makeHtml(truncatedText) }}></p>
                            </div>
                        </Link>
                    );
                })}
            </div>
        </div>
    );
}
