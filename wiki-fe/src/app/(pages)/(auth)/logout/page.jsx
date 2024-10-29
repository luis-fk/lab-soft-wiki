'use client';

import React, { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { terminateSession, getSession } from '@/lib/session';

export default function Page() {
    const router = useRouter();

    useEffect(() => {
        const session = getSession();

        if (session) {
            const logout = async () => {
                await terminateSession();
                router.push('/');
            };

            logout();
        }
    }, [router]);

    return <></>;
}